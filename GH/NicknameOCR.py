from PIL import Image
import NicknameCapture
import pytesseract


class NicknameOCR:
    def __init__(self, tesseract_file_path : str):
        pytesseract.pytesseract.tesseract_cmd = tesseract_file_path #tesseract .exe path
        return

    def __fix_image(self):
        return

    #get nickname from Image list
    def get_nicknames(self, image_list : list):
        nickname_list=[]
        for img in image_list:
            nickname=pytesseract.image_to_string(img, lang='kor+eng',config='--psm 7').strip()
            nickname_list.append(nickname)
        return nickname_list
