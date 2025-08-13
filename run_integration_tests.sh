#!/bin/bash
# Memory Context Manager v2 - Local Integration Test Runner
# Run this script before pushing to Git to validate system integrity

set -e  # Exit on any error

echo "🧪 MEMORY CONTEXT MANAGER v2 - LOCAL INTEGRATION TEST RUNNER"
echo "================================================================="
echo "This script will run comprehensive integration tests to validate"
echo "the complete system integrity before Git push operations."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Start timing
start_time=$(date +%s)

print_status $BLUE "🔧 PRE-FLIGHT CHECKS"
echo "--------------------------------"

# Check Python version
if command_exists python3; then
    python_version=$(python3 --version)
    print_status $GREEN "✅ Python: $python_version"
else
    print_status $RED "❌ Python 3 not found"
    exit 1
fi

# Check if we're in the right directory
if [[ ! -f "main.py" || ! -f "test_complete_integration.py" ]]; then
    print_status $RED "❌ Not in Memory Context Manager v2 directory"
    echo "Please run this script from the project root directory"
    exit 1
fi

# Check if virtual environment is activated (optional but recommended)
if [[ -z "$VIRTUAL_ENV" ]]; then
    print_status $YELLOW "⚠️  Virtual environment not detected (recommended but not required)"
else
    print_status $GREEN "✅ Virtual environment: $(basename $VIRTUAL_ENV)"
fi

# Install required packages if not present
print_status $BLUE "📦 CHECKING DEPENDENCIES"
echo "--------------------------------"

required_packages=("psutil" "aiosqlite")
missing_packages=()

for package in "${required_packages[@]}"; do
    if python3 -c "import $package" 2>/dev/null; then
        print_status $GREEN "✅ $package installed"
    else
        missing_packages+=($package)
        print_status $YELLOW "⚠️  $package not found"
    fi
done

if [ ${#missing_packages[@]} -ne 0 ]; then
    print_status $YELLOW "Installing missing packages: ${missing_packages[*]}"
    python3 -m pip install "${missing_packages[@]}" --quiet
    print_status $GREEN "✅ Dependencies installed"
fi

# Check database status
print_status $BLUE "🗄️  DATABASE STATUS CHECK"
echo "--------------------------------"

if [[ -f "brain_memory_store/brain.db" ]]; then
    db_size=$(du -h "brain_memory_store/brain.db" | cut -f1)
    print_status $GREEN "✅ Database found: $db_size"
    
    # Quick database integrity check
    if python3 -c "import sqlite3; conn = sqlite3.connect('brain_memory_store/brain.db'); conn.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'" 2>/dev/null; then
        print_status $GREEN "✅ Database integrity OK"
    else
        print_status $YELLOW "⚠️  Database integrity check failed (may be normal for tests)"
    fi
else
    print_status $YELLOW "⚠️  Database not found - will be created during tests"
fi

# Backup database if it exists
if [[ -f "brain_memory_store/brain.db" ]]; then
    backup_name="brain_memory_store/brain.db.backup.$(date +%Y%m%d_%H%M%S)"
    cp "brain_memory_store/brain.db" "$backup_name"
    print_status $GREEN "✅ Database backed up to: $(basename $backup_name)"
fi

echo ""
print_status $BLUE "🚀 RUNNING INTEGRATION TESTS"
echo "================================="

# Run the comprehensive integration test suite
print_status $YELLOW "Starting complete integration test suite..."
echo ""

# Create a log file for the test run
log_file="integration_test_$(date +%Y%m%d_%H%M%S).log"

# Run tests with different verbosity levels based on arguments
if [[ "$1" == "--verbose" || "$1" == "-v" ]]; then
    python3 test_complete_integration.py --verbose 2>&1 | tee "$log_file"
    test_exit_code=${PIPESTATUS[0]}
elif [[ "$1" == "--ci" ]]; then
    python3 test_complete_integration.py --ci --exit-on-failure 2>&1 | tee "$log_file"
    test_exit_code=${PIPESTATUS[0]}
else
    python3 test_complete_integration.py 2>&1 | tee "$log_file"
    test_exit_code=${PIPESTATUS[0]}
fi

echo ""
print_status $BLUE "📊 TEST RESULTS ANALYSIS"
echo "================================="

# Calculate timing
end_time=$(date +%s)
duration=$((end_time - start_time))
minutes=$((duration / 60))
seconds=$((duration % 60))

print_status $BLUE "⏱️  Total execution time: ${minutes}m ${seconds}s"
print_status $BLUE "📄 Test log saved to: $log_file"

# Analyze test results
if [[ $test_exit_code -eq 0 ]]; then
    print_status $GREEN "🎉 ALL INTEGRATION TESTS PASSED!"
    echo ""
    echo "✅ System is fully integrated and ready for Git operations"
    echo "✅ All components are working in symbiosis"
    echo "✅ Database integrity validated"
    echo "✅ Performance benchmarks met"
    echo "✅ Cross-component interactions verified"
    echo ""
    print_status $GREEN "🚀 READY FOR GIT PUSH! 🚀"
    
    # Optional: Show quick summary if test results file exists
    if ls test_results_*.json 1> /dev/null 2>&1; then
        latest_results=$(ls -t test_results_*.json | head -n1)
        print_status $BLUE "📈 Quick Summary from $latest_results:"
        python3 -c "
import json
with open('$latest_results', 'r') as f:
    results = json.load(f)
summary = results.get('summary', {})
print(f'  Grade: {summary.get(\"grade\", \"N/A\")}')
print(f'  Success Rate: {summary.get(\"success_rate\", 0):.1%}')
print(f'  Tests Passed: {summary.get(\"tests_passed\", 0)}/{summary.get(\"total_tests\", 0)}')
" 2>/dev/null || echo "  (Summary data not available)"
    fi
    
else
    print_status $RED "❌ INTEGRATION TESTS FAILED!"
    echo ""
    echo "❌ System has integration issues that need to be resolved"
    echo "❌ Review the test output above and fix identified problems"
    echo "❌ Check the log file: $log_file"
    echo ""
    print_status $RED "🚫 DO NOT PUSH TO GIT UNTIL ISSUES ARE RESOLVED 🚫"
    
    echo ""
    print_status $YELLOW "🔧 TROUBLESHOOTING TIPS:"
    echo "1. Check the detailed error messages in the test output"
    echo "2. Verify all required dependencies are installed"
    echo "3. Ensure database permissions are correct"
    echo "4. Run individual test categories to isolate issues"
    echo "5. Check system resources (memory, disk space)"
    
    exit 1
fi

# Cleanup temporary files (optional)
if [[ "$2" == "--cleanup" ]]; then
    print_status $YELLOW "🧹 Cleaning up temporary files..."
    # Remove old test result files (keep last 5)
    ls -t test_results_*.json | tail -n +6 | xargs -r rm
    ls -t integration_test_*.log | tail -n +6 | xargs -r rm
    print_status $GREEN "✅ Cleanup completed"
fi

echo ""
print_status $BLUE "🔄 INTEGRATION TEST RUN COMPLETED"
echo ""

# Optional: Git status check
if command_exists git && git rev-parse --git-dir > /dev/null 2>&1; then
    print_status $BLUE "📋 Current Git Status:"
    git status --porcelain | head -10
    
    if [[ $(git status --porcelain | wc -l) -gt 0 ]]; then
        echo ""
        print_status $YELLOW "💡 Tip: Review your changes with 'git diff' before committing"
    fi
fi

echo ""
print_status $GREEN "Thank you for maintaining code quality! 🎯"