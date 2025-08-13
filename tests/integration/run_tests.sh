#!/bin/bash
# GitHub Actions Integration Test Runner
set -e

echo "🧪 Running Memory Context Manager v2 Integration Tests"
echo "======================================================="

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:../.."
export TEST_ENVIRONMENT="github_actions"

# Navigate to project root
cd ../..

# Create test database directory
mkdir -p brain_memory_store

# Run integration tests
python3 tests/integration/test_complete_integration.py --ci --verbose

echo "✅ Integration tests completed"
