# Análise de Focos de Queimada em SP com Teoria de Grafos

Este diretório contém o código-fonte para o projeto de análise da rede de focos de queimada no estado de São Paulo. O objetivo é utilizar a teoria de grafos para modelar a relação entre os focos de incêndio, identificar pontos críticos e simular a propagação do fogo.

## Estrutura dos Diretórios

O código está organizado nos seguintes subdiretórios, que representam as etapas do pipeline de análise:

- **/data_processing**: Scripts para baixar, limpar e formatar os dados brutos de focos de queimada.
- **/generate**: Scripts para construir o grafo a partir dos dados processados, salvando o objeto do grafo em formato `.gpickle`.
- **/visualize**: Scripts para realizar as análises sobre o grafo gerado, produzindo visualizações (gráficos, mapas, animações) e relatórios.

## Pré-requisitos

Antes de executar os scripts, certifique-se de que você tem o Python 3 instalado e as seguintes bibliotecas:

```bash
pip install networkx matplotlib numpy pandas EoN tqdm pillow
```

## Configuração

O projeto utiliza um arquivo de configuração para gerenciar parâmetros como caminhos de arquivos, níveis de log e parâmetros de análise. Antes de executar, você deve exportar a variável de ambiente `CONFIG` apontando para o seu arquivo de configuração.

```bash
# Exemplo de como configurar no terminal
export CONFIG=/caminho/completo/para/o/seu/config.ini
```

## Como Executar o Pipeline

A execução deve seguir a ordem lógica do processamento de dados.

1.  **Processar os Dados:**
    Navegue até `src/data_processing` e execute o script principal para obter os dados limpos.
    ```bash
    cd src/data_processing
    python process_data.py # (ou o nome do seu script principal aqui)
    ```

2.  **Gerar o Grafo:**
    Com os dados limpos, gere o arquivo `.gpickle` que representa a rede.
    ```bash
    cd ../generate
    python generate_graph.py # (ou o nome do seu script principal aqui)
    ```

3.  **Realizar Análises e Visualizações:**
    Com o grafo pronto, execute as análises. O `Makefile` no diretório `visualize` automatiza a execução de todos os scripts de análise.
    ```bash
    cd ../visualize
    make
    ```

Todos os resultados (imagens, GIFs) serão salvos no diretório `data/`.