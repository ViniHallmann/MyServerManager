from time import sleep
from botocore.client import BaseClient

class AWSUtils:
    """
    Classe utilitária para operações relacionadas à AWS.
    """

    def __init__(self, ec2: BaseClient):
        self.ec2 = ec2

    def describe_instance(self, INSTANCE_ID: str) -> dict:
        """
        Descreve a instância com o ID fornecido.
        """
        return self.ec2.describe_instances(InstanceIds=[INSTANCE_ID])

    def verify_instance_state(self, INSTANCE_ID: str) -> str:
        """
        Verifica o estado atual da instância EC2.
        """
        return self.describe_instance(INSTANCE_ID)["Reservations"][0]["Instances"][0].get("State")["Name"]
        
    def get_instance_ip(self, INSTANCE_ID: str) -> str:
        """
        Obtém o IP público da instância EC2.
        """
        return self.describe_instance(INSTANCE_ID)["Reservations"][0]["Instances"][0].get("PublicIpAddress", "IP não encontrado")
        
    def is_instance_running(self, INSTANCE_ID: str) -> bool:
        """
        Verifica se a instância com o ID fornecido está em execução.
        """
        return self.verify_instance_state(INSTANCE_ID) == "running"

    def start_instance(self, INSTANCE_ID: str) -> None:
        """
        Inicia a instância EC2, se não estiver em execução.
        """
        if self.is_instance_running(INSTANCE_ID): 
            return
        self.ec2.start_instances(InstanceIds=[INSTANCE_ID])

    def stop_instance(self, INSTANCE_ID: str) -> None:
        """
        Para a instância EC2, se estiver em execução.
        """
        if not self.is_instance_running(INSTANCE_ID): 
            return
        self.ec2.stop_instances(InstanceIds=[INSTANCE_ID])

    def wait_for_instance_ip(self, instance_id: str, max_retries: int = 10, delay: int = 10) -> str:
        """
        Aguarda até que a instância esteja em execução e retorna o IP público.
        """
        for _ in range(max_retries):
            if self.is_instance_running(instance_id):
                ip = self.get_instance_ip(instance_id)
                if ip != "IP não encontrado":
                    return ip
            sleep(delay)
        raise TimeoutError("Timeout ao aguardar o IP da instância.")
