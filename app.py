import streamlit as st
from PIL import Image

import cv2
import numpy as np
from matplotlib import pyplot as plt

# 関数定義 入力画像を引数の座標だけ取り出し，表示するする
def CutImage(img, top, bottom, left, right, name):
    img2 = img.copy()
    img2 = img2[top : bottom, left : right]
    st.image(img2, caption="計算する行列の要素", use_column_width=True)
    #cv2.imwrite(name + '.png', img2)

st.title('行列検算アプリ MatCheck')

uploaded_file = st.file_uploader("画像を選んでください", type="png")
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    img_rgb = np.array(img, dtype=np.uint8)
    #img_rgb = cv2.imread()
    st.image(img_rgb, caption="入力画像", use_column_width=True)

    # InputImage
    #img_rgb = cv2.imread('img_data/gyouretu.png')
    #img_rgb = cv2.imread('img_data/Matrix.png')
    #img_rgb = cv2.imread('img_data/Object4.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    # templates
    template1 = cv2.imread('img_data/LeftBracket.png', 0)
    template2 = cv2.rotate(template1, cv2.ROTATE_180)

    w0, h0 = img_gray.shape[::-1]
    w1, h1 = template1.shape[::-1]
    w2, h2 = template2.shape[::-1]

    # テンプレート画像をリサイズする倍率
    magnification = [1.0, 1.5, 0.8, 0.5, 2.0, 3.0, 1.2, 0.3]
    # 切り取り座標(行列A)
    coordinatesA_top = 0
    coordinatesA_bottom = 0
    coordinatesA_left = 0
    coordinatesA_right = 0
    # 切り取り座標(行列B)
    coordinatesB_top = 0
    coordinatesB_bottom = 0
    coordinatesB_left = 0
    coordinatesB_right = 0

    firstFlag1 = True
    firstFlag2 = True

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
            if firstFlag1 : 
                coordinatesA_top = pt[1]
                coordinatesA_bottom = pt[1] + h1a
                coordinatesA_left = pt[0] + w1a
                firstFlag1 = False
            else :
                coordinatesB_top = pt[1]
                coordinatesB_bottom = pt[1] + h1a
                coordinatesB_left = pt[0] + w1a

            successFlag1 = True

        res = cv2.matchTemplate(template2A, img_gray, cv2.TM_CCOEFF_NORMED)
        threshold = 0.6
        loc2 = np.where( res >= threshold)
        for pt in zip(*loc2[::-1]):
            if firstFlag2 :
                coordinatesA_right = pt[0]
                firstFlag2 = False
            else :
                coordinatesB_right = pt[0]
            successFlag2 = True
        # 2つの行列を発見することができた場合
        if successFlag1 == True and successFlag2 == True:
            print("OK")
            CutImage(img_rgb, coordinatesA_top, coordinatesA_bottom, coordinatesA_left, coordinatesA_right, "matrix1")
            CutImage(img_rgb, coordinatesB_top, coordinatesB_bottom, coordinatesB_left, coordinatesB_right, "matrix2")
            break
