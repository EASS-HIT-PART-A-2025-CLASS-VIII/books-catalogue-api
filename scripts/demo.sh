#!/bin/bash
set -e

echo "🚀 Starting EX3 Demo Flow..."


docker compose up -d --build
echo "⏳ Waiting for services to be ready..."
sleep 10


docker exec books-backend alembic upgrade head


echo "🔑 Logging in..."
docker exec books-cli python -m interface.cli login teacher classroom


echo "📚 Adding a new book..."
docker exec books-cli python -m interface.cli add --title "Clean Code" --author "Robert Martin" --year 2008 --genre "Software"

echo "📋 Listing books..."
docker exec books-cli python -m interface.cli list


echo "🔄 Triggering background refresh..."
docker exec books-cli python -m interface.cli refresh


echo "💾 Exporting catalogue..."
docker exec books-cli python -m interface.cli export --filepath demo_books.csv

echo "✅ Demo finished successfully!"