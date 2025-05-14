import os
from dotenv import load_dotenv

def load_config() -> dict:
    """
    Carrega as configurações a partir de variáveis de ambiente definidas no arquivo .env.
    """
    try:
        load_dotenv()
    except Exception as e:
        print(f"Erro ao carregar variáveis de ambiente: {e}")
        raise EnvironmentError("Não foi possível carregar o arquivo .env.")
    

    config = {
        "INSTANCE_ID":      os.getenv("INSTANCE_ID"),
        "KEY_PATH":         os.getenv("KEY_PATH"),
        "USER":             os.getenv("USER", "ubuntu"),
        "STOP_COMMAND":     os.getenv("STOP_COMMAND"),
        "START_COMMAND":    os.getenv("START_COMMAND")
    }

    #if not config["INSTANCE_ID"]:   raise EnvironmentError(f"A variável de ambiente '{"INSTANCE_ID"}' não está definida.")
    #if not config["KEY_PATH"]:      raise EnvironmentError(f"A variável de ambiente '{"KEY_PATH"}' não está definida.")
    #if not config["STOP_COMMAND"]:  raise EnvironmentError(f"A variável de ambiente '{"STOP_COMMAND"}' não está definida.")

    return config

def verify_config_variables(config: dict) -> None:
    for var in config:
        if not config[var]:
            raise EnvironmentError(f"A variável de ambiente '{var}' não está definida.")