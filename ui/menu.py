import os
from enum import Enum
from typing import Dict, Callable, Optional
from variables.globals import set_selected_game, get_selected_game

class Options(Enum):
    """Opções disponíveis no menu principal."""
    SAIR = "0"
    INSTANCIA = "1"
    SERVIDOR = "2"
    CRIAR_ENV = "3"

class Menu:
    def __init__(self):
        self.instance_commands: Dict[str, Callable] = {
            "1": self.start_instance,
            "2": self.stop_instance,
            "3": self.check_instance_status
        }
        self.server_commands: Dict[str, Callable] = {
            "1": self.start_server,
            "2": self.stop_server,
            "3": self.check_server_status
        }
        self.SELECTED_GAME: Optional[str] = None

    @staticmethod
    def clear_screen() -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_header(self, title: str) -> None:
        print("=" * 50)
        print(f"{title.center(48)}")
        print("=" * 50)

    def show_game_selection(self) -> None:
        self.show_header("MENU - SELECIONE O JOGO")
        print("1. Zomboid")
        print("2. Minecraft")
        print("=" * 50)

    def show_main_menu(self) -> None:
        self.show_header(f"MENU PRINCIPAL - {self.SELECTED_GAME.upper()}")
        print("1. Gerenciar instância EC2")
        print("2. Gerenciar servidor")
        print("3. Criar .env")
        print("0. Sair")
        print("=" * 50)

    def show_submenu(self, menu_type: str) -> None:
        self.show_header(f"SUBMENU - {menu_type.upper()} - {self.SELECTED_GAME.upper()}")
        
        if menu_type == "instancia":
            print("1. Iniciar instância EC2")
            print("2. Parar instância EC2")
            print("3. Verificar status da instância")
        elif menu_type == "servidor":
            print("1. Iniciar servidor")
            print("2. Parar servidor")
            print("3. Verificar status do servidor")
            
        print("0. Voltar")
        print("=" * 50)

    def select_game(self) -> bool:
        self.clear_screen()
        self.show_game_selection()
        choice = input("\nEscolha o jogo: ")
        
        if choice == "1":
            set_selected_game("Zomboid")
            self.SELECTED_GAME = "Zomboid"
            return True
        elif choice == "2":
            set_selected_game("Minecraft")
            self.SELECTED_GAME = "Minecraft"
            return True
        
        print("Opção inválida.")
        return False

    def handle_submenu(self, menu_type: str) -> None:
        commands = self.instance_commands if menu_type == "instancia" else self.server_commands
        
        while True:
            self.clear_screen()
            self.show_submenu(menu_type)
            choice = input("\nEscolha uma opção: ")
            
            if choice == "0":
                break
                
            if choice in commands:
                try:
                    print("\nExecutando operação...")
                    commands[choice]()
                except Exception as e:
                    print(f"\nErro: {e}")
            else:
                print("Opção inválida.")
                
            input("\nPressione ENTER para continuar...")

    def start_instance(self):
        import commons.start
        commons.start.start_instance()

    def stop_instance(self):
        import commons.stop
        commons.stop.stop_instance()

    def check_instance_status(self):
        import commons.status
        commons.status.check_instance_status()

    def start_server(self):
        import commons.start
        commons.start.start_server()

    def stop_server(self):
        import commons.stop
        commons.stop.stop_server()

    def check_server_status(self):
        import commons.status
        commons.status.check_server_status()

    def create_env(self):
        import commons.configs.configs
        commons.configs.configs.generate_env_file()