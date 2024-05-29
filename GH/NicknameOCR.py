from PIL import Image
import NicknameCapture
import pytesseract


class NicknameOCR:
    def __init__(self, tesseract_file_path : str):
        pytesseract.pytesseract.tesseract_cmd = tesseract_file_path #tesseract .exe path
        return

