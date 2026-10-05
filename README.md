# Análise — Segundo Turno 2026

Análise por município do 2º turno da eleição presidencial de 2026. Usa o 1º turno de 2026 e os resultados de 2018 e 2022 (TSE), cruzados com indicadores sociais do IBGE (Censo 2022 e PIB municipal de 2021).

## Conteúdo

| Caminho | O que é |
|---|---|
| `analise_2turno.ipynb` | Notebook da análise (executado) |
| `analise_2turno.html` | Versão em HTML do notebook, para leitura |
| `construir_notebook.py` | Gera o notebook |
| `preparar_dados.py` | Monta o painel municipal a partir dos dados brutos |
| `painel/` | Painéis municipais já processados (CSV) |
| `dados/ibge/` | Tabelas do IBGE/SIDRA (JSON) |
| `dados/detalhe_votacao_munzona_2022.zip` | Detalhe de votação de 2022 (TSE) |
| `dados/baixar_fontes.sh` | Baixa os arquivos brutos do TSE |

## Dados brutos fora do repositório

Três arquivos do TSE passam de 100 MB, o limite do GitHub, e por isso não estão no repositório:

- `votacao_candidato_munzona_2022.zip` (~612 MB)
- `votacao_candidato_munzona_2018.zip` (~377 MB)
- `perfil_eleitorado_2026.zip` (~390 MB)

Para reproduzir:

```bash
cd dados && ./baixar_fontes.sh
cd .. && python3 preparar_dados.py
```

`preparar_dados.py` também espera os CSVs do 1º turno de 2026 em `../dados-tse-2026-1T/csv`. São de coleta própria e não estão neste repositório.

## Fontes

- TSE, Dados Abertos: https://dadosabertos.tse.jus.br (arquivos em https://cdn.tse.jus.br/estatistica/sead/odsele)
- IBGE, SIDRA: https://sidra.ibge.gov.br

Todos os dados são públicos e agregados por município. Não há dados pessoais.
