import numpy as np
import cv2 
import imutils
import pytesseract
import pandas as pd
import time

def process_image(image_path):
    # Read image
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    img = imutils.resize(img, width=500)
    cv2.imshow(image_path, img)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply bilateral filter
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    # Apply Canny edge detection
    edged = cv2.Canny(gray, 170, 200)

    # Find contours
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30] 
    NumberPlateCnt = None 

    count = 0
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:  
            NumberPlateCnt = approx 
            break

    # Mask the part other than the number plate
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [NumberPlateCnt], 0, 255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)
    cv2.namedWindow("Final_image", cv2.WINDOW_NORMAL)
    cv2.imshow("Final_image", new_image)

    # Configuration for Tesseract
    tess_config = ('-l eng --oem 1 --psm 3')

    # Run Tesseract OCR on image
    text = str(pytesseract.image_to_string(new_image, config=tess_config))

    # Data is stored in CSV file
    with open('data.csv', 'a') as csv_file:
        csv_file.write(f'{time.asctime(time.localtime(time.time()))},{text}\n')

    # Print recognized text
    print(text)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    image_path = 'images/10.jpg'
    process_image(image_path)
