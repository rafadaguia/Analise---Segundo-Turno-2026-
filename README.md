# Análise — Segundo Turno 2026

Análise por município do 2º turno da eleição presidencial de 2026. Usa o 1º turno de 2026 e os resultados de 2018 e 2022 (TSE), cruzados com indicadores sociais do IBGE (Censo 2022 e PIB municipal de 2021).

## Conteúdo

| Caminho | O que é |
|---|---|
| `analise_2turno.ipynb` | Notebook da análise (executado) |
| `analise_2turno.html` | Versão em HTML do notebook, para leitura |
| `preparar_dados.py` | Etapa 1: monta `painel/painel_municipios.csv` a partir dos dados brutos |
| `gerar_painel_final.py` | Etapa 2: gera os painéis derivados, entre eles `painel/painel_final.csv` |
| `construir_notebook.py` | Etapa 3: gera o notebook |
| `painel/` | Painéis municipais já processados (CSV) |
| `dados/tse2026/` | 1º turno de 2026, presidente por município (TSE): votos por candidato e totais |
| `dados/ibge/` | Tabelas do IBGE/SIDRA (JSON) |
| `dados/detalhe_votacao_munzona_2022.zip` | Comparecimento, brancos e nulos de 2022 (TSE) |
| `dados/baixar_fontes.sh` | Baixa os arquivos brutos do TSE que não cabem no repositório |
| `requirements.txt` | Versões das bibliotecas usadas |

## Como reproduzir

```bash
pip install -r requirements.txt

cd dados && ./baixar_fontes.sh && cd ..   # ~1,4 GB do TSE (ver abaixo)
python3 preparar_dados.py                 # -> painel/painel_municipios.csv
python3 gerar_painel_final.py             # -> painel/painel_modelado, comparecimento_2022,
                                          #    painel_completo, taxas_transferencia_2022, painel_final
python3 construir_notebook.py
jupyter nbconvert --to notebook --execute --inplace analise_2turno.ipynb
```

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
- **Frações de transferência:** as frações a e b usadas no índice de prioridade (seção 7 do notebook) são as estimativas de `taxas_transferencia_2022.csv` arredondadas a três casas. O `gerar_painel_final.py` confere essa correspondência.
- **Pesquisas:** não foram usadas pesquisas de intenção de voto.

## Fontes

- TSE, Dados Abertos: https://dadosabertos.tse.jus.br (arquivos em https://cdn.tse.jus.br/estatistica/sead/odsele)
- TSE, Resultados 2026: https://resultados.tse.jus.br
- IBGE, SIDRA: https://sidra.ibge.gov.br

Todos os dados são públicos. Os painéis são agregados por município. Os arquivos de `dados/tse2026/` trazem os dados públicos de registro dos candidatos, como o TSE os publica.
