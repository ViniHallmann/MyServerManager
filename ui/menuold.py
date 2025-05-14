import os
import sys
import time
import readchar
from typing import List, Dict, Callable, Any, Optional

class TerminalMenu:
    """
    Classe para criar menus interativos no terminal.
    """
    
    def __init__(self, title: str = "Menu Principal"):
        """
        Inicializa o menu.
        """
        self.title = title
        self.options = []
        self.selected_index = 0
        self.running = False
    
    def add_option(self, label: str, action: Optional[Callable] = None, data: Any = None) -> None:
        """
        Adiciona uma opção ao menu.
        """
        self.options.append({"label": label, "action": action, "data": data})
    
    def clear_screen(self) -> None:
        """
        Limpa a tela do terminal.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def draw(self) -> None:
        """
        Desenha o menu na tela.
        """
        self.clear_screen()
        
        # Desenha o cabeçalho
        width = max(len(self.title) + 4, 40)
        print("╔" + "═" * width + "╗")
        print("║" + self.title.center(width) + "║")
        print("╠" + "═" * width + "╣")
        
        # Desenha as opções
        for i, option in enumerate(self.options):
            prefix = "►" if i == self.selected_index else " "
            print(f"║ {prefix} {option['label']}" + " " * (width - len(option["label"]) - 4) + "║")
        
        print("╚" + "═" * width + "╝")
        print("\nUse as setas ↑/↓ ou W/S para navegar, Enter para selecionar, Q para sair")
    
    def handle_input(self) -> bool:
        """
        Gerencia a entrada do usuário.
        """
    
        key = readchar.readkey()
        
        # Navegação
        if key == readchar.key.UP or key.lower() == 'w':
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif key == readchar.key.DOWN or key.lower() == 's':
            self.selected_index = (self.selected_index + 1) % len(self.options)
        
        # Seleção
        elif key == readchar.key.ENTER:
            selected = self.options[self.selected_index]
            if selected["action"]:
                selected["action"](selected["data"])
                return False  # Fecha o menu após a ação
        
        # Sair
        elif key.lower() == 'q':
            return False
        
        return True
    
    def run(self) -> None:
        """
        Executa o menu.
        """
        self.running = True
        
        while self.running and self.options:
            self.draw()
            self.running = self.handle_input()
        
        self.clear_screen()

class ServerManagerMenu:
    """
    Classe para gerenciar os menus do ServerManager.
    """
    
    def __init__(self, config_loader: Callable, available_servers: List[str]):
        """
        Inicializa o gerenciador de menus.
        
        Args:
            config_loader (Callable): Função para carregar configurações
            available_servers (List[str]): Lista de servidores disponíveis
        """
        self.config_loader = config_loader
        self.available_servers = available_servers
        self.commands = {}
    
    def register_command(self, name: str, func: Callable) -> None:
        """
        Registra um comando.
        
        Args:
            name (str): Nome do comando
            func (Callable): Função a ser executada
        """
        self.commands[name] = func
    
    def execute_command(self, command_data: Dict[str, Any]) -> None:
        """
        Executa um comando.
        
        Args:
            command_data (Dict[str, Any]): Dados do comando
        """
        command_name = command_data["command"]
        server_type = command_data["server"]
        
        if command_name in self.commands:
            try:
                if command_name == "list-servers":
                    self.commands[command_name]()
                else:
                    result = self.commands[command_name](server_type)
                    self._show_result(f"Comando '{command_name}' executado para servidor '{server_type}'", 
                                    "Sucesso" if result else "Falha")
            except Exception as e:
                self._show_result(f"Erro ao executar o comando '{command_name}'", str(e), error=True)
        else:
            self._show_result("Erro", f"Comando '{command_name}' não registrado", error=True)
    
    def _show_result(self, title: str, message: str, error: bool = False) -> None:
        """
        Mostra o resultado de um comando.
        
        Args:
            title (str): Título da mensagem
            message (str): Mensagem
            error (bool, optional): Se é uma mensagem de erro. Padrão é False.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        
        width = max(len(title) + 4, len(message) + 4, 40)
        
        print("╔" + "═" * width + "╗")
        print("║" + title.center(width) + "║")
        print("╠" + "═" * width + "╣")
        print("║" + message.center(width) + "║")
        print("╚" + "═" * width + "╝")
        
        input("\nPressione Enter para continuar...")
    
    def select_server(self) -> str:
        """
        Menu para selecionar um servidor.
        
        Returns:
            str: Servidor selecionado
        """
        menu = TerminalMenu("Selecione um Servidor")
        
        for server in self.available_servers:
            menu.add_option(f"{server}", lambda s: s, server)
        
        menu.add_option("Voltar", lambda _: None)
        
        menu.run()
        
        selected = self.available_servers[menu.selected_index] if menu.selected_index < len(self.available_servers) else None
        return selected
    
    def main_menu(self) -> None:
        """
        Exibe o menu principal.
        """
        menu = TerminalMenu("ServerManager - Menu Principal")
        
        # Opções para cada servidor
        for server in self.available_servers:
            menu.add_option(f"Gerenciar {server.upper()}", self.server_menu, server)
        
        # Opções adicionais
        menu.add_option("Listar todos os servidores", self.execute_command, {"command": "list-servers", "server": None})
        menu.add_option("Sair", lambda _: sys.exit(0))
        
        menu.run()
    
    def server_menu(self, server_type: str) -> None:
        """
        Exibe o menu de um servidor específico.
        
        Args:
            server_type (str): Tipo de servidor
        """
        menu = TerminalMenu(f"Gerenciando Servidor: {server_type.upper()}")
        
        # Adiciona as opções para este servidor
        menu.add_option(f"Iniciar instância EC2", self.execute_command, {"command": "start-instance", "server": server_type})
        menu.add_option(f"Iniciar servidor de jogo", self.execute_command, {"command": "start-server", "server": server_type})
        menu.add_option(f"Parar servidor de jogo", self.execute_command, {"command": "stop-server", "server": server_type})
        menu.add_option(f"Parar instância EC2", self.execute_command, {"command": "stop-instance", "server": server_type})
        menu.add_option(f"Parar tudo (servidor + instância)", self.execute_command, {"command": "terminate", "server": server_type})
        menu.add_option(f"Atualizar configurações", self.execute_command, {"command": "update", "server": server_type})
        menu.add_option("Voltar ao menu principal", lambda _: None)
        
        menu.run()
        
        # Retorna ao menu principal quando sair deste menu
        self.main_menu()
    
    def run(self) -> None:
        """
        Executa o gerenciador de menus.
        """
        try:
            self.main_menu()
        except KeyboardInterrupt:
            print("\nSaindo do ServerManager...")
            sys.exit(0)