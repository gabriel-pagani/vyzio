build-project:
	cd frontend/ && npm install && npm run build && \
	cd ../deploy/ && \
	docker compose up -d --build

clean-project:
	cd deploy/ && \
	docker compose down && \
	docker system prune -a --volumes --force && \
    cd .. && rm -rf backend/build/ backend/static/ database/ frontend/node_modules/

start-system:
	cd deploy/ && \
	docker compose up -d

stop-system:
	cd deploy/ && \
	docker compose down

restart-system:
	cd deploy/ && \
	docker compose down && \
	docker compose up -d

list-images:
	docker images

list-containers:
	docker ps -a

container ?= app
container-terminal:
	cd deploy/ && \
	docker compose exec $(container) sh

container-logs:
	cd deploy/ && \
	docker compose logs -f $(container)
