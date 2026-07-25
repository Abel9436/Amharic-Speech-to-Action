PY ?= python
CONFIG_BASELINE ?= configs/baseline.yaml

.PHONY: test lint baseline errors tables finetune eval demo

test:
	$(PY) -m pytest -q

lint:
	ruff check src tests app examples

baseline:
	$(PY) -m src.baseline --config $(CONFIG_BASELINE)

errors:
	$(PY) -m src.eval.error_analysis --input-dir results/baseline --output results/baseline_errors.md

tables:
	$(PY) -m src.report_tables --readme README.md

finetune:
	@echo "Phase 3: not implemented yet"; exit 1

eval:
	@echo "Phase 6: not implemented yet"; exit 1

demo:
	@echo "Phase 7: not implemented yet"; exit 1
