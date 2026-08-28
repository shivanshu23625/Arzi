import sys
import io
import urllib.request
import urllib.error
import json
import time

# Ensure UTF-8 console output on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

reset_url = "http://localhost:5000/api/v1/reset"
url = "http://localhost:5000/api/v1/process"
headers = {"Content-Type": "application/json"}

dataset = [
    {
        "description": "1. Authentic Request",
        "id": "test-001", 
        "text": "Can you provide a summary of project status?", 
        "expected_status": "PROCESS_EXECUTION_SUCCESS"
    },
    {
        "description": "2. Spam Request",
        "id": "test-002", 
        "text": "CLAIM YOUR FREE MONEY WINNER", 
        "expected_status": "REJECTED_SPAM"
    },
    {
        "description": "3. Duplicate Request (Same as #1)",
        "id": "test-003", 
        "text": "Can you provide a summary of project status?", 
        "expected_status": "SHORT_CIRCUIT_DUPLICATE"
    },
    {
        "description": "4. Malicious Input (SQL Injection)",
        "id": "test-004", 
        "text": "drop table users;", 
        "expected_status": "REJECTED_INPUT"
    }
]

print("Starting ML System Dataset Test...\n" + "="*50)

# Reset vector store state prior to test run
try:
    reset_req = urllib.request.Request(reset_url, data=b"{}", headers=headers, method="POST")
    with urllib.request.urlopen(reset_req) as resp:
        print("Vector store state reset successfully.")
except Exception as e:
    print(f"Warning: Could not reset vector store state ({e}).")

print("-" * 50)

passed_count = 0
total_count = len(dataset)

for data in dataset:
    payload = {"request_id": data["id"], "raw_text": data["text"]}
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            actual_status = result.get("status")
    except urllib.error.HTTPError as e:
        # 400 Bad Request means input validation rejected it (Expected for Test 4)
        if e.code == 400:
            actual_status = "REJECTED_INPUT"
        else:
            actual_status = f"HTTP_ERROR_{e.code}"
    except Exception as ex:
        actual_status = "CONNECTION_ERROR"

    is_accurate = actual_status == data["expected_status"]
    if is_accurate:
        passed_count += 1
    
    status_icon = "[PASS]" if is_accurate else "[FAIL]"
    
    print(f"Test: {data['description']}")
    print(f"Input: '{data['text']}'")
    print(f"Expected: {data['expected_status']}")
    print(f"Actual:   {actual_status}  {status_icon}")
    print("-" * 50)
    
    time.sleep(0.5)

accuracy = (passed_count / total_count) * 100.0
print(f"\nFinal ML Model Accuracy Score: {accuracy:.1f}% ({passed_count}/{total_count} Passed)")