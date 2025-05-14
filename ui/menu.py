#menu simples para selecionar opcoes de star e stop dos servidores (minecraft/zomboid)

class Menu:
    """
    Classe para criar um menu simples de terminal.
    """
    
    def __init__(self, title: str, options: list) -> None:
        self.title = title
        self.options = options
        self.selected_option = None

    def run(self) -> None:
        """
        Executa o menu e aguarda a seleção do usuário.
        """
        self.display()
        
        if self.selected_option is not None:
            print(f"Você selecionou: {self.selected_option}")
        else:
            print("Nenhuma opção selecionada.")
    
    def display(self) -> None:
        """
        Exibe o menu e aguarda a seleção do usuário.
        """
        print(self.title)
        for i, option in enumerate(self.options):
            print(f"{i + 1}. {option}")
        
        choice = input("Escolha uma opção: ")
        
        try:
            self.selected_option = self.options[int(choice) - 1]
        except (IndexError, ValueError):
            print("Opção inválida. Tente novamente.")
            self.display()