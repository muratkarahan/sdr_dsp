#!/usr/bin/env python3
"""
Test script for traffic monitoring tools.
This script performs basic validation without requiring a real GitHub token.
"""

import sys
import os
import importlib.util


def test_script_imports():
    """Test that the scripts can be imported without errors."""
    print("Testing script imports...")
    
    # Test fetch_all_repos_traffic.py
    spec = importlib.util.spec_from_file_location(
        "fetch_all_repos_traffic",
        "fetch_all_repos_traffic.py"
    )
    module = importlib.util.module_from_spec(spec)
    
    try:
        spec.loader.exec_module(module)
        print("✅ fetch_all_repos_traffic.py imports successfully")
    except Exception as e:
        print(f"❌ fetch_all_repos_traffic.py import failed: {e}")
        return False
    
    # Test .github/scripts/fetch_traffic.py
    spec = importlib.util.spec_from_file_location(
        "fetch_traffic",
        ".github/scripts/fetch_traffic.py"
    )
    module = importlib.util.module_from_spec(spec)
    
    try:
        spec.loader.exec_module(module)
        print("✅ .github/scripts/fetch_traffic.py imports successfully")
    except Exception as e:
        print(f"❌ .github/scripts/fetch_traffic.py import failed: {e}")
        return False
    
    return True


def test_workflow_exists():
    """Test that the workflow file exists and is valid YAML."""
    print("\nTesting workflow file...")
    
    workflow_path = ".github/workflows/traffic-monitor.yml"
    if not os.path.exists(workflow_path):
        print(f"❌ Workflow file not found: {workflow_path}")
        return False
    
    print(f"✅ Workflow file exists: {workflow_path}")
    
    try:
        import yaml
        with open(workflow_path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Check basic structure
        if 'name' not in data:
            print("❌ Workflow missing 'name' field")
            return False
        
        if 'jobs' not in data:
            print("❌ Workflow missing 'jobs' field")
            return False
        
        print(f"✅ Workflow is valid YAML with name: {data['name']}")
        return True
    except ImportError:
        print("⚠️  pyyaml not installed, skipping YAML validation")
        return True
    except Exception as e:
        print(f"❌ Workflow YAML validation failed: {e}")
        return False


def test_documentation_exists():
    """Test that documentation files exist."""
    print("\nTesting documentation...")
    
    docs = [
        "README.md",
        "TRAFFIC_MONITORING_GUIDE.md",
        "requirements.txt"
    ]
    
    all_exist = True
    for doc in docs:
        if os.path.exists(doc):
            print(f"✅ {doc} exists")
        else:
            print(f"❌ {doc} not found")
            all_exist = False
    
    return all_exist


def test_gitignore():
    """Test that .gitignore exists and contains necessary entries."""
    print("\nTesting .gitignore...")
    
    if not os.path.exists(".gitignore"):
        print("❌ .gitignore not found")
        return False
    
    with open(".gitignore", 'r') as f:
        content = f.read()
    
    required_entries = [
        "__pycache__",
        "*.py[cod]",
        "traffic_summary.txt",
        "traffic_data.json"
    ]
    
    all_found = True
    for entry in required_entries:
        if entry in content:
            print(f"✅ .gitignore contains: {entry}")
        else:
            print(f"❌ .gitignore missing: {entry}")
            all_found = False
    
    return all_found


def main():
    """Run all tests."""
    print("=" * 70)
    print("Traffic Monitoring Tools - Test Suite")
    print("=" * 70)
    
    tests = [
        test_script_imports,
        test_workflow_exists,
        test_documentation_exists,
        test_gitignore
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} raised an exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 70)
    passed = sum(results)
    total = len(results)
    
    if all(results):
        print(f"✅ All tests passed! ({passed}/{total})")
        return 0
    else:
        print(f"❌ Some tests failed. ({passed}/{total} passed)")
        return 1


if __name__ == '__main__':
    sys.exit(main())
