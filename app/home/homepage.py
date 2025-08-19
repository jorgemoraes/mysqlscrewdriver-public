import streamlit as st

# Título da Home Page
st.subheader("📄 Documentação")

# Lê o conteúdo do README.md
with open("./home/homepage.md", "r", encoding="utf-8") as file:
    readme_content = file.read()

# Exibe o conteúdo com renderização Markdown
st.markdown(readme_content, unsafe_allow_html=True)
