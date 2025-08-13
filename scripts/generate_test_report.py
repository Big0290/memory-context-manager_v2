#!/usr/bin/env python3
"""
Generate GitHub Actions test report from integration test results.
This script creates markdown summaries for CI/CD pipeline reporting.
"""

import json
import glob
import os
import sys
from datetime import datetime

def generate_test_report():
    """Generate test report from latest results file."""
    try:
        # Find latest test results file
        result_files = glob.glob('test_results_*.json')
        if not result_files:
            print('⚠️ No test results file found')
            return False
            
        latest_file = max(result_files, key=os.path.getctime)
        print(f'📄 Latest test results: {latest_file}')
        
        with open(latest_file, 'r') as f:
            results = json.load(f)
        
        summary = results.get('summary', {})
        print(f'📈 Test Summary:')
        print(f'  Overall Status: {summary.get("overall_status", "UNKNOWN")}')
        print(f'  Grade: {summary.get("grade", "N/A")}')
        print(f'  Success Rate: {summary.get("success_rate", 0):.1%}')
        print(f'  Tests Passed: {summary.get("tests_passed", 0)}/{summary.get("total_tests", 0)}')
        
        # Create GitHub Actions summary
        with open('integration_test_summary.md', 'w') as f:
            f.write('# Memory Context Manager v2 - Integration Test Results\\n\\n')
            f.write(f'## Overall Status: {summary.get("overall_status", "UNKNOWN")}\\n')
            f.write(f'**Grade:** {summary.get("grade", "N/A")}\\n\\n')
            f.write(f'**Success Rate:** {summary.get("success_rate", 0):.1%}\\n\\n')
            f.write(f'**Tests Passed:** {summary.get("tests_passed", 0)}/{summary.get("total_tests", 0)}\\n\\n')
            
            f.write('## Test Categories\\n\\n')
            for category in results.get('test_categories', []):
                status = '✅' if category.get('passed') else '❌'
                f.write(f'{status} **{category.get("category", "Unknown")}**: {category.get("passed_tests", 0)}/{category.get("total_tests", 0)} passed\\n')
            
            f.write(f'\\n## Test Duration\\n{results.get("total_duration", 0):.2f} seconds\\n')
        
        return True
        
    except Exception as e:
        print(f'❌ Report generation failed: {str(e)}')
        return False

if __name__ == "__main__":
    success = generate_test_report()
    sys.exit(0 if success else 1)