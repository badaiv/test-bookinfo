# test-bookinfo
bookinfo test app  

This demo app  is supposed to show demo setup of Minikube + Istio + bookinfo app using a bit bash scripting and python.

### Requirements
You should have installed:
* python >= 3.6 [download](https://www.python.org/downloads/)
* [minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/)
### Configuration
edit `env.properties` file to setup some properties like Minkube driver or Istio version.

### Start env
this should start minikube, install [Istio](https://istio.io/latest/docs/), install required pip modules and start [pipenv](https://github.com/pypa/pipenv) shell in your terminal.
```
chmod u+x start.sh
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
### Metrics
To access metrics dashboard you can use k8s dashboard
```
minikube dashboard
```
To access Istio metrics collected by sidecar proxy
```
istioctl dashboard kiali
#or
istioctl dashboard grafana
```
### Access productpage
to enable localhost portforwarding from Istio lb
```
minikube tunnel
```
then open in browser `http://127.0.0.1/productpage`
### Destroy env
this will destroy whole k8s cluster
```
minkube delete
```
