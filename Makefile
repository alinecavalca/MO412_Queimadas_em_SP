SUBDIRS := src
SUBDIRSCLEAN=$(addsuffix clean,$(SUBDIRS))

all: $(SUBDIRS)
$(SUBDIRS):
	$(MAKE) -C $@ $(rule)

clean: $(SUBDIRSCLEAN)

$(SUBDIRSCLEAN):
	$(eval folder = $(shell echo $@ |sed "s/clean//"))
	$(MAKE) -C $(folder) clean

.PHONY: all $(SUBDIRS)