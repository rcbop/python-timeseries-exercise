# this makefile will install the required python packages for each component
SHELL:=/usr/bin/zsh
PYTHON_COMPONENTS=data-api data-generator dashboard-plotly dashboard-nicegui
NODE_PROJECT_DIR=dashboard-angular/dashboard
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

.PHONY: test
test:
	docker compose -f docker-compose.test.yaml up --build --abort-on-container-exit

.PHONY: cloc
cloc:
	cloc --exclude-dir=$(tr '\n' ',' < .clocignore) .

.PHONY: tf-docs
tf-docs:
	terraform-docs markdown table --output-file README.md --output-mode inject deployment/terraform

.PHONY: tf-init
tf-init:
	terraform -chdir=deployment/terraform init

.PHONY: tf-plan
tf-plan:
	terraform -chdir=deployment/terraform plan

.PHONY: tf-apply
tf-apply:
	terraform -chdir=deployment/terraform apply

.PHONY: tf-destroy
tf-destroy:
	terraform -chdir=deployment/terraform/ destroy

.PHONY: tf-fmt
tf-fmt:
	terraform fmt -recursive deployment/terraform

.PHONY: localstack-start
localstack-start:
	docker run -d --name=localstack -it -p 4566:4566 -p 4510-4559:4510-4559 localstack/localstack

.PHONY: localstack-stop
localstack-stop:
	docker stop localstack

.PHONY: localstack-destroy
localstack-destroy:
	docker rm localstack

.PHONY: tflocal
tflocal:
	@which tflocal > /dev/null || (echo "tflocal not found, installing" && pip install tflocal)

.PHONY: tflocal-init
tflocal-init: tflocal
	pushd deployment/terraform && tflocal init && popd

.PHONY: tflocal-plan
tflocal-plan: tflocal
	pushd deployment/terraform && tflocal plan && popd

.PHONY: tflocal-apply
tflocal-apply: tflocal
	pushd deployment/terraform && tflocal apply && popd

.PHONY: tflocal-destroy
tflocal-destroy: tflocal
	pushd deployment/terraform && tflocal destroy && popd
