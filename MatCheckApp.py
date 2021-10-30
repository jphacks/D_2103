import streamlit as st
from PIL import Image
import cv2
import numpy as np
import numpy.linalg as LA # linalgモジュールはLAとしてimportするのが慣例。
import pyocr
import pyocr.builders
import os
import re


# 関数定義 入力画像を引数の座標だけ取り出し，返す
def CutImage(img, top, bottom, left, right, name):
    img2 = img.copy()
    img2 = img2[top : bottom, left : right]
    #st.image(img2, caption="計算する行列の要素", use_column_width=True)
    return img2

st.title('行列検算アプリ MatCheck')
st.header("LaTeX画像による認識")
uploaded_file = st.file_uploader("画像(.png)を選択してください。", type="png")
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    img_rgb = np.array(img, dtype=np.uint8)
    st.image(img_rgb, caption="入力画像", use_column_width=True)

    # InputImage
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
            #print("OK")
            PreprocessedImage1 = CutImage(img_rgb, coordinatesA_top, coordinatesA_bottom, coordinatesA_left, coordinatesA_right, "matrix1")
            PreprocessedImage2 = CutImage(img_rgb, coordinatesB_top, coordinatesB_bottom, coordinatesB_left, coordinatesB_right, "matrix2")
            break
        
    # OCRによる読み取りを行う
    # インストール済みのTesseractへパスを通す
    path_tesseract = os.getcwd() + "\lib"
    if path_tesseract not in os.environ["PATH"].split(os.pathsep):
        os.environ["PATH"] += os.pathsep + path_tesseract 

    # #グレースケールに変更
    # image_path = r'C:\Users\tatsuya\Desktop\code\python\eq_rec\gyouretu.png'
    # gray = cv2.imread(image_path, 0)
    # cv2.imwrite('gray_image.png', gray)
    
    # OCRエンジンの取得
    tools = pyocr.get_available_tools()
    print(tools)
    tool = tools[0]
    
    # 画像の読み込み。
    img_org1 = Image.fromarray(PreprocessedImage1)
    img_org2 = Image.fromarray(PreprocessedImage2)

    # OCRの実行
    builder = pyocr.builders.WordBoxBuilder(tesseract_layout=6)
    # builder = pyocr.builders.TextBuilder(tesseract_layout=6)
    result1 = tool.image_to_string(img_org1, lang="eng", builder=builder)
    result2 = tool.image_to_string(img_org2, lang="eng", builder=builder)

    # 識別した行列を確認する
    st.subheader("識別した行列")
    st.markdown("行列A")
    col1A, col2A = st.columns(2)
    st.markdown("行列B")
    col1B, col2B = st.columns(2)
    with col1A:
        matA11 = st.text_input('A11', value=re.sub('[^0-9]*', '', result1[0].content))
        matA21 = st.text_input('A21', value=re.sub('[^0-9]*', '', result1[2].content))
    with col2A:
        matA12 = st.text_input('A12', value=re.sub('[^0-9]*', '', result1[1].content))
        matA22 = st.text_input('A22', value=re.sub('[^0-9]*', '', result1[3].content))
    with col1B:
        matB11 = st.text_input('B11', value=re.sub('[^0-9]*', '', result2[0].content))
        matB21 = st.text_input('B21', value=re.sub('[^0-9]*', '', result2[2].content))
    with col2B:
        matB12 = st.text_input('B12', value=re.sub('[^0-9]*', '', result2[1].content))
        matB22 = st.text_input('B22', value=re.sub('[^0-9]*', '', result2[3].content))
    
    #演算を選択
    ope = st.radio("行う演算を選択", ('和','差', '内積', '固有値/固有ベクトル'))
    # 確認ボタン
    ConfirmedClick = st.button("確認")
    # 数字か判定
    if re.search('[0~9]+', matA11) == False:
        ConfirmedClick = False
    if re.search('[0~9]+', matA12) == False:
        ConfirmedClick = False
    if re.search('[0~9]+', matA21) == False:
        ConfirmedClick = False
    if re.search('[0~9]+', matA22) == False:
        ConfirmedClick = False
    if re.search('[0~9]+', matB11) == False:
        ConfirmedClick = False
    if re.search('[0~9]+', matB12) == False:
        ConfirmedClick = False
    if re.search('[0~9]+', matB21) == False:
        ConfirmedClick = False
    if re.search('[0~9]+', matB22) == False:
        ConfirmedClick = False
    # 数字の確認がとれた場合
    if  ConfirmedClick == True :
        # int型への変換を行う
        matA11 = (int)(matA11)
        matA12 = (int)(matA12)
        matA21 = (int)(matA21)
        matA22 = (int)(matA22)
        matB11 = (int)(matB11)
        matB12 = (int)(matB12)
        matB21 = (int)(matB21)
        matB22 = (int)(matB22)
        #演算を行う
        if ConfirmedClick == True :
            
            if ope == '和':

                e = np.array([[matA11, matA12], [matA21, matA22]])
                f = np.array([[matB11, matB12], [matB21, matB22]]) #２つの行列の足し算

                g = e + f

                st.write(g)
                print(g)

            elif ope == '差':
                
                h = np.array([[matA11, matA12], [matA21, matA22]])
                i = np.array([[matB11, matB12], [matB21, matB22]]) #２つの行列の引き算
                j = h - i

                st.write(j)
                print(j)

            elif ope == '内積':
                a = np.array([[matA11, matA12], [matA21, matA22]])
                b = np.array([[matB11, matB12], [matB21, matB22]])
                np.dot(a,b) #行列の内積

                print(np.dot(a,b))
                st.write(np.dot(a,b))


            elif ope == '固有値/固有ベクトル':
                
                d1 = np.array([[matA11, matA12], [matA21, matA22]])
                d2 = np.array([[matB11, matB12], [matB21, matB22]])

                w1,v1 = LA.eig(d1) # この場合ではwが固有値、vが固有ベクトルに相当する。
                w2,v2 = LA.eig(d2)
                
                st.write('固有値')
                st.write(w1)
                st.write(w2)
                st.write('固有ベクトル')
                st.write(v1)
                st.write(v2)

