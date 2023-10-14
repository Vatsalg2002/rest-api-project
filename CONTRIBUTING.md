# CONTRIBUTING

## How to run the docker dile locally

```
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" rest_api_project sh -c "flask run --host 0.0.0.0"
```