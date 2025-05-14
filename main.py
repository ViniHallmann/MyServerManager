from UI.menu import Menu

def main() -> None:
    menu = Menu()
    
    if not menu.select_game():
        return
    
    while True:
        menu.clear_screen()
        menu.show_main_menu()
        choice = input("\nEscolha uma opção: ")
        
        if choice == "0":
            print("Saindo...")
            break
        elif choice == "1":
            menu.handle_submenu("instancia")
        elif choice == "2":
            menu.handle_submenu("servidor")
        elif choice == "3":
            menu.create_env()
        else:
            print("Opção inválida.")
            input("\nPressione ENTER para continuar...")

if __name__ == "__main__":
    main()