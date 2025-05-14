import paramiko

class SSHUtils:
    """
    Classe utilitária para operações SSH.
    """

    def __init__( self, public_ip: str, key_path: str, user: str = "ubuntu" ):
        self.public_ip = public_ip
        self.key_path = key_path
        self.user = user
        self.ssh_client = None

    def connect( self ) -> bool:
        """
        Conecta ao servidor via SSH.
        """
        try:
            key = paramiko.RSAKey( filename=self.key_path )
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
            self.ssh_client.connect( self.public_ip, username=self.user, pkey=key )
            return True
        except Exception as e:
            print( f"Erro ao conectar via SSH: {e}" )
            return False

    def execute_command( self, command: str ) -> None:
        """
        Executa um comando no servidor via SSH.
        """
        if not self.ssh_client:
            print( "Conexão SSH não estabelecida." )
            return None
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command( command )
            return stdout.read().decode()
        except Exception as e:
            print( f"Erro ao executar comando via SSH: {e}" )

        return None
    
    def close( self ) -> None:
        """Fecha a conexão SSH"""
        if self.ssh_client:
            self.ssh_client.close()
            self.ssh_client = None