SUBDIRS := data generate visualize
SUBDIRSCLEAN=$(addsuffix clean,$(SUBDIRS))

all: init $(SUBDIRS)

init:
	python -m pip install --quiet -r requirements.txt
	mkdir -p ../data
	# save run config file for future checks and log analysis
	cp config.ini ../data/

$(SUBDIRS):
	# export the config folder to inner makes; run sub dir make files using same command (all or clean); 2>&1 redirect stderr to stdout; tee -a copy stdout to screen and append to file
	export CONFIG="../config.ini"; $(MAKE) -C $@ $(rule) 2>&1  | tee -a ../data/log.txt

clean: $(SUBDIRSCLEAN)
	rm -rf ../data

$(SUBDIRSCLEAN):
	$(eval folder = $(shell echo $@ |sed "s/clean//"))
	$(MAKE) -C $(folder) clean

.PHONY: all $(SUBDIRS)