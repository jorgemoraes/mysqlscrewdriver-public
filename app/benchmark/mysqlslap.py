import streamlit as st
import tools.commands as cmd
from tools.sqllite import SessionLocal
import config.functions as func


st.subheader('Run Slap Benchmark')
st.caption('mysqlslap é um programa de diagnóstico projetado para emular a carga do cliente para um servidor MySQL e para relatar o tempo de cada estágio. Ele funciona como se vários clientes estivessem acessando o servidor')

st.warning('Pré requisito para execução: Ter o MySQL Community Server instalado e variavel de ambiente **mysqlslap** configurada')

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

v_sql_clear1 = v_sql_input.replace("\n", " ")
v_sql_clear2 = v_sql_clear1.replace("`", "")

v_sql_final = v_sql_clear2.replace(";", "")
v_sql = v_sql_final
v_sql = "use "+v_database+"; "+v_sql
st.divider()


col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    v_concurrency = st.number_input("concurrency", 0, 130, 10)
    st.caption('Número de clientes a simular ao emitir a instrução SELECT')
with col2:
    v_iterations = st.number_input("iterations ", 0, 130, 10)
    st.caption('Número de vezes para executar os testes')
with col3:
    v_num_query = st.number_input("number of queries ", 0, 10000, 100)
    st.caption('Limite cada cliente a aproximadamente esse número de consultas')
with col4:    
    st.number_input("Total execuções estimadas", value=v_concurrency * v_iterations * v_num_query, disabled=True)
    st.caption('Total execuções estimadas' )
with col5:
    dryrun = st.checkbox("DryRun", value=False)

v_concurrency = str(v_concurrency)
v_iterations = str(v_iterations)
v_num_query = str(v_num_query)


submitedd_slap = st.button("Execute Slap")
# if dryrun:
#    stmt=" --only-print"
if submitedd_slap:
    execstatus = f' Executing "{v_sql}" with concurrency={v_concurrency} iterations={v_iterations} on schema="{v_database}" x times ={v_num_query}'

    with st.status(execstatus, expanded=True, state="running")as status:
        stmt = f'mysqlslap --user="{v_dbauser}"  --password="{v_dbapwd}" --host="{v_host}" --port="{v_port}" --concurrency={v_concurrency} --iterations={v_iterations} --create-schema="{v_database}" --no-drop --number-of-queries={v_num_query} --query="{v_sql}" --verbose'
        if dryrun:
            stmt = stmt+" --only-print"
        # st.write(stmt)
        result = cmd.execute_command(stmt)

        st.success('--- Command Output ---', icon=None)
        st.code(result["output"], language="python")

        st.error('--- Command Error ---', icon=None)
        st.code(result["error"], language="python")

        st.info('--- Return Code ---', icon=None)
        st.code(result["return_code"], language="python")

        status.update(
            label="Execute complete!", state="complete", expanded=True
        )
