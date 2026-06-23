# Makefile for CareerAI

.PHONY: help install run-backend run-frontend test docker-build docker-up clean lint

help:
	@echo "CareerAI - Available Commands"
	@echo "============================"
	@echo "make install        - Install all dependencies"
	@echo "make run-backend    - Start backend API server"
	@echo "make run-frontend   - Start frontend server"
	@echo "make test           - Run unit tests"
	@echo "make docker-build   - Build Docker image"
	@echo "make docker-up      - Start Docker containers"
	@echo "make clean          - Clean cache files"
	@echo "make lint           - Run code linter (future)"

install:
	pip install -r backend/requirements.txt
	pip install -r requirements-frontend.txt
	cp backend/.env.example backend/.env
	python -c "from app.data.database import db; db.init_db()"

run-backend:
	cd backend && python main.py

run-frontend:
	python app.py

test:
	cd backend && pytest -v

docker-build:
	docker-compose build

docker-up:
	docker-compose up

docker-down:
	docker-compose down

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache
	rm -rf *.egg-info
	rm -rf build dist

dev: install
	@echo "✨ Development environment ready!"
	@echo "Next steps:"
	@echo "1. Edit backend/.env with your OpenAI API key"
	@echo "2. Run 'make run-backend' in one terminal"
	@echo "3. Run 'make run-frontend' in another terminal"
