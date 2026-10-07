#!/usr/bin/env python3
"""Monte Carlo dos cenários do 2º turno de 2026, a partir do posterior da inferência ecológica.

Cada sorteio combina três fontes de incerteza:

  1. Parâmetros: uma amostra do posterior do modelo RxC de 2022
     (inferencia_ecologica.py) dá as taxas de transferência de cada município.
  2. Resíduo municipal (bootstrap): o modelo erra a margem de cada município.
     Sorteamos, com reposição, um erro observado em 2022 na mesma faixa e o
     somamos à projeção. É o que o modelo não explica, como clima local e
     candidaturas regionais.
  3. Cenário: hipóteses que os dados de 2022 não informam (abaixo).

Cenários
--------
  base       o comportamento de 2022 se repete com os candidatos de 2026
  direita    a terceira via de 2026 (Cury, Renan Santos, Caiado, Zema) é mais
             à direita que a de 2022: uma fração phi ~ Uniforme(0, 0,5) do que
             ela transferia para Lula vai para o adversário. phi é hipótese,
             não estimativa.
  +2 pp      soma a qualquer cenário 2 pontos de comparecimento nos focos onde
             a mediana do saldo da mobilização é positiva

O "terreno perdido" não depende de taxa de transferência: é a distância até a
queda média nacional. Ele entra como teto, e a única incerteza dele vem do
bootstrap da própria média nacional.

Saídas
------
  painel/focos_ei.csv          os 200 focos, com mediana e intervalo de 90% de cada parcela
  painel/cenarios_frentes.csv  potencial e margem projetada por frente, por cenário
  painel/cenarios_nacional.csv margem nacional projetada por cenário e chance de Lula à frente

Uso:  .venv/bin/python simulacao_montecarlo.py [--sorteios 2000]
"""
import argparse, os, sys
import numpy as np
import pandas as pd
import xarray as xr

from inferencia_ecologica import (PAINEL, MODELO, ROTULOS, SEMENTE, betas, covariaveis,
                                  faixa, montar_2022)
from frentes import frente

FOCO = 200
Q = (0.05, 0.5, 0.95)


def carregar_posterior():
    dt = xr.open_datatree(os.path.join(MODELO, "ei_2022.nc"))
    ref = np.load(os.path.join(MODELO, "ei_2022_ref.npz"))
    return dt["posterior"].to_dataset(), (ref["media"], ref["desvio"])


def residuos_2022(post, ref):
    """Erro da margem (Lula − Bolsonaro, em fração dos aptos) em cada município de 2022, por faixa."""
    d, x, y, N = montar_2022()
    g = d["faixa_ei"].cat.codes.to_numpy()
    w, _ = covariaveis(N, d["renda_dom_pc"], ref)
    sub = post.isel(draw=slice(None, None, 10))
    B = betas(sub, g, w)
    theta = np.einsum("or,sorc->soc", x, B)
    pred = np.median(theta[..., 0] - theta[..., 1], axis=0)
    r = (y[:, 0] - y[:, 1]) - pred
    return {gi: r[g == gi] for gi in range(len(ROTULOS))}, r


def sub_posterior(post, S, rng):
    st = post.stack(s=("chain", "draw"))
    idx = rng.choice(st.sizes["s"], size=S, replace=False)
    st = st.isel(s=idx)
    # volta ao formato (chain, draw) esperado por betas()
    return st.drop_vars(["chain", "draw", "s"]).assign_coords(s=np.arange(S)).rename(s="draw").expand_dims(chain=[0])


