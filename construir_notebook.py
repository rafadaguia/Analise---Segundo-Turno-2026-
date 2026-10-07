#!/usr/bin/env python3
"""Monta o notebook da análise do 2º turno."""
import nbformat as nbf

nb = nbf.v4.new_notebook()
C = []
md = lambda t: C.append(nbf.v4.new_markdown_cell(t))
co = lambda t: C.append(nbf.v4.new_code_cell(t))

md("""# Onde Lula ainda tem voto a buscar no 2º turno de 2026

**Brasil de Fato — núcleo de dados** · análise de 05/10/2026, revista em 07/10/2026

Esta análise cruza o resultado do 1º turno de 2026 com as eleições de 2018 e 2022 e com
o perfil social dos municípios, para responder a uma pergunta operacional: **onde a
campanha deve gastar tempo e dinheiro entre os turnos?**

O recorte é geográfico — Estado e município —, mas a leitura é social: o que separa um
município onde ainda há voto a buscar de outro onde não há é renda, escolaridade e
história eleitoral, não posição no mapa.

> **Aviso de método.** Isto é análise de dados agregados, não previsão. Todos os números
> descrevem o comportamento de municípios, não de pessoas: concluir que *eleitores pobres
> votam em Lula* a partir de que *municípios pobres votam mais em Lula* é falácia
> ecológica. As projeções supõem que as taxas de transferência observadas em 2022 se
> repetem, o que é uma hipótese forte e provavelmente otimista — a terceira via de 2026 é
> mais à direita que a de 2022. Nada aqui substitui pesquisa de intenção de voto.""")

md("""## Resumo executivo

> **Revisão de 07/10/2026.** As taxas de transferência foram reestimadas com inferência
> ecológica bayesiana (seção 10), e os números de potencial ganharam intervalos de 90% por
> simulação de Monte Carlo (seção 11). A revisão mudou duas conclusões da versão de
> 05/10: a "anomalia" da faixa de 45% a 55% era artefato do método, e o retorno da
> mobilização estava superestimado. Este resumo já reflete a versão revisada. As seções 6 a 9
> ficam como estavam, para registro, com remissões à revisão.

**O ponto de partida é ruim e a geografia sozinha não resolve.**

Lula terminou o 1º turno com 45,16% contra 47,03% de Flávio Bolsonaro, **2,24 milhões de
votos atrás**. Quatro achados definem o quadro:

1. **A geografia quase não mudou de 2022 para 2026.** A correlação entre o voto em Lula por
   município nos dois anos é de 0,987. Lula não perdeu lugares específicos: perdeu **5,98
   pontos em todo lugar, quase na mesma medida**.

2. **A terceira via joga contra.** Em 2022, mesmo com Tebet e Ciro declarando apoio, Lula
   levou entre 35% e 59% dos votos de terceira via que escolheram um dos dois, conforme o
   município. Em 2026 a terceira via (Cury, Renan Santos, Caiado, Zema) é mais à direita.

3. **Mobilizar só rende com segurança onde Lula já é muito forte.** Onde ele passa de 65%,
   três em cada quatro eleitores trazidos de volta às urnas votaram nele em 2022. Onde tem
   menos de 35%, só um em cada cinco. **No meio do mapa os dados não decidem**: o
   comparecimento extra se dividiu quase ao meio. A versão anterior dava 62% para Lula na
   faixa de 35% a 45%; o modelo bayesiano dá 47%, com intervalo de 32% a 64%.

4. **A dinâmica entre os turnos pesa mais que o mapa.** Se o movimento de 2022 se repetir, a
   diferença no 2º turno passa de 2,24 para algo entre 6,5 e 7 milhões. Em 2018, com outra
   terceira via, a margem do PT melhorou 7,2 milhões entre os turnos. Esse é o tamanho do
   que a campanha disputa fora da geografia.

**As frentes, com margem de erro.** São os 200 municípios de maior potencial, agrupados.
Potencial = terreno perdido acima da média + 2 pontos de comparecimento onde isso rende;
intervalos de 90% da simulação (seção 11).

| Frente | Focos | Potencial | Tática |
|---|---|---|---|
| **Região metropolitana de SP** | 14 | 110 mil (89–131 mil) | Persuasão. É a única frente em que o sinal da margem projetada está em jogo. Mobilização ampla tende a prejudicar. |
| **Goiás e entorno** | 40 | 106 mil (100–112 mil) | Maior queda do país. Persuasão e contenção de danos; levar mais gente às urnas favorece o adversário. |
| **Nordeste urbano** | 49 | 89 mil (66–114 mil) | A frente mais incerta, porque é a única onde mobilizar pesa. Mobilização segura só nas cidades onde Lula passa de 65%. |
| Sul | 42 | 66 mil (60–72 mil) | Persuasão. |
| Minas Gerais | 31 | 52 mil (47–58 mil) | Potencial difuso; exige capilaridade, não concentração. |
| Norte e demais | 13 | 21 mil (20–21 mil) | |
| Interior de SP | 11 | 16 mil (13–18 mil) | |

**A conta honesta:** os 200 focos somam **459 mil votos (de 407 a 514 mil), cerca de 20% da
diferença do 1º turno**, e quase tudo é terreno perdido a reconquistar por persuasão. O 2º
turno não se ganha no mapa. **O mapa diz onde a margem é mais barata e onde mobilizar é
seguro, não onde está a vitória.**""")

md("""## 1. Fontes

Todas oficiais, todas públicas.

| Fonte | O que traz | Uso |
|---|---|---|
| TSE — divulgação oficial `ele2026` | 1º turno de 2026 por município e zona | ponto de partida |
| TSE — dados abertos, `votacao_candidato_munzona_2022` | presidente 2022, 1º e 2º turnos | base histórica e taxas de transferência |
| TSE — dados abertos, `votacao_candidato_munzona_2018` | presidente 2018, 1º e 2º turnos | tendência de longo prazo |
| TSE — `detalhe_votacao_munzona_2022` | comparecimento, abstenção, brancos e nulos por turno | dinâmica de comparecimento |
| IBGE — Censo 2022 (SIDRA 10295, 10289, 10091, 4709) | renda domiciliar per capita, rendimento mediano, alfabetização, população | perfil social |
| IBGE — PIB municipal 2021 (SIDRA 5938) | PIB per capita | perfil econômico |

**Não usamos pesquisas de intenção de voto.** No dia seguinte ao 1º turno ainda não há
pesquisa registrada no TSE para o 2º turno. Quando houver, elas devem ser o primeiro
contraste a fazer com estas estimativas.""")

co("""import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 50)
plt.rcParams.update({"figure.dpi": 110, "font.size": 9,
                     "axes.grid": True, "grid.alpha": 0.25,
                     "axes.spines.top": False, "axes.spines.right": False})

VERMELHO, AZUL, CINZA = "#E10012", "#4F80FF", "#8A8A8A"

d = pd.read_csv("painel/painel_final.csv", dtype={"cd_mun_tse": str})
print(f"{len(d)} municípios x {len(d.columns)} colunas")

def mil(v):
    return f"{v:,.0f}".replace(",", ".")""")

