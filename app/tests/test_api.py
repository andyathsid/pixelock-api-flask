import requests
import json

BASE_URL = 'http://13.250.38.115:5000/api'

def run_full_test():
    """Run a complete encode-decode cycle test"""
    print("=== Starting Encode-Decode Cycle Test ===")
    
    # First encode test
    encode_data = {
        "image_url": "https://github.com/andyathsid/pixelock-api-flask/blob/main/data/raw/capybara.jpg?raw=true",
        "message": "pneumonoultramicroscopicsilicovolcanoconiosis",
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
                "alphabet": "`,.pyfgcrl/=\aoeuidhtns-;qjkxbmwvz",
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