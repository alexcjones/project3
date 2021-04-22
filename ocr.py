import cv2
import pytesseract
import numpy as np
import os
import re
from fpdf import FPDF
'''
from googletrans import Translator
'''
TESSERACT_PATH = 'TESSDATA_PREFIX'

def ocr(filename):
    """
    Get text from an image.
    :param filename: String, relative path of file in uploaded folder.
    :return: String
    """
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)[1]
    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    contours, _git = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    text = ""
    for p in contours:
        x, y, w, h = cv2.boundingRect(p)
        rect = cv2.rectangle(img, (x, y), (x + w, y + h), 0, 2)
        crop=img[y:y+h,x:x+w]
        text = pytesseract.image_to_string(crop)
    pdf(trim_text(text))
    return trim_text(text)


def trim_text(text):
    text = re.sub('\n +', '', text)
    text = re.sub('\n+', '\n', text)
    print(text)

    return text

def pdf(text):
    pdf=FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=text)
    pdf.output("text.pdf")


if __name__ == '__main__':
    os.chdir('samples/')
    print("Sample:")
    print(ocr('sample.jpg'))
    print('Handwritten:')
    print(ocr('handwritten.jpg'))

'''   
def translate_text(t, d_lang):
    translator = Translator()
    trans = translator.translate(t, dest = d_lang)
    return(trans.text)

print(translate_text("你好吗", "en"))
'''
