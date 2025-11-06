all: download

download: ../../data/queimadas.csv

../../data/queimadas.csv:
	python download_data.py

clean:
	rm -f ../../data/*.csv

.PHONY: all download