md("""## 2. O ponto de partida

Antes de procurar onde ganhar, é preciso saber quanto falta.""")

co("""val = d["validos_26"].sum()
lula, bolso, terc = d["lula_26"].sum(), d["bolso_26"].sum(), d["terceiros_26"].sum()
fora = d["abstencao_26"].sum() + d["brancos_26"].sum() + d["nulos_26"].sum()

print("1º TURNO DE 2026")
print(f"  Lula               {mil(lula):>12}   {100*lula/val:5.2f}%")
print(f"  Flávio Bolsonaro   {mil(bolso):>12}   {100*bolso/val:5.2f}%")
print(f"  terceira via       {mil(terc):>12}   {100*terc/val:5.2f}%")
print(f"  {'-'*44}")
print(f"  diferença          {mil(bolso-lula):>12}   {100*(bolso-lula)/val:5.2f} pp")
print()
print(f"  fora do jogo (abstenção + brancos + nulos)  {mil(fora)}")
print(f"  ... equivalente a {100*fora/d['aptos_26'].sum():.1f}% do eleitorado")""")

md("""Para comparação, 2022 e 2018. O número 13 é sempre o PT; o adversário é o segundo mais
votado do 1º turno de cada ano (Bolsonaro, nº 17 em 2018 e nº 22 em 2022).""")

co("""hist = []
for ano in (2018, 2022):
    for turno in (1, 2):
        cols = [f"lula_{ano}_{turno}t", f"bolso_{ano}_{turno}t", f"outros_{ano}_{turno}t"]
        if cols[0] not in d:
            continue
        s = d[cols].sum()
        hist.append({"ano": ano, "turno": f"{turno}º",
                     "PT_%": 100*s.iloc[0]/s.sum(), "adversário_%": 100*s.iloc[1]/s.sum(),
                     "PT_votos": s.iloc[0]})
hist.append({"ano": 2026, "turno": "1º", "PT_%": 100*lula/val,
             "adversário_%": 100*bolso/val, "PT_votos": lula})
pd.DataFrame(hist).set_index(["ano", "turno"]).round(2)""")

md("""## 3. A geografia quase não mudou

Este é o achado que organiza todo o resto. Se Lula tivesse perdido lugares específicos,
haveria um mapa a reconquistar. Não foi o que aconteceu.""")

co("""d["val_22_2t"] = d[["lula_2022_2t", "bolso_2022_2t", "outros_2022_2t"]].sum(axis=1)
d["lula_pct_22_2t"] = 100*d["lula_2022_2t"]/d["val_22_2t"]
base = d.dropna(subset=["lula_pct_22_2t"]).copy()

r = np.corrcoef(base["lula_pct_22_2t"], base["lula_pct_26"])[0, 1]
X = sm.add_constant(base["lula_pct_22_2t"])
mod = sm.OLS(base["lula_pct_26"], X).fit()
print(f"correlação entre o voto em Lula por município, 2022 (2T) e 2026 (1T): r = {r:.4f}")
print(f"regressão: lula_2026 = {mod.params.iloc[0]:+.2f} + {mod.params.iloc[1]:.3f} * lula_2022    R² = {mod.rsquared:.4f}")
print()
print("Coeficiente ~1 com constante ~-7: a nuvem inteira desceu, quase sem mudar de forma.")""")

co("""fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.4))

a1.scatter(base["lula_pct_22_2t"], base["lula_pct_26"], s=3, alpha=.18, color=VERMELHO, lw=0)
lim = [0, 100]
a1.plot(lim, lim, color=CINZA, lw=1, ls="--", label="sem mudança")
xs = np.linspace(0, 100, 10)
a1.plot(xs, mod.params.iloc[0] + mod.params.iloc[1]*xs, color="black", lw=1.4,
        label=f"ajuste (R²={mod.rsquared:.3f})")
a1.set_xlabel("Lula em 2022, 2º turno (% dos válidos)")
a1.set_ylabel("Lula em 2026, 1º turno (%)")
a1.set_title("Cada ponto é um município", loc="left", fontsize=10, weight="bold")
a1.legend(frameon=False, fontsize=8)
a1.set_xlim(0, 100); a1.set_ylim(0, 100)

base["desloc"] = base["lula_pct_26"] - base["lula_pct_22_2t"]
nac = np.average(base["desloc"], weights=base["validos_26"])
a2.hist(base["desloc"], bins=70, color=VERMELHO, alpha=.75)
a2.axvline(nac, color="black", lw=1.4)
a2.annotate(f"média ponderada\\n{nac:+.2f} pp", xy=(nac, a2.get_ylim()[1]*.8),
            xytext=(nac-9, a2.get_ylim()[1]*.86), fontsize=8,
            arrowprops=dict(arrowstyle="->", lw=.8))
a2.set_xlabel("deslocamento de Lula, 2026 (1T) menos 2022 (2T), em pontos percentuais")
a2.set_ylabel("municípios")
a2.set_title("A perda foi difusa, não concentrada", loc="left", fontsize=10, weight="bold")
fig.tight_layout(); plt.show()

print(f"desvio-padrão do deslocamento: {base['desloc'].std():.2f} pp")
print(f"intervalo p10–p90: {base['desloc'].quantile(.1):+.2f} a {base['desloc'].quantile(.9):+.2f} pp")""")

md("""O histograma concentra-se entre −11 e −4 pontos. Não há uma cauda de municípios
"perdidos": há um país inteiro deslocado. **A margem de manobra está na variação em torno
dessa média**, não na média.""")

md("""## 4. O que explica o voto em Lula: correlação

Antes de modelar, olhar as correlações simples. Elas já mostram que o voto tem estrutura
social forte e estrutura de abstenção nenhuma.""")

co("""d["absten_pct_26"] = 100*d["abstencao_26"]/d["aptos_26"]
d["ter_pct_26"] = 100*d["terceiros_26"]/d["validos_26"]

vars_ = {"lula_pct_22_2t": "Lula 2022 (2º turno)",
         "lula_2018_2t": "PT 2018 (2º turno, votos)",
         "renda_dom_pc": "renda domiciliar per capita",
         "rend_mediano_trab": "rendimento mediano do trabalho",
         "alfabetizacao": "taxa de alfabetização",
         "pib_pc": "PIB per capita",
         "populacao": "população",
         "absten_pct_26": "abstenção 2026 (%)",
         "ter_pct_26": "terceira via 2026 (%)"}

linhas = []
for c, rot in vars_.items():
    s = d[[c, "lula_pct_26"]].dropna()
    linhas.append({"variável": rot, "r": np.corrcoef(s[c], s["lula_pct_26"])[0, 1], "n": len(s)})
corr = pd.DataFrame(linhas).sort_values("r")
display(corr.round(3).to_string(index=False))

fig, ax = plt.subplots(figsize=(7.2, 3.4))
cores = [VERMELHO if v > 0 else AZUL for v in corr["r"]]
ax.barh(corr["variável"], corr["r"], color=cores)
ax.axvline(0, color="black", lw=.8)
ax.set_xlabel("correlação com o % de Lula em 2026")
ax.set_title("Renda e escolaridade puxam contra; abstenção é neutra",
             loc="left", fontsize=10, weight="bold")
fig.tight_layout(); plt.show()""")

