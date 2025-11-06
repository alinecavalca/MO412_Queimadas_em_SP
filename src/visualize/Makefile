all: plot

plot: ../../data/10_km_de_distncia.png

../../data/10_km_de_distncia.png:
	python plot_graph.py

clean:
	rm -f ../../data/*.png

.PHONY: all plot