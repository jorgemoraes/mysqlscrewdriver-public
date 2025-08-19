import os
import platform
import subprocess


def execute_command(command):
    """
    Execute a system command and return output, error, and return code.

    Args:
        command (str): The command to execute.

    Returns:
        dict: A dictionary containing the output, error, and return code.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )
        return {
            "output": result.stdout.strip(),
            "error": result.stderr.strip(),
            "return_code": result.returncode
        }
    except Exception as e:
        return {
            "output": "",
            "error": str(e),
            "return_code": -1
        }


def gerar_url_presinada(v_arquivo, v_expiretime=604800):
    """
    Gera uma URL pré-assinada para um objeto S3 usando AWS CLI.

    Args:
        bucket (str): Nome do bucket S3.
        v_arquivo (str): Caminho/arquivo dentro do bucket.
        v_expiretime (int): Tempo de expiração da URL, em segundos (padrão: 604800 = 7 dias).

    Returns:
        str: URL pré-assinada, ou None se houver erro.
    """
    cmd = [
        'aws', 's3', 'presign',
        f'{v_arquivo}',
        '--expires-in', str(v_expiretime)
    ]

    try:
        resultado = subprocess.run(
            cmd, capture_output=True, text=True, check=True)
        return resultado.stdout.strip()
    except subprocess.CalledProcessError as e:
        return {
            "output": "",
            "error": str(e),
            "return_code": -1
        }


def run_docker_mysqlsh(container_name, user, password, host, port, stmt):
    """
    Executa o comando docker exec para iniciar o mysqlsh no container especificado.

    Exemplo de comando:
    docker exec -it mysqlsh_client mysqlsh --uri user:password@host:3306 <stmt>
    """
    # Monta a URI de conexão
    uri = f"{user}:{password}@{host}:{port} {stmt}"
    # Prepara o comando conforme o formato desejado
    cmd = ["docker", "exec", "-it", container_name, "mysqlsh", "--uri", uri]

    try:
        # Executa o comando e captura a saída (stdout e stderr)
        result = subprocess.run(
            cmd, capture_output=True, text=True, check=True)
        print("Saída do comando:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Erro ao executar o comando:")
        print(e.stderr)


# def run_docker_mysqlsh2(container_name, user, password, host, port, stmt):
#     """
#     Executa o comando docker exec para iniciar o mysqlsh no container especificado.

#     Exemplo de comando:
#     docker exec -it mysqlsh_client mysqlsh --uri user:password@host:3306 <stmt>
#     """
#     # Monta a URI de conexão
#     uri = f"{user}:{password}@{host}:{port} {stmt}"
#     # Prepara o comando conforme o formato desejado
#     cmd = f'mysqlsh --uri {uri}'

#     try:
#         client = docker.from_env()
#         container = client.containers.run(container_name, detach=True)
#         exec_result = container.exec_run(cmd)
#     except subprocess.CalledProcessError as e:
#         return {exec_result.output.decode('utf-8')}
