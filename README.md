# microservices-rmq

```
poetry run python -m unittest -v app/tests/test_rest.py
```

```
poetry export --output requirements.txt --without-hashes
```

```
curl -X POST -v http://0.0.0.0:8080/api/values/ -d '{"key": "123", "value": "test sdf"}'
```

```
curl -X GET -v http://0.0.0.0:8080/api/values/123/
```
