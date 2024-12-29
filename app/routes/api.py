from flask import Blueprint, request, jsonify
from app.services.steganography import encode as steg_encode, decode as steg_decode
from app.services.caesar_cipher import (
    preprocess_text, caesar_cipher, encode_key, 
    decode_key, shift_alphabet
)
from app.utils.image_helpers import load_image
from app.utils.s3_storage import upload_image
from app.utils.storage import generate_filename

from io import BytesIO
import json

api = Blueprint('api', __name__)

@api.route('/encrypt', methods=['POST'])
def encode_image_upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
        
    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    data = request.form.get('data')
    if not data:
        return jsonify({'error': 'Message data is required'}), 400
        
    try:
        data = json.loads(data)
        
        if 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
            
        shift_key = data.get('key')
        alphabet = data.get('alphabet')
        case_strategy = data.get('case_strategy')
        ignore_foreign = data.get('ignore_foreign')
        
        # Load image
        image_bytes = BytesIO(image_file.read())
        image = load_image(image_bytes)
        
        # Preprocess and encrypt the message
        processed_text = preprocess_text(data['message'])
        encrypted_text = caesar_cipher(
            processed_text,
            alphabet,
            shift_key,
            mode='encrypt',
            case_strategy=case_strategy,
            ignore_foreign=ignore_foreign
        )
        
        # Include metadata in steganography message
        metadata = f"{case_strategy}|{1 if ignore_foreign else 0}|"
        encoded_key = encode_key(shift_key, alphabet)
        steg_message = f"{encoded_key}|{metadata}{encrypted_text}"
        encoded_image = steg_encode(image, steg_message)
        
        # Upload to S3
        filename = generate_filename()
        image_url = upload_image(encoded_image, filename)
        
        return jsonify({
            'image_url': image_url,
            'encrypted_message': encrypted_text,
            'shifted_alphabet': shift_alphabet(alphabet, shift_key)
        })
        
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON data'}), 400
    except Exception as e:
        return jsonify({'error': f'Error processing request: {str(e)}'}), 500
    
@api.route('/decrypt', methods=['POST'])
def decode_image_upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
        
    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    data = request.form.get('data')
    if not data:
        return jsonify({'error': 'Parameters data is required'}), 400
        
    try:
        data = json.loads(data)
        alphabet = data.get('alphabet')
        
        # Load and decode image
        image_bytes = BytesIO(image_file.read())
        image = load_image(image_bytes)
        steg_message = steg_decode(image)
        
        try:
            # Extract key and metadata
            encoded_key, rest = steg_message.split('|', 1)
            case_strategy, ignore_foreign, encrypted_text = rest.split('|', 2)
            ignore_foreign = bool(int(ignore_foreign))
            shift_key = decode_key(encoded_key, alphabet)
            
            decrypted_text = caesar_cipher(
                encrypted_text,
                alphabet,
                shift_key,
                mode='decrypt',
                case_strategy=case_strategy,
                ignore_foreign=ignore_foreign
            )
            
            return jsonify({
                'decrypted_message': decrypted_text,
                'encrypted_message': encrypted_text,
                'shift_key': shift_key,
                'case_strategy': case_strategy,
                'ignore_foreign': ignore_foreign
            })
            
        except ValueError:
            return jsonify({'error': 'Invalid message format in image'}), 400
            
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON data'}), 400
    except Exception as e:
        return jsonify({'error': f'Error processing request: {str(e)}'}), 500