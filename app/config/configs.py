import streamlit as st
from sqlalchemy.orm import Session
from config.models import Config
from tools.sqllite import SessionLocal, init_db
import uuid

init_db()
session = SessionLocal()

st.title("Gestão de Configurações")
st.markdown("""
<style>
.stTable th, .stTable td {text-align: left !important;}
</style>
""", unsafe_allow_html=True)

def validate_config(name, value):
    errors = []
    if not name or len(name.strip()) < 2:
        errors.append("Nome da configuração deve ter pelo menos 2 caracteres.")
    if not value or len(str(value).strip()) < 1:
        errors.append("Valor da configuração não pode ser vazio.")
    return errors

def create_config(session: Session, name: str, value: str):
    if session.query(Config).filter(Config.name == name, Config.value == value).first():
        st.error("Já existe uma configuração com esse nome e valor.")
        return
    config = Config(name=name, value=value)
    session.add(config)
    session.commit()
    st.success("Configuração criada com sucesso!")

def read_configs(session: Session):
    return session.query(Config).all()

def update_config(session: Session, config_id: int, new_name: str, new_value: str):
    config = session.query(Config).filter(Config.id == config_id).first()
    if config:
        config.name = new_name
        config.value = new_value
        session.commit()
        st.success("Configuração atualizada com sucesso!")
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

tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Adicionar", "Atualizar", "Deletar"])

with tab1:
    st.subheader("Configurações cadastradas")
    configs = read_configs(session)
    if configs:
        st.table([{"ID": c.id, "Nome": c.name, "Valor": c.value} for c in configs])
    else:
        st.info("Nenhuma configuração cadastrada.")

with tab2:
    st.subheader("Adicionar Configuração")
    with st.form("add_form", clear_on_submit=True):
        config_dict = {f"{c.name}": c for c in configs}
        selected = st.selectbox("Selecione a configuração", list(config_dict.keys()), key="add_selectbox", accept_new_options=True)
        name = config_dict[selected].name
        value = st.text_area("Valor", height=80)
        submitted = st.form_submit_button("Adicionar")
        if submitted:
            errors = validate_config(name, value)
            if errors:
                for err in errors:
                    st.error(err)
            else:
                create_config(session, name, value)

with tab3:
    st.subheader("Atualizar Configuração")
    configs = read_configs(session)
    if not configs:
        st.info("Nenhuma configuração para atualizar.")
    else:
        config_dict = {f"{c.id} - {c.name} - {c.value}": c for c in configs}
        selected = st.selectbox("Selecione a configuração", list(config_dict.keys()), key="update_selectbox")
        config = config_dict[selected]
        new_name = st.text_input("Novo nome", value=config.name)
        new_value = st.text_area("Novo valor", value=config.value, height=80)
        if st.button("Atualizar"):
            errors = validate_config(new_name, new_value)
            if errors:
                for err in errors:
                    st.error(err)
            else:
                update_config(session, config.id, new_name, new_value)

with tab4:
    st.subheader("Deletar Configuração")
    configs = read_configs(session)
    if not configs:
        st.info("Nenhuma configuração para deletar.")
    else:
        config_dict = {f"{c.id} - {c.name} - {c.value}": c for c in configs}
        selected = st.selectbox("Selecione a configuração", list(config_dict.keys()), key="delete_selectbox")
        config = config_dict[selected]
        confirm = st.checkbox("Confirmar deleção")
        if confirm:
            if st.button("Deletar"):
                delete_config(session, config.id)
                st.rerun()
        else:
            st.warning("Marque a caixa para confirmar a deleção.")