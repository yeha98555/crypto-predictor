run-dev:
	uv run python run.py

build:
	docker build -f Dockerfile -t trades .

run: build
	docker run -it \
		--network redpanda-dev-cluster_redpanda_network \
		trades

# Run ruff linter
lint:
	uv run ruff check .

# Run ruff formatter
format:
	uv run ruff check --fix .
