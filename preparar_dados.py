#!/usr/bin/env python3
"""Monta o painel municipal que a análise do 2º turno usa.

Junta, por município (código IBGE):

  2026 1º turno   nossa coleta do TSE (dados-tse-2026-1T), copiada em dados/tse2026
  2022 1º e 2º    TSE, votacao_candidato_munzona_2022_BR.csv
  2018 1º e 2º    TSE, votacao_candidato_munzona_2018_BR.csv
  Censo 2022      IBGE: renda, alfabetização, população
  PIB 2021        IBGE

Uma linha por município, com voto, comparecimento e perfil social. É o
insumo único do notebook — a análise não volta a tocar em arquivo cru.
"""
import csv, io, json, gzip, os, sys, urllib.request, zipfile
import pandas as pd

RAIZ   = os.path.dirname(os.path.abspath(__file__))
DADOS  = os.path.join(RAIZ, "dados")
PAINEL = os.path.join(RAIZ, "painel")
CSV26  = os.path.join(DADOS, "tse2026")   # recorte de presidente/município da coleta dados-tse-2026-1T

LULA, BOLSO = "13", "22"


# --------------------------------------------------------------- 2026

def ler_2026():
    cand = pd.read_csv(os.path.join(CSV26, "candidatos", "municipio", "presidente",
                                    "TODOS.csv"), dtype=str) if False else None
    partes = []
    pasta = os.path.join(CSV26, "candidatos", "municipio", "presidente")
    for arq in sorted(os.listdir(pasta)):
        partes.append(pd.read_csv(os.path.join(pasta, arq), dtype=str))
    cand = pd.concat(partes, ignore_index=True)
    cand["votos"] = pd.to_numeric(cand["votos"], errors="coerce").fillna(0)

    chave = ["uf", "cd_municipio_tse", "cd_municipio_ibge", "municipio"]
    tabela = cand.pivot_table(index=chave, columns="numero_urna", values="votos",
                              aggfunc="sum").fillna(0)
    outros = [c for c in tabela.columns if c not in (LULA, BOLSO)]
    saida = pd.DataFrame({
        "lula_26": tabela.get(LULA, 0),
        "bolso_26": tabela.get(BOLSO, 0),
        "terceiros_26": tabela[outros].sum(axis=1),
    }).reset_index()

    # o 3º colocado nacional isolado: a composição do resto importa para
    # estimar transferência, não só o tamanho
    nac = cand.groupby("numero_urna")["votos"].sum().sort_values(ascending=False)
    terceiro = [n for n in nac.index if n not in (LULA, BOLSO)][0]
    saida["terceiro_colocado_26"] = tabela.get(terceiro, 0).values

    partes = []
    pasta = os.path.join(CSV26, "totais", "municipio", "presidente")
    for arq in sorted(os.listdir(pasta)):
        partes.append(pd.read_csv(os.path.join(pasta, arq), dtype=str))
    tot = pd.concat(partes, ignore_index=True)
    cols = {"eleitorado_apto": "aptos_26", "comparecimento": "comparec_26",
            "abstencao": "abstencao_26", "votos_validos": "validos_26",
            "votos_brancos": "brancos_26", "votos_nulos_total": "nulos_26",
            "secoes_totalizadas": "secoes_tot_26", "secoes_total": "secoes_26"}
    for c in cols:
        tot[c] = pd.to_numeric(tot[c], errors="coerce")
    tot = tot[["uf", "cd_municipio_tse"] + list(cols)].rename(columns=cols)

    saida = saida.merge(tot, on=["uf", "cd_municipio_tse"], how="left")
    saida["cd_mun_tse"] = saida["cd_municipio_tse"].str.lstrip("0")
    return saida, terceiro


# ------------------------------------------------------- TSE histórico

def ler_historico(zip_nome, interno, ano):
    """Votos de presidente por município e turno, de um zip do TSE."""
    caminho = os.path.join(DADOS, zip_nome)
    # O número do adversário muda de eleição para eleição (Bolsonaro foi 17 em
    # 2018 e 22 em 2022). Em vez de fixar, descobre quem foi o segundo mais
    # votado do 1º turno naquele ano e usa esse número.
    bruto = []
    with zipfile.ZipFile(caminho) as z:
        with z.open(interno) as f:
            r = csv.DictReader(io.TextIOWrapper(f, encoding="latin-1"), delimiter=";")
            for l in r:
                if l["CD_CARGO"] != "1":
                    continue
                bruto.append((l["SG_UF"], l["CD_MUNICIPIO"], l["NR_TURNO"],
                              l["NR_CANDIDATO"], int(l["QT_VOTOS_NOMINAIS"] or 0)))

    nacional = {}
    for _, _, turno, nr, v in bruto:
        if turno == "1":
            nacional[nr] = nacional.get(nr, 0) + v
    ordem = sorted(nacional, key=nacional.get, reverse=True)
    adversario = next(n for n in ordem if n != LULA)
    print(f"  adversário em {ano}: nº {adversario} "
          f"({nacional[adversario]:,} votos no 1º turno)".replace(",", "."), flush=True)

    linhas = {}
    for uf, mun, turno, nr, v in bruto:
        d = linhas.setdefault((uf, mun, turno), {"lula": 0, "bolso": 0, "outros": 0})
        if nr == LULA:
            d["lula"] += v
        elif nr == adversario:
            d["bolso"] += v
        else:
            d["outros"] += v

    reg = []
    for (uf, mun, turno), d in linhas.items():
        reg.append({"uf": uf, "cd_mun_tse": mun.lstrip("0"), "turno": int(turno), **d})
    df = pd.DataFrame(reg)
    saida = None
    for turno in sorted(df["turno"].unique()):
        p = df[df["turno"] == turno].drop(columns="turno").set_index(["uf", "cd_mun_tse"])
        p.columns = [f"{c}_{ano}_{turno}t" for c in p.columns]
        saida = p if saida is None else saida.join(p, how="outer")
    return saida.reset_index()


