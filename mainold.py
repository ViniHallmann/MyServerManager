import sys
import os

from typing import Dict, Callable

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Automation.Server_Functions.start import start_instance
from Automation.Server_Functions.start import start_server
from Automation.Server_Functions.stop import stop_server_and_instance
from Automation.Server_Functions.stop import stop_server
from Automation.Server_Functions.stop import stop_instance
from Automation.Server_Functions.update import update_ini

USAGE_MESSAGE = """
Uso: python main.py <comando> [opções]

Comandos disponíveis:
  start-instance   - Inicia a instância EC2 (o servidor inicia automaticamente)
  start-server     - Inicia o servidor do Zomboid
  terminate        - Para o servidor e a instância EC2
  stop-server      - Para apenas o servidor do Zomboid
  stop-instance    - Para apenas a instância EC2
  update           - Atualiza o arquivo Server.ini
"""
UNKNOWN_COMMAND_MESSAGE = "Comando desconhecido: {}"
COMMANDS: Dict[str, Callable] = {
    "start-instance": start_instance, 
    "start-server": start_server,
    "terminate": stop_server_and_instance,
    "stop-server": stop_server,
    "stop-instance": stop_instance,
    "update": update_ini
}

def main() -> None:
    
    if len(sys.argv) < 2:
        print(USAGE_MESSAGE)
        
    command = sys.argv[1].lower()
    
    if command not in COMMANDS:
        print(UNKNOWN_COMMAND_MESSAGE.format(command))
        print(USAGE_MESSAGE)
        sys.exit(1)

    try:
        COMMANDS[command]()
    except Exception as e:
        print(f"Erro ao executar o comando '{command}': {e}")
        sys.exit(1) 

if __name__ == "__main__":
    main()