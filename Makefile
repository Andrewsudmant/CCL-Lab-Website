.PHONY: install validate generate test build linkcheck linkcheck-external accessibility check handoff preview clean

HANDOFF_SUMMARY ?= docs/handoffs/gate-0-1-handoff.md

install:
	python3 -m pip install -r requirements-dev.txt

validate:
	python3 scripts/validate_content.py

generate:
	python3 scripts/generate_site.py

test: generate
	python3 -m pytest

build:
	./scripts/quarto.sh render

linkcheck: build
	python3 scripts/check_links.py

linkcheck-external: build
	python3 scripts/check_links.py --external

accessibility: build
	python3 scripts/check_accessibility.py

check: validate test build
	python3 scripts/check_links.py
	python3 scripts/check_accessibility.py

handoff:
	python3 scripts/package_handoff.py --summary "$(HANDOFF_SUMMARY)"

preview: generate
	./scripts/quarto.sh preview

clean:
	./scripts/quarto.sh clean