md("""Dois pontos valem destaque:

- **Renda e alfabetização correlacionam forte e negativamente** (−0,79 e −0,82). É o eixo
  social clássico do voto em Lula, e continua firme em 2026.
- **A abstenção não correlaciona com nada** (r = −0,02). Isso derruba a ideia de que
  "quem não foi votar é eleitor de Lula". Não é — nem o contrário. Onde a abstenção
  ajuda ou atrapalha depende do município, e é isso que a seção 6 mede.""")

md("""## 5. Modelo estrutural: onde Lula está abaixo do próprio potencial

Regressão do percentual de Lula em 2026 sobre a base histórica, o perfil social e efeito
fixo de UF. O que interessa não é o ajuste — é o **resíduo**: municípios que votaram menos
em Lula do que o seu próprio perfil faria esperar.""")

co("""mdl = d.dropna(subset=["lula_pct_22_2t", "renda_dom_pc", "alfabetizacao", "populacao"]).copy()
mdl["log_renda"] = np.log(mdl["renda_dom_pc"])
mdl["log_pop"] = np.log(mdl["populacao"])

X = pd.get_dummies(mdl[["lula_pct_22_2t", "log_renda", "alfabetizacao", "log_pop", "uf"]],
                   columns=["uf"], drop_first=True).astype(float)
X = sm.add_constant(X)
est = sm.OLS(mdl["lula_pct_26"].astype(float), X).fit()

print(f"n = {int(est.nobs)}   R² = {est.rsquared:.4f}   (inclui efeito fixo de UF)\\n")
for nome in ["const", "lula_pct_22_2t", "log_renda", "alfabetizacao", "log_pop"]:
    print(f"  {nome:18s} coef = {est.params[nome]:+8.4f}   erro = {est.bse[nome]:.4f}   p = {est.pvalues[nome]:.2g}")

mdl["resid"] = est.resid
print(f"\\nresíduo: média {mdl['resid'].mean():+.3f} pp, desvio {mdl['resid'].std():.2f} pp")""")

md("""Leitura dos coeficientes:

- **`lula_pct_22_2t` = +0,90** — o passado manda. Cada ponto que Lula tinha em 2022 vale
  0,90 ponto em 2026.
- **`log_renda` = −2,62** — dobrar a renda domiciliar per capita do município custa cerca
  de 2,6 pontos a Lula, *já controlando pela história eleitoral*. É efeito social puro.
- **`alfabetizacao` ≈ 0 e não significante** — a escolaridade aparece forte na correlação
  simples, mas some quando se controla por renda e por 2022. Ela não acrescenta
  informação própria; é um reflexo da renda.
- **`log_pop` = +0,50** — municípios maiores votam um pouco mais em Lula, mantido o resto
  constante.""")

md("""## 6. O mecanismo: para onde foram os votos entre os turnos de 2022

Esta é a parte decisiva. Entre o 1º e o 2º turno existe uma quantidade conhecida de votos
em disputa, e uma identidade contábil que fecha:

```
votos em disputa = terceira via no 1º turno
                 + variação do comparecimento
                 − variação de brancos e nulos
```

Tudo isso vira voto de Lula, voto do adversário, ou nada. Estimamos as duas frações com
regressão **sem intercepto**, para que os coeficientes somem exatamente 1.""")

co("""h = d.dropna(subset=["QT_COMPARECIMENTO_1t"]).copy()
h["bn_1t"] = h["QT_VOTOS_BRANCOS_1t"] + h["QT_VOTOS_NULOS_1t"]
h["bn_2t"] = h["QT_VOTOS_BRANCOS_2t"] + h["QT_VOTOS_NULOS_2t"]
h["dcomp_liq"] = (h["QT_COMPARECIMENTO_2t"] - h["QT_COMPARECIMENTO_1t"]) - (h["bn_2t"] - h["bn_1t"])
h["terc"] = h["outros_2022_1t"]
h["dlula"] = h["lula_2022_2t"] - h["lula_2022_1t"]
h["dbols"] = h["bolso_2022_2t"] - h["bolso_2022_1t"]
h["pool"] = h["terc"] + h["dcomp_liq"]

t = h[["pool", "dlula", "dbols"]].sum()
print("2022 — BRASIL")
print(f"  votos em disputa entre os turnos   {mil(t['pool']):>12}")
print(f"  foram para Lula                    {mil(t['dlula']):>12}   {100*t['dlula']/t['pool']:.1f}%")
print(f"  foram para Bolsonaro               {mil(t['dbols']):>12}   {100*t['dbols']/t['pool']:.1f}%")
print(f"  resíduo da identidade              {mil(t['pool']-t['dlula']-t['dbols']):>12}")""")

co("""hh = h[h["terc"] > 300].copy()
hh["faixa"] = pd.cut(hh["lula_pct_22_2t"], [0, 35, 45, 55, 65, 100],
                     labels=["<35%", "35-45%", "45-55%", "55-65%", ">65%"])

linhas = []
for faixa in list(hh["faixa"].cat.categories) + ["TODOS"]:
    s = hh if faixa == "TODOS" else hh[hh["faixa"] == faixa]
    Xs = s[["terc", "dcomp_liq"]].astype(float)
    rl = sm.OLS(s["dlula"].astype(float), Xs).fit()
    rb = sm.OLS(s["dbols"].astype(float), Xs).fit()
    linhas.append({
        "força de Lula em 2022": str(faixa), "municípios": len(s),
        "terceira via → Lula": rl.params["terc"],
        "terceira via → adversário": rb.params["terc"],
        "quem voltou → Lula": rl.params["dcomp_liq"],
        "quem voltou → adversário": rb.params["dcomp_liq"]})
taxas = pd.DataFrame(linhas).set_index("força de Lula em 2022")
display(taxas.round(3))""")

co("""tx = taxas.drop("TODOS")
fig, ax = plt.subplots(figsize=(7.6, 3.6))
x = np.arange(len(tx)); larg = 0.36
ax.bar(x - larg/2, tx["terceira via → Lula"], larg, color=CINZA, label="votos de terceira via")
ax.bar(x + larg/2, tx["quem voltou → Lula"], larg, color=VERMELHO, label="eleitores que voltaram às urnas")
ax.axhline(0.5, color="black", lw=1, ls="--")
ax.annotate("acima da linha, Lula ganha a troca", xy=(3.2, .52), fontsize=8)
ax.set_xticks(x); ax.set_xticklabels(tx.index)
ax.set_xlabel("quanto Lula tinha no 2º turno de 2022 (% dos válidos no município)")
ax.set_ylabel("fração capturada por Lula")
ax.set_ylim(0, .8)
ax.set_title("Mobilizar funciona; herdar terceira via, não", loc="left", fontsize=10, weight="bold")
ax.legend(frameon=False, fontsize=8)
fig.tight_layout(); plt.show()""")

