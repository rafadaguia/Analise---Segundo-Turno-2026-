#!/usr/bin/env python3
"""Gera os painéis derivados a partir de painel/painel_municipios.csv.

Reproduz, na mesma ordem, as etapas que produziram os arquivos usados pelo
notebook:

  1. painel_modelado.csv           modelo estrutural (resíduo, esperado) e reservatórios
  2. comparecimento_2022.csv       aptos, comparecimento, brancos e nulos por turno (TSE 2022)
  3. painel_completo.csv           junta 1 e 2
  4. painel_final.csv              taxa de captura prevista para 2026
  5. taxas_transferencia_2022.csv  frações a (terceira via) e b (comparecimento) por faixa
  6. painel_final.csv              saldo por +1 pp de comparecimento, por faixa
  7. painel_final.csv              deslocamento, anomalia, terreno perdido e prioridade

Cada etapa grava em disco e a seguinte relê o arquivo, como na análise
original; a ida e volta pelo CSV faz parte do resultado (tipos e arredondamento).

Uso:
    python3 gerar_painel_final.py            # grava em painel/
    python3 gerar_painel_final.py --saida X  # grava em X/ (para conferir contra painel/)

Pré-requisitos: painel/painel_municipios.csv (de preparar_dados.py) e
dados/detalhe_votacao_munzona_2022.zip.
"""
import argparse, collections, csv, io, os, sys, zipfile
import numpy as np
import pandas as pd
import statsmodels.api as sm

RAIZ  = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(RAIZ, "dados")

FAIXAS = [0, 35, 45, 55, 65, 100]
ROTULOS = ["<35%", "35-45%", "45-55%", "55-65%", ">65%"]

# Frações por faixa usadas nas etapas 6 e 7 e no notebook (seção 7). São as
# estimativas da etapa 5 arredondadas a 3 casas; a etapa 5 confere isso.
TX_A = {"<35%": 0.215, "35-45%": 0.306, "45-55%": 0.407, "55-65%": 0.407, ">65%": 0.436}
TX_B = {"<35%": 0.301, "35-45%": 0.621, "45-55%": 0.331, "55-65%": 0.647, ">65%": 0.613}


def etapa1_modelado(entrada, saida):
    """Modelo estrutural do % de Lula em 2026 e reservatórios de voto."""
    d = pd.read_csv(entrada)
    # Sai quem não tem 2022 ou Censo — na prática, só Boa Esperança do Norte (MT),
    # município novo, sem votação própria em 2022.
    d = d[(d["validos_26"] > 0)].dropna(subset=["lula_2022_2t", "renda_dom_pc", "alfabetizacao"]).copy()
    d["val_22_2t"] = d[["lula_2022_2t", "bolso_2022_2t", "outros_2022_2t"]].sum(axis=1)
    d["lula_pct_26"] = 100*d["lula_26"]/d["validos_26"]
    d["lula_pct_22_2t"] = 100*d["lula_2022_2t"]/d["val_22_2t"]
    d["absten_pct_26"] = 100*d["abstencao_26"]/d["aptos_26"]
    d["bn_pct_26"] = 100*(d["brancos_26"]+d["nulos_26"])/d["comparec_26"]
    d["log_pop"] = np.log(d["populacao"])
    d["log_renda"] = np.log(d["renda_dom_pc"])

    # base histórica + perfil social + efeito fixo de UF
    X = pd.get_dummies(d[["lula_pct_22_2t", "log_renda", "alfabetizacao", "log_pop", "uf"]],
                       columns=["uf"], drop_first=True).astype(float)
    X = sm.add_constant(X)
    m = sm.OLS(d["lula_pct_26"].astype(float), X).fit()
    print(f"[1] modelo estrutural: n={int(m.nobs)}  R²={m.rsquared:.4f}")
    d["resid"] = m.resid
    d["esperado"] = m.fittedvalues

    # R1 terceira via à taxa de 2022; R2 fora da urna ponderado pela inclinação
    # local; R3 sub-performance estrutural (só o lado negativo do resíduo)
    TAXA_LULA_22 = 0.398
    d["r1_terceira_via"] = d["terceiros_26"]*TAXA_LULA_22
    d["r1_adversario"] = d["terceiros_26"]*(1-TAXA_LULA_22)
    d["lean"] = d["lula_pct_26"]/100
    d["r2_mobilizacao"] = (d["abstencao_26"]+d["brancos_26"]+d["nulos_26"])*d["lean"]
    d["r3_subperf"] = np.where(d["resid"] < 0, -d["resid"]/100*d["validos_26"], 0)
    d.to_csv(saida, index=False)


