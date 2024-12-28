# Pixelock API

## Overview

This project is a Flask application that provides an API for encoding and decoding hidden messages in images using steganography and cryptography techniques. This is developed as part of my university Cybersecurity course project and is part of a system that includes a [Flutter Android app](https://github.com/Wilimaxs/KriptoApp).

## 🌟 Features

### Caesar Cipher
Inspired by  [cryptii.com caesar cipher](https://cryptii.com/pipes/caesar-cipher) implementation by [Wierk](https://wierk.lu/)
- Multiple case handling strategies:
  - Strict: Preserves exact casing
  - Maintain: Keeps original character case
  - Ignore: Case-insensitive encryption
- Configurable foreign character handling
- Built-in key encoding/decoding

### Steganography 
- LSB image steganography
- Supports PNG and JPG formats
- Secure message embedding and extraction
- Maintains visual image quality

## 📦 Prerequisites

- Python 3.11+
- Key dependencies:
  - Flask 3.0.3
  - scikit-image 0.24.0
  - numpy 1.26.4
  - matplotlib 3.9.2

## 🚀 Installation

### Local Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/andyathsid/pixelock-api-flask.git
    cd pixelock-api-flask
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the server:

    Use a WSGI server to start the app. You may encounter issues if you use the Flask development server instead.
    #### On Windows (Waitress)

    ```bash
    # Install Waitress if not already installed
    pip install waitress

    waitress-serve --host=0.0.0.0 --port=5000 app:app
    ```

    #### On Linux (Gunicorn)
    ```bash
    # Install Gunicorn if not already installed
    pip install gunicorn

    # Run the server
    gunicorn --bin 0.0.0.0:5000 --timeout 300 --workers 2 --worker-tmp-dir /dev/shm app:app # Change temporary directory to /dev/shm and set minimum workers to 2 to improve performance 
    ```

### Docker Setup

1. Ensure Docker is installed on your system. If not, install it from [Docker's official website](https://www.docker.com/).

1. Build the Docker image:
    ```bash
    docker build -t pixelock-api .
    ```

2. Run the Docker container:
    ```bash
    docker run -p 5000:5000 pixelock-api
    ```

## 📁 Project Structure
```bash
app/
├── routes/         # API endpoints
├── services/       # Core encryption & steganography logic
└── utils/          # Helper functions
data/
├── encoded/        # Processed images
└── raw/           # Original images
notebooks/         # Development notebooks
```

## 🔧 API Endpoints

### Encode Endpoints

#### 1. URL-based Encoding
- `POST api/encode`: Encrypt text and hide in image from URL
    - Example Request Body:
    ```json
    {
        "image_url": "https://example.com/image.jpg",
        "message": "This is a test message!",
        "alphabet": "`,.pyfgcrl/=\\aoeuidhtns-;qjkxbmwvz",
        "key": 7,
        "case_strategy": "maintain",
        "ignore_foreign": false
    }
    ```
    - Example Response:
    ```json
    {
        "success": true,
        "encrypted_message": "Kj;b ;b a ksbk psbbaos!",
        "image_url": "http://api.example.com/static/uploads/20241226_134326_e44d8b17.png",
        "shifted_alphabet": "crl/=\\oeuidhtns-;qjkxbmwvz`,.pyfg"
    }
    ```

#### 2. File Upload Encoding
- `POST api/encode/upload`: Encrypt text and hide in uploaded image
    - Request Format: `multipart/form-data`
    - Form Fields:
        - `image`: Image file
        - [data](http://_vscodecontentref_/0): JSON string containing parameters
    - Example Data JSON:
    ```json
    {
        "message": "This is a test message!",
        "alphabet": "`,.pyfgcrl/=\\aoeuidhtns-;qjkxbmwvz",
        "key": 7,
        "case_strategy": "maintain",
        "ignore_foreign": false
    }
    ```
    - Example Response: Same as `/encode` endpoint

### Decode Endpoints

#### 1. URL-based Decoding
- `POST api/decode`: Extract and decrypt message from image URL
    - Example Request Body:
    ```json
    {
        "image_url": "https://example.com/encoded-image.png",
        "alphabet": "`,.pyfgcrl/=\\aoeuidhtns-;qjkxbmwvz",
        "case_strategy": "maintain",
        "ignore_foreign": false
    }
    ```
    - Example Response:
    ```json
    {
        "success": true,
        "decrypted_message": "This is a test message!",
        "encrypted_message": "Kj;b ;b a ksbk psbbaos!",
        "shift_key": 7
    }
    ```

#### 2. File Upload Decoding
- `POST api/decode/upload`: Extract and decrypt message from uploaded image
    - Request Format: `multipart/form-data`
    - Form Fields:
        - `image`: Encoded image file
        - [data](http://_vscodecontentref_/1): JSON string containing parameters
    - Example Data JSON:
    ```json
    {
        "alphabet": "`,.pyfgcrl/=\\aoeuidhtns-;qjkxbmwvz",
        "case_strategy": "maintain",
        "ignore_foreign": false
    }
    ```
    - Example Response: Same as `/decode` endpoint


## 🧪 Testing

You can test the API by making a test request:

```bash
# Using default BASE_URL (http://localhost:5000/api)
python app/tests/test_api.py

# Or specify a custom BASE_URL
export API_BASE_URL=http://your-api-url:5000/api
python app/tests/test_api.py
```