md("""Três conclusões operacionais saem deste gráfico:

1. **A terceira via nunca passou de 44%** para Lula, nem nos municípios onde ele tinha
   mais de 65% dos votos — e isso em 2022, quando Tebet e Ciro o apoiaram no 2º turno. Em
   2026 a terceira via é Cury, Renan Santos, Caiado e Zema, todos à direita de Lula.
   **A hipótese realista é uma transferência pior que a de 2022, não melhor.**

2. **Quem volta às urnas vota em Lula na maioria dos casos — mas só em parte do mapa.**
   Nas faixas de 35–45%, 55–65% e acima de 65%, entre 61% e 65% dos eleitores recuperados
   foram para ele. Na faixa abaixo de 35%, só 30%.

3. **A faixa de 45–55% é a exceção estranha** *(revisto na seção 10: era artefato do método)*: ali quem voltou votou 67% no adversário.
   São municípios de disputa equilibrada onde a mobilização de 2022 foi do outro lado.
   Registramos o que os dados mostram, sem alisar a curva — mas é o resultado de que
   menos confiamos, e merece checagem antes de virar decisão.""")

md("""## 7. Os reservatórios, em votos

Com as taxas da seção anterior, dá para pôr número em cada caminho possível.""")

co("""TX_A = {"<35%": 0.215, "35-45%": 0.306, "45-55%": 0.407, "55-65%": 0.407, ">65%": 0.436}
TX_B = {"<35%": 0.301, "35-45%": 0.621, "45-55%": 0.331, "55-65%": 0.647, ">65%": 0.613}

d["faixa"] = pd.cut(d["lula_pct_26"], [0, 35, 45, 55, 65, 100],
                    labels=list(TX_A)).astype(str)
d["a"] = d["faixa"].map(TX_A)
d["b"] = d["faixa"].map(TX_B)

# saldo líquido = o que Lula ganha menos o que o adversário ganha
d["saldo_terceira_via"] = d["terceiros_26"] * (2*d["a"] - 1)
d["saldo_por_pp"] = d["aptos_26"] * 0.01 * (2*d["b"] - 1)

gap = bolso - lula
print("RESERVATÓRIOS (saldo líquido para Lula, em votos)\\n")
print(f"  terceira via, à taxa de 2022        {mil(d['saldo_terceira_via'].sum()):>12}")
print(f"  comparecimento, +1 pp em todo país  {mil(d['saldo_por_pp'].sum()):>12}")
print(f"  comparecimento, +1 pp só onde rende {mil(d.loc[d['saldo_por_pp']>0,'saldo_por_pp'].sum()):>12}")
print(f"  {'-'*48}")
print(f"  diferença a cobrir                  {mil(gap):>12}")""")

md("""Dois números pesam:

- Se a terceira via se comportar como em 2022, ela **tira** de Lula um saldo líquido de
  cerca de 1,9 milhão de votos. O reservatório que parece mais óbvio é o que mais custa.
- Um ponto percentual de comparecimento a mais **no país inteiro** dá saldo negativo. O
  mesmo ponto, **aplicado só onde rende**, dá cerca de 184 mil votos líquidos. É a
  diferença entre fazer campanha em todo lugar e fazer campanha em algum lugar.""")

md("""## 8. Terreno perdido acima da média

Como a perda foi quase uniforme (−5,98 pp), o que distingue um município do outro é
**quanto ele caiu além da média**. Essa diferença é o terreno que peers comparáveis não
perderam — e, portanto, o que há de mais concreto para reconquistar.""")

co("""d["desloc"] = d["lula_pct_26"] - d["lula_pct_22_2t"]
NAC = np.average(d["desloc"].fillna(0), weights=d["validos_26"])
d["anomalia"] = d["desloc"] - NAC
d["terreno_perdido"] = np.where(d["anomalia"] < 0, -d["anomalia"]/100*d["validos_26"], 0)

# índice: terreno a recuperar + mobilização realista (+2 pp onde ela rende)
d["mobilizacao_2pp"] = np.maximum(d["saldo_por_pp"], 0) * 2
d["prioridade"] = d["terreno_perdido"] + d["mobilizacao_2pp"]

print(f"deslocamento nacional ponderado: {NAC:+.2f} pp")
print(f"terreno perdido acima da média:  {mil(d['terreno_perdido'].sum())} votos")
print(f"mobilização realista (+2 pp):    {mil(d['mobilizacao_2pp'].sum())} votos")
print(f"potencial somado:                {mil(d['prioridade'].sum())} votos")
print(f"diferença a cobrir:              {mil(gap)} votos")
print()
print(f"-> o potencial geográfico cobre {100*d['prioridade'].sum()/gap:.0f}% da diferença.")""")

co("""pos = d.sort_values("prioridade", ascending=False)
acum = pos["prioridade"].cumsum() / pos["prioridade"].sum()

fig, ax = plt.subplots(figsize=(7.2, 3.4))
ax.plot(range(1, len(acum)+1), 100*acum.values, color=VERMELHO, lw=1.6)
for k in (50, 200, 400):
    ax.plot([k, k], [0, 100*acum.iloc[k-1]], color=CINZA, lw=.8, ls=":")
    ax.annotate(f"{k} municípios\\n{100*acum.iloc[k-1]:.0f}%", xy=(k, 100*acum.iloc[k-1]),
                xytext=(k*1.25, 100*acum.iloc[k-1]-11), fontsize=8,
                arrowprops=dict(arrowstyle="->", lw=.7))
ax.set_xscale("log")
ax.set_xlabel("municípios, do maior potencial para o menor (escala log)")
ax.set_ylabel("% do potencial acumulado")
ax.set_title("Metade do potencial está em 400 municípios — 7% do país",
             loc="left", fontsize=10, weight="bold")
ax.set_ylim(0, 100)
fig.tight_layout(); plt.show()""")

md("""## 9. As frentes

### Por Estado""")

co("""g = d.groupby("uf")
uf = pd.DataFrame({
    "terreno_perdido": g["terreno_perdido"].sum(),
    "mobilizacao_2pp": g["mobilizacao_2pp"].sum(),
    "deslocamento_pp": g[["desloc", "validos_26"]].apply(
        lambda x: np.average(x["desloc"].fillna(0), weights=x["validos_26"])),
    "saldo_atual": g["lula_26"].sum() - g["bolso_26"].sum(),
    "lula_pct": 100*g["lula_26"].sum()/g["validos_26"].sum(),
})
uf["potencial"] = uf["terreno_perdido"] + uf["mobilizacao_2pp"]
uf["potencial_vs_deficit"] = np.where(uf["saldo_atual"] < 0,
                                      100*uf["potencial"]/-uf["saldo_atual"], np.nan)
top_uf = uf.sort_values("potencial", ascending=False).head(14)
display(top_uf.round(1))""")

