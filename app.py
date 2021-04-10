import numpy as np
from flask import Flask, request, jsonify, render_template
import cv2
import pytesseract
from PIL import Image
from gtts import gTTS
import os

app = Flask(__name__)


 
 
@app.route('/')  
def upload():  
    return render_template("index.html")  
 
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(f.filename)  
        name = f.filename
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        # Path of working folder on Disk
        src_path = './'
        def get_string(img_path):
            # Read image with opencv
            img = cv2.imread(img_path)
            # Convert to gray
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Apply dilation and erosion to remove some noise
            kernel = np.ones((1, 1), np.uint8)
            img = cv2.dilate(img, kernel, iterations=1)
            img = cv2.erode(img, kernel, iterations=1)
            # Write image after removed noise
            cv2.imwrite(src_path + "removed_noise.png", img)
            #  Apply threshold to get image with only black and white
            img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
            # Write the image after apply opencv to do some ...
            cv2.imwrite(src_path + "thres.png", img)
            # Recognize text with tesseract for python
            result = pytesseract.image_to_string(Image.open(src_path + "thres.png"))
            # Remove template file
            # #os.remove(temp)
            return result
        print('--- Recognizing text from image ---')
        img2txt = get_string(src_path + name)
        print(img2txt)
        myobj = gTTS(text=img2txt, lang='en', slow=False)
        myobj.save('output1.mp3')
        #os.system('mpg321 output1.mp3')
        os.system('output1.mp3')
        print("------ Done -------")

        return render_template("index.html" )  
  
if __name__ == '__main__':  
    app.run(debug = True) 





