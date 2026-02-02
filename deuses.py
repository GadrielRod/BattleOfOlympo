from utils import Cores

class DeusBase:
    def __init__(self, nome, icone, descricao):
        self.nome = nome
        self.icone = icone
        self.descricao = descricao

    def ativar_especial(self, usuario, oponente):
        print(f"{Cores.AMARELO}>>> {self.icone} ESPECIAL DE {self.nome}!{Cores.RESET}")
        return 0 

class Zeus(DeusBase):
    def __init__(self):
        super().__init__("Zeus", "⚡", "Relampago: Dano alto (40%).")
    def ativar_especial(self, usuario, oponente):
        super().ativar_especial(usuario, oponente)
        print("Raio cai dos ceus! -40% estabilidade no inimigo.")
        oponente.receber_dano(40)
        return 0
        
class Kratos(DeusBase):
    def __init__(self):
     super().__init__("Kratos", "⚔️", "Furia Espartana: Empurra 3 casas.")
    def ativar_especial(self, usuario, oponente):
     super().ativar_especial(usuario, oponente)
     print("Fúria espartana empurra o inimigo!")
     return 3

class Hades(DeusBase):
    def __init__(self):
        super().__init__("Hades", "💀", "Submundo: Rouba vida.")
    def ativar_especial(self, usuario, oponente):
        super().ativar_especial(usuario, oponente)
        print("Hades drena a vitalidade! -20% nele, +20% em voce.")
        oponente.receber_dano(20)
        usuario.curar(20)
        return 0

class Poseidon(DeusBase):
    def __init__(self):
        super().__init__("Poseidon", "🌊", "Maremoto: Empurra 2 casas extra.")
    def ativar_especial(self, usuario, oponente):
        super().ativar_especial(usuario, oponente)
        print("Onda gigante empurra o inimigo!")
        return 2

class Ares(DeusBase):
    def __init__(self):
        super().__init__("Ares", "🗡", "Guerra: Dano e Ganha 1 item.")
    def ativar_especial(self, usuario, oponente):
        super().ativar_especial(usuario, oponente)
        print("Ataque furioso! Dano de 20% + 1 item.")
        oponente.receber_dano(20)
        usuario.ganhar_item()
        return 0

class Hera(DeusBase):
    def __init__(self):
        super().__init__("Hera", "🦚", "Protecao: Cura muito (50%).")
    def ativar_especial(self, usuario, oponente):
        super().ativar_especial(usuario, oponente)
        print("Hera cura seu campeao em 40%!")
        usuario.curar(40)
        return 0

class Artemis(DeusBase):
    def __init__(self):
        super().__init__("Artemis", "🏹", "Cacada: Dano certeiro (20%) e empurra 1.")
    def ativar_especial(self, usuario, oponente):
        super().ativar_especial(usuario, oponente)
        print("Flecha certeira! -20% estabilidade.")
        oponente.receber_dano(20)
        return 1

class Apolo(DeusBase):
    def __init__(self):
        super().__init__("Apolo", "☀️", "Luz Solar: Cura (20%) e ganha 1 item.")
    def ativar_especial(self, usuario, oponente):
        super().ativar_especial(usuario, oponente)
        print("Luz solar cura seu campeao em 20% e lhe concede 1 item.")
        usuario.curar(20)
        usuario.ganhar_item()
        return 0

class Atena(DeusBase):
    def __init__(self):
        super().__init__("Atena", "🦉", "Sabedoria: Cura (15%) e escolhe item.")
    def ativar_especial(self, usuario, oponente):
        super().ativar_especial(usuario, oponente)
        print("Estratégia Suprema! Atena permite que você escolha o item perfeito e se cure em 15.")
        usuario.escolher_item_manual()
        usuario.curar(15)
        return 0

TODOS_OS_DEUSES = [Zeus, Hades, Poseidon, Ares, Hera, Artemis, Apolo, Atena]