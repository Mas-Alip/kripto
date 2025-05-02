from flask import Flask, request, jsonify
from src.encryption.aes import AESCipher
from src.steganography.embed import embed_file
from src.steganography.extract import extract_file
from src.types import ...
import os

app = Flask(__name__)
cipher = AESCipher()

@app.route('/embed', methods=['POST'])
def embed():
    if 'image' not in request.files or 'file' not in request.files:
        return jsonify({'error': 'No image or file provided'}), 400
    
    image = request.files['image']
    file_to_embed = request.files['file']
    password = request.form.get('password')

    if not password:
        return jsonify({'error': 'No password provided'}), 400

    try:
        encrypted_file = cipher.encrypt_file(file_to_embed, password)
        output_image = embed_file(image, encrypted_file)
        return jsonify({'message': 'File embedded successfully', 'output_image': output_image}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/extract', methods=['POST'])
def extract():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    image = request.files['image']
    password = request.form.get('password')

    if not password:
        return jsonify({'error': 'No password provided'}), 400

    try:
        extracted_file = extract_file(image, password)
        return jsonify({'message': 'File extracted successfully', 'extracted_file': extracted_file}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)