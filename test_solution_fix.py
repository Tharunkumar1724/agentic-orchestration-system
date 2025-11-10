"""
Test script to verify solution functionality
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_create_solution():
    """Test creating a solution"""
    print("🧪 Testing Solution Creation...")
    
    solution_data = {
        "id": "test_solution_001",
        "name": "Test Solution",
        "description": "A test solution to verify functionality",
        "workflows": ["retest"],  # Using existing workflow
        "communication_config": {},
        "metadata": {"test": True}
    }
    
    try:
        # Delete if exists
        requests.delete(f"{BASE_URL}/solutions/test_solution_001")
        time.sleep(0.5)
        
        # Create solution
        response = requests.post(f"{BASE_URL}/solutions/", json=solution_data)
        print(f"Create Response Status: {response.status_code}")
        print(f"Create Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Solution created successfully!")
            return True
        else:
            print(f"❌ Failed to create solution: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_get_solution():
    """Test getting a solution"""
    print("\n🧪 Testing Get Solution...")
    
    try:
        response = requests.get(f"{BASE_URL}/solutions/test_solution_001")
        print(f"Get Response Status: {response.status_code}")
        print(f"Get Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Solution retrieved successfully!")
            return True
        else:
            print(f"❌ Failed to get solution: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_list_solutions():
    """Test listing all solutions"""
    print("\n🧪 Testing List Solutions...")
    
    try:
        response = requests.get(f"{BASE_URL}/solutions/")
        print(f"List Response Status: {response.status_code}")
        
        if response.status_code == 200:
            solutions = response.json()
            print(f"Found {len(solutions)} solution(s)")
            for sol in solutions:
                print(f"  - {sol.get('id')}: {sol.get('name')}")
            print("✅ Solutions listed successfully!")
            return True
        else:
            print(f"❌ Failed to list solutions: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_get_solution_workflows():
    """Test getting workflows in a solution"""
    print("\n🧪 Testing Get Solution Workflows...")
    
    try:
        response = requests.get(f"{BASE_URL}/solutions/test_solution_001/workflows")
        print(f"Get Workflows Response Status: {response.status_code}")
        
        if response.status_code == 200:
            workflows = response.json()
            print(f"Found {len(workflows)} workflow(s)")
            for wf in workflows:
                print(f"  - {wf.get('id')}: {wf.get('name')}")
            print("✅ Solution workflows retrieved successfully!")
            return True
        else:
            print(f"❌ Failed to get workflows: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    print("=" * 60)
    print("SOLUTION FUNCTIONALITY TEST")
    print("=" * 60)
    
    results = []
    
    # Test 1: Create solution
    results.append(("Create Solution", test_create_solution()))
    
    # Test 2: Get solution
    results.append(("Get Solution", test_get_solution()))
    
    # Test 3: List solutions
    results.append(("List Solutions", test_list_solutions()))
    
    # Test 4: Get solution workflows
    results.append(("Get Solution Workflows", test_get_solution_workflows()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    total_passed = sum(1 for _, r in results if r)
    print(f"\nTotal: {total_passed}/{len(results)} tests passed")
    
    return all(r for _, r in results)


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
