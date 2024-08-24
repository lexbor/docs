SPHINX		?= sphinx-build
SERVER		?= python3 -mhttp.server
VENVDIR		?= .venv
VENV		?= $(VENVDIR)/bin/activate

URL			?= https://lexbor.com

BUILDDIR	?= build
DEPLOYDIR	?= deploy


.PHONY: install html run check clean deploy

$(VENVDIR):
	python3 -m venv $(VENVDIR)

install: $(VENVDIR)
	. $(VENV); pip install \
	    --require-virtualenv \
	    --upgrade -r requirements.txt \
        --log .venv/pip_install.log

html: $(VENVDIR) $(BUILDDIR)
	. $(VENV); $(SPHINX) -E -b dirhtml source "$(BUILDDIR)"

$(BUILDDIR):
	mkdir "$(BUILDDIR)"

run: SPHINX=sphinx-autobuild
run: html

check: $(VENVDIR)
	. $(VENV); $(SPHINX) -b linkcheck -d "$(BUILDDIR)/.doctrees" source .

clean-doc:
	rm -rf $(BUILDDIR) $(DEPLOYDIR)

clean: clean-doc
	rm -rf $(VENVDIR)

deploy: html
	$(eval TMP := $(shell mktemp -d))
	rsync -rv $(EXCLUDE) "$(BUILDDIR)/" "$(TMP)"
	rsync -rcv --delete --exclude='*.gz' --exclude='tmp.*' \
		  "$(TMP)/" "$(DEPLOYDIR)"
	-rm -rf "$(TMP)"
	chmod -R g=u "$(DEPLOYDIR)"
