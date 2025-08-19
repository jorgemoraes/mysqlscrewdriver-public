import streamlit as st
import tools.db as db
import tools.passgen as passgen
from tools.sqllite import SessionLocal
import config.functions as func

st.subheader('Create or Reset Account')


session = SessionLocal()

with st.form("param_validate_user"):
    v_jira = st.text_input("Ticket: :red[*]")
    col1, col2 = st.columns(2)
    with col1:

        dfhost = func.read_host(session)
        dfhost_values = [u.value for u in dfhost]
        v_host = st.selectbox("EndPoint: :red[*]",
                              dfhost_values, index=None, accept_new_options=True)
        # v_host = st.text_input("EndPoint: ")
    with col2:
        v_port = st.text_input("Port: :red[*]", value="3306")

    col1, col2 = st.columns(2)
    with col1:
        v_dbauser = st.text_input("User to Connect: :red[*]")
    with col2:
        v_dbapwd = st.text_input(
            "Password to Connect: :red[*]", type="password")
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        v_username = st.text_input("User to Create/Reset: :red[*]")
    with col2:
        dfrole = func.read_role(session)
        dfrole_values = [u.value for u in dfrole]
        v_role = st.selectbox("Role IF New User: ", dfrole_values,
                              index=None, accept_new_options=True)
    # ToDo: Cadastro de roles e associação com atributos de roles
    v_password = passgen.generate_password(16, True, True, True, False, True)

    if v_role == "rl_dba":
        v_attributes = "default role "+v_role+""
    elif v_role == "rl_leitura":
        v_attributes = "default role "+v_role + \
            " with max_user_connections 5 password expire interval 180 day failed_login_attempts 10 password_lock_time 1 comment '" + v_jira + "'"
    else:
        v_attributes = ""
    # Todo Verificar se user já existe :
    comando_create = "create user %s@'%' IDENTIFIED WITH caching_sha2_password  BY %s " + v_attributes
    binds = (v_username, v_password)

    v_msgpwd = f'**Usuario**: {v_username} \n \n \n **Senha**: {v_password} \n \n \n'

    # Verifica se já existe uma mensagem customizada de boas vindas para o usuário
    v_cust_msg = func.read_msg(session)
    if v_cust_msg:
        v_msg = v_msgpwd + v_cust_msg[0].value
    else:
        v_msg = '''
                Você recebeu um usuário e senha de acesso. É fundamental seguir as recomendações de segurança abaixo para proteger suas credenciais:            

                1.  **Guarde seu usuário e senha em local seguro**. Não compartilhe essas informações com outras pessoas, evitando acessos não autorizados.

                2.  **A senha tem validade de 180 dias**. Caso a senha  esteja próximo a expirar ou expirada pedimos que entre em contato com o DBA ou o time de INFRA.
                    
                3.  **Não salve a senha em dispositivos públicos ou compartilhados** e evite anotá-la em locais expostos.                            
                    
                4.  **Atenção a tentativas de phishing**: nunca informe sua senha em respostas a e-mails suspeitos ou em links não confiáveis.
                
                O descumprimento dessas recomendações pode comprometer a segurança de seus dados e sistemas. 
                
                Agradecemos por seguir essas práticas para manter um ambiente seguro para todos.

                **Peço que informe ao visualizar essa mensagem pois ela será excluída**        
            '''

    st.divider()

    col1, col2 = st.columns(2)
    with col1:

        submitedd_create = st.form_submit_button("Create User")
        if submitedd_create:
            db.executar_comando_sql(
                v_host, v_port, v_dbauser, v_dbapwd, comando_create, binds)
            st.write(v_msg)

    with col2:
        comando_reset = "alter user %s@'%' IDENTIFIED WITH caching_sha2_password  BY %s "
        binds = (v_username, v_password)
        submitedd_reset = st.form_submit_button("Reset Password")
        if submitedd_reset:
            db.executar_comando_sql(
                v_host, v_port, v_dbauser, v_dbapwd, comando_reset, binds)
            st.write(v_msg)
