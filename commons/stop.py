import boto3
from botocore.client import BaseClient
import commons.utils.aws     as AWS
import commons.utils.ssh as SERVER
from commons.configs import load_config

def terminate() -> None:
    """
    Para o servidor e depois a instância EC2.
    """
    config: dict = load_config()
    ec2: BaseClient = boto3.client("ec2")
    ssh = None
    
    try:
        stop_server()
        stop_instance()

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        if ssh:
            ssh.close()
            print("Conexão encerrada.")

def stop_server() -> None:
    """
    Para o servidor do zomboid.
    """
    config: dict = load_config()
    ec2: BaseClient = boto3.client("ec2")
    ssh = None
    try:
        if not AWS.is_instance_running(ec2, config["INSTANCE_ID"]):
            print("Instância está parada.")
            return
        print("Instância está rodando.")

        ip: str = AWS.get_instance_ip(ec2, config["INSTANCE_ID"])
        if ip == "IP não encontrado": raise ValueError("Não foi possível obter o IP da instância.")

        ### CRIAR COMANDO PARA VERIFICAR JANELA DO SERVIDOR ANTES

        print("Conectando ao servidor...")
        ssh = SERVER.connect_ssh(ip, config["KEY_PATH"], config["USER"])
        
        print("Finalizando servidor...")
        SERVER.execute_command(ssh, config["STOP_COMMAND"])

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        if ssh:
            ssh.close()
            print("Conexão encerrada.")

def stop_instance() -> None:
    """
    Para a instância EC2.
    """
    config: dict = load_config()
    ec2: BaseClient = boto3.client("ec2")
    try:
        if not AWS.is_instance_running(ec2, config["INSTANCE_ID"]):
            print("Instância está parada.")
            return
        #PRECISA VERIFICAR SE O SERVIDOR ESTA RODANDO 
        AWS.stop_instance(ec2, config["INSTANCE_ID"])
        print("Instância parada.")

    except Exception as e:
        print(f"Erro: {e}")