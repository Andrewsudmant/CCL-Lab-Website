.PHONY: install validate generate test build linkcheck linkcheck-external accessibility check preview clean

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

preview: generate
	./scripts/quarto.sh preview

clean:
	./scripts/quarto.sh clean
