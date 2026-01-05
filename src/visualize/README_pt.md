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
  (É um experimento inicial, idealmente deve ser feito uma melhoria, e utilizar dados de data do dataset e outras informações para obter um resultado mais realista, e também seria interessante cruzar com outras informações para ver os reais impactos.)

- **`find_critical_nodes.py`**:
  - **O que faz:** Executa a análise mais crítica do ponto de vista prático. Simula um incêndio começando em *cada nó* da rede e mede o tamanho final do estrago.
  - **Resultado:** Identifica e destaca em um mapa os **5 pontos de ignição mais perigosos** — aqueles que, se um incêndio começar ali, têm o maior potencial de causar um desastre em larga escala.

- **`animate_propagation.py`**:
  - **O que faz:** Gera animações (GIFs) que mostram a propagação do fogo no mapa geográfico para diferentes cenários de `tau`.
  - **Resultado:** Arquivos `.gif` que visualizam a dinâmica do incêndio.
  (É um experimento inicial, idealmente deve ser feito uma melhoria, e utilizar dados de data do dataset e outras informações para obter um resultado mais realista, e também seria interessante cruzar com outras informações para ver os reais impactos.)

- **`animate_community_propagation.py`**:
  - **O que faz:** Combina a detecção de comunidades com a simulação de propagação para criar uma animação avançada.
  - **Resultado:** Uma animação `.gif` que mostra o fogo se espalhando dentro e entre as diferentes zonas de risco (comunidades).
  (É um experimento inicial, idealmente deve ser feito uma melhoria, e utilizar dados de data do dataset e outras informações para obter um resultado mais realista, e também seria interessante cruzar com outras informações para ver os reais impactos.)

## Como Executar

Certifique-se de que o arquivo `graph_50.gpickle` existe no diretório `data/`.

Para rodar todos os scripts de análise em sequência:
```bash
make
```

Para limpar todos os arquivos gerados:
```bash
make clean
```

