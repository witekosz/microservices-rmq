# microservices-rmq

Async python microservices with RabbitMQ.

Available endpoints:
- **/api/values/{value_id}/** _GET_ - Retrive value
- **/api/values/** _POST_ - Add or update value

### Local demo

Run containers:
```sh
docker-compose up -d --build
```

Check if server is working(should return 404):
```sh
curl -X GET -v http://0.0.0.0:8080/api/values/123/
```

Send value:
```sh
curl -X POST -v http://0.0.0.0:8080/api/values/ -d '{"key": "123", "value": "test sdf"}'
```

Retrive added value:
```sh
curl -X GET -v http://0.0.0.0:8080/api/values/123/
```
### Development

Recomended [poetry](https://github.com/python-poetry/poetry) for local development.

Run services in different processes:
```sh
python -m app.rest
python -m app.rpc_server
```

Exporting requirements:
```sh
poetry export --output requirements.txt --without-hashes
```

#### Tests
```sh
poetry run pytest app/tests/
```

#### Coverage

```sh
poetry run coverage run --source=. -m pytest app/tests/
poetry run coverage report
poetry run coverage html
```
