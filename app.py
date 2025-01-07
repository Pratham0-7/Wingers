from flask import Flask, render_template, request, send_file, send_from_directory, url_for, redirect
import cv2
import numpy as np
import os
import random
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

def string_to_bin(message):
    binary_message = ""
    for char in message:
        binary_char = bin(ord(char))[2:].zfill(8)
        binary_message += binary_char
    binary_message += '00000000'
    return binary_message

def embed_bit(channel, bit):
    if bit == '0':
        return channel & 0xFE
    else:
        return channel | 0x01

def encrypt_stego(cover_image, message):
    height, width, depth = cover_image.shape
    binary_message = string_to_bin(message)
    message_index = 0

    for row in range(height):
        for column in range(width):
            for channel in range(depth):
                if message_index < len(binary_message):
                    channel_value = cover_image[row, column, channel]
                    bit_to_embed = binary_message[message_index]
                    modified_channel = embed_bit(channel_value, bit_to_embed)
                    cover_image[row, column, channel] = modified_channel
                    message_index += 1
                else:
                    cover_image[row, column, channel] = embed_bit(channel_value, '0')
                    return cover_image
    return cover_image

def decrypt_stego(stego_image):
    binary_message = ""
    height, width, depth = stego_image.shape
    message_index = 0

    for row in range(height):
        for column in range(width):
            for channel in range(depth):
                channel_value = stego_image[row, column, channel]
                extracted_LSB = channel_value & 0x01
                binary_message += str(extracted_LSB)
                message_index += 1

                if message_index % 8 == 0 and binary_message[-8:] == '00000000':
                    return binary_message[:-8]

    return binary_message

def binary_to_string(binary_ciphertext):
    ciphertext = ""
    for i in range(0, len(binary_ciphertext), 8):
        byte = binary_ciphertext[i:i + 8]
        char = chr(int(byte, 2))
        ciphertext += char
    return ciphertext

def encrypt_caesar(plaintext, key):
    ciphertext = ""
    for char in plaintext:
        if char.islower():
            encrypted_char = chr((ord(char) + key - ord('a')) % 26 + ord('a'))
        elif char.isupper():
            encrypted_char = chr((ord(char) + key - ord('A')) % 26 + ord('A'))
        else:
            encrypted_char = char
        ciphertext += encrypted_char
    return ciphertext

def decrypt_caesar(ciphertext, key):
    plaintext = ""
    for char in ciphertext:
        if char.islower():
            decrypted_char = chr((ord(char) - key - ord('a')) % 26 + ord('a'))
        elif char.isupper():
            decrypted_char = chr((ord(char) - key - ord('A')) % 26 + ord('A'))
        else:
            decrypted_char = char
        plaintext += decrypted_char
    return plaintext

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    message = ""
    encrypted_text = ""
    key = None
    if request.method == 'POST':
        file = request.files.get('file')
        text = request.form.get('text')
        key = random.randint(2, 25)
        encrypted_text = encrypt_caesar(text, key)
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            img = cv2.imread(file_path)
            stego_img = encrypt_stego(img, encrypted_text)
            stego_path = os.path.splitext(file_path)[0] + '_stego.png'

            cv2.imwrite(stego_path, stego_img)
            os.remove(file_path)
            message = f"Image encrypted with key {key}."
            return render_template('index.html', message=message, key=key)

    return redirect(url_for('home'))

@app.route('/decrypt', methods=['POST'])
def decrypt():
    decrypted_text = ""
    message = ""
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            img = cv2.imread(file_path)
            binary_ciphertext = decrypt_stego(img)
            string_ciphertext = binary_to_string(binary_ciphertext)
            key = int(request.form.get('key'))
            decrypted_text = decrypt_caesar(string_ciphertext, key)
            message = "Decryption successful."
    return render_template('index.html', message=message, decrypted_text=decrypted_text)

@app.route('/clear', methods=['POST'])
def clear():
    return redirect(url_for('home'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(port=5000, debug=True)
