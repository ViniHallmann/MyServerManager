import boto3
from botocore.client    import BaseClient
from commons.utils.aws          import AWSUtils 
from commons.utils.ssh          import SSHUtils 
from commons.configs            import load_config


def check_instance_status() -> None:
    
    config: dict = load_config()
    ec2: BaseClient = boto3.client("ec2")
    AWS = AWSUtils(ec2)

    try:
        response = AWS.verify_instance_state( config["INSTANCE_ID"] )
        print(f"Estado da instância: {response}")

    except Exception as e:
        print(f"Erro ao verificar estado da instância: {e}")
        return None, None

def check_server_status() -> None:
    config: dict = load_config()
    ec2: BaseClient = boto3.client("ec2")
    AWS: AWSUtils   = AWSUtils(ec2)

    try:
        if not AWS.is_instance_running( config["INSTANCE_ID"] ):
            print("Instância está parada.")
            return

        ip: str = AWS.get_instance_ip( config["INSTANCE_ID"] )
        if ip == "IP não encontrado": raise ValueError("Não foi possível obter o IP da instância.")

        print("Conectando ao servidor...")
        SSH: SSHUtils = SSHUtils(ip, config["KEY_PATH"], config["USER"])
        if not SSH.connect():
            print("Falha ao conectar via SSH.")
            return False

        print("Verificando status do servidor...")
        response = SSH.execute_command( config["STATUS_COMMAND"] )
        print(response)

    except Exception as e:
        print(f"Erro: {e}")



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