from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from validator import kubeconform_validate, validate_yaml_only

class Payload(BaseModel):
    text: Optional[str] = None
    yaml: Optional[str] = None

app = FastAPI(title="YAML Validator Service", version="1.0.0")

# Allow frontend usage
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"service": "yaml-validator", "status": "running"}

@app.post("/validate")
def validate_yaml(payload: Payload):
    """Generic YAML syntax validation (strictyaml)."""
    content = payload.text or payload.yaml
    if not content:
        raise HTTPException(400, "Provide 'text' or 'yaml' field")

    return validate_yaml_only(content)

@app.post("/validate/k8s")
def validate_k8s_yaml(payload: Payload):
    content = payload.text or payload.yaml
    if not content:
        raise HTTPException(400, "Provide 'text' or 'yaml' field")

    syntax_result = validate_yaml_only(content)

    if syntax_result["valid"] is False:
        return {
            "valid": False,
            "syntax_errors": syntax_result["syntax_errors"],
            "k8s_errors": [],
            "parsed": None
        }

    k8s_errors = kubeconform_validate(content)

    return {
        "valid": len(k8s_errors) == 0,
        "syntax_errors": [],
        "k8s_errors": k8s_errors,
        "parsed": syntax_result["parsed"]
    }