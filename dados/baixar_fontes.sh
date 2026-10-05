#!/bin/bash
# Fontes oficiais para a análise do 2º turno.
B="https://cdn.tse.jus.br/estatistica/sead/odsele"
set -u
baixa() {
  local url="$1" nome="$2"
  if [ -s "$nome" ]; then echo "já tenho $nome"; return; fi
  echo "baixando $nome ..."
  curl -sS --max-time 1800 --retry 3 --retry-delay 5 -o "$nome.parcial" "$url" \
    && mv "$nome.parcial" "$nome" && echo "ok $nome ($(du -h "$nome" | cut -f1))"
}
baixa "$B/detalhe_votacao_munzona/detalhe_votacao_munzona_2022.zip" detalhe_votacao_munzona_2022.zip
baixa "$B/votacao_candidato_munzona/votacao_candidato_munzona_2022.zip" votacao_candidato_munzona_2022.zip
baixa "$B/votacao_candidato_munzona/votacao_candidato_munzona_2018.zip" votacao_candidato_munzona_2018.zip
baixa "$B/perfil_eleitorado/perfil_eleitorado_2026.zip" perfil_eleitorado_2026.zip
echo "FIM DOS DOWNLOADS"
