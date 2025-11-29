SUBDIRS := data generate visualize
SUBDIRSCLEAN=$(addsuffix clean,$(SUBDIRS))

all: init $(SUBDIRS)

init:
	python -m pip install --quiet -r requirements.txt
	mkdir -p ../data

$(SUBDIRS):
	export CONFIG="../config.ini"; $(MAKE) -C $@ $(rule)

clean: $(SUBDIRSCLEAN)
	rm -rf ../data

$(SUBDIRSCLEAN):
	$(eval folder = $(shell echo $@ |sed "s/clean//"))
	$(MAKE) -C $(folder) clean

.PHONY: all $(SUBDIRS)