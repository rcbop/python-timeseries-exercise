#!/usr/bin/env bash
set -euo pipefail
ENVIRONMENT=${ENVIRONMENT:-dev}

# This script validates the manifests in the deployment/k8s directory.
find deployment/k8s/${ENVIRONMENT} -name 'kustomization.yaml' | xargs -I{} dirname {} | xargs -I{} kubectl kustomize {} | kubeconform -verbose
