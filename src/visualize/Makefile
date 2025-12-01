all: plot

plot: ../../data/10_km_de_distncia.png

../../data/10_km_de_distncia.png:
	python propagation_analysis.py
	python community_analysis.py
	python plot_graph.py
	python degree_analysis.py

clean:
	rm -f ../../data/*.png

.PHONY: all plot