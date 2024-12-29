# Pixelock API

## Overview

This project is a Flask application that provides an API for encoding and decoding hidden messages in images using steganography and cryptography techniques. This is developed as part of my university Cybersecurity course project and is part of a system that includes a [Flutter Android app](https://github.com/Wilimaxs/KriptoApp).

## 🌟 Features

### Caesar Cipher
Inspired by [cryptii.com caesar cipher](https://cryptii.com/pipes/caesar-cipher) implementation by [Wierk](https://wierk.lu/)
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

### Storage
- AWS S3 integration for image storage
- Secure and scalable cloud storage
- Direct S3 URL generation for processed images

## 📦 Prerequisites

- Python 3.11+
- AWS Account with S3 bucket
- Key dependencies:
  - Flask 
  - scikit-image 
  - numpy 
  - boto3
  - python-decouple

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

4. Configure AWS credentials:
    Create a [.env](http://_vscodecontentref_/1) file with your AWS credentials:
    ```
    AWS_ACCESS_KEY=your_access_key
    AWS_SECRET_KEY=your_secret_key
    AWS_REGION=your_region
    AWS_BUCKET=your_bucket_name
    ```

5. Run the server:
    #### On Windows (Waitress)
    ```bash
    pip install waitress
    waitress-serve --host=0.0.0.0 --port=5000 wsgi:app
    ```

    #### On Linux (Gunicorn)
    ```bash
    pip install gunicorn
    gunicorn --bind 0.0.0.0:5000 --timeout 300 --workers 2 --worker-tmp-dir /dev/shm wsgi:app
    ```

### Docker Setup

1. Ensure Docker is installed on your system.

2. Build the Docker image:
    ```bash
    docker build -t pixelock-api .
    ```

3. Run the Docker container:
    ```bash
    # Using .env file (recommended)
    docker run -p 5000:5000 --env-file .env pixelock-api

    # Or specify environment variables directly
    docker run -p 5000:5000 \
    -e AWS_ACCESS_KEY=your_access_key \
    -e AWS_SECRET_KEY=your_secret_key \
    -e AWS_BUCKET=your_bucket_name \
    -e AWS_REGION=your_region \
    pixelock-api
    ```

## 📁 Project Structure
```bash
app/
├── routes/         # API endpoints
├── services/       # Core encryption & steganography logic
└── utils/          # Helper functions and S3 storage
data/
├── encoded/        # Sample encoded images
└── raw/           # Sample original images
notebooks/         # Development notebooks
```

## 🔧 API Endpoints

### Internal Key Endpoints
These endpoints store the encryption key within the image metadata.

#### 1. Internal Key Encryption
- `POST /api/encrypt/internal-key`: Encrypt text and store key in image
    - Request Format: `multipart/form-data`
    - Form Fields:
        - `image`: Image file
        - `data`: JSON string containing parameters
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
    - Example Response:
    ```json
    {
        "image_url": "https://pixelock-images.s3.ap-southeast-1.amazonaws.com/uploads/20240226_134326_e44d8b17.png",
        "encrypted_message": "Kj;b ;b a ksbk psbbaos!",
        "shifted_alphabet": "crl/=\\oeuidhtns-;qjkxbmwvz`,.pyfg"
    }
    ```

#### 2. Internal Key Decryption
- `POST /api/decrypt/internal-key`: Extract key and decrypt message from image
    - Request Format: `multipart/form-data`
    - Form Fields:
        - [image](http://_vscodecontentref_/0): Encoded image file
        - [data](http://_vscodecontentref_/1): JSON string containing parameters
    - Example Data JSON:
    ```json
    {
        "alphabet": "`,.pyfgcrl/=\\aoeuidhtns-;qjkxbmwvz"
    }
    ```
    - Example Response:
    ```json
    {
        "decrypted_message": "This is a test message!",
        "encrypted_message": "Kj;b ;b a ksbk psbbaos!",
        "shift_key": 7,
        "case_strategy": "maintain",
        "ignore_foreign": false
    }
    ```

### External Key Endpoints
These endpoints keep the encryption key separate from the image.

#### 1. External Key Encryption
- `POST /api/encrypt/external-key`: Encrypt text without storing key
    - Request Format: Same as internal key encryption
    - Example Response: Same as internal key encryption

#### 2. External Key Decryption
- `POST /api/decrypt/external-key`: Decrypt message using provided key
    - Request Format: `multipart/form-data`
    - Form Fields:
        - [image](http://_vscodecontentref_/2): Encoded image file
        - [data](http://_vscodecontentref_/3): JSON string containing parameters
    - Example Data JSON:
    ```json
    {
        "alphabet": "`,.pyfgcrl/=\\aoeuidhtns-;qjkxbmwvz",
        "key": 7
    }
    ```
    - Example Response: Same as internal key decryption

## 🧪 Testing

You can test the API by running the prepared test scripts:

```bash
# Using default BASE_URL (http://localhost:5000/api)
python app/tests/test_api.py

# Or specify a custom BASE_URL
export API_BASE_URL=http://your-api-url:5000/api
python app/tests/test_api.py

# Test S3 connection
python app/tests/test_s3_connection.py
```