co("""fig, ax = plt.subplots(figsize=(8, 4.2))
t = top_uf.sort_values("potencial")
ax.barh(t.index, t["terreno_perdido"], color=VERMELHO, label="terreno perdido acima da média")
ax.barh(t.index, t["mobilizacao_2pp"], left=t["terreno_perdido"], color=AZUL,
        label="mobilização realista (+2 pp)")
for i, (nome, lin) in enumerate(t.iterrows()):
    ax.annotate(f"{lin['deslocamento_pp']:+.1f} pp", xy=(lin["potencial"], i),
                xytext=(6, -3), textcoords="offset points", fontsize=7.5, color="#555")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, p: f"{v/1000:.0f} mil"))
ax.set_xlabel("votos líquidos recuperáveis")
ax.set_title("Potencial por Estado (à direita, o deslocamento desde 2022)",
             loc="left", fontsize=10, weight="bold")
ax.legend(frameon=False, fontsize=8, loc="lower right")
fig.tight_layout(); plt.show()""")

md("""### As quatro frentes

Uma frente não é uma região administrativa: é um conjunto de municípios que compartilham o
mesmo problema e, por isso, a mesma tática. Em vez de desenhá-las no mapa, nós as tiramos
**do próprio ranking**: pegamos os municípios de maior potencial e os agrupamos.

O corte é nos 200 primeiros. É onde a curva da seção 8 ainda é íngreme — depois disso cada
município novo acrescenta pouco e dilui o esforço.""")

co("""FOCO = 200
alvo = d.sort_values("prioridade", ascending=False).head(FOCO).copy()

NE = ["BA", "PE", "CE", "MA", "PI", "RN", "PB", "AL", "SE"]
RMSP = ["SAO PAULO", "SÃO PAULO", "GUARULHOS", "OSASCO", "SANTO ANDRÉ",
        "SÃO BERNARDO DO CAMPO", "SÃO CAETANO DO SUL", "DIADEMA", "MAUÁ", "BARUERI",
        "COTIA", "TABOÃO DA SERRA", "CARAPICUÍBA", "ITAPEVI", "EMBU DAS ARTES",
        "ITAQUAQUECETUBA", "SUZANO", "MOGI DAS CRUZES", "SANTOS", "SÃO VICENTE",
        "GUARUJÁ", "JANDIRA", "FERRAZ DE VASCONCELOS", "SANTANA DE PARNAÍBA"]

def frente(r):
    if r["uf"] == "MG":
        return "1. Minas Gerais"
    if r["uf"] == "SP" and r["municipio"] in RMSP:
        return "2. Metropolitana de SP"
    if r["uf"] == "SP":
        return "2b. Interior de SP"
    if r["uf"] in NE:
        return "3. Nordeste urbano"
    if r["uf"] in ("GO", "DF", "MT", "MS", "TO"):
        return "4. Goiás e entorno"
    if r["uf"] == "RJ":
        return "5. Rio de Janeiro"
    if r["uf"] in ("RS", "SC", "PR"):
        return "6. Sul"
    return "7. Norte e demais"

alvo["frente"] = alvo.apply(frente, axis=1)

res = alvo.groupby("frente").agg(
    municípios=("municipio", "count"),
    eleitorado=("aptos_26", "sum"),
    saldo_atual=("lula_26", "sum"),
    terreno_perdido=("terreno_perdido", "sum"),
    mobilizacao_2pp=("mobilizacao_2pp", "sum"),
    potencial=("prioridade", "sum"))
gf = alvo.groupby("frente")
res["saldo_atual"] = gf["lula_26"].sum() - gf["bolso_26"].sum()
res["Lula_%"] = 100*gf["lula_26"].sum()/gf["validos_26"].sum()
res = res.sort_values("potencial", ascending=False)
res.loc["TOTAL"] = res.sum(numeric_only=True)
res.loc["TOTAL", "Lula_%"] = 100*alvo["lula_26"].sum()/alvo["validos_26"].sum()
# eficiência: quanto potencial existe por mil eleitores a cobrir
res["por_mil_eleitores"] = 1000*res["potencial"]/res["eleitorado"]

display(res[["municípios", "eleitorado", "Lula_%", "saldo_atual", "terreno_perdido",
             "mobilizacao_2pp", "potencial", "por_mil_eleitores"]].round(1).style.format(
    {"eleitorado": "{:,.0f}", "saldo_atual": "{:,.0f}", "terreno_perdido": "{:,.0f}",
     "mobilizacao_2pp": "{:,.0f}", "potencial": "{:,.0f}", "Lula_%": "{:.1f}",
     "por_mil_eleitores": "{:.1f}"}))""")

co("""print(f"{FOCO} municípios = {100*FOCO/len(d):.1f}% dos municípios do país")
print(f"   {mil(alvo['aptos_26'].sum())} eleitores "
      f"({100*alvo['aptos_26'].sum()/d['aptos_26'].sum():.0f}% do eleitorado nacional)")
print(f"   {mil(alvo['prioridade'].sum())} votos de potencial "
      f"({100*alvo['prioridade'].sum()/d['prioridade'].sum():.0f}% do potencial do país)")
print(f"   diferença a cobrir: {mil(gap)}")
print()
print("Comparação — e se a campanha fosse para todo lugar:")
for k in (FOCO, 1000, len(d)):
    sub = d.sort_values("prioridade", ascending=False).head(k)
    print(f"   {k:>5} municípios -> {100*sub['prioridade'].sum()/d['prioridade'].sum():5.1f}% do potencial, "
          f"{mil(sub['aptos_26'].sum()):>12} eleitores a cobrir")
print()
print("O potencial é quase proporcional ao eleitorado: concentrar não multiplica o retorno.")
print("O que concentrar evita é o PREJUÍZO — e esse é muito desigual:")
bom = d[d["saldo_por_pp"] > 0]; ruim2 = d[d["saldo_por_pp"] < 0]
print(f"   onde mobilizar rende:    {len(bom):>5} municípios, {mil(bom['aptos_26'].sum()):>12} eleitores, "
      f"{mil(bom['saldo_por_pp'].sum()):>9} votos por +1 pp")
print(f"   onde mobilizar prejudica:{len(ruim2):>5} municípios, {mil(ruim2['aptos_26'].sum()):>12} eleitores, "
      f"{mil(ruim2['saldo_por_pp'].sum()):>9} votos por +1 pp")""")

md("""### Os 40 municípios prioritários""")

