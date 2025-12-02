all: plot

plot: ../../data/10_km_de_distncia.png

../../data/10_km_de_distncia.png:
	python animate_propagation.py
	python animate_community_propagation.py
	python find_critical_nodes.py
	python propagation_analysis.py
	python community_analysis.py
	python plot_graph.py
	python degree_analysis.py

clean:
	rm -f ../../data/*.png

.PHONY: all plot