#!/usr/bin/env bash
set -x

#load some properties
load_env_properties() {
  source env.properties
}

#check env dependencies
check_env() {
  #check minikube is present on system
  command -v minikube >/dev/null 2>&1 || {
    echo >&2 "there is no 'minikube' in you PATH. aborting."
    exit 1
  }
  # check that we have pyton3
  command -v python3 >/dev/null 2>&1 || {
    echo >&2 "there is no python3 in you PATH. aborting."
    exit 1
  }
}

start_istio() {
  ISTIO_PATH=${PWD}/istio-${ISTIO_VERSION}
  if ! ls ${ISTIO_PATH} 1>/dev/null 2>&1; then
    curl -L https://istio.io/downloadIstio | sh -
  fi
  export PATH=${ISTIO_PATH}/bin:$PATH
  echo "istioctl version:"
  istioctl version
  echo "istioctl install:"
  istioctl manifest generate --set profile=demo > generated-manifest.yaml
  istioctl verify-install -f generated-manifest.yaml || ( istioctl install --set profile=demo && istioctl verify-install -f generated-manifest.yaml )
}

start_minikube() {
  echo "minikube version:"
  minikube version
  echo "minikube start cluster:"
  minikube status  || ( minikube start --driver=$MINIKUBE_DRIVER && minikube status)
}

#start environment
start_env() {
  start_minikube
  start_istio
}

main() {
  load_env_properties
  check_env
  start_env
}

main "$@"