co("""cols = ["municipio", "uf", "faixa", "lula_pct_26", "desloc", "validos_26",
        "abstencao_26", "terreno_perdido", "mobilizacao_2pp", "prioridade"]
top = pos.head(40)[cols].copy()
top["lula_pct_26"] = top["lula_pct_26"].round(1)
top["desloc"] = top["desloc"].round(1)
top.insert(0, "#", range(1, len(top)+1))
display(top.set_index("#").style.format({
    "validos_26": "{:,.0f}", "abstencao_26": "{:,.0f}", "terreno_perdido": "{:,.0f}",
    "mobilizacao_2pp": "{:,.0f}", "prioridade": "{:,.0f}"}))""")

md("""### Onde **não** investir

*Revisto nas seções 10 e 11: com o modelo bayesiano, a mobilização é claramente prejudicial
abaixo de 35% e claramente favorável acima de 65%; no meio, os dados não decidem.*

Mobilizar não é neutro. Nos municípios em que Lula ficou abaixo de 35%, cada eleitor
trazido de volta à urna vota 70% das vezes no adversário.""")

co("""perigo = d.groupby("faixa").agg(
    municipios=("municipio", "count"),
    eleitorado=("aptos_26", "sum"),
    abstencao=("abstencao_26", "sum"),
    saldo_por_pp=("saldo_por_pp", "sum")).reindex(list(TX_B))
perigo["por_novo_eleitor"] = 2*pd.Series(TX_B) - 1
display(perigo.round(2))

ruim = d[d["saldo_por_pp"] < 0]
print(f"\\n{len(ruim)} municípios ({100*len(ruim)/len(d):.0f}% do país, "
      f"{mil(ruim['aptos_26'].sum())} eleitores) têm saldo NEGATIVO de mobilização.")
print(f"Somados, uma campanha de comparecimento de +1 pp neles custaria "
      f"{mil(-ruim['saldo_por_pp'].sum())} votos líquidos a Lula.")""")

md("""## 10. Revisão: as taxas de transferência com inferência ecológica bayesiana

*Seção acrescentada em 07/10/2026.* A seção 6 estimou as taxas com uma regressão linear sem
intercepto por faixa (o método de Goodman). Ela produziu a "exceção estranha" da faixa de
45% a 55%. Antes de usar essas taxas para decidir onde mobilizar, testamos se a anomalia
resiste. Há quatro problemas no método original:

1. **As faixas foram definidas pelo resultado.** Os municípios foram agrupados pelo voto de
   Lula no 2º turno de 2022, que é justamente o que a regressão tenta explicar. E as taxas
   foram aplicadas a 2026 por uma faixa do 1º turno, ou seja, por outra régua.
2. **A regressão é sobre votos absolutos.** São Paulo, Rio e Belo Horizonte, sozinhos, mexem
   no coeficiente de faixas com centenas de municípios.
3. **O comparecimento líquido mistura fluxos.** Quem deixou de votar e quem passou a votar
   se cancelam no saldo, e a regressão não separa um do outro.
4. **Os erros-padrão (±0,01) eram falsos.** Eles supõem que o modelo está certo. O
   bootstrap abaixo mostra a incerteza real.""")

co("""diag = pd.read_csv("painel/diagnostico_anomalia.csv")
tab = diag[["definicao_faixa", "faixa", "municipios", "b_goodman", "b_boot_p05", "b_boot_p95",
            "b_sem_3_maiores", "3_maiores"]].copy()
tab.columns = ["faixa definida pelo", "faixa", "municípios", "b (Goodman)", "bootstrap p5",
               "bootstrap p95", "b sem os 3 maiores", "3 maiores municípios da faixa"]
display(tab.round(3).set_index(["faixa definida pelo", "faixa"]))""")

md("""**O método escolhido.** O EI de King (1997) resolve tabelas 2x2. Aqui o eleitorado sai
do 1º turno em quatro grupos (Lula, Bolsonaro, terceira via, fora: abstenção, brancos e
nulos) e chega ao 2º em três (Lula, Bolsonaro, fora). A generalização bayesiana do método de
King para esse caso é o modelo RxC hierárquico de Rosen, Jiang, King e Tanner (2001), que
implementamos em PyMC (`inferencia_ecologica.py`):

- cada município tem sua própria tabela de transferência 4x3;
- as tabelas são puxadas para a média da faixa, e as médias das faixas para uma média
  nacional (agregação parcial: uma faixa só se afasta das outras se os dados sustentarem);
- porte e renda do município deslocam as taxas; a força de Lula **não** entra como
  covariável, porque fazer a taxa depender da própria composição torna o modelo não
  identificável com dados agregados;
- a verossimilhança é Dirichlet sobre as proporções do 2º turno, com concentração que
  cresce com o eleitorado num expoente estimado (rho). Com rho perto de 0,25, um município
  100 vezes maior pesa cerca de 3 vezes mais, não 100;
- as faixas passam a ser definidas pelo voto de Lula **no 1º turno**, antes da transferência,
  e são aplicadas a 2026 pela mesma régua.

O resultado é uma distribuição para cada taxa, não um número só.""")

co("""tx = pd.read_csv("painel/taxas_ei_2022.csv")
ordem = ["<35%", "35-45%", "45-55%", "55-65%", ">65%"]
cond = tx[tx["destino"] == "lula_entre_votantes"]
fora = cond[cond["origem"] == "fora"].set_index("faixa").reindex(ordem)
terc = cond[cond["origem"] == "terceira_via"].set_index("faixa").reindex(ordem)

resumo_ei = pd.DataFrame({
    "quem passou a votar → Lula": fora["mediana"],
    "  (90%)": [f"{a:.2f} a {b:.2f}" for a, b in zip(fora["p05"], fora["p95"])],
    "b antigo": pd.Series(TX_B),
    "terceira via → Lula": terc["mediana"],
    "  (90%) ": [f"{a:.2f} a {b:.2f}" for a, b in zip(terc["p05"], terc["p95"])],
})
display(resumo_ei.round(3))

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.8), sharey=True)
x = np.arange(len(ordem))
for ax, df, tit, antigo in ((a1, fora, "Quem passou a votar no 2º turno", TX_B),
                            (a2, terc, "Eleitor da terceira via", TX_A)):
    ax.vlines(x, df["p05"], df["p95"], color=VERMELHO, lw=6, alpha=.35, label="EI bayesiano, 90%")
    ax.plot(x, df["mediana"], "o", color=VERMELHO, ms=6, label="EI bayesiano, mediana")
    ax.plot(x + .18, [antigo[f] for f in ordem], "x", color=CINZA, ms=7, mew=1.6, label="método antigo")
    ax.axhline(.5, color="black", lw=.8, ls="--")
    ax.set_xticks(x); ax.set_xticklabels(ordem)
    ax.set_title(tit, loc="left", fontsize=10, weight="bold")
    ax.set_xlabel("voto de Lula no 1º turno de 2022")
a1.set_ylabel("fração que foi para Lula (entre os dois)")
a1.set_ylim(0, 1)
a1.legend(frameon=False, fontsize=8, loc="upper left")
fig.tight_layout(); plt.show()""")