def etapa2_comparecimento(saida):
    """Comparecimento, abstenção, brancos e nulos de presidente em 2022, por turno."""
    z = zipfile.ZipFile(os.path.join(DADOS, "detalhe_votacao_munzona_2022.zip"))
    nome = [n for n in z.namelist() if n.endswith("_BR.csv")]
    alvo = nome[0] if nome else [n for n in z.namelist() if n.endswith(".csv")][0]
    acc = collections.defaultdict(lambda: collections.defaultdict(int))
    with z.open(alvo) as f:
        r = csv.DictReader(io.TextIOWrapper(f, encoding="latin-1"), delimiter=";")
        for l in r:
            if l.get("CD_CARGO") != "1":
                continue
            k = (l["SG_UF"], l["CD_MUNICIPIO"].lstrip("0"))
            t = l["NR_TURNO"]
            for c in ("QT_APTOS", "QT_COMPARECIMENTO", "QT_ABSTENCOES", "QT_VOTOS_BRANCOS", "QT_VOTOS_NULOS"):
                if c in l:
                    acc[k][f"{c}_{t}t"] += int(l[c] or 0)
    df = pd.DataFrame([{"uf": k[0], "cd_mun_tse": k[1], **v} for k, v in acc.items()])
    print(f"[2] comparecimento 2022: {len(df)} municípios")
    df.to_csv(saida, index=False)


def etapa3_completo(modelado, comparec, saida):
    c = pd.read_csv(comparec, dtype={"cd_mun_tse": str})
    d = pd.read_csv(modelado, dtype={"cd_mun_tse": str})
    m = d.merge(c, on=["uf", "cd_mun_tse"], how="left")
    m = m.dropna(subset=["QT_COMPARECIMENTO_1t"])
    m["dcomp_22"] = m["QT_COMPARECIMENTO_2t"]-m["QT_COMPARECIMENTO_1t"]
    m["dcomp_pct_22"] = 100*m["dcomp_22"]/m["QT_APTOS_1t"]
    m["dlula_22"] = m["lula_2022_2t"]-m["lula_2022_1t"]
    print(f"[3] painel completo: {len(m)} municípios")
    m.to_csv(saida, index=False)


def etapa4_captura(completo, saida):
    """Modelo da taxa de captura em 2022, aplicado a 2026."""
    m = pd.read_csv(completo, dtype={"cd_mun_tse": str})
    m["bn_1t"] = m["QT_VOTOS_BRANCOS_1t"]+m["QT_VOTOS_NULOS_1t"]
    m["bn_2t"] = m["QT_VOTOS_BRANCOS_2t"]+m["QT_VOTOS_NULOS_2t"]
    # votos em disputa entre os turnos = terceira via + Δcomparecimento − Δbrancos/nulos
    m["pool"] = m["outros_2022_1t"]+(m["QT_COMPARECIMENTO_2t"]-m["QT_COMPARECIMENTO_1t"])-(m["bn_2t"]-m["bn_1t"])
    m["dlula"] = m["lula_2022_2t"]-m["lula_2022_1t"]
    v = m[m["pool"] > 500].copy()
    v["captura"] = v["dlula"]/v["pool"]
    v = v[(v["captura"] > -0.5) & (v["captura"] < 1.5)]
    v["log_renda"] = np.log(v["renda_dom_pc"])
    v["log_pop"] = np.log(v["populacao"])
    X = sm.add_constant(v[["lula_pct_22_2t", "log_renda", "alfabetizacao", "log_pop"]].astype(float))
    cap = sm.OLS(v["captura"].astype(float), X).fit()
    print(f"[4] modelo de captura (2022): n={int(cap.nobs)}  R²={cap.rsquared:.3f}")

    m["log_renda"] = np.log(m["renda_dom_pc"])
    m["log_pop"] = np.log(m["populacao"])
    X26 = sm.add_constant(m[["lula_pct_26", "log_renda", "alfabetizacao", "log_pop"]].astype(float))
    X26.columns = X.columns
    m["captura_prev"] = np.clip(cap.predict(X26), 0.05, 0.75)
    m["novos_por_pp"] = m["aptos_26"]*0.01
    m["saldo_por_pp"] = m["novos_por_pp"]*(2*m["captura_prev"]-1)
    m["pool_terc"] = m["terceiros_26"]
    m["saldo_terc"] = m["pool_terc"]*(2*m["captura_prev"]-1)
    m["saldo_resid"] = m["r3_subperf"]
    m.to_csv(saida, index=False)


