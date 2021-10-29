import cv2
import numpy as np
from matplotlib import pyplot as plt

# InputImage
#img_rgb = cv2.imread('img_data/gyouretu.png')
img_rgb = cv2.imread('img_data/Matrix.png')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
# templates
template1 = cv2.imread('img_data/LeftBracket.png', 0)
template2 = cv2.rotate(template1, cv2.ROTATE_180)

w0, h0 = img_gray.shape[::-1]
w1, h1 = template1.shape[::-1]
w2, h2 = template2.shape[::-1]
# テンプレート画像をリサイズする倍率
magnification = [1.0, 1.5, 0.8, 0.5, 2.0, 3.0, 1.2, 0.3]
for mag in magnification:
    # テンプレートマッチングが成功したらループを抜け出す
    successFlag1 = False
    successFlag2 = False
    # テンプレート画像(左括弧)のリサイズ
    template1A = template1.copy()
    template1A = cv2.resize(template1A, (int(w1*mag), int(h1*mag)))
    w1a, h1a = template1A.shape[::-1]
    # テンプレート画像(右括弧)のリサイズ
    template2A = template2.copy()
    template2A = cv2.resize(template2A, (int(w2*mag), int(h2*mag)))
    w2a, h2a = template2A.shape[::-1]
    # 入力画像がテンプレートの幅/高さよりも小さい場合を除外する
    if img_gray.shape[0] <= template1A.shape[0] or img_gray.shape[1] <= template1A.shape[1] :
        continue  
    if img_gray.shape[0] <= template2A.shape[0] or img_gray.shape[1] <= template2A.shape[1] :
        continue  
    print("倍率:", mag)
    print(img_gray.shape, template1A.shape, template2A.shape)
    # テンプレートマッチング
    res = cv2.matchTemplate(template1A, img_gray, cv2.TM_CCOEFF_NORMED)
    threshold = 0.6
    loc1 = np.where( res >= threshold)
    for pt in zip(*loc1[::-1]):
        print("LeftTop(×",mag,"):", pt)
        print("RightBottom(×",mag,"):", (pt[0] + w1a, pt[1] + h1a))
        cv2.rectangle(img_rgb, pt, (pt[0] + w1a, pt[1] + h1a), (0, 0, 255), 2)
        successFlag1 = True

    res = cv2.matchTemplate(template2A, img_gray, cv2.TM_CCOEFF_NORMED)
    threshold = 0.6
    loc2 = np.where( res >= threshold)
    for pt in zip(*loc2[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w2a, pt[1] + h2a), (0, 0, 255), 2)
        print("LeftTop(×",mag,"):", pt)
        print("RightBottom(×",mag,"):", (pt[0] + w2a, pt[1] + h2a))
        successFlag2 = True
    if successFlag1 == True and successFlag2 == True:
        print("OK")
        break
cv2.imwrite('res.png', img_rgb)