co("""val = pd.read_csv("painel/validacao_ei.csv")
val.columns = ["faixa", "municípios fora da amostra", "cobertura do intervalo de 90%", "erro mediano da margem (pp)"]
display(val.round(3).set_index("faixa"))""")

md("""**O que a revisão mostra.**

- **A anomalia era do método, não do eleitorado.** Com as faixas definidas pelo 1º turno, a
  fração de quem passou a votar que foi para Lula fica em 0,20, 0,47, 0,40, 0,47 e 0,74, da
  faixa mais fraca para a mais forte. A faixa de 45% a 55% (0,40, com intervalo de 0,28 a
  0,54) se sobrepõe às duas vizinhas e não se distingue delas. O "salto" de 0,62 para 0,33 e
  de volta para 0,65 sumiu.
- **O problema estava nas faixas vizinhas.** O método antigo dava 0,62 e 0,65 nas faixas de
  35% a 45% e de 55% a 65%. O modelo dá 0,47 nas duas, com intervalo que inclui 0,5. **O
  retorno da mobilização estava superestimado em boa parte do mapa.**
- **Só nas pontas os dados decidem.** Onde Lula teve mais de 65% no 1º turno de 2022, três
  em cada quatro eleitores recuperados foram para ele (0,74, de 0,64 a 0,85). Onde teve menos
  de 35%, um em cada cinco (0,20, de 0,12 a 0,31). No meio, o comparecimento extra se dividiu
  quase ao meio.
- **A terceira via confirma a seção 6:** entre os dois candidatos, ela foi para Lula em 35% a
  59% dos casos, conforme a faixa, e nunca passou de 64% nem no limite do intervalo.

**Validação.** Ajustado em 80% dos municípios, o modelo previu a margem dos outros 20% com
erro mediano de 0,9 ponto, e o intervalo de 90% acertou 98,8% dos casos. Os intervalos são,
portanto, conservadores (um pouco largos demais), não otimistas. Diagnósticos do amostrador:
R-hat máximo de 1,016, amostra efetiva mínima de 832, 1 divergência em 4.000 amostras.

**Limites do modelo.** O efeito de porte e renda é limitado a ±2,5 desvios, para não ser
extrapolado nas capitais. Sem o limite, São Paulo (6,2 desvios acima da média em porte)
tinha sua taxa decidida pela extrapolação. O custo disso é que o modelo reconstrói a margem
nacional de 2022 com um viés de cerca de 0,4 milhão a favor de Bolsonaro (1,71 milhão
contra 2,13 milhões reais). Esse viés passa para as projeções nacionais da seção 11.""")

md("""## 11. Cenários: simulação de Monte Carlo

Com as taxas na forma de distribuição, cada número da análise também vira uma distribuição.
`simulacao_montecarlo.py` sorteia 2.000 vezes. Em cada sorteio:

1. **Parâmetros:** uma amostra do posterior dá a tabela de transferência de cada município.
2. **Resíduo municipal (bootstrap):** somamos à margem de cada município um erro que o modelo
   cometeu em 2022, sorteado com reposição entre os municípios da mesma faixa.
3. **Cenário:** no cenário *direita*, uma fração entre 0 e 50% do que a terceira via dava a
   Lula em 2022 vai para Flávio, sorteada a cada rodada. É hipótese, não estimativa: a
   terceira via de 2026 (Cury, Renan Santos, Caiado, Zema) é mais à direita que a de 2022.

O terreno perdido não depende de taxa de transferência; sua única incerteza vem do bootstrap
da queda média nacional. Ele continua sendo um teto.""")

co("""cn = pd.read_csv("painel/cenarios_nacional.csv")
cn_fmt = cn.assign(**{c: (cn[c]/1e6).round(2) for c in ("p05", "mediana", "p95")})
cn_fmt["prob_lula_a_frente"] = (100*cn["prob_lula_a_frente"]).round(0)
cn_fmt.columns = ["cenário", "p5 (mi)", "mediana (mi)", "p95 (mi)", "% dos sorteios com Lula à frente"]
display(cn_fmt.set_index("cenário"))

s18 = d[["lula_2018_1t", "bolso_2018_1t", "lula_2018_2t", "bolso_2018_2t"]].sum()
s22 = d[["lula_2022_1t", "bolso_2022_1t", "lula_2022_2t", "bolso_2022_2t"]].sum()
print("variação da margem do PT entre os turnos (votos):")
print(f"  2018 (terceira via com Ciro, Alckmin, Marina): {mil((s18.iloc[2]-s18.iloc[3])-(s18.iloc[0]-s18.iloc[1])):>12}")
print(f"  2022 (terceira via com Tebet e Ciro):          {mil((s22.iloc[2]-s22.iloc[3])-(s22.iloc[0]-s22.iloc[1])):>12}")""")

co("""cf = pd.read_csv("painel/cenarios_frentes.csv")
pot = cf[(cf["medida"] == "potencial (terreno + 2 pp)") & (cf["frente"] != "TODOS OS FOCOS")].sort_values("mediana")
tot = cf[(cf["medida"] == "potencial (terreno + 2 pp)") & (cf["frente"] == "TODOS OS FOCOS")].iloc[0]

fig, ax = plt.subplots(figsize=(8, 3.8))
y = np.arange(len(pot))
ax.hlines(y, pot["p05"], pot["p95"], color=VERMELHO, lw=7, alpha=.35)
ax.plot(pot["mediana"], y, "o", color=VERMELHO, ms=6)
for yi, (_, l) in zip(y, pot.iterrows()):
    ax.annotate(f"{l['mediana']/1000:.0f} mil ({l['p05']/1000:.0f}–{l['p95']/1000:.0f})",
                xy=(l["p95"], yi), xytext=(6, -3), textcoords="offset points", fontsize=7.5, color="#555")
ax.set_yticks(y); ax.set_yticklabels([f"{f} ({m})" for f, m in zip(pot["frente"], pot["municipios"])])
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, p: f"{v/1000:.0f} mil"))
ax.set_xlabel("votos líquidos de potencial (terreno perdido + 2 pp onde mobilizar rende), intervalo de 90%")
ax.set_xlim(0, pot["p95"].max()*1.3)
ax.set_title(f"Potencial por frente: {tot['mediana']/1000:.0f} mil nos 200 focos "
             f"(90%: {tot['p05']/1000:.0f} a {tot['p95']/1000:.0f} mil)", loc="left", fontsize=10, weight="bold")
fig.tight_layout(); plt.show()

med = ["mobilização +2 pp", "terceira via, base", "terceira via, direita",
       "margem projetada, base", "margem projetada, direita"]
t = cf[cf["medida"].isin(med)].copy()
t["valor"] = [f"{m/1000:+,.0f} mil ({a/1000:+,.0f} a {b/1000:+,.0f})".replace(",", ".")
              for m, a, b in zip(t["mediana"], t["p05"], t["p95"])]
display(t.pivot(index="frente", columns="medida", values="valor")[med])""")

