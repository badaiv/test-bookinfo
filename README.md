# test-bookinfo
bookinfo test app  

This demo app  is supposed to show demo setup of Minikube + Istio + bookinfo app using a bit bash scripting and python.

### Requirements
You should have installed:
* python >= 3.6 [download](https://www.python.org/downloads/)
* [minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/)
  
### Start env
this should start minikube, install [Istio](https://istio.io/latest/docs/), install required pip modules and start [pipenv](https://github.com/pypa/pipenv) shell in your terminal.
```
./start.sh
```
### Create resources in k8s
after you started pipenv you can create resources in terraform. 
```
pyhton main.py
```
this will also start curl container which will poll product page container each 10 sec.
you can check logs of container.
```
kubectl logs -l app=curl -c curl -f
```
### configuration
edit `env.properties` file to setup some properties like Minkube driver or Istio version.

### Metrics
To access metrics dashboard you can use k8s dashboard
```
minikube dashboard
```
To access Istio metrics collected by proxy
```
istioctl dashboard kiali
#or
istioctl dashboard grafana
```

## destroy env
this will destroy whole k8s cluster
```
minkube delete
```
