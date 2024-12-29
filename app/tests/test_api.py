import requests
import json
import os
from typing import Dict, Any
from pathlib import Path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app.utils.colors import green, red, blue

# Test Configuration
BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000/api')
TEST_DATA = {
    "message": "This is a test message!",
    "alphabet": "`,.pyfgcrl/=\\aoeuidhtns-;qjkxbmwvz",
    "key": 7
}

TEST_CASES = [
    {"case_strategy": "strict", "ignore_foreign": False, "expected_message": "This is a test message!"},
    {"case_strategy": "maintain", "ignore_foreign": False, "expected_message": "This is a test message!"},
    {"case_strategy": "ignore", "ignore_foreign": False, "expected_message": "this is a test message!"},
    {"case_strategy": "strict", "ignore_foreign": True, "expected_message": "thisisatestmessage"},
]

# Test image path
TEST_IMAGE_PATH = Path(__file__).parent.parent.parent / 'data' / 'raw' / 'capybara.jpg'

def validate_encode_response(response: requests.Response) -> Dict[str, Any]:
    """Validates encode response and returns the result"""
    if response.status_code != 200:
        raise ValueError(f"Encode failed with status {response.status_code}: {response.text}")
    
    result = response.json()
    required_fields = ['image_url', 'encrypted_message', 'shifted_alphabet']
    
    if not all(field in result for field in required_fields):
        raise ValueError(f"Missing required fields in response: {result}")
        
    return result

def validate_decode_response(response: requests.Response, expected_message: str) -> None:
    """Validates decode response against expected message"""
    if response.status_code != 200:
        raise ValueError(f"Decode failed with status {response.status_code}: {response.text}")
    
    result = response.json()
    if result.get('decrypted_message') != expected_message:
        raise ValueError(f"Decoded message doesn't match expected:\nExpected: {expected_message}\nGot: {result.get('decrypted_message')}")

def test_single_case(case_config: Dict[str, Any]) -> bool:
    """Tests a single encode-decode cycle with given configuration"""
    print(f"\n=== Testing with config: {case_config} ===")
    
    # Prepare encode data
    encode_data = TEST_DATA.copy()
    encode_data.update(case_config)
    
    try:
        # Test encode with file upload
        print("\nEncoding...")
        with open(TEST_IMAGE_PATH, 'rb') as img:
            files = {
                'image': ('test.jpg', img, 'image/jpeg'),
                'data': (None, json.dumps(encode_data), 'application/json')
            }
            encode_response = requests.post(f"{BASE_URL}/encrypt/internal-key", files=files)
        
        encode_result = validate_encode_response(encode_response)
        print(f"{green('Encode successful')}")
        
        # Download the encoded image for decode test
        print("\nDownloading encoded image...")
        encoded_image_response = requests.get(encode_result['image_url'])
        if encoded_image_response.status_code != 200:
            raise ValueError("Failed to download encoded image")
        
        # Test decode with file upload
        print("\nDecoding...")
        decode_data = {
            "alphabet": TEST_DATA['alphabet'],
            "case_strategy": case_config['case_strategy'],
            "ignore_foreign": case_config['ignore_foreign']
        }
        
        files = {
            'image': ('encoded.png', encoded_image_response.content, 'image/png'),
            'data': (None, json.dumps(decode_data), 'application/json')
        }
        decode_response = requests.post(f"{BASE_URL}/decrypt/internal-key", files=files)
        validate_decode_response(decode_response, case_config['expected_message'])
        print(f"{green('Decode successful')}")
        
    except Exception as e:
        print(f"{red('❌ Test failed:')} {str(e)}")
        return False
    
    print(f"{green('✅ Test passed')}")
    return True

def test_external_key_case(case_config: Dict[str, Any]) -> bool:
    """Tests encode-decode cycle using external key endpoints"""
    print(f"\n=== Testing External Key with config: {case_config} ===")
    
    # Prepare encode data
    encode_data = TEST_DATA.copy()
    encode_data.update(case_config)
    
    try:
        # Test encode with file upload
        print("\nEncoding with external key...")
        with open(TEST_IMAGE_PATH, 'rb') as img:
            files = {
                'image': ('test.jpg', img, 'image/jpeg'),
                'data': (None, json.dumps(encode_data), 'application/json')
            }
            encode_response = requests.post(f"{BASE_URL}/encrypt/external-key", files=files)
        
        encode_result = validate_encode_response(encode_response)
        print(f"{green('Encode successful')}")
        
        # Download the encoded image for decode test
        print("\nDownloading encoded image...")
        encoded_image_response = requests.get(encode_result['image_url'])
        if encoded_image_response.status_code != 200:
            raise ValueError("Failed to download encoded image")
        
        # Test decode with file upload and external key
        print("\nDecoding with external key...")
        decode_data = {
            "alphabet": TEST_DATA['alphabet'],
            "key": TEST_DATA['key'],  # External key required
            "case_strategy": case_config['case_strategy'],
            "ignore_foreign": case_config['ignore_foreign']
        }
        
        files = {
            'image': ('encoded.png', encoded_image_response.content, 'image/png'),
            'data': (None, json.dumps(decode_data), 'application/json')
        }
        decode_response = requests.post(f"{BASE_URL}/decrypt/external-key", files=files)
        validate_decode_response(decode_response, case_config['expected_message'])
        print(f"{green('Decode successful')}")
        
    except Exception as e:
        print(f"{red('❌ Test failed:')} {str(e)}")
        return False
    
    print(f"{green('✅ Test passed')}")
    return True

def run_all_tests() -> None:
    """Runs all test cases"""
    print("=== Starting Full Test Suite ===")
    
    if not TEST_IMAGE_PATH.exists():
        print(f"{red('❌ Test image not found at')} {TEST_IMAGE_PATH}")
        return
    
    results = []
    
    # Run standard tests
    print(f"\n{blue('Running Internal Key Encryption Tests...')}")
    for case in TEST_CASES:
        results.append(test_single_case(case))
    
    # Run external key tests
    print(f"\n{blue('Running External Key Encryption Tests...')}")
    for case in TEST_CASES:
        results.append(test_external_key_case(case))
    
    # Summary
    total = len(results)
    passed = sum(results)
    print(f"\n{blue('=== Test Summary ===')}") 
    print(f"{blue('Total:')} {total}")
    print(f"{green('Passed:')} {passed}")
    print(f"{red('Failed:')} {total - passed}")
    
if __name__ == "__main__":
    run_all_tests()