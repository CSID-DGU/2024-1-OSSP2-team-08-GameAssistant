import cv2
import numpy as np
    
# BGR로 특정 색을 추출하는 함수
def bgrExtraction(image, bgrLower, bgrUpper):
    img_mask = cv2.inRange(image, bgrLower, bgrUpper) 
    result = cv2.bitwise_and(image, image, mask=img_mask) 
    return result    
    
def masking_image(image, font_color, tolerance = 200):
    #이미지 2배화
    image_resized = cv2.resize(image, (0, 0), fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    # BGR로 색추출
    bgrLower = np.array(font_color) - tolerance   # 추출할 색의 하한
    bgrUpper = np.array(font_color) + tolerance   # 추출할 색의 상한
    bgrResult = bgrExtraction(image_resized, bgrLower, bgrUpper)
    return bgrResult