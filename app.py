from flask import Flask, render_template, request
from PIL import Image
import pytesseract
import time
from datetime import datetime, timedelta
import threading
import os
import requests

API_URL = 'https://api.api-ninjas.com/v1/imagetotext'


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # os.chmod(r'./Tesseract-OCR/tesseract.exe', 0o0777)
    
    pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'


    # Get the uploaded image file from the form
    image_file = request.files['image']

    print(image_file)

    # Open the image using PIL
    # image = Image.open(image_file)
    # image.tobytes("xbm", "rgb")
    image = image_file.read() # open(image_file, 'rb')

    # Get the extraction time from the form
    extraction_time_str = request.form['extraction_time']

    # Parse the extraction time as a datetime object
    extraction_time = datetime.strptime(extraction_time_str, '%Y-%m-%dT%H:%M')

    # Calculate the time difference from the current time to the extraction time
    now_time = datetime.utcnow() + timedelta(hours=5.5) #datetime.datetime.now()
    if extraction_time > now_time:
        dif = (extraction_time - now_time).total_seconds()
    else:
        dif = 0
    time.sleep(dif)
    files = {'image': image}
    r = requests.post(API_URL,headers={'X-Api-Key': 'ycee22h9ItBexlq6lKbvJQ==Kaa1FJCgG7VllCBc'}, files=files)
    # print(r.json())
    json_rst = r.json()
    extracted_text = " ".join([i['text'] for i in json_rst])

    # extracted_text = pytesseract.image_to_string(image)
    return render_template('result.html', text=extracted_text)


    # Schedule the extraction process to run after the time difference
    # extraction_thread = threading.Timer(dif, perform_extraction, args=(image,))
    # extraction_thread.start()
    # extraction_thread.join()

    return render_template('result.html')

# def perform_extraction(image):
#     # Perform OCR on the image
#     extracted_text = pytesseract.image_to_string(image)
#     # return render_template('result.html', text=extracted_text)
#     print("Extracted Text:", extracted_text)

if __name__ == '__main__':
    app.run(debug=True)
