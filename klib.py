from os import path
import yaml
from kubernetes import client, config
import time

class App():
    """Class that read the yaml and create objects in k8s"""
    def __init__(self, yaml_file, namespace="default"):
        # read yaml file
        with open(path.join(path.dirname(__file__), yaml_file)) as f:
            # because of safe_load_all returns generator need to convert to list
            yaml_list = list(yaml.safe_load_all(f))
            # remove None values
            self.yaml_config = [i for i in yaml_list if i]
            self.namespace = namespace
            self.k8s_config = config.load_kube_config()
            self.k8s_apps_v1 = client.AppsV1Api()
            self.k8s_core_v1 = client.CoreV1Api()
            self.k8s_custom_obj = client.CustomObjectsApi()

    def check_for_repeating_resources(self):
        pass

    def print_yaml(self):
        for resource in self.yaml_config:
            print(resource)

    def k_apply(self):
        for resource in self.yaml_config:
            print(f"resource yaml: {resource}")
            if resource['kind'] == 'Deployment':
                self.apply_deployment(resource)
            elif resource['kind'] == 'Service':
                self.apply_service(resource)
            elif resource['kind'] == 'ServiceAccount':
                self.apply_service_account(resource)
            else:
                self.apply_custom_object(resource)

    def k_delete(self):
        for resource in self.yaml_config:
            print(f"resource yaml: {resource}")
            try:
                if resource['kind'] == 'Deployment':
                    self.delete_deployment(resource)
                elif resource['kind'] == 'Service':
                    self.delete_service(resource)
                elif resource['kind'] == 'ServiceAccount':
                    self.delete_service_account(resource)
                else:
                    self.delete_custom_object(resource)
            except client.rest.ApiException:
                pass

    def k_check_status(self):
        for resource in self.yaml_config:
            if resource['kind'] == 'Deployment':
                self.wait_for_deployment_complete(resource)

    def apply_custom_object(self, body):
        bgroup, bversion = body['apiVersion'].split('/')
        bname = body['metadata']['name']
        try:
            resp = self.k8s_custom_obj.create_namespaced_custom_object(
                group=bgroup,
                version=bversion,
                namespace=self.namespace,
                plural=f"{body['kind'].lower()}s",
                body=body)
            print(f"Custom objet created. name='%s'" % resp['metadata']['name'])
        except client.rest.ApiException:
            resp = self.k8s_custom_obj.patch_namespaced_custom_object(
                name=bname,
                group=bgroup,
                version=bversion,
                namespace=self.namespace,
                plural=f"{body['kind'].lower()}s",
                body=body)
            print("Custom objet updated. name='%s'" % resp['metadata']['name'])

    def apply_service_account(self, body):
        try:
            resp = self.k8s_core_v1.create_namespaced_service_account(
                body=body, namespace=self.namespace)
            print("Service account created. name='%s'" % resp.metadata.name)
        except client.rest.ApiException:
            resp = self.k8s_core_v1.patch_namespaced_service_account(
                name=body['metadata']['name'], body=body, namespace=self.namespace)
            print("Service account updated. name='%s'" % resp.metadata.name)

    def apply_deployment(self, body):
        try:
            resp = self.k8s_apps_v1.create_namespaced_deployment(
                body=body, namespace=self.namespace)
            print("Deployment created. name='%s'" % resp.metadata.name)
        except client.rest.ApiException:
            resp = self.k8s_apps_v1.patch_namespaced_deployment(
                name=body['metadata']['name'], body=body, namespace=self.namespace)
            print("Deployment updated. name='%s'" % resp.metadata.name)

    def apply_service(self, body):
        try:
            resp = self.k8s_core_v1.create_namespaced_service(
                body=body, namespace=self.namespace)
            print("Service created. name='%s'" % resp.metadata.name)
        except client.rest.ApiException:
            resp = self.k8s_core_v1.patch_namespaced_service(
                name=body['metadata']['name'], body=body, namespace=self.namespace)
            print("Service updated. name='%s'" % resp.metadata.name)

    def delete_deployment(self, body):
        resp = self.k8s_apps_v1.delete_namespaced_deployment(
            name=body['metadata']['name'], namespace=self.namespace)
        print("Deployment deleted. status='%s'" % resp.status)

    def delete_service(self, body):
        resp = self.k8s_core_v1.delete_namespaced_service(
            name=body['metadata']['name'], namespace=self.namespace)
        print("Deployment deleted. status='%s'" % resp.status)

    def delete_service_account(self, deployment_body):
            resp = self.k8s_core_v1.delete_namespaced_service_account(
                name=deployment_body['metadata']['name'], namespace=self.namespace)
            print("Deployment deleted. status='%s'" % resp.status)

    def delete_custom_object(self, body):
        bgroup, bversion = body['apiVersion'].split('/')
        bname = body['metadata']['name']
        resp = self.k8s_custom_obj.delete_namespaced_custom_object(
            group=bgroup,
            version=bversion,
            namespace=self.namespace,
            plural=f"{body['kind'].lower()}s",
            name=bname)
        print(f"Custom objet deleted. name='%s'" % bname)

    def wait_for_deployment_complete(self, body, timeout=600):
        start = time.time()
        name = body['metadata']['name']
        while time.time() - start < timeout:
            time.sleep(1)
            resp = self.k8s_apps_v1.read_namespaced_deployment_status(
                name=name, namespace=self.namespace)
            s = resp.status
            if (s.updated_replicas == resp.spec.replicas and
                    s.replicas == resp.spec.replicas and
                    s.available_replicas == resp.spec.replicas and
                    s.observed_generation >= resp.metadata.generation):
                print(f"deployment rollout {name} completed.")
                return True
            else:
                print(f"waiting deployment {name} to be completed...", )

        raise RuntimeError(f'Waiting timeout for deployment {name}')



