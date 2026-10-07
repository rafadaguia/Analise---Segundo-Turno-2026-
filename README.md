# Análise — Segundo Turno 2026

Análise por município do 2º turno da eleição presidencial de 2026. Usa o 1º turno de 2026 e os resultados de 2018 e 2022 (TSE), cruzados com indicadores sociais do IBGE (Censo 2022 e PIB municipal de 2021).

## Conteúdo

| Caminho | O que é |
|---|---|
| `analise_2turno.ipynb` | Notebook da análise (executado) |
| `analise_2turno.html` | Versão em HTML do notebook, para leitura |
| `preparar_dados.py` | Etapa 1: monta `painel/painel_municipios.csv` a partir dos dados brutos |
| `gerar_painel_final.py` | Etapa 2: gera os painéis derivados, entre eles `painel/painel_final.csv` |
| `inferencia_ecologica.py` | Etapa 3: inferência ecológica bayesiana (RxC hierárquico, PyMC) das transferências entre os turnos de 2022 |
| `simulacao_montecarlo.py` | Etapa 4: Monte Carlo com bootstrap dos cenários de 2026; intervalos por frente e por município |
| `frentes.py` | Definição das frentes geográficas, usada pela simulação e pelo mapa |
| `construir_notebook.py` | Etapa 5: gera o notebook |
| `modelo/` | Posterior do modelo de inferência ecológica (NetCDF) |
| `painel/` | Painéis municipais já processados (CSV) |
| `dados/tse2026/` | 1º turno de 2026, presidente por município (TSE): votos por candidato e totais |
| `dados/ibge/` | Tabelas do IBGE/SIDRA (JSON) |
| `dados/detalhe_votacao_munzona_2022.zip` | Comparecimento, brancos e nulos de 2022 (TSE) |
| `dados/baixar_fontes.sh` | Baixa os arquivos brutos do TSE que não cabem no repositório |
| `requirements.txt` | Versões das bibliotecas usadas (etapas 1, 2 e 5) |
| `requirements-ei.txt` | Ambiente das etapas 3 e 4 (Python 3.12, PyMC, nutpie) |
| `mapa/` | Mapa interativo dos 200 municípios prioritários: `construir_mapa.py` gera a página a partir de `modelo.html` |
| `docs/` | Site do GitHub Pages: índice em https://rafadaguia.github.io/Analise---Segundo-Turno-2026-/, mapa completo em `/mapa/` e mapa para matérias em `/embed/` |
| `dados/geo/` | Contornos estaduais (IBGE) e coordenadas das sedes municipais ([kelvins/municipios-brasileiros](https://github.com/kelvins/municipios-brasileiros)) |

## Como reproduzir

```bash
pip install -r requirements.txt

cd dados && ./baixar_fontes.sh && cd ..   # ~1,4 GB do TSE (ver abaixo)
python3 preparar_dados.py                 # -> painel/painel_municipios.csv
python3 gerar_painel_final.py             # -> painel/painel_modelado, comparecimento_2022,
                                          #    painel_completo, taxas_transferencia_2022, painel_final

# inferência ecológica e cenários (Python 3.12, ver requirements-ei.txt)
uv venv .venv --python 3.12 && uv pip install --python .venv/bin/python -r requirements-ei.txt
.venv/bin/python inferencia_ecologica.py --sem-validacao & .venv/bin/python inferencia_ecologica.py --so-validacao; wait
.venv/bin/python simulacao_montecarlo.py   # -> painel/focos_ei.csv, cenarios_frentes.csv, cenarios_nacional.csv

python3 construir_notebook.py
jupyter nbconvert --to notebook --execute --inplace analise_2turno.ipynb
.venv/bin/python mapa/construir_mapa.py
```

O ajuste bayesiano leva cerca de 14 minutos em 16 núcleos. As sementes são fixas.

Para checar os painéis publicados sem sobrescrevê-los, gere os derivados em outra pasta e compare:

```bash
python3 gerar_painel_final.py --saida /tmp/conferencia
```

Com as versões do `requirements.txt`, as duas etapas reproduzem exatamente os CSVs de `painel/`. Isso foi verificado em 05/10/2026: `painel_municipios.csv` saiu idêntico byte a byte, e os cinco painéis derivados bateram valor a valor.

Para conferir só as conclusões, basta o notebook. Ele lê apenas `painel/painel_final.csv`, que está no repositório.

### Dados brutos fora do repositório

Três arquivos do TSE passam de 100 MB, o limite do GitHub. O `dados/baixar_fontes.sh` baixa todos da fonte oficial:

- `votacao_candidato_munzona_2022.zip` (~612 MB)
- `votacao_candidato_munzona_2018.zip` (~377 MB)
- `perfil_eleitorado_2026.zip` (~390 MB)

### Dados de 2026

O TSE ainda não publicou os arquivos de dados abertos do 1º turno de 2026. Os CSVs em `dados/tse2026/` são um recorte (presidente, nível municipal) da coleta própria feita em 05/10/2026 em `resultados.tse.jus.br/oficial/ele2026`. Quando o TSE publicar os arquivos oficiais, vale conferir os totais contra eles.

## Notas metodológicas

- **Municípios:** a base de 2026 tem 5.571 municípios e a análise usa 5.570. Fica de fora **Boa Esperança do Norte (MT)**, município novo, sem votação própria em 2022 nem dados no Censo 2022. Sem a base histórica, ele não entra no modelo. São 4.326 eleitores aptos em 2026.
- **Frações de transferência (versão 1.0):** as frações a e b das seções 6 a 9 do notebook são as estimativas de `taxas_transferencia_2022.csv` arredondadas a três casas. O `gerar_painel_final.py` confere essa correspondência.
- **Revisão de 07/10/2026:** as taxas foram reestimadas com inferência ecológica bayesiana (modelo RxC hierárquico de Rosen, Jiang, King e Tanner, 2001, em PyMC). As faixas passaram a ser definidas pelo voto de Lula no 1º turno, e os números de potencial ganharam intervalos de 90% por simulação de Monte Carlo com bootstrap. A revisão desfaz a anomalia da faixa de 45% a 55% e reduz muito o papel da mobilização. Ver as seções 10 e 11 do notebook. O mapa usa a versão revisada.
- **Pesquisas:** não foram usadas pesquisas de intenção de voto.

## Fontes

- TSE, Dados Abertos: https://dadosabertos.tse.jus.br (arquivos em https://cdn.tse.jus.br/estatistica/sead/odsele)
- TSE, Resultados 2026: https://resultados.tse.jus.br
- IBGE, SIDRA: https://sidra.ibge.gov.br

Todos os dados são públicos. Os painéis são agregados por município. Os arquivos de `dados/tse2026/` trazem os dados públicos de registro dos candidatos, como o TSE os publica.

## Mapa para matérias (iframe)

O mapa compacto fica em https://rafadaguia.github.io/Analise---Segundo-Turno-2026-/embed/ . Para incorporar numa notícia, cole no bloco de HTML:

```html
<figure style="margin:0">
  <iframe id="focos2t" src="https://rafadaguia.github.io/Analise---Segundo-Turno-2026-/embed/"
    title="Onde Lula tem mais votos a recuperar no 2º turno" loading="lazy" scrolling="no"
    style="width:100%;border:0;height:1100px;display:block"></iframe>
</figure>
<script>
  window.addEventListener("message", function (e) {
    if (e.origin !== "https://rafadaguia.github.io" || !e.data || e.data.tipo !== "focos2t-altura") return;
    document.getElementById("focos2t").style.height = e.data.altura + "px";
  });
</script>
```

O script ajusta a altura do iframe ao conteúdo. Sem ele, o mapa funciona com altura fixa de 1.100 pixels. A página inicial do site tem o mesmo código com um botão de copiar.