co("""fo = pd.read_csv("painel/focos_ei.csv")
cert_rende = (fo["prob_mob_rende"] >= .9).sum()
cert_preju = (fo["prob_mob_rende"] <= .1).sum()
incerto = len(fo) - cert_rende - cert_preju
print(f"Nos {len(fo)} focos, a chance de +2 pp de comparecimento render votos líquidos a Lula:")
print(f"   ≥ 90% (mobilizar com segurança):     {cert_rende:>4}")
print(f"   ≤ 10% (mobilizar prejudica):         {cert_preju:>4}")
print(f"   entre 10% e 90% (dados não decidem): {incerto:>4}")
print()
print("Antes, com taxas fixas por faixa, cada município caía em 'rende' ou 'prejudica', sem meio-termo.")""")

md("""**O que a simulação mostra.**

1. **O potencial geográfico encolheu e ganhou margem de erro:** 459 mil votos nos 200 focos
   (90%: 407 mil a 514 mil), contra 586 mil na versão anterior. Quase tudo vem do terreno
   perdido. A mobilização, que antes respondia por 172 mil votos, cai para 17 mil (de −8 mil
   a +40 mil): o retorno de levar mais gente às urnas era o número mais frágil da análise.

2. **Mobilizar é seguro em 25 focos, prejudicial em 97 e indefinido em 78.** Os 25 seguros
   são cidades médias do interior do Nordeste onde Lula passa de 65% (Crato, Barbalha,
   Araripina, Ipirá, Barreirinhas). Nos 78 indefinidos, uma campanha de comparecimento é uma
   aposta, não uma tática.

3. **Por frente, a ordem se mantém, mas com faixas:** região metropolitana de São Paulo
   (110 mil, de 89 a 131 mil) e Goiás e entorno (106 mil, de 100 a 112 mil) empatam na
   frente. O Nordeste urbano (89 mil, de 66 a 114 mil) é a frente mais incerta, porque é a
   única onde a mobilização pesa. A região metropolitana de São Paulo é a única frente em que
   o sinal da margem projetada está em jogo (de −330 mil a +133 mil no cenário base).

4. **A dinâmica entre os turnos pesa mais que o mapa inteiro.** Se o movimento de 2022 se
   repetir, a margem do 2º turno vai a cerca de −6,9 milhões (90%: −7,3 a −6,6 milhões;
   descontado o viés de reconstrução, perto de −6,5 milhões). No cenário em que a terceira
   via é mais à direita, a cerca de −8,8 milhões. Para comparação, em 2018 a margem do PT
   melhorou 7,2 milhões entre os turnos. A diferença entre esses dois anos (mais de 11
   milhões de votos) dá a escala do que está fora do modelo: a composição e o comportamento
   da terceira via valem muito mais que os 459 mil votos de potencial geográfico.

**Como ler os intervalos.** Eles medem a incerteza do modelo e o erro municipal de 2022. Não
medem a incerteza política: um apoio, um debate ou a própria campanha podem levar o
resultado para fora deles. A probabilidade de 0% de Lula à frente nos cenários quer dizer
apenas que, **com o comportamento de 2022**, nenhuma das 2.000 simulações vira o placar. Não
é uma previsão, e não deve ser publicada como chance de vitória.""")

md("""## 12. O que isto não diz

Uma análise que só confirma o que a redação gostaria de ouvir não serve para decidir nada.
As limitações aqui são grandes e precisam andar junto com os números:

1. **Falácia ecológica.** Tudo aqui é município, não pessoa. Que municípios mais pobres
   votem mais em Lula não autoriza dizer que eleitores mais pobres votam mais em Lula —
   embora pesquisas individuais apontem na mesma direção, esta análise não prova isso.

2. **As taxas de transferência vêm de 2022 e são otimistas.** Em 2022 a terceira via
   (Tebet, Ciro) apoiou Lula no 2º turno. Em 2026 ela é formada por Cury, Renan Santos,
   Caiado e Zema. Usar as taxas de 2022 **superestima** o que Lula pode herdar. Os
   números de terceira via desta análise devem ser lidos como teto, não como projeção.

3. **A faixa de 45–55% contrariava a lógica do resto** na versão de 05/10. A seção 10 mostra
   que era artefato do método. O que fica é uma incerteza maior: no meio do mapa, os dados
   de 2022 não dizem se mobilizar ajuda ou atrapalha.

4. **Não há pesquisa de intenção de voto aqui.** No dia seguinte ao 1º turno não existe
   pesquisa registrada no TSE para o 2º. Quando houver, elas mandam mais que este modelo
   em qualquer divergência.

5. **O modelo não sabe de política.** Apoios, debates, escândalos e a campanha em si são
   exatamente o que move os 5,98 pontos — e nada disso está nos dados.

6. **Correlação não é causa.** O resíduo da seção 5 aponta municípios onde Lula vai pior
   que o esperado. "Esperado" significa "comparado a municípios parecidos", não "onde ele
   deveria estar". A causa da diferença pode ser qualquer coisa que o modelo não vê.

**Antes de publicar qualquer número daqui**, vale passar por edição e, se virar matéria
sobre estratégia de campanha, pela checagem com fontes da própria campanha. E convém
deixar explícito para o leitor que são estimativas de um modelo, não resultados.""")

md("""## 13. Reprodução

```
analise-2t/
├── preparar_dados.py          fontes oficiais -> painel/painel_municipios.csv
├── gerar_painel_final.py      -> painel/painel_final.csv (seções 2 a 9)
├── inferencia_ecologica.py    modelo RxC bayesiano de 2022 -> modelo/, painel/taxas_ei_2022.csv (seção 10)
├── simulacao_montecarlo.py    cenários e intervalos -> painel/focos_ei.csv, cenarios_*.csv (seção 11)
├── construir_notebook.py      gera este notebook
└── mapa/construir_mapa.py     mapa interativo dos focos
```

As seções 2 a 9 rodam com o Python do sistema (`requirements.txt`). A inferência
ecológica precisa de PyMC e nutpie (`requirements-ei.txt`, Python 3.12):

```
uv venv .venv --python 3.12 && uv pip install --python .venv/bin/python -r requirements-ei.txt
.venv/bin/python inferencia_ecologica.py --sem-validacao & .venv/bin/python inferencia_ecologica.py --so-validacao; wait
.venv/bin/python simulacao_montecarlo.py
```

O ajuste leva cerca de 14 minutos em 16 núcleos. As sementes são fixas; com as mesmas
versões, os resultados se repetem.""")

nb["cells"] = C
nb.metadata = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
               "language_info": {"name": "python"}}
nbf.write(nb, "analise_2turno.ipynb")
print(f"notebook escrito: {len(C)} células")
