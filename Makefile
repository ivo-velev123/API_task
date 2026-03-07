build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

test-e2e:
	docker-compose exec frontend python create_user.py
	pytest tests/e2e
