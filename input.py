import streamlit as st
import pandas as pd

st.title("input show")

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)



with col1:
     text11 = st.text_input('A11', )
     text21 = st.text_input('A21', )
     text31 = st.text_input('A31', )
with col2:
     text12 = st.text_input('A12', )
     text22 = st.text_input('A22', )
     text32 = st.text_input('A32', )

with col3:
      text13 = st.text_input('A13', )
      text23 = st.text_input('A23', )
      text33 = st.text_input('A33', )

with col4:
      st.text('|        |')
      st.text('|        |')
      st.text('|        |')
      st.text('|        |')
      st.text('|        |')
      st.text('|        |')
      st.text('|        |')
      st.text('|        |')
      


with col5:
     text15 = st.text_input('B11', )
     text25 = st.text_input('B21', )
     text35 = st.text_input('B31', )

with col6:
     text16 = st.text_input('B12', )
     text26 = st.text_input('B22', )
     text36 = st.text_input('B32', )

with col7:
      text17 = st.text_input('B13', )
      text27 = st.text_input('B23', )
      text37 = st.text_input('B33', )