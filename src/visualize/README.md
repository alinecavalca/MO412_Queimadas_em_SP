# Módulo de Análise e Visualização de Grafos

Este diretório contém os scripts para analisar o grafo de focos de queimada e gerar visualizações. Cada script foca em um tipo diferente de análise, fornecendo insights sobre a estrutura da rede, sua robustez e a dinâmica de propagação de incêndios.

## Scripts de Análise

Abaixo está a descrição de cada script e o que ele produz. Para executar todos de uma vez, utilize o comando `make` neste diretório.

- **`plot_graph.py`**:
  - **O que faz:** Gera uma visualização geográfica básica do grafo, plotando os focos de queimada (nós) em suas coordenadas de latitude e longitude.
  - **Resultado:** Um mapa da rede salvo em `data/`.

- **`degree_analysis.py`**:
  - **O que faz:** Realiza uma análise estrutural completa da rede, calculando e plotando métricas como distribuição de grau, coeficiente de agrupamento e centralidade de intermediação. Também executa uma análise de robustez, simulando a remoção de nós e medindo o impacto na conectividade da rede.
  - **Resultados:** Gráficos de distribuição, um gráfico de análise de robustez e logs com as principais métricas.

- **`community_analysis.py`**:
  - **O que faz:** Aplica o algoritmo de Louvain para detectar "comunidades" ou "clusters" de focos de incêndio densamente conectados.
  - **Resultado:** Um mapa da rede onde cada comunidade é colorida de forma distinta, ajudando a identificar "zonas de risco".

- **`propagation_analysis.py`**:
  - **O que faz:** Utiliza o modelo epidemiológico **SIR (Suscetível-Infectado-Recuperado)** para simular a propagação de um incêndio. Realiza uma análise de sensibilidade para diferentes taxas de propagação (`tau`).
  - **Resultado:** Gráficos que mostram a evolução do número de nós suscetíveis, queimando e queimados ao longo do tempo para diferentes cenários.

## Como Executar

Certifique-se de que o arquivo `graph_50.gpickle` existe no diretório `data/`.

Para rodar todos os scripts de análise em sequência:
```bash
make
```

Para limpar todos os arquivos geradoss:
```bash
make clean
```

