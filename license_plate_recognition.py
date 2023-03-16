# setup
import cv2
import numpy as np
import base64
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = 'S:\\Tesseract-OCR\\tesseract.exe'


# recognize method
def recognize(base64_image):
    # Extract the encoded data portion of the string
    # image_data = base64_image.split(',')[1]
    # Decode the base64 data into a binary format
    image_binary = base64.b64decode(base64_image)
    # Convert the binary data to a numpy array
    image_array = np.frombuffer(image_binary, dtype=np.uint8)
    # Open image using OpenCV
    original_image = cv2.imdecode(image_array, flags=cv2.IMREAD_COLOR)
    # Gray image
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("greyed image", gray_image)
    cv2.waitKey(0)
    # Smoothen image
    gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)
    # cv2.imshow("smoothened image", gray_image)
    # cv2.waitKey(0)
    # Edge detection
    edged_image = cv2.Canny(gray_image, 30, 200)
    # cv2.imshow("edged image", edged_image)
    # cv2.waitKey(0)
    # Find contours
    cnts, new = cv2.findContours(edged_image.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    image1 = original_image.copy()
    cv2.drawContours(image1, cnts, -1, (0, 255, 0), 3)
    # cv2.imshow("contours", image1)
    # cv2.waitKey(0)
    # Sort contours
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
    screenCnt = None
    image2 = original_image.copy()
    cv2.drawContours(image2, cnts, -1, (0, 255, 0), 3)
    # cv2.imshow("Top 30 contours", image2)
    # cv2.waitKey(0)
    # Find the contour with 4 corners and crop it
    i = 7
    for c in cnts:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
        if len(approx) == 4:
            screenCnt = approx

            x, y, w, h = cv2.boundingRect(c)
            new_img = original_image[y:y + h, x:x + w]
            cv2.imwrite('./' + str(i) + '.png', new_img)
            i += 1
            break
    # Draw the contour
    try:
        cv2.drawContours(image1, [screenCnt], -1, (0, 255, 0), 3)
    except:
        return None
    # cv2.imshow("image with detected license plate", image1)
    # cv2.waitKey(0)
    # Recognize the license plate
    Cropped_loc = './7.png'
    # cv2.imshow("cropped", cv2.imread(Cropped_loc))
    plate_num = pytesseract.image_to_string(Cropped_loc, lang='eng')
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # Treat plate with regex
    treated_plate_num = re.sub(r'[^A-Za-z0-9+$]', '', plate_num)
    # Check for a danish license plate, to increase the accuracy of recognition
    danish_plate_num = extract_danish_license_plate(treated_plate_num)
    if danish_plate_num:
        print(danish_plate_num)  # Output: DK12345
    else:
        print("No license plate found.")
    return danish_plate_num


def extract_danish_license_plate(text):
    pattern = r'[A-Z]{2}\d{5}'
    match = re.search(pattern, text)
    if match:
        return match.group()
    else:
        return None
