from flask import Flask, render_template, request, send_file
import os
import sys
from PIL import Image
from werkzeug.utils import secure_filename
# import numpy as np

app = Flask(__name__)

UPLOAD_FOLDER = 'upload'
DOWNLOAD_FOLDER = 'download'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app_directory = os.path.dirname(os.path.abspath(__file__))
steganography_path = os.path.join(app_directory, 'app')
sys.path.append(steganography_path)

# import jsteg_f3

@app.route("/")
def index():
    return render_template("home.html")

import sys
import os
from PIL import Image
import io

from jpeg_encoder import *
from jpeg_decoder import *
from B import *

import math
import random
import time

class Encoder:
    def __init__(self, image, quality, out):
        self.out = out
        self.jpeg_encoder = jpegEncoder(image, quality, out, 'by: Jatin Mandav')

    def write(self, data):
        self.data = data
        self.jpeg_encoder.writeHeads()

        self.embedData_f3()
        self.jpeg_encoder.writeImage()

    def embedData_f3(self):
        coeff=self.jpeg_encoder.coeff
        byte_embed=len(self.data)
        if byte_embed>0x7fffffff: byte_embed=0x7fffffff
        bit_embed=byte_embed&1
        byte_embed>>=1
        need_embed=31
        data_index=0
        for i,j in enumerate(coeff):
            if i%64==0 or j==0: continue
            if j>0 and (j&1)!=bit_embed: coeff[i]-=1
            elif j<0 and (j&1)!=bit_embed: coeff[i]+=1
            if coeff[i]!=0:
                if need_embed==0:
                    if data_index>=len(self.data): break
                    byte_embed=ord(self.data[data_index])
                    data_index+=1
                    need_embed=8
                bit_embed=byte_embed&1
                byte_embed>>=1
                need_embed-=1
class Decoder:
    def __init__(self, data, out):
        self.out = out
        self.data = data
        self.jpeg_decoder = jpegDecoder(data)

    def read(self):
        self.jpeg_decoder.readHeads()
        self.jpeg_decoder.readImage()

        self.extractData_f3()

    def extractData_f3(self):
        coeff=self.jpeg_decoder.coeff
        i,pos=0,-1
        finish,length=0,0
        need_extract=0
        byte_extract=0
        while i<32:
            pos+=1
            j=pos-pos%64+ZAGZIG[pos%64]
            if j%64==0 or coeff[j]==0: continue
            if coeff[j]&1: length|=1<<i
            i+=1

        while finish<length:
            pos+=1
            j=pos-pos%64+ZAGZIG[pos%64]
            if j%64==0 or coeff[j]==0: continue
            if coeff[j]&1: byte_extract|=1<<need_extract
            need_extract+=1
            if need_extract==8:
                self.out.write(chr(byte_extract&0xff))
                need_extract=0
                byte_extract=0
                finish+=1

@app.route('/embed', methods=['POST', 'GET'])
def encode():
    error_message = ''
    stego_image_path = None
    quality_default = 50

    if request.method == 'POST':
        if 'file' not in request.files or 'message' not in request.files:
            error_message = 'No file or message uploaded.'
            return render_template('embed.html', header=error_message)

        file = request.files['file']
        message = request.files['message']

        if file.filename == '' or message.filename == '':
            return render_template('embed.html', header='Error: No selected file.')

        if not allowed_file(file.filename) or not allowed_file(message.filename):
            return render_template('embed.html', header='Error: Unsupported file format.')

        try:
            print("Start encoding process")
            
            # Save the uploaded files
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(file_path)
            print(f"Image file saved to {file_path}")
            
            message_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(message.filename))
            message.save(message_path)
            print(f"Message file saved to {message_path}")

            # Open the image file
            image = Image.open(file_path)
            print(f"Image opened: {image}")

            # Read message data from the uploaded message file
            with open(message_path, 'r') as file_:
                data = file_.read()
            print(f"Message data: {data}")

            # Prepare output file path
            stego_image_path = os.path.join(app.config['DOWNLOAD_FOLDER'], f"stego_{file.filename}")

            # Open the output file in binary write mode
            output = open(stego_image_path, 'wb')
            print(f"Output file path: {stego_image_path}")

            # Create an instance of the Encoder class
            encoder = Encoder(image, quality_default, output)
            print("Encoder initialized")

            # Call the write method to encode the message into the image
            encoder.write(data)
            print("Message encoded")

            # Re-open the stego image and save it to ensure it's properly closed
            image = Image.open(stego_image_path)
            image.save(stego_image_path)
            stego_image_path = f"static/downloads/stego_{file.filename}"
            
        except Exception as e:
            print(e)
            error_message = str(e)
    
    return render_template('embed.html', image=stego_image_path, error=error_message)

@app.route("/extract", methods=['POST', 'GET'])
def decode():
    error_message = ''
    decoded_message = ''

    if request.method == 'POST':
        if 'file' not in request.files:
            error_message = 'No file uploaded.'
            return render_template('embed.html', header=error_message)

        file = request.files['file']

        if file.filename == '':
            return render_template('embed.html', header='Error: No selected file.')

        if not allowed_file(file.filename):
            return render_template('embed.html', header='Error: Unsupported file format.')

        try:
            print("Start decoding process")
            
            # Save the uploaded file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(file_path)
            print(f"Image file saved to {file_path}")

            # Open the image file
            with open(file_path, 'rb') as image:
                print(f"Image opened: {image}")

                # Create a StringIO to capture the output
                output = io.StringIO()

                # Create an instance of the Decoder class
                decoder = Decoder(image.read(), output)
                print("Decoder initialized")

                # Call the read method to decode the message from the image
                decoder.read()
                print("Message decoded")

                # Get the decoded message
                decoded_message = output.getvalue()
                print("Decoded Message: ", decoded_message)

                output.close()
            
        except Exception as e:
            print(e)
            error_message = str(e)

    return render_template("extract.html", error=error_message, decoded_message=decoded_message)


if __name__ == "__main__":
    app.run(debug=True)