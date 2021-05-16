import os
import kopf
import kubernetes
import yaml


# @kopf.on.login()
# def login_fn(**kwargs):
#     return kopf.ConnectionInfo(
#         server="https://192.168.99.105:8443",
#         insecure=True,
#         certificate_path='/Users/yimo/.minikube/profiles/minikube/client.crt',
#         private_key_path='/Users/yimo/.minikube/profiles/minikube/client.key',
#     )


@kopf.on.create('ephemeralvolumeclaims')
def create_fn(spec, name, namespace, logger, **kwargs):
    size = spec.get('size')
    if not size:
        raise kopf.PermanentError(f"Size must be set. Got {size!r}.")

    path = os.path.join(os.path.dirname(__file__), 'pvc.yaml')
    tmpl = open(path, 'rt').read()
    text = tmpl.format(name=name, size=size)
    data = yaml.safe_load(text)

    api = kubernetes.client.CoreV1Api()
    obj = api.create_namespaced_persistent_volume_claim(
        namespace=namespace,
        body=data,
    )
    logger.info(f"PVC child is created: %s", obj)


@kopf.on.field('ephemeralvolumeclaims', field='metadata.labels')
def relabel(old, new, status, namespace, **kwargs):
    pvc_name = status['create_fn']['pvc-name']
    pvc_patch = {'metadata': {'labels': new}}

    api = kubernetes.client.CoreV1Api()
    api.patch_namespaced_persistent_volume_claim(
        namespace=namespace,
        name=pvc_name,
        body=pvc_patch,
    )
