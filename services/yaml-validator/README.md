# YAML Validator Service

Simple FastAPI microservice that validates YAML/JSON text.

## Endpoints
- `GET /` - health check
- `POST /validate` - validate payload: `{ "yaml": "<yaml-or-json-here>" }`
- `POST /validate/k8s` - validate k8s manifests: `{ "yaml": "<yaml-or-json-here>" }`

## Local run
```bash
cd services/yaml-validator
pip install -r app/requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8003
```

## Docker
```
docker build -t YOUR_DOCKERHUB_USERNAME/yaml-validator:latest .
docker run -p 8003:8003 YOUR_DOCKERHUB_USERNAME/yaml-validator:latest
```