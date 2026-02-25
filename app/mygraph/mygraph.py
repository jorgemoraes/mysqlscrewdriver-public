import streamlit as st
from datetime import datetime
import tools.commands as cmd
from tools.sqllite import SessionLocal
import config.functions as func
import subprocess
import os
import base64
import streamlit.components.v1 as components


def valida_variable(host, port, user, pwd, database):
    comando = f'mysql -h "{host}" -P {port} -u "{user}" -p\"{pwd}\" -D "{database}" -e "select @@explain_json_format_version;"'
    resultado = cmd.execute_command(comando)
    if resultado["output"].strip().split()[-1] != "2":
        st.error(f"Deve ser usada a versão 2 do Explain JSON Format")
        return
    pass


def render_svg(svg_file):
    with open(svg_file, "r") as f:
        lines = f.readlines()
        svg = "".join(lines)

        """Renders the given svg string."""
        b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
        html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
        return html
        

st.subheader('Explain Analyze MySQL Statement')

st.warning('Explain será realizado na base indicada, acompanhar a performance do ambiente')


col1, col2 = st.columns(2)
with col1:
    session = SessionLocal()
    dfhost = func.read_host(session)
    dfhost_values = [u.value for u in dfhost]
    v_host = st.selectbox("EndPoint: :red[*]",
                          dfhost_values, index=None, accept_new_options=True)
with col2:
    v_port = st.text_input("Port: :red[*]", value="3306")

col1, col2, col3 = st.columns(3)
with col1:
    v_dbauser = st.text_input("User to Connect: :red[*]")
with col2:
    v_dbapwd = st.text_input("Password to Connect: :red[*]", type="password")
with col3:
    v_database = st.text_input("Database: :red[*]")
v_sql_input = st.text_area("Statement to test: ", height=200)

v_sql = v_sql_input.replace("\n", " ")
v_sql = v_sql.replace("`", "")
v_sql = v_sql.replace(";", "")
v_sql = "EXPLAIN ANALYZE FORMAT=JSON "+v_sql

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

v_sql_digest = f"sql_{v_host}_{v_database}_{timestamp}"

# Usar caminhos absolutos para evitar problemas com cwd
base_dir = os.path.abspath(os.path.dirname(__file__))
app_dir = os.path.dirname(base_dir)

perl_script_path = os.path.join(base_dir, "mysql-explain.pl")
input_file = os.path.join(app_dir, "outputdir", f"{v_sql_digest}.json")
output_file = os.path.join(app_dir, "outputdir", f"{v_sql_digest}.svg")

# Usar string shell com caminhos absolutos
gengraph = f'perl "{perl_script_path}" "{input_file}" > "{output_file}"'



### Execute 

submitedd_explain = st.button("Execute Explainer")
if submitedd_explain:    
    execstatus = f' Executando explain analyze na base  schema="{v_database}" com usuario {v_dbauser}'
    if v_host and v_port and v_dbauser and v_dbapwd and v_database:
        valida_variable(v_host, v_port, v_dbauser, v_dbapwd, v_database)
    else:
        st.error("Preencha todos os campos.")

    with st.status(execstatus, expanded=True, state="running")as status:
        stmt = f'mysql -h {v_host} -P {v_port} -p\"{v_dbapwd}\" -D {v_database} -u {v_dbauser} -N -B --raw -e "{v_sql}" > "./outputdir/{v_sql_digest}.json"'        
        try:
            result = cmd.execute_command(stmt)    
        except Exception as e:
            st.error(f"Erro ao executar o comando: {str(e)}")
            st.stop()                
        
        try:
            result = subprocess.run(gengraph, shell=True, capture_output=True, text=True, cwd="./mygraph")
            if result.returncode != 0:
                st.error(f"Erro ao gerar SVG: {result.stderr}")
            else:
                st.session_state.generated_files = [output_file]
                with open(output_file, "rb") as file:
                    st.session_state.svg_content = file.read()
                st.session_state.svg_filename = v_sql_digest + ".svg"
                st.session_state.auto_download = True
        except Exception as e:
            st.error(f"Erro ao executar o comando: {str(e)}")
            st.stop()

        st.success('--- Command Output ---', icon=None)
        st.code(result.stdout, language="python")

        st.error('--- Command Error ---', icon=None)
        st.code(result.stderr, language="python")

        st.info('--- Return Code ---', icon=None)
        st.code(result.returncode, language="python")

        status.update(
            label="Execute complete!", state="complete", expanded=False
        )

# Read the SVG file content
if st.session_state.get("generated_files"):
    st.download_button(
        label="Download FlameGraph",
        data=st.session_state.svg_content,
        file_name=st.session_state.svg_filename,
        mime="image/svg+xml",
        key="download_flamegraph",
        on_click="ignore",
    )

    if st.session_state.get("auto_download"):
        b64 = base64.b64encode(st.session_state.svg_content).decode("utf-8")
        components.html(
            f"""
            <a id="autoDl" href="data:image/svg+xml;base64,{b64}" download="{st.session_state.svg_filename}" style="display:none;"></a>
            <script>
              const a = document.getElementById('autoDl');
              if (a) a.click();
            </script>
            """,
            height=0,
            width=0,
        )
        st.session_state.auto_download = False

    b64 = base64.b64encode(st.session_state.svg_content).decode("utf-8")
    components.html(
        f"""
        <iframe
          src="data:image/svg+xml;base64,{b64}"
          style="width: 100%; height: 700px; border: 1px solid #ddd; border-radius: 6px;"
        ></iframe>
        """,
        height=700,
    )

    st.session_state.generated_files = None

