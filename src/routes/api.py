from flask import Blueprint, request, jsonify, url_for
from services.steganography import encode as steg_encode, decode as steg_decode
from services.caesar_cipher import (
    preprocess_text, caesar_cipher, encode_key, 
    decode_key, shift_alphabet
)
from utils.image_helpers import load_image, save_image
from utils.storage import UPLOAD_FOLDER, generate_filename
import requests
from io import BytesIO
import os

api = Blueprint('api', __name__)

@api.route('/encode', methods=['POST'])
def encode_image():
    data = request.get_json()
    
    if not data or 'image_url' not in data or 'message' not in data:
        return jsonify({'error': 'Image URL and message are required'}), 400
        
    # Get cipher parameters with defaults
    shift_key = data.get('key', 3)  # Default shift of 3
    alphabet = data.get('alphabet', 'abcdefghijklmnopqrstuvwxyz')
    case_strategy = data.get('case_strategy', 'maintain')  # or 'strict' or 'ignore'
    ignore_foreign = data.get('ignore_foreign', False)
    
    try:
        # Download and load image
        image_response = requests.get(data['image_url'])
        image_response.raise_for_status()
        image_bytes = BytesIO(image_response.content)
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
        
        # Get the shifted alphabet
        shifted_alphabet = shift_alphabet(alphabet, shift_key)
        
        # Encode the encrypted message into the image
        encoded_key = encode_key(shift_key, alphabet)
        steg_message = f"{encoded_key}|{encrypted_text}"
        encoded_image = steg_encode(image, steg_message)
        
        # Save and return image
        filename = generate_filename()
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        save_image(encoded_image, filepath)
        
        image_url = url_for('static', filename=f'uploads/{filename}', _external=True)
        
        return jsonify({
            'success': True,
            'image_url': image_url,
            'encrypted_message': encrypted_text,
            'shifted_alphabet': shifted_alphabet
        })
        
    except requests.RequestException as e:
        return jsonify({'error': f'Failed to download image: {str(e)}'}), 400

@api.route('/decode', methods=['POST'])
def decode_image():
    data = request.get_json()
    
    if not data or 'image_url' not in data:
        return jsonify({'error': 'Image URL is required'}), 400
        
    # Get cipher parameters with defaults
    alphabet = data.get('alphabet', 'abcdefghijklmnopqrstuvwxyz')
    case_strategy = data.get('case_strategy', 'maintain')
    ignore_foreign = data.get('ignore_foreign', False)
    
    try:
        # Download and load image
        image_response = requests.get(data['image_url'])
        image_response.raise_for_status()
        image_bytes = BytesIO(image_response.content)
        image = load_image(image_bytes)
        
        # Extract hidden message from image
        steg_message = steg_decode(image)
        
        try:
            # Split encoded key and ciphertext
            encoded_key, encrypted_text = steg_message.split('|', 1)
            shift_key = decode_key(encoded_key, alphabet)
            
            # Decrypt the message
            decrypted_text = caesar_cipher(
                encrypted_text,
                alphabet,
                shift_key,
                mode='decrypt',
                case_strategy=case_strategy,
                ignore_foreign=ignore_foreign
            )
            
            return jsonify({
                'success': True,
                'decrypted_message': decrypted_text,
                'encrypted_message': encrypted_text,
                'shift_key': shift_key
            })
            
        except ValueError:
            return jsonify({'error': 'Invalid message format in image'}), 400
            
    except requests.RequestException as e:
        return jsonify({'error': f'Failed to download image: {str(e)}'}), 400