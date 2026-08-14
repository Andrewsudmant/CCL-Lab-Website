.PHONY: install validate generate test build linkcheck linkcheck-external accessibility check handoff owner-package preview clean

HANDOFF_SUMMARY ?= docs/handoffs/gate-2-3a-handoff.md
PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)

install:
	$(PYTHON) -m pip install -r requirements-dev.txt

validate:
	$(PYTHON) scripts/validate_content.py

generate:
	$(PYTHON) scripts/generate_site.py

test: generate
	$(PYTHON) -m pytest

build:
	./scripts/quarto.sh render

linkcheck: build
	$(PYTHON) scripts/check_links.py

linkcheck-external: build
	$(PYTHON) scripts/check_links.py --external

accessibility: build
	$(PYTHON) scripts/check_accessibility.py

check: validate test build
	$(PYTHON) scripts/check_links.py
	$(PYTHON) scripts/check_accessibility.py

handoff:
	$(PYTHON) scripts/package_handoff.py --summary "$(HANDOFF_SUMMARY)"

owner-package:
	$(PYTHON) scripts/package_owner_review.py

preview: generate
	./scripts/quarto.sh preview

clean:
	./scripts/quarto.sh clean
