import streamlit as st


st.set_page_config(page_title=None, page_icon=None,
                   layout="wide", initial_sidebar_state="expanded")

st.title('Mysql ScrewDriver')

pages = {
    "Home": [
        st.Page("home/homepage.py", title="Home"),
    ],
    "Settings": [
        st.Page("config/configs.py", title="Configure Parameters"),
    ],
    "Account": [
        st.Page("account/create_account.py", title="Create or Reset Account"),
    ],
    "Backup Table": [
        st.Page("exporttable/backupcli_local.py", title="Table Local Backup"),
        st.Page("exporttable/backupcli_S3.py", title="Table S3 Backup"),
    ],
    "Performance Tests": [
        st.Page("benchmark/mysqlslap.py", title="Run Slap Benchmark"),
    ],
    "Documentation": [
        st.Page("document/schemaspy.py", title="Generate with SchemaSpy"),
    ],
}

pg = st.navigation(pages, position="top", expanded=True)
pg.run()
