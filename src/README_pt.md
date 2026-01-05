# Análise de Focos de Queimada em SP com Teoria de Grafos

Este diretório contém o código-fonte para o projeto de análise da rede de focos de queimada no estado de São Paulo. O objetivo é utilizar a teoria de grafos para modelar a relação entre os focos de incêndio, identificar pontos críticos e simular a propagação do fogo.

## Estrutura dos Diretórios

O código está organizado nos seguintes subdiretórios, que representam as etapas do pipeline de análise:

- **/data_processing**: Scripts para baixar, limpar e formatar os dados brutos de focos de queimada.
- **/generate**: Scripts para construir o grafo a partir dos dados processados, salvando o objeto do grafo em formato `.gpickle`.
- **/visualize**: Scripts para realizar as análises sobre o grafo gerado, produzindo visualizações (gráficos, mapas, animações) e relatórios.

## Execução com Makefile (Modo Automatizado)

Este projeto inclui um Makefile principal em src/ que automatiza toda a pipeline: instalação de dependências, processamento de dados, geração do grafo e análises.
O Makefile também chama automaticamente os Makefiles dos subdiretórios.

### 🔧 make all

Para executar todo o pipeline com um único comando:

```bash
make all
```

O que esse comando faz:

1. Instala dependências via pip install -r requirements.txt.

2. Cria o diretório data/ onde ficarão logs, resultados e arquivos intermediários.

3. Copia o arquivo config.ini para data/ para registrar com qual configuração a execução foi realizada.

4. Entra automaticamente nos diretórios data_processing, generate e visualize, executando o make correspondente de cada um.

5. Durante a execução:

    * a variável de ambiente CONFIG é exportada para cada subdiretório;

    * toda saída (stdout e stderr) é registrada em data/log.txt, além de aparecer na tela.

Em outras palavras, o comando caminha pelos subdiretórios e executa seu conteúdo automaticamente, mantendo um log completo da execução.

### 🧹 make clean

Para limpar todos os artefatos gerados:

```bash
make clean
```

Esse comando:

* chama make clean dentro de cada subdiretório (data_processing, generate, visualize);

* remove completamente o diretório data/, apagando resultados, logs e arquivos temporários.


## Execução Manual (Sem Makefile)

Caso o usuário prefira executar cada etapa manualmente, basta seguir a ordem lógica do pipeline:

### Pré-requisitos

Antes de executar os scripts, certifique-se de que você tem o Python 3 instalado e as seguintes bibliotecas:

```bash
pip install -r requirements.txt
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

Todos os resultados serão salvos no diretório `data/`.