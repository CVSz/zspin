from zspin.k8s.registry import pod_key, service_key


def test_k8s_registry_key_layouts() -> None:
    assert pod_key("default", "nginx") == "/registry/pods/default/nginx"
    assert service_key("default", "api") == "/registry/services/default/api"
