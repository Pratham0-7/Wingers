Flask Steganography Application

This Flask-based application performs encryption and decryption of text messages using Caesar cipher encryption and hides the encrypted text within an image using steganography techniques. The application also provides a simple web interface for users to upload files and interact with the application.

Features

1. Encrypt Text into an Image:
   - Text is encrypted using a Caesar cipher.
   - The encrypted text is then embedded into the least significant bits (LSB) of an image.

2. Decrypt Text from an Image:
   - Retrieves and decrypts the hidden message from an image.

3. Web Interface:
   - Allows file uploads and key management via a web browser.

4. Key Management:
   - A random key is generated during encryption.


Prerequisites

 Software Requirements

- Python 3.x
- Flask
- OpenCV (cv2)

 Encrypting a Message

1. Enter the text you want to encrypt.
2. Upload an image file (PNG, JPG, JPEG, or GIF formats are allowed).
3. Submit the form to receive an encrypted image and a generated key.

 Decrypting a Message

1. Upload the stego image containing the hidden message.
2. Enter the key used during encryption.
3. Submit the form to retrieve the decrypted text.

---

 Example Workflow

1. Encryption:
   - Input text: `Hello World`
   - Random key generated: `7`
   - Image: `image.png`
   - Output: `image_stego.png` with the hidden message.

2. Decryption:
    Input: `image_stego.png`
    Key: `7`
    Output: `Hello World`


