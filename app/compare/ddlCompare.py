import os
import streamlit as st
from datetime import datetime
import tools.commands as cmd
from tools.sqllite import SessionLocal
import config.functions as func
import difflib
import re
import threading



# Testa os Endpoints
def test_connection(host, port, user, pwd, database):
    comando = f'mysql -h "{host}" -P {port} -u "{user}" --password="{pwd}" -D "{database}" -e "SELECT DATABASE();"'
    resultado = cmd.execute_command(comando)
    if resultado["return_code"] != 0:
        st.error(f"Erro ao conectar (código {resultado['return_code']}):")
        if resultado["error"]:
            st.code(resultado["error"], language="bash")
        else:
            st.warning("Sem mensagem de erro; verifique credenciais e rede.")
        return
    st.success(f"Conectado ao banco {database} com sucesso.")
    
# Deleta o arquivo de ddl apos a execução.
def clear_file(v_file_used):
    try:
        os.remove(v_file_used)
        return True
    except Exception as e:
        st.error(f"Erro ao deletar arquivo: {str(e)}")
        return False

# Exporta o DDL do banco de dados
def export_ddl(host, port, user, pwd, database, outputfile):
    v_command = f'mysqldump -h "{host}" -P {port} -u "{user}" --password="{pwd}" --no-data --skip-opt --skip-dump-date --skip-comments --no-create-db  --triggers --routines --set-gtid-purged=off --lock-tables=false "{database}"   > "{outputfile}"'
    result = cmd.execute_command(v_command)
    if result["return_code"] != 0:
        st.error(f"Erro ao exportar dump (código {result['return_code']}):")
        if result["error"]:
            st.code(result["error"], language="bash")
        else:
            st.warning("Sem mensagem de erro; verifique credenciais e rede.")
        return
    st.success(f"Banco {database} exportado com sucesso.")

# Função para  Sanitização das DDL para comparação 
def sanitize_file(sql: str) -> list[str]:
    auto_increment_pattern = re.compile(r"AUTO_INCREMENT=\d+\s*", flags=re.IGNORECASE)
    definer_pattern = re.compile(r"\sDEFINER=`[^`]*`@`[^`]*`", flags=re.IGNORECASE)
    cleaned = auto_increment_pattern.sub("", sql)
    cleaned = definer_pattern.sub("", cleaned)
    return cleaned.splitlines()

# Executa a Sanitização e comparação da DDLs
def compare_files(origin: str, target: str) -> None:
    if not os.path.exists(origin):
        st.error(f"Arquivo de origem não encontrado: {origin}")
        return

    if not os.path.exists(target):
        st.error(f"Arquivo de destino não encontrado: {target}")
        return

    with open(origin, "r", encoding="utf-8") as file_origin:
        origin_text = file_origin.read()
    with open(target, "r", encoding="utf-8") as file_target:
        target_text = file_target.read()    

    origin_lines = sanitize_file(origin_text)
    target_lines = sanitize_file(target_text)

    diff = difflib.unified_diff(
        origin_lines,
        target_lines,
        fromfile=f"origin: {origin}",
        tofile=f"target: {target}",
        lineterm="",
    )

    diff_text = "\n".join(diff)

    if diff_text:
        result = diff_text
        return result
    else:        
        return None
    


################################################ Layout ###########################################################
st.subheader('Mysql DDL Compare')


