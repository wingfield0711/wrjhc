import streamlit as st
import streamlit.components.v1 as components

# 设置页面全屏，去掉多余的留白
st.set_page_config(page_title="无人机航测规划器", layout="wide")

# 隐藏 Streamlit 自带的多余菜单和页眉
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .block-container {padding-top: 0rem; padding-bottom: 0rem;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 读取本地的 HTML 文件并展示
with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# 设定一个足够大的高度，防止网页被截断
components.html(html_content, height=1200, scrolling=True)