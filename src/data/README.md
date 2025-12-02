# Módulo de Processamento de Dados

Este diretório contém os scripts responsáveis pela coleta e limpeza dos dados de focos de queimada.

## Funcionalidade

O principal objetivo deste módulo é transformar os dados brutos, geralmente obtidos de fontes como o INPE (Instituto Nacional de Pesquisas Espaciais), em um formato estruturado e limpo, pronto para a modelagem em grafo.

As principais etapas realizadas pelos scripts aqui são:
- Download dos dados de focos de queimada para o período de interesse.
- Filtragem dos dados para o estado de São Paulo.
- Limpeza de dados ausentes ou inconsistentes.
- Salvamento dos dados processados em um formato intermediário (ex: `.csv` ou `.parquet`) no diretório `data/`.