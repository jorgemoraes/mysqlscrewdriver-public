import streamlit as st
from sqlalchemy.orm import Session
from config.models import Config
from tools.sqllite import SessionLocal, init_db

init_db()

def create_config(session: Session, name: str, value: str):
    # Verifica duplicidade de nome+valor
    if session.query(Config).filter(Config.name == name, Config.value == value).first():
        st.error("Já existe uma configuração com esse nome e valor.")
        return
    config = Config(name=name, value=value)
    session.add(config)
    session.commit()
    st.success("Configuração criada com sucesso!")

def read_config(session: Session):
    return session.query(Config).all()

def update_config(session: Session, config_id: int, new_name: str, new_value: str):
    config = session.query(Config).filter(Config.id == config_id).first()
    if config:
        config.name = new_name
        config.value = new_value
        session.commit()
        st.success("Config atualizado com sucesso!")
    else:
        st.error("Configuração não encontrada.")

def delete_config(session: Session, config_id: int):
    config = session.query(Config).filter(Config.id == config_id).first()
    if config:
        session.delete(config)
        session.commit()
        st.success("Configuração deletada com sucesso!")
    else:
        st.error("Configuração não encontrada.")

# Interface
st.subheader("Configure Parameters")
menu = st.selectbox("Opção", ["Read", "Create", "Update", "Delete"])
session = SessionLocal()

if menu == "Create":
    st.subheader("Criar nova Configuração")
    name = st.selectbox("Nome", ["host", "role", "msg", "bucketS3"])
    value = st.text_area("Valor", height=100) if name == "msg" else st.text_input("Valor")
    if st.button("Criar"):
        if not name or not value:
            st.error("Preencha todos os campos.")
        else:
            create_config(session, name, value)

elif menu == "Read":
    st.subheader("Todas as Configurações")
    configs = read_config(session)
    if configs:
        st.table([{"ID": u.id, "Nome": u.name, "Valor": u.value} for u in configs])
    else:
        st.info("Nenhuma configuração encontrada.")

elif menu == "Update":
    st.subheader("Atualizar Configuração")
    configs = read_config(session)
    if not configs:
        st.info("Nenhuma configuração para atualizar.")
    else:
        config_dict = {f"{u.id} - {u.name}": u for u in configs}
        selected = st.selectbox("Selecione a configuração", list(config_dict.keys()))
        config = config_dict[selected]
        new_name = st.text_input("Novo nome", value=config.name)
        new_value = st.text_input("Novo valor", value=config.value)
        if st.button("Atualizar"):
            if not new_name or not new_value:
                st.error("Preencha todos os campos.")
            else:
                update_config(session, config.id, new_name, new_value)

elif menu == "Delete":
    st.subheader("Deletar Configuração")
    configs = read_config(session)
    if not configs:
        st.info("Nenhuma configuração para deletar.")
    else:
        config_dict = {f"{u.id} - {u.name}": u for u in configs}
        selected = st.selectbox("Selecione a configuração", list(config_dict.keys()))
        config = config_dict[selected]
        if st.button("Deletar"):
            if st.checkbox("Confirmar deleção"):
                delete_config(session, config.id)
            else:
                st.warning("Marque a caixa para confirmar a deleção.")