if uploaded_file is None:
    st.header("キーボード入力による演算")
    st.subheader("行列Aと行列Bを定義")

    col1, col2, col3, col4, col5, = st.columns(5)



    with col1:
        text11 = st.text_input('A11', )
        text21 = st.text_input('A21', )
        

    with col2:
        text12 = st.text_input('A12', )
        text22 = st.text_input('A22', )
        

    with col3:
        st.text('|          |')
        st.text('|          |')
        st.text('|          |')
        st.text('|          |')
        st.text('|          |')
        st.text('|          |')
        

    with col4:
        text15 = st.text_input('B11', )
        text25 = st.text_input('B21', )

    with col5:
        text16 = st.text_input('B12', )
        text26 = st.text_input('B22', )


    #0は足し算、1は引き算、2は内積、3は外積、その他は固有値、固有ベクトル

    matrix = st.radio("行う演算を選択して下さい。",('和', '差', '内積', '固有値/固有ベクトル'))
    # 確認ボタン
    ConfirmedClick2 = st.button("確認")

    if ConfirmedClick2 == True :

        if matrix == '和':
            text11 = int(text11)
            text21 = int(text21)
            text12 = int(text12)
            text22 = int(text22)
            text15 = int(text15)
            text25 = int(text25)
            text16 = int(text16)
            text26 = int(text26)

            e = np.array([[text11, text12], [text21, text22]])
            f = np.array([[text15, text16], [text25, text26]]) #２つの行列の足し算

            g = e + f

            st.write(g)
            print(g)

        elif matrix == '差':
            text11 = int(text11)
            text21 = int(text21)
            text12 = int(text12)
            text22 = int(text22)
            text15 = int(text15)
            text25 = int(text25)
            text16 = int(text16)
            text26 = int(text26)

            h = np.array([[text11, text12], [text21, text22]])
            i = np.array([[text15, text16], [text25, text26]]) #２つの行列の引き算
            j = h - i

            st.write(j)
            print(j)

        elif matrix == '内積':
            text11 = int(text11)
            text21 = int(text21)
            text12 = int(text12)
            text22 = int(text22)
            text15 = int(text15)
            text25 = int(text25)
            text16 = int(text16)
            text26 = int(text26)

            a = np.array([[text11, text12], [text21, text22]]) #中に数字を入れる
            b = np.array([[text15, text16], [text25, text26]])
            np.dot(a,b) #行列の内積

            print(np.dot(a,b))
            st.write(np.dot(a,b))


        elif matrix == '固有値/固有ベクトル':
            text11 = int(text11)
            text21 = int(text21)
            text12 = int(text12)
            text22 = int(text22)
            text15 = int(text15)
            text25 = int(text25)
            text16 = int(text16)
            text26 = int(text26)
            
            d1 = np.array([[text11 ,text12], [text21, text22]]) # 2×2の行列で試す。
            d2 = np.array([[text15 ,text16], [text25, text26]])


            w1,v1 = LA.eig(d1) # この場合ではwが固有値、vが固有ベクトルに相当する。
            w2,v2 = LA.eig(d2)
            
            st.write('固有値')
            st.write(w1)
            st.write(w2)
            st.write('固有ベクトル')
            st.write(v1)
            st.write(v2)
