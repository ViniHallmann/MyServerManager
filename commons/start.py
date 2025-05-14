import boto3
from botocore.client    import BaseClient
from commons.utils.aws          import AWSUtils 
from commons.utils.ssh          import SSHUtils 
from commons.configs            import load_config

#todo: criar função para verificar janela do servidor antes de iniciar o servidor

def start_instance() -> None:
    """
    Inicializa a instância EC2.
    """
    config: dict = load_config()
    ec2: BaseClient = boto3.client("ec2")
    AWS = AWSUtils(ec2)

    try:
        if AWS.is_instance_running( config["INSTANCE_ID"] ):
            print("Instância já está iniciada.")
            return
        
        AWS.start_instance( config["INSTANCE_ID"] )
        print("Instância iniciada.")

        ip: str = AWS.wait_for_instance_ip( config["INSTANCE_ID"] )
        print(f"IP da instância: {ip}")

    except Exception as e:
        print(f"Erro ao inicializar instância: {e}")
        return None, None

def start_server() -> None:
    """
    Inicia o servidor.
    """
    config: dict    = load_config()
    ec2: BaseClient = boto3.client("ec2")
    AWS: AWSUtils   = AWSUtils(ec2)
    
    try:
        if not AWS.is_instance_running( config["INSTANCE_ID"] ):
            print("Instância está parada.")
            return
        print("Instância está rodando.")
        
        ip: str = AWS.get_instance_ip( config["INSTANCE_ID"] )
        if ip == "IP não encontrado": raise ValueError("Não foi possível obter o IP da instância.")
 
        print("Conectando ao servidor...")
        SSH: SSHUtils = SSHUtils(ip, config["KEY_PATH"], config["USER"] )

        if not SSH.connect():
            print("Falha ao conectar via SSH.")
            return False

        print("Iniciando servidor...")
        response = SSH.execute_command( config["START_COMMAND"] )
        print(response)

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        if SSH:
            SSH.close()
            print("Conexão encerrada.")