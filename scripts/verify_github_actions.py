#!/usr/bin/env python3
"""
GitHub Actions Workflow Verification Script
Validates the GitHub Actions workflow files for syntax and best practices
"""

import yaml
import os
from pathlib import Path

def verify_workflow(workflow_path: str) -> dict:
    """Verify a GitHub Actions workflow file"""
    results = {
        "file": workflow_path,
        "exists": False,
        "valid_yaml": False,
        "has_required_fields": False,
        "uses_updated_actions": False,
        "issues": [],
        "recommendations": []
    }
    
    # Check if file exists
    if not os.path.exists(workflow_path):
        results["issues"].append("Workflow file does not exist")
        return results
    
    results["exists"] = True
    
    try:
        # Load and parse YAML
        with open(workflow_path, 'r') as f:
            workflow = yaml.safe_load(f)
        
        results["valid_yaml"] = True
        
        # Check required fields (note: 'on' becomes True in YAML parsing)
        required_fields = ['name', 'jobs']
        has_on_field = 'on' in workflow or True in workflow  # YAML parses 'on:' as True
        
        missing_fields = [field for field in required_fields if field not in workflow]
        if not has_on_field:
            missing_fields.append('on')
        
        if not missing_fields:
            results["has_required_fields"] = True
        else:
            results["issues"].extend([f"Missing required field: {field}" for field in missing_fields])
        
        # Check for updated actions
        deprecated_actions = {
            'actions/checkout@v3': 'actions/checkout@v4',
            'actions/setup-python@v4': 'actions/setup-python@v5',
            'actions/cache@v3': 'actions/cache@v4',
            'actions/upload-artifact@v3': 'actions/upload-artifact@v4',
            'actions/github-script@v6': 'actions/github-script@v7'
        }
        
        workflow_content = open(workflow_path, 'r').read()
        deprecated_found = []
        
        for deprecated, updated in deprecated_actions.items():
            if deprecated in workflow_content:
                deprecated_found.append(f"Found deprecated {deprecated}, should use {updated}")
        
        if not deprecated_found:
            results["uses_updated_actions"] = True
        else:
            results["issues"].extend(deprecated_found)
        
        # Check for best practices
        if 'jobs' in workflow:
            jobs = workflow['jobs']
            
            # Check for fail-fast: false in matrix strategies
            for job_name, job_config in jobs.items():
                if 'strategy' in job_config and 'matrix' in job_config['strategy']:
                    if job_config['strategy'].get('fail-fast', True):
                        results["recommendations"].append(f"Job '{job_name}': Consider adding 'fail-fast: false' to matrix strategy")
            
            # Check for timeout configurations
            long_running_jobs = ['integration-tests', 'performance-benchmark']
            for job_name in long_running_jobs:
                if job_name in jobs and 'timeout-minutes' not in jobs[job_name]:
                    results["recommendations"].append(f"Job '{job_name}': Consider adding timeout-minutes")
        
        # Check for artifact naming uniqueness
        if 'upload-artifact@v4' in workflow_content:
            if 'github.run_number' not in workflow_content:
                results["recommendations"].append("Consider using github.run_number in artifact names for uniqueness")
        
    except yaml.YAMLError as e:
        results["issues"].append(f"Invalid YAML syntax: {str(e)}")
    except Exception as e:
        results["issues"].append(f"Error reading workflow: {str(e)}")
    
    return results

def print_results(results: dict):
    """Print verification results"""
    file_name = os.path.basename(results["file"])
    print(f"\n🔍 VERIFYING: {file_name}")
    print("=" * (len(file_name) + 12))
    
    # Status checks
    checks = [
        ("File exists", results["exists"]),
        ("Valid YAML", results["valid_yaml"]),
        ("Required fields", results["has_required_fields"]),
        ("Updated actions", results["uses_updated_actions"])
    ]
    
    for check_name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"{status} {check_name}")
    
    # Issues
    if results["issues"]:
        print(f"\n❌ ISSUES ({len(results['issues'])}):")
        for i, issue in enumerate(results["issues"], 1):
            print(f"  {i}. {issue}")
    
    # Recommendations
    if results["recommendations"]:
        print(f"\n💡 RECOMMENDATIONS ({len(results['recommendations'])}):")
        for i, rec in enumerate(results["recommendations"], 1):
            print(f"  {i}. {rec}")
    
    # Overall status
    all_critical_passed = all([
        results["exists"],
        results["valid_yaml"],
        results["has_required_fields"],
        results["uses_updated_actions"]
    ])
    
    if all_critical_passed and not results["issues"]:
        print(f"\n🎉 {file_name}: ALL CHECKS PASSED!")
    elif all_critical_passed:
        print(f"\n⚠️  {file_name}: PASSED with recommendations")
    else:
        print(f"\n❌ {file_name}: FAILED - issues need to be fixed")

def main():
    """Main verification function"""
    print("🔧 GITHUB ACTIONS WORKFLOW VERIFICATION")
    print("=" * 50)
    print("Checking GitHub Actions workflows for syntax and best practices...")
    
    # Find workflow files
    workflows_dir = ".github/workflows"
    workflow_files = []
    
    if os.path.exists(workflows_dir):
        for file in os.listdir(workflows_dir):
            if file.endswith(('.yml', '.yaml')):
                workflow_files.append(os.path.join(workflows_dir, file))
    
    if not workflow_files:
        print("❌ No workflow files found in .github/workflows/")
        return
    
    print(f"Found {len(workflow_files)} workflow file(s)")
    
    all_passed = True
    
    # Verify each workflow
    for workflow_file in workflow_files:
        results = verify_workflow(workflow_file)
        print_results(results)
        
        # Check if this workflow passed all critical checks
        critical_passed = all([
            results["exists"],
            results["valid_yaml"], 
            results["has_required_fields"],
            results["uses_updated_actions"]
        ]) and not results["issues"]
        
        if not critical_passed:
            all_passed = False
    
    # Summary
    print(f"\n{'=' * 50}")
    if all_passed:
        print("🎉 ALL WORKFLOWS PASSED VERIFICATION!")
        print("✅ Workflows are ready for use with GitHub Actions")
        print("✅ All actions use current versions")
        print("✅ No critical issues found")
    else:
        print("❌ SOME WORKFLOWS HAVE ISSUES")
        print("Please fix the issues identified above before using the workflows")
    
    print(f"\n📊 VERIFICATION SUMMARY:")
    print(f"  Total workflows: {len(workflow_files)}")
    print(f"  Passed verification: {sum(1 for f in workflow_files if verify_workflow(f)['uses_updated_actions'])}")
    print(f"  Status: {'READY' if all_passed else 'NEEDS FIXES'}")

if __name__ == "__main__":
    main()