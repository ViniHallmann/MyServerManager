import sys
import os
from typing import Dict, Callable, Optional

import commons.start 
import commons.stop

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Variável global para armazenar o jogo selecionado
SELECTED_GAME: Optional[str] = None

def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


instance_commands: Dict[str, Callable] = {
    "1": commons.start.start_instance,
    "2": commons.stop.stop_instance
}
server_commands: Dict[str, Callable] = {
    "1": commons.start.start_server,
    "2": commons.stop.stop_server
}

def show_game_server_option() -> None:
    print("=" * 50)
    print("MENU - SELECIONE O JOGO")
    print("=" * 50)
    print("1. Zomboid")
    print("2. Minecraft")
    print("=" * 50)

def show_main_menu() -> None:
    print("=" * 50)
    print(f"MENU PRINCIPAL - {SELECTED_GAME.upper()}")
    print("=" * 50)
    print("1. Gerenciar instância EC2")
    print("2. Gerenciar servidor")
    print("3. Criar .env")
    print("0. Sair")
    print("=" * 50)

def show_submenu(tipo: str) -> None:
    print("=" * 50)
    print(f"SUBMENU - {tipo.upper()} - {SELECTED_GAME.upper()}")
    print("=" * 50)
    if tipo == "instancia":
        print("1. Iniciar instância EC2")
        print("2. Parar instância EC2")
    elif tipo == "servidor":
        print("1. Iniciar servidor")
        print("2. Parar servidor")
    print("0. Voltar")
    print("=" * 50)

def submenu(tipo: str) -> None:
    commands = instance_commands if tipo == "instancia" else server_commands
    while True:
        clear_screen()
        show_submenu(tipo)
        choice = input("\nEscolha uma opção: ")
        clear_screen()
        if choice == "0":
            break
        if choice in commands:
            try:
                print("Executando operação...\n")
                commands[choice]()
                #print("\nOperação concluída com sucesso!")
            except Exception as e:
                print(f"\nErro: {e}")
        else:
            print("Opção inválida.")
        input("\nPressione ENTER para continuar...")
        clear_screen()

def select_game() -> bool:
    global SELECTED_GAME
    clear_screen()
    show_game_server_option()
    choice = input("\nEscolha o jogo: ")
    clear_screen()
    if choice == "1":
        SELECTED_GAME = "Zomboid"
    elif choice == "2":
        SELECTED_GAME = "Minecraft"
    else:
        print("Opção inválida.")
        return False
    return True

def main() -> None:
    if not select_game():
        return
    
    while True:
        clear_screen()
        show_main_menu()
        choice = input("\nEscolha uma opção: ")
        clear_screen()
        if choice == "0":
            print("Saindo...")
            break
        elif choice == "1":
            submenu("instancia")
        elif choice == "2":
            submenu("servidor")
        else:
            print("Opção inválida.")
            input("\nPressione ENTER para continuar...")

if __name__ == "__main__":
    main()
