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

#### Coverage

```sh
poetry run coverage run --source=. -m pytest app/tests/
poetry run coverage report
poetry run coverage html
```