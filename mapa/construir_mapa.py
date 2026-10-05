#!/usr/bin/env python3
"""Gera mapa/mapa_prioridades.html (e a cópia docs/index.html, servida pelo GitHub Pages): os 200 municípios prioritários e a ação indicada em cada um.

Lê painel/painel_final.csv (gerar_painel_final.py), os contornos estaduais do IBGE
(dados/geo/ibge_ufs_qualidade_minima.json) e as coordenadas das sedes municipais
(dados/geo/municipios_coordenadas.csv, de github.com/kelvins/municipios-brasileiros).
Injeta tudo em mapa/modelo.html, que vira uma página única e autocontida.
"""
import json, os
import numpy as np
import pandas as pd

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOCO = 200   # mesmo corte do notebook, seção 9

# frações b de 2022 por faixa (notebook, seção 7): parcela de quem voltou às urnas que foi para Lula
TX_B = {"<35%": 0.301, "35-45%": 0.621, "45-55%": 0.331, "55-65%": 0.647, ">65%": 0.613}

NE = ["BA", "PE", "CE", "MA", "PI", "RN", "PB", "AL", "SE"]
RMSP = ["SAO PAULO", "SÃO PAULO", "GUARULHOS", "OSASCO", "SANTO ANDRÉ",
        "SÃO BERNARDO DO CAMPO", "SÃO CAETANO DO SUL", "DIADEMA", "MAUÁ", "BARUERI",
        "COTIA", "TABOÃO DA SERRA", "CARAPICUÍBA", "ITAPEVI", "EMBU DAS ARTES",
        "ITAQUAQUECETUBA", "SUZANO", "MOGI DAS CRUZES", "SANTOS", "SÃO VICENTE",
        "GUARUJÁ", "JANDIRA", "FERRAZ DE VASCONCELOS", "SANTANA DE PARNAÍBA"]


def frente(r):
    if r["uf"] == "MG": return "Minas Gerais"
    if r["uf"] == "SP" and r["municipio"] in RMSP: return "Metropolitana de SP"
    if r["uf"] == "SP": return "Interior de SP"
    if r["uf"] in NE: return "Nordeste urbano"
    if r["uf"] in ("GO", "DF", "MT", "MS", "TO"): return "Goiás e entorno"
    if r["uf"] == "RJ": return "Rio de Janeiro"
    if r["uf"] in ("RS", "SC", "PR"): return "Sul"
    return "Norte e demais"


def acao(r):
    """Ação principal, pela composição do potencial do município."""
    parte = r["terreno_perdido"] / r["prioridade"] if r["prioridade"] > 0 else 0
    if parte >= 0.6: return "reconquistar"
    if parte <= 0.4: return "mobilizar"
    return "ambas"


def main():
    d = pd.read_csv(os.path.join(RAIZ, "painel", "painel_final.csv"))
    d["mobilizacao_2pp"] = np.maximum(d["saldo_pp"], 0)*2
    NAC = np.average(d["desloc"], weights=d["validos_26"])
    gap = d["bolso_26"].sum() - d["lula_26"].sum()

    t = d.sort_values("prioridade", ascending=False).head(FOCO).copy()
    coord = pd.read_csv(os.path.join(RAIZ, "dados", "geo", "municipios_coordenadas.csv"))
    t = t.merge(coord[["codigo_ibge", "latitude", "longitude", "nome"]],
                left_on="cd_municipio_ibge", right_on="codigo_ibge", how="left")
    assert t["latitude"].notna().all(), "município sem coordenada"

    cidades = []
    for i, r in enumerate(t.itertuples(index=False), 1):
        r = r._asdict()
        cidades.append({
            "rank": i, "nome": r["nome"], "uf": r["uf"], "lat": r["latitude"], "lon": r["longitude"],
            "frente": frente(r), "acao": acao(r),
            "mob_prejudica": bool(TX_B[r["faixa"]] < 0.5),
            "faixa": r["faixa"], "b": TX_B[r["faixa"]],
            "lula": round(r["lula_pct_26"], 1), "lula22": round(r["lula_pct_22_2t"], 1),
            "desloc": round(r["desloc"], 2), "anomalia": round(r["anomalia"], 2),
            "aptos": int(r["aptos_26"]), "validos": int(r["validos_26"]),
            "abst": int(r["abstencao_26"]), "abst_pct": round(r["absten_pct_26"], 1),
            "saldo": int(r["lula_26"] - r["bolso_26"]),
            "terreno": round(r["terreno_perdido"]), "mob": round(r["mobilizacao_2pp"]),
            "pot": round(r["prioridade"]),
        })

    meta = {
        "foco": FOCO, "municipios_pais": len(d), "nac_desloc": round(NAC, 2), "gap": int(gap),
        "pot_foco": round(t["prioridade"].sum()), "pot_pais": round(d["prioridade"].sum()),
        "aptos_foco": int(t["aptos_26"].sum()), "aptos_pais": int(d["aptos_26"].sum()),
    }
    ufs = json.load(open(os.path.join(RAIZ, "dados", "geo", "ibge_ufs_qualidade_minima.json")))

    dados = json.dumps({"meta": meta, "cidades": cidades, "ufs": ufs},
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
    print(json.dumps(meta, ensure_ascii=False))
    print(pd.Series([c["acao"] for c in cidades]).value_counts().to_dict(),
          "| mobilização contraindicada:", sum(c["mob_prejudica"] for c in cidades))


if __name__ == "__main__":
    main()
