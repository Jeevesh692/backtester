.PHONY: build run test
build:
	docker build -t backtester .
run:
	docker run --rm backtester
test:
	docker compose run --rm -T tests
