import os
import streamlit as st
from datetime import datetime
import tools.commands as cmd
from tools.sqllite import SessionLocal
import config.functions as func

st.subheader('Table Local Backup')

st.warning(
    'Export será realizado na base indicada, acompanhar a performance do ambiente')

col1, col2 = st.columns(2)
with col1:
    session = SessionLocal()
    dfhost = func.read_host(session)
    dfhost_values = [u.value for u in dfhost]
    v_host = st.selectbox("EndPoint:  :red[*]",
                          dfhost_values, index=None, accept_new_options=True)
with col2:
    v_port = st.text_input("Port: :red[*]", value="3306")

col1, col2 = st.columns(2)
with col1:
    v_dbauser = st.text_input("User to Connect: :red[*]")
with col2:
    v_dbapwd = st.text_input("Password to Connect: :red[*]", type="password")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    v_database = st.text_input("Database: :red[*]")
with col2:
    v_table = st.text_input("Table or View: :red[*]")
with col3:
    v_column = st.text_input("Where ex:    **id_column = 10**")
if not v_column:
    v_column = "1=1"
with col4:
    v_cfilename = st.text_input("bkp_:blue[custom_filename]_datetime")
with col5:
    v_compression = st.checkbox("Use Compress", value=False)


# Data e Hora para criação de arquivo unico
curdate = datetime.now().strftime("%Y%m%d%H%M")
main_repo = f'./outputdir/'

# ARQUIVOS
# Nome do arquivo de parametros
v_file_param = main_repo+"param_"+v_table+"_"+curdate+".js"

v_file_backup = f'{main_repo}bkp_{v_cfilename}_{curdate}' if v_cfilename else f'bkp_{v_table}_{curdate}'

if v_compression:
    # Nome do arquivo de backup comprimido
    v_file_backup = v_file_backup+".gz"
else:
    v_file_backup = v_file_backup+".csv"


# Deleta o arquivo de parametros se existir.
def del_file_param():
    if os.path.exists(v_file_param):
        os.remove(v_file_param)


# Cria o conteúdo do arquivo de parametros
def criar_arquivo_param(v_file_param):
    conteudo = f"""util.exportTable("{v_database}.{v_table}","{v_file_backup}",{{
    where: "{v_column}",
    dialect: "csv",
    showProgress: true,
    defaultCharacterSet: "utf8mb4",
    fieldsOptionallyEnclosed: true,
    fieldsTerminatedBy: ",",
    linesTerminatedBy: "\\n",
    fieldsEnclosedBy: '"',
    maxRate: "100M"{',compression:"gzip"' if v_compression else ''}
    }});
    """
    # Cria e escreve no arquivo
    with open(v_file_param, 'w') as arquivo:
        arquivo.write(conteudo)
    return v_file_param


submitedd_backup = st.button("Execute Backup")
if submitedd_backup:
    if not v_dbauser or not v_dbapwd or not v_database:
        st.error("Por favor, preencha todos os campos obrigatórios.")
        st.stop()
    execstatus = f' Executando backup da tabela "{v_table}" no banco "{v_database}"'

    with st.status(execstatus, expanded=True, state="running")as status:
        v_command = f"mysqlsh {v_dbauser}@{v_host}:{v_port} -p\"{v_dbapwd}\" --save-passwords=never --js --file={criar_arquivo_param(v_file_param)}"
        # debug: st.write(v_command)
        try:
            result = cmd.execute_command(v_command)
        except Exception as e:
            st.error(f"Erro ao executar o comando: {str(e)}")
            st.stop()

        st.success('--- Command Output ---', icon=None)
        st.code(result["output"], language="python")

        st.error('--- Command Error ---', icon=None)
        st.code(result["error"], language="python")

        st.info('--- Return Code ---', icon=None)
        st.code(result["return_code"], language="python")

        status.update(
            label="Execute complete!         Confira os detalhes da execução ---->>> ", state="complete", expanded=False
        )

        del_file_param()

        # st.page_link(v_download, label="Home", icon="🏠")
        st.link_button("Download", v_file_backup)