def etapa5_taxas(final, saida):
    """Δvotos = a*terceira_via + b*Δcomparecimento_líquido, sem intercepto, por faixa."""
    m = pd.read_csv(final, dtype={"cd_mun_tse": str})
    m["dcomp_liq"] = (m["QT_COMPARECIMENTO_2t"]-m["QT_COMPARECIMENTO_1t"])-(m["bn_2t"]-m["bn_1t"])
    m["terc"] = m["outros_2022_1t"]
    m["dlula"] = m["lula_2022_2t"]-m["lula_2022_1t"]
    v = m[m["terc"] > 300].copy()
    v["faixa"] = pd.cut(v["lula_pct_22_2t"], FAIXAS, labels=ROTULOS)
    linhas = []
    for faixa in list(v["faixa"].cat.categories)+["TODOS"]:
        s = v if faixa == "TODOS" else v[v["faixa"] == faixa]
        rl = sm.OLS(s["dlula"].astype(float), s[["terc", "dcomp_liq"]].astype(float)).fit()
        linhas.append({"faixa": str(faixa), "a_lula": rl.params["terc"],
                       "b_lula": rl.params["dcomp_liq"], "n": len(s)})
    t = pd.DataFrame(linhas)
    t.to_csv(saida, index=False)
    print("[5] taxas de transferência 2022:")
    print(t.round(3).to_string(index=False))
    for _, l in t[t["faixa"] != "TODOS"].iterrows():
        assert round(l["a_lula"], 3) == TX_A[l["faixa"]], f"a diverge em {l['faixa']}"
        assert round(l["b_lula"], 3) == TX_B[l["faixa"]], f"b diverge em {l['faixa']}"


def etapa6_saldo(final):
    m = pd.read_csv(final, dtype={"cd_mun_tse": str})
    m["faixa"] = pd.cut(m["lula_pct_26"], FAIXAS, labels=list(TX_B)).astype(str)
    m["b"] = m["faixa"].map(TX_B)
    m["a"] = m["faixa"].map(TX_A)
    m["saldo_pp"] = m["aptos_26"]*0.01*(2*m["b"]-1)      # +1 pp de comparecimento
    m["saldo_terc"] = m["terceiros_26"]*(2*m["a"]-1)     # terceira via se repetir 2022
    m["saldo_total_pp"] = m["saldo_pp"]
    m.to_csv(final, index=False)
    print(f"[6] saldo de +1 pp: {m['saldo_pp'].sum():,.0f} votos".replace(",", "."))


def etapa7_prioridade(final):
    m = pd.read_csv(final, dtype={"cd_mun_tse": str})
    m["val_22_2t"] = m[["lula_2022_2t", "bolso_2022_2t", "outros_2022_2t"]].sum(axis=1)
    m["lula_pct_22_2t"] = 100*m["lula_2022_2t"]/m["val_22_2t"]
    m["desloc"] = m["lula_pct_26"]-m["lula_pct_22_2t"]
    NAC = np.average(m["desloc"], weights=m["validos_26"])
    m["anomalia"] = m["desloc"]-NAC                       # quanto caiu além da média
    m["terreno_perdido"] = np.where(m["anomalia"] < 0, -m["anomalia"]/100*m["validos_26"], 0)
    m["prioridade"] = m["terreno_perdido"]+np.maximum(m["saldo_pp"], 0)*2   # +2 pp de comparecimento
    m.to_csv(final, index=False)
    print(f"[7] deslocamento nacional {NAC:+.2f} pp | prioridade somada "
          f"{m['prioridade'].sum():,.0f} votos".replace(",", "."))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--saida", default=os.path.join(RAIZ, "painel"))
    args = ap.parse_args()
    os.makedirs(args.saida, exist_ok=True)
    p = lambda n: os.path.join(args.saida, n)

    entrada = os.path.join(RAIZ, "painel", "painel_municipios.csv")
    etapa1_modelado(entrada, p("painel_modelado.csv"))
    etapa2_comparecimento(p("comparecimento_2022.csv"))
    etapa3_completo(p("painel_modelado.csv"), p("comparecimento_2022.csv"), p("painel_completo.csv"))
    etapa4_captura(p("painel_completo.csv"), p("painel_final.csv"))
    etapa5_taxas(p("painel_final.csv"), p("taxas_transferencia_2022.csv"))
    etapa6_saldo(p("painel_final.csv"))
    etapa7_prioridade(p("painel_final.csv"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
