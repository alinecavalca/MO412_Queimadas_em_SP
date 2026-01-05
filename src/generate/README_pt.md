# Módulo de Geração de Grafo

Este diretório contém os scripts para construir a rede (grafo) a partir dos dados de queimadas processados.

## Funcionalidade

O script principal (`generate_graph.py`) lê os dados limpos e realiza as seguintes ações:

1.  Cria um nó para cada foco de queimada, armazenando seus atributos (Latitude, Longitude, FRP, etc.).
2.  Adiciona arestas entre os nós com base em um critério de proximidade geográfica (ex: todos os focos a menos de 50 km de distância). O peso da aresta pode representar a distância inversa.
3.  Salva o objeto do grafo `networkx` final em um arquivo `.gpickle` no diretório `data/`. Este arquivo é o principal insumo para todos os scripts de análise e visualização.

A distância para a criação de arestas é configurável através do arquivo `config.ini`.