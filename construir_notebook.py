#!/usr/bin/env python3
"""Monta o notebook da análise do 2º turno."""
import nbformat as nbf

nb = nbf.v4.new_notebook()
C = []
md = lambda t: C.append(nbf.v4.new_markdown_cell(t))
co = lambda t: C.append(nbf.v4.new_code_cell(t))

md("""# Onde Lula ainda tem voto a buscar no 2º turno de 2026

**Brasil de Fato — núcleo de dados** · análise de 05/10/2026

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

**O ponto de partida é ruim e a geografia sozinha não resolve.**

Lula terminou o 1º turno com 45,16% contra 47,03% de Flávio Bolsonaro — **2,24 milhões de
votos atrás**. Três achados definem o que fazer:

1. **A geografia quase não mudou de 2022 para 2026.** A correlação entre o voto em Lula
   por município nos dois anos é de 0,987, e uma regressão simples explica 97,5% da
   variação. Lula não perdeu lugares específicos: perdeu **5,98 pontos percentuais em
   todo lugar, quase na mesma medida**. Isso significa que não existe um punhado de
   municípios "perdidos" para reconquistar — existe uma perda difusa.

2. **A terceira via joga contra.** Em 2022, mesmo com Tebet e Ciro declarando apoio,
   Lula capturou só **30,2%** dos votos em disputa entre os turnos; Bolsonaro levou
   69,8%. Em 2026 a terceira via (Cury, Renan Santos, Caiado, Zema) é mais à direita que
   a de 2022. Contar com ela é contar com prejuízo: aplicando as taxas de 2022 faixa a
   faixa, os 9,3 milhões de votos de terceira via rendem a Lula um **saldo líquido
   negativo de 3,4 milhões** — mais que a própria diferença a cobrir.

3. **O comparecimento é o único reservatório favorável — e só em parte do mapa.** Quem
   voltou às urnas no 2º turno de 2022 votou em Lula em 62% dos casos **onde ele já tinha
   entre 35% e 45%**, e em 61% onde tinha mais de 65%. Mas onde ele tinha menos de 35%,
   só 30% dos novos eleitores foram para ele — **mobilizar ali entrega 70% dos votos ao
   adversário.**

**As frentes, em ordem de prioridade.** Saem do próprio ranking: são os 200 municípios de
maior potencial, agrupados. Juntas, as quatro primeiras somam **426 mil votos em 129
municípios**.

| # | Frente | Municípios | Potencial | Por eleitor | Tática |
|---|---|---|---|---|---|
| 1 | **Região metropolitana de São Paulo** | 19 | 131 mil | baixa (9/mil) | **Reduzir a derrota**, não vencer. É a maior massa de terreno perdido do país: 113 mil dos 131 mil vêm de recuperar voto, não de mobilizar. |
| 2 | **Goiás e entorno** | 33 | 110 mil | **a mais alta (20/mil)** | Maior queda do país (−10,3 pp). Mas Lula está em 33%: **contenção de danos e persuasão, nunca campanha de comparecimento** — ali mobilizar entrega 70% dos novos votos ao adversário. |
| 3 | **Nordeste urbano** | 43 | 107 mil | 12/mil | A única frente onde **mobilizar é o caminho principal**: 44 mil dos 107 mil vêm de comparecimento. Salvador, Recife, Fortaleza, Teresina, São Luís, Feira de Santana. |
| 4 | **Minas Gerais** | 34 | 78 mil | 12/mil | Estado decisivo: a diferença é de só 591 mil. **Mas o potencial mineiro é difuso** — no Estado inteiro são 222 mil votos espalhados por 494 municípios. Exige campanha de capilaridade, não de concentração. |
| 5 | Sul (RS, SC, PR) | 34 | 64 mil | 17/mil | Eficiência alta, terreno muito perdido (RS caiu 7,8 pp). Persuasão. |

Os números de cada frente estão calculados na seção 9 — não são estimativas de texto.

**Onde não ir — e por que focar importa.** O potencial de votos é quase proporcional ao
eleitorado: concentrar esforço em 200 municípios entrega 38% do potencial cobrindo 34% dos
eleitores. **Focar não multiplica o ganho.** O que focar evita é o prejuízo, e esse sim é
muito desigual: 2.389 municípios — 43% do país, 76,6 milhões de eleitores — têm saldo
**negativo** de mobilização. Uma campanha de comparecimento de +1 ponto neles custaria a
Lula 287 mil votos líquidos. São os 1.745 municípios abaixo de 35% e, por razão diferente
e menos confiável, a faixa de 45% a 55%. **A regra de foco não é "vá aos maiores": é "não
leve às urnas quem vai votar no adversário".**

**A conta honesta:** recuperar todo o terreno perdido acima da média (1,12 milhão) e somar
mobilização agressiva nos lugares certos (401 mil) dá **1,53 milhão — 68% da diferença de
2,24 milhões**, e isso ignorando o prejuízo da terceira via. O 2º turno não se ganha no
mapa: se ganha recuperando parte dos 5,98 pontos perdidos em todo o país. **O mapa diz
onde a margem é mais barata, não onde está a vitória.**""")

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

3. **A faixa de 45–55% é a exceção estranha**: ali quem voltou votou 67% no adversário.
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

md("""## 10. O que isto não diz

Uma análise que só confirma o que a redação gostaria de ouvir não serve para decidir nada.
As limitações aqui são grandes e precisam andar junto com os números:

1. **Falácia ecológica.** Tudo aqui é município, não pessoa. Que municípios mais pobres
   votem mais em Lula não autoriza dizer que eleitores mais pobres votam mais em Lula —
   embora pesquisas individuais apontem na mesma direção, esta análise não prova isso.

2. **As taxas de transferência vêm de 2022 e são otimistas.** Em 2022 a terceira via
   (Tebet, Ciro) apoiou Lula no 2º turno. Em 2026 ela é formada por Cury, Renan Santos,
   Caiado e Zema. Usar as taxas de 2022 **superestima** o que Lula pode herdar. Os
   números de terceira via desta análise devem ser lidos como teto, não como projeção.

3. **A faixa de 45–55% contraria a lógica do resto** (quem voltou às urnas votou 67% no
   adversário). Pode ser real, pode ser composição de amostra. Antes de virar decisão de
   campanha, precisa de checagem específica.

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

md("""## 11. Reprodução

```
analise-2t/
├── preparar_dados.py          monta painel/painel_municipios.csv das fontes oficiais
├── analise_2turno.ipynb       este notebook
├── painel/painel_final.csv    base analítica, uma linha por município
└── dados/                     zips do TSE e cache do IBGE
```

Para refazer do zero: `python3 preparar_dados.py` e depois executar o notebook. O painel
tem 5.571 linhas e é o único insumo — o notebook não toca em arquivo cru.""")

nb["cells"] = C
nb.metadata = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
               "language_info": {"name": "python"}}
nbf.write(nb, "analise_2turno.ipynb")
print(f"notebook escrito: {len(C)} células")
