def pod_key(namespace: str, name: str) -> str:
    return f"/registry/pods/{namespace}/{name}"


def service_key(namespace: str, name: str) -> str:
    return f"/registry/services/{namespace}/{name}"
