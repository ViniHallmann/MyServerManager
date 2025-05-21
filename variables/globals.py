SELECTED_SERVER: str = None 

#Preciso de uma funcao para retornar o id da instancia dependendo do servidor selecionado
def get_instance_id() -> str:
    if SELECTED_SERVER == "Zomboid":
        return "i-0efbd9be2b2c3f505"
    elif SELECTED_SERVER == "Minecraft":
        return "i-0a4371abf059289e4"
    elif SELECTED_SERVER == "N8N":
        return "i-0b40f7ce83e610157"
    else:
        raise ValueError("Servidor não suportado.")

def set_selected_server(server: str) -> None:
    global SELECTED_SERVER
    SELECTED_SERVER = server

def get_selected_server() -> str:
    global SELECTED_SERVER
    return SELECTED_SERVER