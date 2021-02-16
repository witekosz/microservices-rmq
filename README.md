# microservices-rmq

```
poetry run python -m unittest -v app/tests/test_rest.py
```

```
curl -X POST http://0.0.0.0:8080/api/values/ -d '{"key": "123", "value": "test sdf"}'
```

```
curl -X GET http://0.0.0.0:8080/api/values/128/
```

https://docs.aiohttp.org/en/stable/testing.html#aiohttp.test_utils.TestClient

https://aio-pika.readthedocs.io/en/latest/
