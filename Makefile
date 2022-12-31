# this makefile will install the required python packages for each component
SHELL:=/usr/bin/zsh
PYTHON_COMPONENTS=data-api data-generator plotly-dashboard
NODE_PROJECT_DIR=angular-dashboard/dashboard
VERSION=3.11.1
PYTHON=${VENV_DIR}/bin/python

.PHONY: install
install:
	for component in $(PYTHON_COMPONENTS); do \
		pushd $$component; \
		pip install --upgrade pip; \
		pyenv virtualenv --force $(VERSION) $$component; \
		pyenv activate $$component; \
		pip install -r requirements.txt; \
		pip install -r requirements-dev.txt; \
		popd; \
	done;
	pushd $(NODE_PROJECT_DIR); \
	npm install; \
	popd;

# delete all the python virtual environments
.PHONY: clean
clean:
	for component in $(PYTHON_COMPONENTS); do \
		pyenv virtualenv-delete -f $$component; \
	done;
	pushd $(NODE_PROJECT_DIR); \
	rm -rf node_modules; \
	popd;

.PHONY: compose-build
compose-build:
	docker compose build

.PHONY: compose-up
compose-up:
	docker compose up -d

.PHONY: compose-down
compose-down:
	docker compose down

.PHONY: compose-clean
compose-clean:
	docker compose down --rmi all --volumes
