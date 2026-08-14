.PHONY: install validate generate test build linkcheck linkcheck-external accessibility check publications-refresh research-watch-fixture research-watch-pilot research-watch-recheck calibration-pack browser-qa handoff owner-review owner-package preview clean

HANDOFF_SUMMARY ?= docs/handoffs/gate-3b-4a-handoff.md
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

publications-refresh:
	PYTHONPATH=. $(PYTHON) scripts/refresh_publications.py --output-dir reports/content

research-watch-fixture:
	PYTHONPATH=. $(PYTHON) -m research_watch.run --adapter fixture

research-watch-pilot:
	PYTHONPATH=. $(PYTHON) scripts/run_research_watch_pilot.py

research-watch-recheck:
	PYTHONPATH=. $(PYTHON) scripts/recheck_research_watch.py

calibration-pack:
	$(PYTHON) scripts/package_calibration.py

browser-qa: build
	$(PYTHON) scripts/check_browser_qa_artifacts.py

handoff:
	$(PYTHON) scripts/package_handoff.py --summary "$(HANDOFF_SUMMARY)"

owner-package:
	$(PYTHON) scripts/package_owner_review.py

owner-review: owner-package

preview: generate
	./scripts/quarto.sh preview

clean:
	./scripts/quarto.sh clean
