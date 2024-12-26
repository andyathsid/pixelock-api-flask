from flask import Blueprint, request, jsonify, url_for
from services.steganography import encode, decode
from utils.image_helpers import load_image, save_image
from utils.storage import UPLOAD_FOLDER, generate_filename
import requests
from io import BytesIO
import os

api = Blueprint('api', __name__)

@api.route('/encode', methods=['POST'])
def encode_image():
    data = request.get_json()
    
    if not data or 'image' not in data or 'message' not in data:
        return jsonify({'error': 'Image URL and message are required'}), 400
    
    try:
        image_response = requests.get(data['image'])
        image_response.raise_for_status()
        image_bytes = BytesIO(image_response.content)
    except requests.RequestException as e:
        return jsonify({'error': f'Failed to download image: {str(e)}'}), 400
    
    image = load_image(image_bytes)
    encoded_image = encode(image, data['message'])
    
    filename = generate_filename()
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    save_image(encoded_image, filepath)
    
    image_url = url_for('static', filename=f'uploads/{filename}', _external=True)
    
    return jsonify({
        'success': True,
        'image_url': image_url,
    })

@api.route('/decode', methods=['POST'])
def decode_image():
    data = request.get_json()
    
    if not data or 'image_url' not in data:
        return jsonify({'error': 'Image URL is required'}), 400
    
    try:
        image_response = requests.get(data['image_url'])
        image_response.raise_for_status()
        image_bytes = BytesIO(image_response.content)
    except requests.RequestException as e:
        return jsonify({'error': f'Failed to download image: {str(e)}'}), 400
    
    image = load_image(image_bytes)
    decoded_message = decode(image)
    
    return jsonify({
        'success': True,
        'message': decoded_message
    })