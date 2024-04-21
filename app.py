from flask import Flask, render_template, request, send_file
import os
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
app = Flask(__name__)

UPLOAD_FOLDER = 'upload'
DOWNLOAD_FOLDER = 'download'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

import sys
import os
import argparse
from PIL import Image
from io import BytesIO
import io

from jpeg_encoder import *
from jpeg_decoder import *

import math
import random
import time
from B import *

from tqdm import tqdm

def create(value=None, *args):
    if len(args) and args[0]:
        return [create(value,*args[1:]) for i in range(round(args[0]))]
    else: return value

class Encoder:
    def __init__(self, image, quality, out):
        self.out = out
        self.jpeg_encoder = jpegEncoder(image, quality, out, 'DCT')

    def write(self, data, password, use_simulated_annealing=True, annealing_iterations=1000, initial_temperature=100.0, cooling_rate=0.003):
        self.data = data
        self.password = password
        self.jpeg_encoder.writeHeads()

        start_time = time.time()


        if use_simulated_annealing:
            self.embedData_f3()
        else:
            self.embedData_simulated_annealing(annealing_iterations, initial_temperature, cooling_rate)

        self.jpeg_encoder.writeImage()
        end_time = time.time()
        print("Embedding process took {:.2f} seconds".format(end_time - start_time))

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

    def embedData_simulated_annealing(self, iterations, initial_temperature, cooling_rate):
        coeff = self.jpeg_encoder.coeff
        best_coeff = list(coeff)  
        best_score = self.evaluateSolution(coeff)

        temperature = initial_temperature
        for _ in range(iterations):
            # Generate a neighbor solution by modifying coefficients randomly
            neighbor_coeff = self.generateNeighborSolution(coeff)
            neighbor_score = self.evaluateSolution(neighbor_coeff)

            # Calculate the difference in scores between neighbor and current solutions
            delta_score = neighbor_score - best_score

            # Decide whether to accept the neighbor solution or not
            if delta_score < 0 or random.random() < math.exp(-delta_score / temperature):
                coeff = list(neighbor_coeff)  
                best_score = neighbor_score

                # Update the best solution found so far
                if best_score < self.evaluateSolution(best_coeff):
                    best_coeff = list(coeff)

            # Cool down the temperature
            temperature *= 1 - cooling_rate

        # Set the coefficients to the best solution found
        self.jpeg_encoder.coeff = best_coeff

    def evaluateSolution(self, coeff):
        # For simplicity, let's return the sum of absolute values of coefficients as a proxy for solution quality
        return sum(abs(c) for c in coeff)

    def generateNeighborSolution(self, coeff):
        # Generate a neighbor solution by modifying coefficients randomly
        # For simplicity, we can perturb a random subset of coefficients
        neighbor_coeff = list(coeff)
        num_perturbations = random.randint(1, len(neighbor_coeff) // 10)  # Perturb a random subset of coefficients
        indices = random.sample(range(len(neighbor_coeff)), num_perturbations)
        for index in indices:
            neighbor_coeff[index] = random.randint(-32768, 32767)  # Perturb the coefficient randomly
        return neighbor_coeff
    
class Decoder:
    def __init__(self, data, out):
        self.out = out
        self.data = data
        self.jpeg_decoder = jpegDecoder(data)

    def read(self, password):
        self.password = password
        self.jpeg_decoder.readHeads()
        self.jpeg_decoder.readImage()

        start_time = time.time() 

        self.extractData_f3()

        end_time = time.time() 
        print("Extraction process took {:.2f} seconds".format(end_time - start_time))

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


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/embed', methods=['POST', 'GET'])
def encode():
    error_message = ''
    stego_image_path = None

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
            # Save the uploaded files
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            message_filename = secure_filename(message.filename)
            message_path = os.path.join(app.config['UPLOAD_FOLDER'], message_filename)
            message.save(message_path)

            # Read message data from the uploaded message file
            with open(message_path, 'rb') as f:
                message_data = f.read()

            # Open the image file
            img = Image.open(file_path)
            img_array = np.array(img)

            # Create an instance of the Encoder class
            encoder = Encoder(img_array, quality=100, out=None)

            # Call the write method to encode the message into the image
            stego_image_path = os.path.join(app.config['DOWNLOAD_FOLDER'], f"stego_{filename}")
            encoder.write(message_data, password=None)

            # Save the encoded image to the download folder
            img.save(stego_image_path)

            header = f"Encoded Image: stego_{filename}"
            
        except Exception as e:
            error_message = str(e)

    return render_template('embed.html', image=stego_image_path, error=error_message)

# @app.route('/extract', methods=['POST', 'GET'])
# def decode():
#     header = 'Decoded text:'
#     global last_decoded_text
#     decoded_text = ""
    
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return render_template('/extract.html', header=header)

#         file = request.files['file']
#         if file.filename == '':
#             return render_template('/extract.html', header='Error: No file was selected')

#         try:
#             # Save the uploaded file to the static folder
#             filename = secure_filename(file.filename)
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(file_path)

#             # Call the extract function with the file object
#             decoded_text = extract(file_path)

#             # Store the decoded message
#             last_decoded_text = decoded_text
#         except ValueError as e:
#             return render_template('/extract.html', header='Error: {}'.format(str(e)))

#     return render_template('/extract.html', header=header, text=decoded_text)

# @app.route('/image/last/extracted')
# def get_last_decoded_message():
# 	global last_decoded_text

# 	if last_decoded_text is None:
# 		return 'No extracted data available.'

# 	return last_decoded_text

# @app.route("/embed")
# def encode():
#     return render_template("embed.html")

@app.route("/extract")
def decode():
    return render_template("/extract.html")

@app.route('/download_embedded_image')
def download_embedded_image():
    embedded_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'embedded_image.png')
    return send_file(embedded_image_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)