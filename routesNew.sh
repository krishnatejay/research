curl -X POST -d '{"address": "10.0.1.1/24"}' http://localhost:8080/router/0000000000000040
curl -X POST -d '{"address": "10.0.2.1/24"}' http://localhost:8080/router/0000000000000040
curl -X POST -d '{"address": "10.0.2.2/24"}' http://localhost:8080/router/0000000000000050
curl -X POST -d '{"address": "10.0.3.1/24"}' http://localhost:8080/router/0000000000000050
curl -X POST -d '{"address": "10.0.4.1/24"}' http://localhost:8080/router/0000000000000050
curl -X POST -d '{"gateway": "10.0.2.2"}' http://localhost:8080/router/0000000000000040
curl -X POST -d '{"gateway": "10.0.2.1"}' http://localhost:8080/router/0000000000000050
