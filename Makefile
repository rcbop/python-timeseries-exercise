# this makefile will install the required python packages for each component
SHELL:=/bin/bash
COMPONENTS=data-api data-generator
VERSION=3.11.1
PYTHON=${VENV_DIR}/bin/python

.PHONY: install
install:
	for component in $(COMPONENTS); do \
		pushd $$component; \
		pip install --upgrade pip; \
		if [ -d $(HOME)/.pyenv/versions/$$component ]; then \
			pyenv activate $$component; \
		else \
			pyenv virtualenv $(VERSION) $$component; \
			pyenv activate $$component; \
		fi; \
		pip install -r requirements.txt; \
		pip install -r requirements_dev.txt; \
		popd; \
	done

.PHONY: clean
clean:
	for component in $(COMPONENTS); do \
		pushd $$component; \
		rm -rf $(HOME)/.pyenv/versions/$$component; \
		popd; \
	done

.PHONY: test
test:
	for component in $(COMPONENTS); do \
		pushd $$component; \
		pyenv activate $$component; \
		pytest; \
		popd; \
	done

.PHONY: data-api
data-api:
	pushd data-api; \
	pyenv activate data-api; \
	python main.py; \
	popd;

.PHONY: data-generator
data-generator:
	pushd data-generator; \
	pyenv activate data-generator; \
	python main.py; \
	popd;

.PHONY: compose-up
compose-up:
	docker-compose up -d

.PHONY: compose-down
compose-down:
	docker-compose down -v
