from flask import Flask, render_template, request
from PIL import Image
import pytesseract
import datetime, time
import threading

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():

    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


    # Get the uploaded image file from the form
    image_file = request.files['image']

    # Open the image using PIL
    image = Image.open(image_file)

    # Get the extraction time from the form
    extraction_time_str = request.form['extraction_time']

    # Parse the extraction time as a datetime object
    extraction_time = datetime.datetime.strptime(extraction_time_str, '%Y-%m-%dT%H:%M')

    # Calculate the time difference from the current time to the extraction time
    now_time = datetime.datetime.now()
    if extraction_time > now_time:
        dif = (extraction_time - datetime.datetime.now()).total_seconds()
    else:
        dif = 0
    time.sleep(dif)
    extracted_text = pytesseract.image_to_string(image)
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
