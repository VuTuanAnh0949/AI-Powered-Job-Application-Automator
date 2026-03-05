# Makefile for AutoApply AI

.PHONY: help install dev prod clean test lint format

help:
	@echo "AutoApply AI - Development Commands"
	@echo ""
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@echo "  install       Install all dependencies (backend + frontend)"
	@echo "  dev          Start development servers (Docker)"
	@echo "  dev-local    Start development servers (local)"
	@echo "  prod         Start production servers (Docker)"
	@echo "  stop         Stop all Docker services"
	@echo "  clean        Clean build artifacts and caches"
	@echo "  test         Run all tests"
	@echo "  lint         Run linters"
	@echo "  format       Format code"
	@echo "  logs         Show Docker logs"

install:
	@echo "Installing backend dependencies..."
	cd apps/backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd apps/frontend && npm install
	@echo "✓ All dependencies installed"

dev:
	@echo "Starting development environment with Docker..."
	docker-compose -f docker-compose.dev.yml up

dev-backend:
	@echo "Starting backend development server..."
	cd apps/backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	@echo "Starting frontend development server..."
	cd apps/frontend && npm run dev

prod:
	@echo "Starting production environment..."
	docker-compose up -d
	@echo "✓ Services started"
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"

stop:
	@echo "Stopping all services..."
	docker-compose down
	docker-compose -f docker-compose.dev.yml down

clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".vite" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✓ Cleaned"

test:
	@echo "Running backend tests..."
	cd apps/backend && pytest
	@echo "Running frontend tests..."
	cd apps/frontend && npm run test

lint:
	@echo "Linting backend..."
	cd apps/backend && ruff check .
	@echo "Linting frontend..."
	cd apps/frontend && npm run lint

format:
	@echo "Formatting backend code..."
	cd apps/backend && ruff format .
	@echo "Formatting frontend code..."
	cd apps/frontend && npm run format

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

build:
	@echo "Building Docker images..."
	docker-compose build

setup-env:
	@echo "Setting up environment files..."
	test -f apps/backend/.env || cp apps/backend/.env.example apps/backend/.env
	test -f apps/frontend/.env || cp apps/frontend/.env.example apps/frontend/.env
	test -f .env || cp .env.docker.example .env
	@echo "✓ Environment files created. Please edit them with your credentials."
