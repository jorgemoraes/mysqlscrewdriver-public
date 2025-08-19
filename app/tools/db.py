import mysql.connector
from mysql.connector import Error
import streamlit as st


def validar_conexao(ihost, iport, iuser, ipass):
    try:
        conexao = mysql.connector.connect(
            host=ihost,
            port=iport,
            user=iuser,
            password=ipass
        )

        if conexao.is_connected():
            st.success("Conexão bem-sucedida!")
            info_bd = conexao.get_server_info()
            st.success(f"Conectado ao servidor MySQL versão {info_bd}")
        else:
            st.error("Falha na conexão.")

    except Error as e:
        st.error(f"Erro ao conectar ao MySQL: {e}")

    finally:
        if 'conexao' in locals() and conexao.is_connected():
            conexao.close()
            st.info("Conexão encerrada.")

# Chama a função para validar a conexão


def executar_comando_sql(host, port, user, password, comando_sql, binds):
    """
    Função para executar comandos SQL em um banco de dados MySQL.

    Parâmetros:
    host (str): O endereço do servidor MySQL.
    port (str): Porta personalizada
    user (str): O nome de usuário do banco de dados.
    password (str): A senha do banco de dados.
    database (str): O nome do banco de dados.
    comando_sql (str): O comando SQL a ser executado.

    Retorna:
    bool: True se o comando foi executado com sucesso, False caso contrário.
    """
    try:
        # Estabelece a conexão com o banco de dados
        conexao = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password
        )

        if conexao.is_connected():
            cursor = conexao.cursor()
            cursor.execute(comando_sql, binds)
            conexao.commit()  # Confirma as mudanças no banco de dados
            st.success("Comando executado com sucesso.")
            return True

    except Error as e:
        if mysql.connector.Error and e.errno == 1045:
            st.error("Erro de autenticação: Verifique o usuário e a senha.")
        elif mysql.connector.Error and e.errno == 1396:
            st.error("Usuário já existe. Tente outro nome de usuário.")
        else:
            st.error(f"Erro ao executar comando SQL: {e}")
        return False

    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()
