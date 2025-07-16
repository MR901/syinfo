# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Custom targets for SyInfo documentation

# Build all documentation formats
all: html pdf epub

# Build HTML documentation
html:
	@echo "Building HTML documentation..."
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@echo "HTML documentation built in $(BUILDDIR)/html/"

# Build PDF documentation
pdf:
	@echo "Building PDF documentation..."
	@$(SPHINXBUILD) -M latexpdf "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@echo "PDF documentation built in $(BUILDDIR)/latex/"

# Build EPUB documentation
epub:
	@echo "Building EPUB documentation..."
	@$(SPHINXBUILD) -M epub "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@echo "EPUB documentation built in $(BUILDDIR)/epub/"

# Clean build directory
clean:
	@echo "Cleaning build directory..."
	@rm -rf "$(BUILDDIR)"
	@echo "Build directory cleaned."

# Serve HTML documentation locally
serve: html
	@echo "Starting local server at http://localhost:8000"
	@echo "Press Ctrl+C to stop"
	@python -m http.server 8000 -d "$(BUILDDIR)/html"

# Check for broken links
linkcheck:
	@echo "Checking for broken links..."
	@$(SPHINXBUILD) -M linkcheck "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Spell check documentation
spelling:
	@echo "Running spell check..."
	@$(SPHINXBUILD) -M spelling "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Build documentation for GitHub Pages
gh-pages: html
	@echo "Building documentation for GitHub Pages..."
	@cp -r "$(BUILDDIR)/html/"* ./
	@echo "Documentation ready for GitHub Pages deployment."

# Install dependencies
install-deps:
	@echo "Installing documentation dependencies..."
	@pip install sphinx sphinx-rtd-theme sphinx-autodoc-typehints
	@echo "Dependencies installed."

# Full documentation build with checks
full: install-deps clean html linkcheck spelling
	@echo "Full documentation build completed."

# Quick documentation build
quick: html
	@echo "Quick documentation build completed."

# Build API documentation
api: html
	@echo "API documentation built."

# Build user guide
user-guide: html
	@echo "User guide built."

# Build developer documentation
dev-docs: html
	@echo "Developer documentation built." 