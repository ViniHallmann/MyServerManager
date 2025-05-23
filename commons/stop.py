import boto3
from botocore.client import BaseClient
from commons.utils.aws          import AWSUtils 
from commons.utils.ssh          import SSHUtils 
from commons.configs            import load_config

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
    AWS: AWSUtils   = AWSUtils(ec2)
    
    try:
        if not AWS.is_instance_running( config["INSTANCE_ID"] ):
            print("Instância está parada.")
            return
        print("Instância está rodando.")

        ip: str = AWS.get_instance_ip( config["INSTANCE_ID"] )
        if ip == "IP não encontrado": raise ValueError("Não foi possível obter o IP da instância.")

        ### CRIAR COMANDO PARA VERIFICAR JANELA DO SERVIDOR ANTES

        print("Conectando ao servidor...")
        SSH: SSHUtils = SSHUtils(ip, config["KEY_PATH"], config["USER"])
        if not SSH.connect():
            print("Falha ao conectar via SSH.")
            return False
        
        print("Finalizando servidor...")
        
        response = SSH.execute_command( config["STOP_COMMAND"] )
        print(response)

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        if SSH:
            SSH.close()
            print("Conexão encerrada.")

def stop_instance() -> None:
    """
    Para a instância EC2.
    """
    config: dict = load_config()
    ec2: BaseClient = boto3.client("ec2")
    AWS: AWSUtils   = AWSUtils(ec2)
    try:
        if not AWS.is_instance_running( config["INSTANCE_ID"] ):
            print("Instância está parada.")
            return
        #PRECISA VERIFICAR SE O SERVIDOR ESTA RODANDO 
        AWS.stop_instance( config["INSTANCE_ID"])
        print("Instância parada.")

    except Exception as e:
        print(f"Erro: {e}")