import os
import sys
from time import sleep
from pathlib import Path
from dotenv import load_dotenv
from variables.globals import get_selected_game


def load_config() -> dict:
    """
    Carrega as configurações a partir de variáveis de ambiente definidas no arquivo .env
    específico para o jogo selecionado.
    """
    selected_game = get_selected_game()
    
    if not selected_game:
        raise EnvironmentError("Nenhum jogo foi selecionado. Selecione um jogo antes de continuar.")
    
    base_dir = Path(__file__).resolve().parent.parent.parent
    env_path = base_dir / "variables" / f"{selected_game.lower()}.env"
    
    try:
        load_dotenv(dotenv_path=env_path)
        print(f"Arquivo de configuração carregado: {env_path}")
    except Exception as e:
        print(f"Erro ao carregar variáveis de ambiente: {e}")
        raise EnvironmentError(f"Não foi possível carregar o arquivo {env_path}.")
    
    config = {
        "INSTANCE_ID":      os.getenv("INSTANCE_ID"),
        "KEY_PATH":         os.getenv("KEY_PATH"),
        "USER":             os.getenv("USER", "ubuntu"),
        "STOP_COMMAND":     os.getenv("STOP_COMMAND"),
        "START_COMMAND":    os.getenv("START_COMMAND")
    }
    
    verify_config_variables(config)

    return config

def generate_env_file() -> None:
    selected_game = get_selected_game()

    if not selected_game:
        raise EnvironmentError("Nenhum jogo foi selecionado. Selecione um jogo antes de continuar.")

    base_dir = Path(__file__).resolve().parents[2]
    env_dir = base_dir / "variables"
    env_path = env_dir / f"{selected_game.lower()}.env"

    env_dir.mkdir(parents=True, exist_ok=True)

    key_path = input("Digite o caminho da chave .pem: ").strip()

    env_content = f"""
INSTANCE_ID=i-0a4371abf059289e4
KEY_PATH={key_path}
START_COMMAND=screen -S {selected_game} -dm bash -c 'cd /home/ubuntu/{selected_game} && ./run.sh'
STOP_COMMAND=screen -S {selected_game} -p 0 -X stuff 'stop\\n'
STATUS_COMMAND=screen -list | grep {selected_game}
    """

    with open(env_path, "w") as f:
        f.write(env_content)

def verify_config_variables(config: dict) -> None:
    """
    Verifica se todas as variáveis necessárias estão definidas no arquivo .env.
    """
    required_vars = ["INSTANCE_ID", "KEY_PATH", "STOP_COMMAND", "START_COMMAND"]
    missing_vars = [var for var in required_vars if not config[var]]
    
    if missing_vars:
        raise EnvironmentError(f"As seguintes variáveis de ambiente não estão definidas: {', '.join(missing_vars)}")