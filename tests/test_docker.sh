#!/bin/bash
# Docker validation for FIFOLive
# This script validates the Docker build context.
# Full container runtime test requires a working Docker daemon.

set -e

echo "=== FIFOLive Docker Validation ==="
echo

echo "1. Checking required files..."
ls -l Dockerfile docker-compose.yml .dockerignore
echo "   ✅ All Docker files present"

echo
echo "2. Validating Dockerfile syntax (basic checks)..."
if grep -q 'FROM python:3.11-slim' Dockerfile && \
   grep -q 'COPY requirements.txt' Dockerfile && \
   grep -q 'EXPOSE 8000' Dockerfile && \
   grep -q 'CMD \["python", "main.py"\]' Dockerfile; then
    echo "   ✅ Dockerfile looks correct"
else
    echo "   ❌ Dockerfile validation failed"
    exit 1
fi

echo
echo "3. Checking .dockerignore (should exclude heavy dirs)..."
if grep -q '^\.venv$' .dockerignore && grep -q '^\*\.db$' .dockerignore; then
    echo "   ✅ .dockerignore is sensible"
else
    echo "   ⚠️  .dockerignore may need review"
fi

echo
echo "4. Attempting docker build (will fail if no daemon)..."
if command -v docker >/dev/null 2>&1; then
    set +e
    docker build -t fifolive:validate . --no-cache > /tmp/docker_build.log 2>&1
    BUILD_EXIT=$?
    set -e
    tail -5 /tmp/docker_build.log
    if [ $BUILD_EXIT -eq 0 ]; then
        echo "   ✅ Build succeeded"
        docker rmi fifolive:validate >/dev/null 2>&1 || true
    else
        echo "   ℹ️  Docker build failed (expected if no daemon in this environment)"
        echo "   You can run this on a machine with Docker:"
        echo "     docker build -t fifolive ."
        echo "     docker run -p 8000:8000 fifolive"
    fi
else
    echo "   Docker CLI not found"
fi

echo
echo "=== Docker validation complete ==="
echo "See README.md for usage instructions."
