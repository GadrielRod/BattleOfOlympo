import random
from utils import Cores

class Jogador:
    def __init__(self, nome, deus_escolhido):
        self.nome = nome
        self.deus = deus_escolhido
        self.estabilidade = 100 
        self.inventario = [] 
        self.max_itens = 3
        self.dados_atuais = []
        
        # Atributos de Efeito
        self.escudo_ativo = False
        self.furia_ativa = False   
        self.ataque_extra = False  
        self.modificador_dados = 0 

    @property
    def vulnerabilidade(self):
        if self.estabilidade > 50: return 1 
        elif self.estabilidade > 0: return 2 
        else: return 3 

    def receber_dano(self, qtd):
        if self.escudo_ativo:
            print(f"{Cores.AZUL}🛡️ {self.nome} usou o Escudo e anulou o dano!{Cores.RESET}")
            self.escudo_ativo = False
            return

        self.estabilidade = max(0, self.estabilidade - qtd)
        print(f"{Cores.VERMELHO}> {self.nome} perdeu defesa! Agora tem {self.estabilidade}%{Cores.RESET}")

    def curar(self, qtd):
        self.estabilidade = min(100, self.estabilidade + qtd)
        print(f"{Cores.VERDE}> {self.nome} recuperou defesa! {self.estabilidade}%{Cores.RESET}")

    def ganhar_item(self):
        """Ganha um item aleatório (padrão do par de 2)."""
        if len(self.inventario) >= self.max_itens:
            print("Inventario cheio! Item perdido.")
            return

        itens_possiveis = [
            "Nectar", "Ambrosia", "Escudo", 
            "Lanca", "Medusa", "Velocino dourado",
            "Bencao de Hermes", "Caixa de Pandora"
        ]
        
        # Pesos de raridade
        pesos = [25, 20, 15, 10, 5, 5, 10, 10] 
        novo_item = random.choices(itens_possiveis, weights=pesos, k=1)[0]
        self.inventario.append(novo_item)
        print(f"{Cores.MAGENTA}Sorte dos dados! Voce ganhou: {novo_item}!{Cores.RESET}")

    def escolher_item_manual(self):
        """Função especial (usada por Atena no 6-6-6)."""
        if len(self.inventario) >= self.max_itens:
            print("Inventario cheio! Não pode escolher item agora.")
            return

        itens_possiveis = [
            "Nectar", "Ambrosia", "Escudo", 
            "Lanca", "Medusa", "Velocino dourado",
            "Bencao de Hermes", "Caixa de Pandora"
        ]
        
        print(f"\n{Cores.CIANO}🦉 SABEDORIA DE ATENA! Escolha seu item:{Cores.RESET}")
        for i, item in enumerate(itens_possiveis):
            print(f"{i+1}. {item}")
        
        while True:
            try:
                escolha = int(input("Digite o numero do item: ")) - 1
                if 0 <= escolha < len(itens_possiveis):
                    novo_item = itens_possiveis[escolha]
                    self.inventario.append(novo_item)
                    print(f"{Cores.MAGENTA}Atena concedeu: {novo_item}!{Cores.RESET}")
                    return
                else:
                    print("Opção inválida.")
            except ValueError:
                print("Digite um número.")

    def usar_item(self, oponente):
        if not self.inventario:
            return

        print(f"\n{Cores.AMARELO}--- SEU INVENTARIO ---{Cores.RESET}")
        for i, item in enumerate(self.inventario):
            print(f"{i+1}. {item}")
        print("0. Nao usar nada")

        try:
            escolha_str = input("Escolha um item: ")
            if not escolha_str.isdigit(): return
            
            idx = int(escolha_str) - 1
            if idx == -1: return

            if 0 <= idx < len(self.inventario):
                item = self.inventario.pop(idx)
                print(f"Usando {item}...")
                
                if item == "Nectar":
                    print("Recupera 25% de Defesa.")
                    self.curar(25)
                elif item == "Velocino dourado":
                    print("Cura Lendaria! Recupera 100% da Defesa.")
                    self.curar(100)
                elif item == "Ambrosia":
                    print("Forca bruta! Empurrao +1 neste turno.")
                    self.furia_ativa = True
                elif item == "Lanca":
                    print("Afiar armas! Proximo ataque +25% de dano.")
                    self.ataque_extra = True
                elif item == "Escudo":
                    print("Protecao ativada para o proximo ataque.")
                    self.escudo_ativo = True
                elif item == "Medusa":
                    if oponente.inventario:
                        item_destruido = oponente.inventario.pop()
                        print(f"Medusa petrificou o item {item_destruido} do inimigo!")
                    else:
                        print("Medusa olhou, mas inimigo estava sem itens.")
                elif item == "Bencao de Hermes":
                    print(f"{Cores.VERDE}Velocidade! +1 Dado neste turno.{Cores.RESET}")
                    self.modificador_dados += 1
                elif item == "Caixa de Pandora":
                    print(f"{Cores.VERMELHO}Maldição! Oponente terá -1 Dado.{Cores.RESET}")
                    oponente.modificador_dados -= 1
            else:
                print("Item invalido.")
        except ValueError:
            pass

    def rolar_dados(self, quantidade):
        return [random.randint(1, 6) for _ in range(quantidade)]
