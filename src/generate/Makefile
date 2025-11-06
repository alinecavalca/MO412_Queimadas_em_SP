all: gen expand

gen: ../../data/graph_1_10.gpickle

../../data/graph_1_10.gpickle:
	python gen_graph.py

expand: ../../data/graph_50.gpickle

../../data/graph_50.gpickle:
	python increase_radius.py

clean:
	rm -f ../../data/*.gpickle

.PHONY: all gen expand