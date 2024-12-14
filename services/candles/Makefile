run-dev:
	uv run python run.py

build:
	docker build -f Dockerfile -t candles .

run: build
	docker run -it \
		--network redpanda-dev-cluster_redpanda_network \
		candles

# Run ruff linter
lint:
	uv run ruff check .

# Run ruff formatter
format:
	uv run ruff check --fix .
	uv run ruff format
