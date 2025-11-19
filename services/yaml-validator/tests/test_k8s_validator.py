from unittest.mock import patch
from app.validator import validate_yaml_k8s, kubeconform_validate


def test_k8s_yaml_valid():
    yaml_text = """
    apiVersion: v1
    kind: Pod
    metadata:
      name: test-pod
    spec:
      containers:
      - name: busy
        image: busybox
        command: ["echo", "hello"]
    """

    # Mock kubeconform to return no errors
    with patch("app.validator.kubeconform_validate", return_value=[]):
        result = validate_yaml_k8s(yaml_text)

    assert result["syntax_errors"] == []
    assert result["k8s_errors"] == []
    assert result["valid"] is True


def test_k8s_yaml_invalid_schema():
    yaml_text = """
    apiVersion: v1
    kind: Pod
    metadata: {}
    spec:
      containers:
      - name: test
        invalidField: true   # Should trigger schema error
    """

    # Mock kubeconform: simulate schema errors
    with patch("app.validator.kubeconform_validate", return_value=["Invalid schema"]):
        result = validate_yaml_k8s(yaml_text)

    assert result["syntax_errors"] == []
    assert result["k8s_errors"] == ["Invalid schema"]
    assert result["valid"] is False
