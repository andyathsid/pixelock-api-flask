import requests
import json

BASE_URL = 'http://127.0.0.1:5000/api'

# def test_encode():
#     """Test the encode endpoint with various configurations"""
    
#     # Test data
#     test_cases = [
#         {
#             "name": "Basic encode with defaults",
#             "data": {
#                 "image_url": "https://github.com/andyathsid/pixelock-api-flask/blob/main/data/raw/capybara.jpg?raw=true",
#                 "message": "Hello, World!"
#             }
#         },
#         {
#             "name": "Encode with custom parameters",
#             "data": {
#                 "image_url": "https://github.com/andyathsid/pixelock-api-flask/blob/main/data/raw/capybara.jpg?raw=true",
#                 "message": "Hello, World!",
#                 "key": 7,
#                 "alphabet": "abcdefghijklmnopqrstuvwxyz",
#                 "case_strategy": "maintain",
#                 "ignore_foreign": False
#             }
#         },
#         {
#             "name": "Encode with strict case",
#             "data": {
#                 "image_url": "https://github.com/andyathsid/pixelock-api-flask/blob/main/data/raw/capybara.jpg?raw=true",
#                 "message": "Hello, World!",
#                 "case_strategy": "strict"
#             }
#         }
#     ]

#     for test in test_cases:
#         print(f"\nRunning test: {test['name']}")
#         try:
#             response = requests.post(f"{BASE_URL}/encode", json=test['data'])
#             print(f"Status Code: {response.status_code}")
#             print("Response:", json.dumps(response.json(), indent=2))
#         except Exception as e:
#             print(f"Error: {str(e)}")

# def test_decode(encoded_image_url):
#     """Test the decode endpoint with various configurations"""
    
#     test_cases = [
#         {
#             "name": "Basic decode with defaults",
#             "data": {
#                 "image_url": encoded_image_url
#             }
#         },
#         {
#             "name": "Decode with custom parameters",
#             "data": {
#                 "image_url": encoded_image_url,
#                 "alphabet": "abcdefghijklmnopqrstuvwxyz",
#                 "case_strategy": "maintain",
#                 "ignore_foreign": False
#             }
#         },
#         {
#             "name": "Decode with strict case",
#             "data": {
#                 "image_url": encoded_image_url,
#                 "case_strategy": "strict"
#             }
#         }
#     ]

#     for test in test_cases:
#         print(f"\nRunning test: {test['name']}")
#         try:
#             response = requests.post(f"{BASE_URL}/decode", json=test['data'])
#             print(f"Status Code: {response.status_code}")
#             print("Response:", json.dumps(response.json(), indent=2))
#         except Exception as e:
#             print(f"Error: {str(e)}")

def run_full_test():
    """Run a complete encode-decode cycle test"""
    print("=== Starting Encode-Decode Cycle Test ===")
    
    # First encode test
    encode_data = {
        "image_url": "https://github.com/andyathsid/pixelock-api-flask/blob/main/data/raw/capybara.jpg?raw=true",
        "message": "This is a test message!",
        "alphabet": "`,.pyfgcrl/=\aoeuidhtns-;qjkxbmwvz",
        "key": 7,
        "case_strategy": "maintain",
        "ignore_foreign": False
    }
    
    print("\nTesting Encode:")
    try:
        encode_response = requests.post(f"{BASE_URL}/encode", json=encode_data)
        encode_result = encode_response.json()
        print("Encode Status:", encode_response.status_code)
        print("Encode Response:", json.dumps(encode_result, indent=2))
        
        if encode_response.status_code == 200:
            # Use the encoded image URL for decode test
            print("\nTesting Decode:")
            decode_data = {
                "image_url": encode_result['image_url'],
                "case_strategy": "maintain",
                "ignore_foreign": False
            }
            
            decode_response = requests.post(f"{BASE_URL}/decode", json=decode_data)
            print("Decode Status:", decode_response.status_code)
            print("Decode Response:", json.dumps(decode_response.json(), indent=2))
            
    except Exception as e:
        print(f"Error during test: {str(e)}")

if __name__ == "__main__":
    # Uncomment the test you want to run
    
    # Run individual encode tests
    # test_encode()
    
    # Run individual decode tests (replace with actual encoded image URL)
    # test_decode("http://127.0.0.1:5000/static/uploads/your_encoded_image.png")
    
    # Run full encode-decode cycle test
    run_full_test()