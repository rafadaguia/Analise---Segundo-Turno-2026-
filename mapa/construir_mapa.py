#!/usr/bin/env python3
"""Gera mapa/mapa_prioridades.html (e a cópia docs/index.html, servida pelo GitHub Pages): os 200 municípios prioritários e a ação indicada em cada um.

Lê painel/focos_ei.csv e painel/cenarios_frentes.csv (simulacao_montecarlo.py), painel/painel_final.csv, os contornos estaduais do IBGE
(dados/geo/ibge_ufs_qualidade_minima.json) e as coordenadas das sedes municipais
(dados/geo/municipios_coordenadas.csv, de github.com/kelvins/municipios-brasileiros).
Injeta tudo em mapa/modelo.html, que vira uma página única e autocontida.
"""
import json, os, sys
import numpy as np
import pandas as pd

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)


def acao(terreno, mob):
    """Ação principal, pela composição do potencial (mobilização só conta se a mediana for positiva)."""
    m = max(mob, 0)
    parte = terreno/(terreno + m) if terreno + m > 0 else 0
    if parte >= 0.6: return "reconquistar"
    if parte <= 0.4: return "mobilizar"
    return "ambas"


def veredito(p):
    """Mobilizar: rende (chance >= 90%), prejudica (<= 10%) ou incerto."""
    return "rende" if p >= 0.9 else "prejudica" if p <= 0.1 else "incerto"


def main():
    d = pd.read_csv(os.path.join(RAIZ, "painel", "painel_final.csv"))
    f = pd.read_csv(os.path.join(RAIZ, "painel", "focos_ei.csv"))
    cf = pd.read_csv(os.path.join(RAIZ, "painel", "cenarios_frentes.csv"))
    gap = d["bolso_26"].sum() - d["lula_26"].sum()
    NAC = np.average(d["desloc"], weights=d["validos_26"])

    t = f.merge(d, on=["cd_municipio_ibge", "uf", "municipio"], how="left")
    coord = pd.read_csv(os.path.join(RAIZ, "dados", "geo", "municipios_coordenadas.csv"))
    t = t.merge(coord[["codigo_ibge", "latitude", "longitude", "nome"]],
                left_on="cd_municipio_ibge", right_on="codigo_ibge", how="left")
    assert t["latitude"].notna().all(), "município sem coordenada"

    r0 = lambda v: int(round(v))
    cidades = []
    for r in t.to_dict("records"):
        cidades.append({
            "rank": int(r["rank"]), "nome": r["nome"], "uf": r["uf"], "lat": r["latitude"], "lon": r["longitude"],
            "frente": r["frente"], "acao": acao(r["terreno"], r["mob_p50"]),
            "mob_veredito": veredito(r["prob_mob_rende"]), "prob_rende": round(r["prob_mob_rende"], 3),
            "faixa": r["faixa_ei"],
            "novos": [round(r["frac_lula_novos_p05"], 3), round(r["frac_lula_novos_p50"], 3), round(r["frac_lula_novos_p95"], 3)],
            "lula": round(r["lula_pct_26_x"] if "lula_pct_26_x" in r else r["lula_pct_26"], 1),
            "lula22": round(r["lula_pct_22_2t"], 1),
            "desloc": round(r["desloc"], 2), "anomalia": round(r["anomalia"], 2),
            "aptos": int(r["aptos_26"]), "validos": int(r["validos_26"]),
            "abst": int(r["abstencao_26"]), "abst_pct": round(r["absten_pct_26"], 1),
            "saldo": int(r["lula_26"] - r["bolso_26"]),
            "terreno": r0(r["terreno"]),
            "mob": [r0(r["mob_p05"]), r0(r["mob_p50"]), r0(r["mob_p95"])],
            "pot": [r0(r["pot_p05"]), r0(r["pot_p50"]), r0(r["pot_p95"])],
        })

    def faixa_cf(frente, medida):
        l = cf[(cf["frente"] == frente) & (cf["medida"] == medida)].iloc[0]
        return [r0(l["p05"]), r0(l["mediana"]), r0(l["p95"])]

    frentes = []
    for fr in sorted(set(f["frente"])):
        frentes.append({"nome": fr, "n": int((f["frente"] == fr).sum()),
                        "pot": faixa_cf(fr, "potencial (terreno + 2 pp)"),
                        "mob": faixa_cf(fr, "mobilização +2 pp"),
                        "terc_base": faixa_cf(fr, "terceira via, base"),
                        "terc_dir": faixa_cf(fr, "terceira via, direita")})
    frentes.sort(key=lambda x: -x["pot"][1])

    tot = faixa_cf("TODOS OS FOCOS", "potencial (terreno + 2 pp)")
    meta = {
        "foco": len(f), "municipios_pais": len(d), "nac_desloc": round(NAC, 2), "gap": int(gap),
        "pot": tot, "mob": faixa_cf("TODOS OS FOCOS", "mobilização +2 pp"),
        "aptos_foco": int(t["aptos_26"].sum()), "aptos_pais": int(d["aptos_26"].sum()),
    }
    ufs = json.load(open(os.path.join(RAIZ, "dados", "geo", "ibge_ufs_qualidade_minima.json")))

    dados = json.dumps({"meta": meta, "cidades": cidades, "frentes": frentes, "ufs": ufs},
                       ensure_ascii=False, separators=(",", ":"))
    modelo = open(os.path.join(RAIZ, "mapa", "modelo.html"), encoding="utf-8").read()
    saida = os.path.join(RAIZ, "mapa", "mapa_prioridades.html")
    pagina = modelo.replace("/*__DADOS__*/null", dados)
    open(saida, "w", encoding="utf-8").write(pagina)
    print(f"{len(cidades)} municípios -> {saida}")

    # cópia para o GitHub Pages (pasta docs/), como documento completo
    pages = os.path.join(RAIZ, "docs", "index.html")
    os.makedirs(os.path.dirname(pages), exist_ok=True)
    open(pages, "w", encoding="utf-8").write('<!doctype html>\n<html lang="pt-BR">\n' + pagina + "\n</html>\n")
    open(os.path.join(RAIZ, "docs", ".nojekyll"), "w").close()
    print(f"GitHub Pages -> {pages}")

    # versão compacta para incorporar em matérias (iframe): mesmos dados, sem a lista de frentes
    leve = json.dumps({"meta": meta, "cidades": cidades, "ufs": ufs}, ensure_ascii=False, separators=(",", ":"))
    emb = open(os.path.join(RAIZ, "mapa", "embed_modelo.html"), encoding="utf-8").read().replace("/*__DADOS__*/null", leve)
    open(os.path.join(RAIZ, "mapa", "embed.html"), "w", encoding="utf-8").write(emb)
    open(os.path.join(RAIZ, "docs", "embed.html"), "w", encoding="utf-8").write(
        '<!doctype html>\n<html lang="pt-BR">\n' + emb + "\n</html>\n")
    print("embed -> mapa/embed.html, docs/embed.html")
    print(json.dumps(meta, ensure_ascii=False))
    print(pd.Series([c["acao"] for c in cidades]).value_counts().to_dict(),
          "| mobilizar:", pd.Series([c["mob_veredito"] for c in cidades]).value_counts().to_dict())


if __name__ == "__main__":
    main()
