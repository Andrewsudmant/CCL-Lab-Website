.PHONY: install validate generate test build linkcheck linkcheck-external accessibility check publications-refresh current-conversations-fixture current-conversations-discover openalex-diagnostics current-conversations-pilot current-conversations-recheck current-conversations-stage current-conversations-rollback-test model-benchmark calibration-pack browser-qa handoff owner-review owner-package thematic-owner-review research-watch-fixture research-watch-pilot research-watch-recheck preview clean

HANDOFF_SUMMARY ?= docs/handoffs/gate-5b-handoff.md
PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)

install:
	$(PYTHON) -m pip install -r requirements-dev.txt
validate:
	$(PYTHON) scripts/validate_content.py
generate:
	$(PYTHON) scripts/generate_site.py
test: generate
	$(PYTHON) -m pytest
build: generate
	./scripts/quarto.sh render
linkcheck: build
	$(PYTHON) scripts/check_links.py
linkcheck-external: build
	$(PYTHON) scripts/check_links.py --external
accessibility: build
	$(PYTHON) scripts/check_accessibility.py
check: validate build
	$(PYTHON) -m pytest
	$(PYTHON) scripts/check_links.py
	$(PYTHON) scripts/check_accessibility.py
publications-refresh:
	PYTHONPATH=. $(PYTHON) scripts/refresh_publications.py --output-dir reports/content
	$(PYTHON) scripts/build_complete_publications.py
current-conversations-fixture:
	PYTHONPATH=. $(PYTHON) -m current_conversations.run --adapter fixture
current-conversations-discover:
	PYTHONPATH=. $(PYTHON) -m current_conversations.run --adapter openalex --limit 2
openalex-diagnostics:
	PYTHONPATH=. $(PYTHON) scripts/diagnose_openalex.py
current-conversations-pilot:
	PYTHONPATH=. $(PYTHON) scripts/run_current_conversations_pilot.py --mode fixture-only
current-conversations-recheck:
	PYTHONPATH=. $(PYTHON) scripts/recheck_current_conversations.py
current-conversations-stage:
	PYTHONPATH=. $(PYTHON) scripts/run_current_conversations_pilot.py --mode staging-write
	PYTHONPATH=scripts $(PYTHON) scripts/exercise_staging_branch.py
current-conversations-rollback-test:
	$(PYTHON) -m pytest tests/test_gate_4b_5a_controls.py -k rollback
model-benchmark:
	PYTHONPATH=. $(PYTHON) scripts/benchmark_current_conversations_models.py
calibration-pack: current-conversations-pilot
	$(PYTHON) scripts/package_calibration.py
browser-qa: build
	$(PYTHON) scripts/check_browser_qa_artifacts.py
handoff:
	$(PYTHON) scripts/package_handoff.py --summary "$(HANDOFF_SUMMARY)"
owner-package:
	$(PYTHON) scripts/package_owner_review.py
owner-review: owner-package
thematic-owner-review:
	$(PYTHON) scripts/package_thematic_review.py
research-watch-fixture:
	@echo "Deprecated: use current-conversations-fixture"
	@$(MAKE) current-conversations-fixture
research-watch-pilot:
	@echo "Deprecated: use current-conversations-pilot"
	@$(MAKE) current-conversations-pilot
research-watch-recheck:
	@echo "Deprecated: use current-conversations-recheck"
	@$(MAKE) current-conversations-recheck
preview: generate
	./scripts/quarto.sh preview
clean:
	./scripts/quarto.sh clean