# ----------------------------------------------------------- IBGE

def ibge(agregado, variavel, periodo, nome, cache):
    arq = os.path.join(cache, f"ibge_{agregado}_{variavel}_{periodo}.json")
    if not os.path.exists(arq):
        url = (f"https://servicodados.ibge.gov.br/api/v3/agregados/{agregado}"
               f"/periodos/{periodo}/variaveis/{variavel}?localidades=N6[all]")
        req = urllib.request.Request(url, headers={"Accept-Encoding": "gzip",
                                                   "User-Agent": "BrasilDeFato/1.0"})
        b = urllib.request.urlopen(req, timeout=300).read()
        if b[:2] == b"\x1f\x8b":
            b = gzip.decompress(b)
        open(arq, "wb").write(b)
    d = json.load(open(arq, encoding="utf-8"))
    reg = []
    for s in d[0]["resultados"][0]["series"]:
        v = list(s["serie"].values())[0]
        reg.append({"cd_municipio_ibge": int(s["localidade"]["id"]),
                    nome: pd.to_numeric(v, errors="coerce")})
    return pd.DataFrame(reg)


def ler_social():
    cache = os.path.join(DADOS, "ibge")
    os.makedirs(cache, exist_ok=True)
    pecas = [
        ibge(10295, 13431, 2022, "renda_dom_pc", cache),      # renda domiciliar per capita
        ibge(10289, 13537, 2022, "rend_mediano_trab", cache), # rendimento mediano do trabalho
        ibge(10091, 2513, 2022, "alfabetizacao", cache),      # taxa de alfabetização 15+
        ibge(4709, 93, 2022, "populacao", cache),             # população residente
        ibge(5938, 37, 2021, "pib_mil", cache),               # PIB a preços correntes
    ]
    social = pecas[0]
    for p in pecas[1:]:
        social = social.merge(p, on="cd_municipio_ibge", how="outer")
    social["pib_pc"] = social["pib_mil"] * 1000 / social["populacao"]
    return social


# ----------------------------------------------------------- montagem

def main():
    print("lendo 2026 ...", flush=True)
    base, terceiro = ler_2026()
    print(f"  {len(base)} municípios | 3º colocado nacional: nº {terceiro}", flush=True)

    for ano, zipn, interno in (
        (2022, "votacao_candidato_munzona_2022.zip", "votacao_candidato_munzona_2022_BR.csv"),
        (2018, "votacao_candidato_munzona_2018.zip", "votacao_candidato_munzona_2018_BR.csv")):
        if not os.path.exists(os.path.join(DADOS, zipn)):
            print(f"  (sem {zipn}, pulando {ano})", flush=True)
            continue
        print(f"lendo {ano} ...", flush=True)
        h = ler_historico(zipn, interno, ano)
        print(f"  {len(h)} municípios", flush=True)
        base = base.merge(h, on=["uf", "cd_mun_tse"], how="left")

    print("lendo IBGE ...", flush=True)
    social = ler_social()
    base["cd_municipio_ibge"] = pd.to_numeric(base["cd_municipio_ibge"], errors="coerce")
    base = base.merge(social, on="cd_municipio_ibge", how="left")

    os.makedirs(PAINEL, exist_ok=True)
    destino = os.path.join(PAINEL, "painel_municipios.csv")
    base.to_csv(destino, index=False)
    print(f"\n{len(base)} linhas x {len(base.columns)} colunas -> {destino}")
    print("\ncobertura das colunas principais:")
    for c in ("lula_26", "lula_2022_1t", "lula_2022_2t", "lula_2018_2t",
              "renda_dom_pc", "alfabetizacao", "pib_pc"):
        if c in base.columns:
            print(f"  {c:22s} {base[c].notna().sum():5d}/{len(base)} preenchidos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
