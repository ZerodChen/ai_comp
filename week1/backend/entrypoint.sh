#!/bin/sh

# Let the DB start
echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Run migrations
echo "Running migrations..."

# Ensure versions directory exists
mkdir -p alembic/versions

# Check if migration file exists (look for .py files), if not, generate it
if [ -z "$(find alembic/versions -maxdepth 1 -name '*.py' -print -quit)" ]; then
   echo "No migrations found, generating initial migration..."
   alembic revision --autogenerate -m "Initial migration"
fi
alembic upgrade head

# Start app
echo "Starting app..."
exec "$@"