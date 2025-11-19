import tempfile
import json
import subprocess
from typing import Any, Dict, List
from strictyaml import load, YAMLValidationError, YAMLError


# ------------------------
# Strict YAML syntax parsing
# ------------------------
def strict_parse(text: str) -> Any:
    """Strict YAML parsing using strictyaml"""
    if not text or not text.strip():
        raise ValueError("Empty YAML input")

    try:
        parsed = load(text)
        return parsed.data  # return native Python
    except (YAMLValidationError, YAMLError) as e:
        raise ValueError(str(e))
    except Exception as e:
        raise ValueError(f"Unexpected parsing error: {e}")


# ------------------------
# Kubernetes schema validation with kubeconform
# ------------------------
def kubeconform_validate(text: str, kubeconform_path="kubeconform") -> List[str]:
    """Run kubeconform on YAML text and capture validation errors."""

    errors = []

    with tempfile.NamedTemporaryFile(mode="w+", suffix=".yaml", delete=True) as tf:
        tf.write(text)
        tf.flush()

        cmd = [
            kubeconform_path,
            "-strict",
            "-summary",
            "-output", "json",
            tf.name
        ]

        proc = subprocess.run(cmd, capture_output=True, text=True)
        stdout = proc.stdout.strip()

        if not stdout:
            return ["No output from kubeconform"]

        try:
            results = json.loads(stdout)
        except json.JSONDecodeError:
            return [f"Kubeconform returned non-JSON output: {stdout}"]

        # NEW structure: results["resources"] is a list
        resources = results.get("resources", [])

        for item in resources:

            status = item.get("status")
            msg = item.get("msg", "")

            # Error states
            if status in ["invalid", "statusError", "error"]:
                if msg:
                    errors.append(msg)
                else:
                    # fallback to structured errors
                    for e in item.get("errors", []):
                        errors.append(e)

        return errors



# ------------------------
# Combined validation
# ------------------------
def validate_yaml_only(text: str) -> Dict[str, Any]:
    """Strict YAML only."""
    result = {
        "valid": False,
        "syntax_errors": [],
        "parsed": None
    }

    try:
        parsed = strict_parse(text)
        result["parsed"] = parsed
        result["valid"] = True
    except ValueError as ve:
        result["syntax_errors"].append(str(ve))

    return result


def validate_yaml_k8s(text: str) -> Dict[str, Any]:
    """Strict YAML + Kubernetes schema validation."""
    result = {
        "valid": False,
        "syntax_errors": [],
        "k8s_errors": [],
        "parsed": None
    }

    # Step 1: Syntax Validation
    try:
        parsed = strict_parse(text)
        result["parsed"] = parsed
    except ValueError as ve:
        result["syntax_errors"].append(str(ve))
        return result

    # Step 2: K8s schema validation (FIXED HERE)
    result["k8s_errors"] = kubeconform_validate(text)

    result["valid"] = (
        len(result["syntax_errors"]) == 0 and
        len(result["k8s_errors"]) == 0
    )
    return result
