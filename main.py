import sys
from typing import NoReturn
from UI.menu import Menu
from UI.menu import Options

def main() -> NoReturn:
    """
    Função principal que inicia a aplicação.
    Gerencia o fluxo de controle do menu principal.
    """
    try:
        menu = Menu()
        if not menu.select_server():
            print("Nenhum servidor selecionado. Encerrando...")
            sys.exit(0)
        
        while True:
            menu.clear_screen()
            menu.show_main_menu()
            
            choice = input("\nEscolha uma opção: ")
            
            handle_menu_choice(menu, choice)
            
    except KeyboardInterrupt:
        print("\nOperação interrompida pelo usuário. Encerrando...")
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        input("\nPressione ENTER para continuar...")
        raise


def handle_menu_choice(menu: Menu, choice: str) -> None:
    """
    Processa a escolha do usuário no menu principal.
    """
    try:
        option = Options(choice)
        
        if option == Options.SAIR: sys.exit(0)

        elif option == Options.INSTANCIA: menu.handle_submenu("instancia")

        elif option == Options.SERVIDOR:  menu.handle_submenu("servidor")
        
        elif option == Options.CRIAR_ENV: menu.create_env()
            
    except ValueError:
        print("Opção inválida.")
        input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    main()