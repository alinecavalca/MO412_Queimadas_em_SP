SUBDIRS := data generate visualize
SUBDIRSCLEAN=$(addsuffix clean,$(SUBDIRS))

all: init $(SUBDIRS)

init:
	python -m pip install --quiet -r requirements.txt

$(SUBDIRS):
	$(MAKE) -C $@ $(rule)

clean: $(SUBDIRSCLEAN)

$(SUBDIRSCLEAN):
	$(eval folder = $(shell echo $@ |sed "s/clean//"))
	$(MAKE) -C $(folder) clean

.PHONY: all $(SUBDIRS)