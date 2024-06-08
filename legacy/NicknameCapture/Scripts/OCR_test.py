from PIL import Image

import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

data = []

for i in range(4):
    print(pytesseract.image_to_string(Image.open('./capture_image/test' + str(i) +'.png'),\
                                      lang='kor+eng',config='--psm 7'))


