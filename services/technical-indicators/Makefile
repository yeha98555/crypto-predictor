run-dev:
	uv run python run.py

build:
	docker build -f Dockerfile -t technical-indicators .

run: build
	docker run -it \
		--network redpanda-dev-cluster_redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda:9092 \
		technical-indicators

# Run ruff linter
lint:
	uv run ruff check .

# Run ruff formatter
format:
	uv run ruff check --fix .
	uv run ruff format
