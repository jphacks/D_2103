import streamlit as st
from PIL import Image

st.title('feature_ImageInput')

uploaded_filie = st.file_uploader("画像を選んでください", type="jpg")
if uploaded_filie is not None:
    img = Image.open(uploaded_filie)
    st.image(img, caption="Uploaded Image", use_column_width=True)
    