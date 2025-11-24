SPHINX      ?= sphinx-build
SERVER      ?= python3 -m http.server
VENVDIR     ?= .venv
VENV        ?= $(VENVDIR)/bin/activate

HOST        ?= lexbor.com

SOURCEDIR   ?= source
BUILDDIR    ?= build
DEPLOYDIR   ?= deploy
REMOTEDIR   ?= /data/lexbor.com/docs/www/

TODAY       = $(shell date '+%F')
TMPDIR      = /tmp/$(TODAY)
BACKUP      = backup/$(TODAY).tar.gz

# Helper to activate the virtual environment and run a command
define venv_exec
    . $(VENV); $(1)
endef

# Ensure virtual environment exists
$(VENVDIR):
	python3 -m venv $(VENVDIR)

# Install dependencies inside virtual environment
.PHONY: install
install: $(VENVDIR)
	$(call venv_exec, pip install --require-virtualenv --upgrade -r requirements.txt --log .venv/pip_install.log)

# Build HTML documentation using Sphinx
.PHONY: html
html: $(VENVDIR) $(BUILDDIR)
	$(call venv_exec, $(SPHINX) -E -b dirhtml $(SOURCEDIR) $(BUILDDIR))

# Ensure build directory exists
$(BUILDDIR):
	mkdir -p $(BUILDDIR)

# Run the local server with live reloading for development
.PHONY: run
run: SPHINX=sphinx-autobuild
run: html
	$(call venv_exec, $(SPHINX) --watch $(SOURCEDIR) $(SOURCEDIR) $(BUILDDIR))

# Check for broken links in the documentation
.PHONY: check
check: $(VENVDIR)
	$(call venv_exec, $(SPHINX) -b linkcheck -d $(BUILDDIR)/.doctrees $(SOURCEDIR))

# Clean up documentation build files and temporary files
.PHONY: clean-doc
clean-doc:
	rm -rf $(BUILDDIR) $(DEPLOYDIR) || true
	find $(SOURCEDIR) -type f \( -name '*.orig' -o -name '*.rej' -o -name '* 2.*' -o -name '*.pyc' -o -name '.DS_Store' \) -delete || true

# Clean the entire environment, including virtual environment
.PHONY: clean
clean: clean-doc
	rm -rf $(VENVDIR) || true

# Deploy the site locally before uploading to the remote server
.PHONY: deploy
deploy: html
	$(eval TMP := $(shell mktemp -d))
	rsync -rv $(EXCLUDE) $(BUILDDIR)/ $(TMP)/
	rsync -rcv --delete --exclude='*.gz' --exclude='tmp.*' $(TMP)/ $(DEPLOYDIR)/
	-rm -rf $(TMP)
	rm -f $(DEPLOYDIR)/index.html
	rm -rf $(DEPLOYDIR)/.doctrees
	rm -f $(DEPLOYDIR)/objects.inv
	rm -f $(DEPLOYDIR)/.buildinfo
	rm -rf $(DEPLOYDIR)/_sources
	cp index.htm $(DEPLOYDIR)/
	chmod -R g=u $(DEPLOYDIR)

# Backup the remote directory and sync locally
.PHONY: backup
backup:
	mkdir -p $(shell dirname $(BACKUP))
	# Backup remote directory to local
	rsync -rctv $(HOST):$(REMOTEDIR) $(TMPDIR)/
	tar -zcvf $(BACKUP) $(TMPDIR) && rm -rf $(TMPDIR)
	# Sync remote to local deploy directory
	rsync -rctv $(HOST):$(REMOTEDIR) $(DEPLOYDIR)/

# Clean docs, backup, and then upload merged updates to the remote server
.PHONY: upload
upload: clean-doc backup deploy
	# Dry-run sync to remote server for verification
	rsync -rctvn $(DEPLOYDIR)/ $(HOST):$(REMOTEDIR)
	# Final sync if dry-run is successful
	rsync -rctv $(DEPLOYDIR)/ $(HOST):$(REMOTEDIR)