with st.container(border=True,key="origin"):
    st.header("Origin",divider=True)
    #Host/Port
    col1, col2 = st.columns(2)
    with col1:
        sessionorigin = SessionLocal()
        dfhostorigin = func.read_host(sessionorigin)
        dfhostorigin_values = [u.value for u in dfhostorigin]
        v_host_origin = st.selectbox("EndPoint Origin:  :red[*]",
                            dfhostorigin_values, index=None, accept_new_options=True,key="host_origin")
    with col2:
        v_port_origin = st.text_input("Port Origin: :red[*]", value="3306",key="port_origin")
    #User/Pwd/Database
    col1, col2, col3 = st.columns(3)
    with col1:
        v_dbauser_origin = st.text_input("User to Connect: :red[*]",key="user_origin")
    with col2:
        v_dbapwd_origin = st.text_input("Password to Connect: :red[*]", type="password",key="pwd_origin")
    with col3:
        v_database_origin = st.text_input("Database Origin: :red[*]",key="database_origin")    
    with st.container(horizontal=True,key="container_origin"):    
        if st.button("Test Connection Origin",key="test_connection_origin"):
            if v_host_origin and v_port_origin and v_dbauser_origin and v_dbapwd_origin and v_database_origin:
                test_connection(v_host_origin, v_port_origin, v_dbauser_origin, v_dbapwd_origin, v_database_origin)
            else:
                st.error("Preencha todos os campos.")




with st.container(border=True,key="target"):
    st.header("Target",divider=True)
    #Host/Port
    col1, col2 = st.columns(2)
    with col1:
        sessiontarget = SessionLocal()
        dfhosttarget = func.read_host(sessiontarget)
        dfhosttarget_values = [u.value for u in dfhosttarget]
        v_host_target = st.selectbox("EndPoint Target:  :red[*]",
                            dfhosttarget_values, index=None, accept_new_options=True,key="host_target")
    with col2:
        v_port_target = st.text_input("Port Target: :red[*]", value="3306",key="port_target")
    #User/Pwd/Database
    col1, col2, col3 = st.columns(3)
    with col1:
        v_dbauser_target = st.text_input("User to Connect: :red[*]",key="user_target")
    with col2:
        v_dbapwd_target = st.text_input("Password to Connect: :red[*]", type="password",key="pwd_target")
    with col3:
        v_database_target = st.text_input("Database Target: :red[*]",key="database_target")
    with st.container(horizontal=True,key="container_target"):
        if st.button("Test Connection Target",key="test_connection_target"):
            if v_host_target and v_port_target and v_dbauser_target and v_dbapwd_target and v_database_target:
                test_connection(v_host_target, v_port_target, v_dbauser_target, v_dbapwd_target, v_database_target)
            else:
                st.error("Preencha todos os campos.")



# Data e Hora para criação de arquivo unico
curdate = datetime.now().strftime("%Y%m%d%H%M")
main_repo = f'./outputdir/'

# ARQUIVOS
# Nome do arquivo de parametros
v_file_origin = f'{main_repo}origin_{v_database_origin}_{curdate}.sql'
v_file_target = f'{main_repo}target_{v_database_target}_{curdate}.sql'



if st.button("Execute Compare",key="execute_compare",type="primary"):
    st.session_state.generated_files = [v_file_origin, v_file_target]
    if v_host_origin and v_port_origin and v_dbauser_origin and v_dbapwd_origin and v_database_origin and v_host_target and v_port_target and v_dbauser_target and v_dbapwd_target and v_database_target:
     with st.spinner("Exportando DDL's e realizando comparação...",show_time=True):
        t1=threading.Thread(target=export_ddl, args=(v_host_origin, v_port_origin, v_dbauser_origin, v_dbapwd_origin, v_database_origin, v_file_origin))
        t2=threading.Thread(target=export_ddl, args=(v_host_target, v_port_target, v_dbauser_target, v_dbapwd_target, v_database_target, v_file_target))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        diff = compare_files(v_file_origin, v_file_target)        
        st.success("Comparações finalizadas com sucesso.")
        if diff:
            st.code(diff, language="diff")
            st.download_button(label="Download Diff", data=diff, file_name="comparacao.diff", mime="text/plain", key="download_diff",on_click="ignore")
        else: 
            st.success("Os arquivos são idênticos.")
    else:
        st.error("Preencha todos os campos.")

#Limpar arquivos
if st.session_state.get("generated_files"):
    if st.button("Clear Files", key="clear_files"):
        for path in st.session_state.generated_files:
            clear_result = clear_file(path)
            if clear_result:
                st.success(f"Arquivo {path} deletado com sucesso.")
            else:
                st.error(f"Erro ao deletar arquivo {path}.")
        st.session_state.generated_files = None
    