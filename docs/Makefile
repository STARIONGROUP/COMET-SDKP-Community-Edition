# Minimal makefile for Sphinx documentation

SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

.PHONY: help Makefile

help:
    @$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)"

.PHONY: html
html:
    @$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: clean
clean:
    rm -rf "$(BUILDDIR)"

.PHONY: serve
serve: html
    python -m http.server -d _build/html 8000