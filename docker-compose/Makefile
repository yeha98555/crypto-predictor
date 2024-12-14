start-redpanda:
	docker compose -f redpanda.yml up -d

stop-redpanda:
	docker compose -f redpanda.yml down

delete-redpanda-topic-all:
	@echo "警告：這將刪除所有 topics！"
	@read -p "確定要繼續嗎？ [y/N] " confirm; \
	if [ "$$confirm" = "y" ]; then \
		for topic in $$(docker compose -f redpanda.yml exec redpanda rpk topic list | awk 'NR>2 {split($$0,a," "); print a[1]}'); do \
			echo "Deleting topic: $$topic"; \
			docker compose -f redpanda.yml exec redpanda rpk topic delete $$topic; \
		done \
	fi

build-technical-indicators-pipeline:
	docker compose -f technical-indicators-pipeline.yml build

start-technical-indicators-pipeline: build-technical-indicators-pipeline
	docker compose -f technical-indicators-pipeline.yml up -d

stop-technical-indicators-pipeline:
	docker compose -f technical-indicators-pipeline.yml down
