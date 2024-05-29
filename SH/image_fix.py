from PIL import Image
import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
# BGR로 특정 색을 추출하는 함수
def bgrExtraction(image, bgrLower, bgrUpper):
    img_mask = cv2.inRange(image, bgrLower, bgrUpper) 
    result = cv2.bitwise_and(image, image, mask=img_mask) 
    return result    
    
def masking_image(file_path, font_color, tolerance = 200):
    image = cv2.imread(file_path)
    #이미지 2배화
    image_resized = cv2.resize(image, (0, 0), fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    # BGR로 색추출
    bgrLower = np.array(font_color) - tolerance   # 추출할 색의 하한
    bgrUpper = np.array(font_color) + tolerance   # 추출할 색의 상한
    bgrResult = bgrExtraction(image_resized, bgrLower, bgrUpper)
    cv2.imshow('BGR_test1', bgrResult)
    cv2.waitKey(0)
    text = pytesseract.image_to_string(bgrResult, lang='kor+eng', config='--psm 7') # 텍스트 추출
    return text

# 출력 테스트를 위한 예시 코드였었음, 사용할 필요 없다
# def read_text(file_path):
#     image = Image.open(file_path)
#     resize_image = image.resize((image.width * 2, image.height * 2), Image.LANCZOS)
#     text = pytesseract.image_to_string(resize_image, lang='kor+eng', config='--psm 7') # 텍스트 추출
#     return text


# def text_color(file_path, font_color, change_color):
#     image = cv2.imread(file_path)
#     rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
#     font_color = np.array(font_color, dtype=np.uint8)
#     change_color = np.array(change_color, dtype=np.uint8)
    
#     mask = np.all(rgb_image == font_color, axis=-1)
#     image[mask] = change_color
    
#     return image

image_path = "./imagefile/test3.png"
check = masking_image(image_path, [71, 192, 233]) #BGR값 입력
print(check)
