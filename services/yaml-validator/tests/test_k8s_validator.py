import validator
from unittest.mock import patch

def fake_kubeconform_success(*args, **kwargs):
    return [{"filename": "x", "status": "valid"}]

@patch("app.validator.kubeconform_validate", return_value=[])
def test_k8s_valid(mocked):
    text = """
apiVersion: v1
kind: Pod
metadata:
  name: test
spec:
  containers:
  - name: c
    image: nginx
"""
    result = validator.validate_yaml_k8s(text)
    assert result["valid"] is True

@patch("app.validator.kubeconform_validate", return_value=["bad schema"])
def test_k8s_invalid(mocked):
    text = "key: value"
    result = validator.validate_yaml_k8s(text)
    assert result["valid"] is False
    assert len(result["k8s_errors"]) == 1