def q(a, axis=0):
    return np.quantile(a, Q, axis=axis)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sorteios", type=int, default=2000)
    args = ap.parse_args()
    rng = np.random.default_rng(SEMENTE + 7)
    S = args.sorteios

    post, ref = carregar_posterior()
    pool, r22 = residuos_2022(post, ref)
    print(f"resíduo da margem em 2022: desvio {100*r22.std():.2f} pp dos aptos")

    # ---------------------------------------------------------- 2026
    d = pd.read_csv(os.path.join(PAINEL, "painel_final.csv"))
    N = d["aptos_26"].to_numpy(float)
    L, Bv, T = (d[c].to_numpy(float) for c in ("lula_26", "bolso_26", "terceiros_26"))
    n = np.c_[L, Bv, T, N - L - Bv - T]                          # eleitores por origem
    lula_pct = 100*L/(L + Bv + T)
    g = faixa(pd.Series(lula_pct)).cat.codes.to_numpy()
    w, _ = covariaveis(N, d["renda_dom_pc"], ref)

    # terreno perdido, com bootstrap da média nacional
    desloc = d["desloc"].to_numpy(float)
    val = d["validos_26"].to_numpy(float)
    nac = np.average(desloc, weights=val)
    bi = rng.integers(0, len(d), size=(S, len(d)))
    nac_b = (desloc[bi]*val[bi]).sum(1)/val[bi].sum(1)
    terreno = lambda m: np.maximum(-(desloc - m), 0)/100*val
    print(f"queda média nacional: {nac:+.2f} pp (bootstrap 90%: {np.quantile(nac_b, .05):+.2f} a {np.quantile(nac_b, .95):+.2f})")

    sub = sub_posterior(post, S, rng)
    phi = rng.uniform(0, 0.5, S)

    # acumula sorteio a sorteio, em blocos, para não montar um array de S x 5.570 x 4 x 3
    mob = np.empty((S, len(d)), np.float32)        # saldo líquido de +2 pp
    terc_base = np.empty((S, len(d)), np.float32)
    marg_base = np.empty((S, len(d)), np.float32)
    frac_lula_novos = np.empty((S, len(d)), np.float32)
    tl = np.empty((S, len(d)), np.float32)         # votos de terceira via que vão para Lula
    bloco = 100
    for i0 in range(0, S, bloco):
        Bs = betas(sub.isel(draw=slice(i0, i0 + bloco)), g, w)    # b, obs, origem, destino
        b = Bs.shape[0]
        proj = np.einsum("or,borc->boc", n, Bs)
        res = np.stack([pool[gi][rng.integers(0, len(pool[gi]), b)] for gi in g], axis=1)
        marg_base[i0:i0 + b] = proj[..., 0] - proj[..., 1] + res*N
        c = Bs[:, :, 3, 0]/(Bs[:, :, 3, 0] + Bs[:, :, 3, 1])   # fração para Lula entre quem passa a votar
        frac_lula_novos[i0:i0 + b] = c
        mob[i0:i0 + b] = 0.02*N*(2*c - 1)
        terc_base[i0:i0 + b] = T*(Bs[:, :, 2, 0] - Bs[:, :, 2, 1])
        tl[i0:i0 + b] = T*Bs[:, :, 2, 0]
        print(f"  sorteios {i0 + b}/{S}", end="\r")
    print()
    # cenário direita: uma fração phi do que a terceira via dava a Lula passa ao adversário
    marg_dir = marg_base - 2*phi[:, None]*tl
    terc_dir = terc_base - 2*phi[:, None]*tl

    # ------------------------------------------------------ focos
    mob_med = np.median(mob, axis=0)
    rende = mob_med > 0
    terr = terreno(nac)
    prioridade = terr + np.where(rende, mob_med, 0)
    ordem = np.argsort(-prioridade)
    focos = ordem[:FOCO]
    pot = terreno(nac_b[:, None])[:, focos] + np.where(rende[focos], mob[:, focos], 0)

    fr = np.array([frente(u, m) for u, m in zip(d["uf"], d["municipio"])])
    f = d.iloc[focos][["uf", "municipio", "cd_municipio_ibge"]].copy()
    f.insert(0, "rank", np.arange(1, FOCO + 1))
    f["frente"] = fr[focos]
    f["faixa_ei"] = np.array(ROTULOS)[g[focos]]
    f["lula_pct_26"] = lula_pct[focos]
    f["terreno"] = terr[focos]
    for nome, arr in (("mob", mob[:, focos]), ("pot", pot), ("frac_lula_novos", frac_lula_novos[:, focos]),
                      ("terc_base", terc_base[:, focos]), ("terc_dir", terc_dir[:, focos]),
                      ("margem_base", marg_base[:, focos]), ("margem_dir", marg_dir[:, focos])):
        lo, md, hi = q(arr)
        f[f"{nome}_p05"], f[f"{nome}_p50"], f[f"{nome}_p95"] = lo, md, hi
    f["prob_mob_rende"] = (mob[:, focos] > 0).mean(0)
    f.to_csv(os.path.join(PAINEL, "focos_ei.csv"), index=False)

    # --------------------------------------------------- frentes
    linhas = []
    grupos = [("TODOS OS FOCOS", np.ones(FOCO, bool))] + [(fn, f["frente"].to_numpy() == fn) for fn in sorted(set(f["frente"]))]
    for nome, msk in grupos:
        cols = focos[msk]
        mob_f = np.where(rende[cols], mob[:, cols], 0).sum(1)
        regs = {
            "potencial (terreno + 2 pp)": pot[:, msk].sum(1),
            "mobilização +2 pp": mob_f,
            "terceira via, base": terc_base[:, cols].sum(1),
            "terceira via, direita": terc_dir[:, cols].sum(1),
            "margem projetada, base": marg_base[:, cols].sum(1),
            "margem projetada, direita": marg_dir[:, cols].sum(1),
            "margem projetada, base + 2 pp": marg_base[:, cols].sum(1) + mob_f,
            "margem projetada, direita + 2 pp": marg_dir[:, cols].sum(1) + mob_f,
        }
        for k, a in regs.items():
            lo, md, hi = q(a)
            linhas.append({"frente": nome, "municipios": int(msk.sum()), "medida": k,
                           "p05": lo, "mediana": md, "p95": hi, "prob_positivo": float((a > 0).mean())})
    fr_df = pd.DataFrame(linhas)
    fr_df.to_csv(os.path.join(PAINEL, "cenarios_frentes.csv"), index=False)

    # --------------------------------------------------- nacional
    mob_todos_focos = np.where(rende[focos], mob[:, focos], 0).sum(1)
    nac_regs = {
        "base": marg_base.sum(1),
        "direita": marg_dir.sum(1),
        "base + 2 pp nos focos": marg_base.sum(1) + mob_todos_focos,
        "direita + 2 pp nos focos": marg_dir.sum(1) + mob_todos_focos,
    }
    linhas = []
    for k, a in nac_regs.items():
        lo, md, hi = q(a)
        linhas.append({"cenario": k, "p05": lo, "mediana": md, "p95": hi, "prob_lula_a_frente": float((a > 0).mean())})
    na = pd.DataFrame(linhas)
    na.to_csv(os.path.join(PAINEL, "cenarios_nacional.csv"), index=False)

    pd.set_option("display.width", 200)
    fm = lambda v: f"{v/1e3:,.0f} mil".replace(",", ".")
    print("\nMARGEM NACIONAL PROJETADA (Lula − Flávio, 2º turno) — simulação condicional, não previsão")
    for _, l in na.iterrows():
        print(f"  {l['cenario']:28s} {fm(l['mediana']):>12}  (90%: {fm(l['p05'])} a {fm(l['p95'])})  P(Lula à frente) {100*l['prob_lula_a_frente']:.0f}%")
    print("\nPOTENCIAL POR FRENTE (terreno + 2 pp), 200 focos")
    t = fr_df[fr_df["medida"] == "potencial (terreno + 2 pp)"].sort_values("mediana", ascending=False)
    for _, l in t.iterrows():
        print(f"  {l['frente']:22s} {l['municipios']:>4}  {fm(l['mediana']):>10}  (90%: {fm(l['p05'])} a {fm(l['p95'])})")
    print(f"\nfocos onde mobilizar rende (mediana > 0): {int(rende[focos].sum())} de {FOCO}; "
          f"com probabilidade < 90% de render: {int(((f['prob_mob_rende'] > .1) & (f['prob_mob_rende'] < .9)).sum())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
