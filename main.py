from utils import limpar_tela, Cores
from jogo import BattleOfOlympo
from deuses import TODOS_OS_DEUSES

def mostrar_regras():
    """Exibe as regras detalhadas com visual aprimorado e desenhos dos dados."""
    limpar_tela()
    print(f"{Cores.NEGRITO}=== 📜 REGRAS DO BATTLE OF OLYMPO ==={Cores.RESET}\n")
    
    # Seção 1: Objetivo
    print(f"{Cores.AMARELO}1. OBJETIVO 🏆{Cores.RESET}")
    print("   Empurrar o marcador da Arena para o lado do oponente.")
    print("   Se o marcador passar da casa 4, você vence a partida.\n")

    # Seção 2: Dados
    print(f"{Cores.AMARELO}2. OS DADOS 🎲{Cores.RESET}")
    print("   • No 1º turno de ambos os jogadores: Lança-se 3 dados.")
    print("   • Nos demais Turnos: Lança-se 5 dados.")
    print("   • Você pode rerrolar até 2 vezes, mas deve manter pelo menos 1 dos dados rolado.")
    print(f"  • {Cores.VERMELHO}Dados com valor 1 (⚀) são 'Azarentos': ficam TRAVADOS e não podem ser rerrolados{Cores.RESET}\n")

    # Seção 3: Combos (Com desenho ASCII dos dados)
    print(f"{Cores.AMARELO}3. COMBINAÇÕES (O que os dados fazem){Cores.RESET}")
    print(f"   • {Cores.CIANO}Par de 2 (⚁⚁) {Cores.RESET}  ➔  GANHA 1 ITEM ALEATORIO (Máx 3)")
    print(f"   • {Cores.CIANO}Par de 3/4 (⚂⚂ ou ⚃⚃) {Cores.RESET}  ➔  ATAQUE (Reduz a defesa do inimigo)")
    print(f"   • {Cores.CIANO}Par de 5/6 (⚄⚄ ou ⚅⚅) {Cores.RESET} ➔ EMPURRAO (Move a arena contra o oponente)")
    print(f"   • {Cores.CIANO}Trio de 6 (⚅⚅⚅) {Cores.RESET} ➔  ESPECIAL (Ativa o golpe unico do seu deus escolhido)\n")

    # Seção 4: Mecânica de Defesa (Estabilidade)
    print(f"{Cores.AMARELO}4. ESTABILIDADE = DEFESA{Cores.RESET}")
    print("   Aqui sua % representa seu DEFESA.")
    print("   Quanto mais próximo de 100%, mais 'pesado' difícil sera de empurrar voce.")
    print("   Se sua defesa cai, você fica 'leve' e voa longe com qualquer empurrao!")
    print("\n   TABELA DE VULNERABILIDADE:")
    print(f"   • {Cores.VERDE}100% a 51%:{Cores.RESET} PESADO (O inimigo te empurra apenas 1 casa)")
    print(f"   • {Cores.AMARELO}50% a 1%:{Cores.RESET}   LEVE   (O inimigo te empurra 2 casas)")
    print(f"   • {Cores.VERMELHO}0%:{Cores.RESET}          PENA   (PERIGO! O inimigo te empurra 3 casas)\n")

    input(f"{Cores.VERDE}[Pressione Enter para voltar ao Menu...]{Cores.RESET}")

def mostrar_itens():
    limpar_tela()
    print(f"{Cores.NEGRITO}=== 🎒 ENCICLOPÉDIA DE ITENS ==={Cores.RESET}\n")
    
    print(f"{Cores.MAGENTA}1. NÉCTAR 🍯{Cores.RESET} Recupera 25% de Defesa.")
    print(f"{Cores.MAGENTA}2. AMBROSIA 🍰{Cores.RESET} +1 Força de Empurrão.")
    print(f"{Cores.MAGENTA}3. ESCUDO 🛡️{Cores.RESET} Bloqueia o próximo dano.")
    print(f"{Cores.AMARELO}4. LANÇA ⚔️{Cores.RESET} +25% Dano no próximo ataque.")
    print(f"{Cores.AMARELO}5. MEDUSA 🐍{Cores.RESET} Destrói um item do inimigo.")
    
    print(f"{Cores.CIANO}--- NOVOS ITENS DE DADOS ---{Cores.RESET}")
    print(f"{Cores.VERDE}6. BÊNÇÃO DE HERMES 👟{Cores.RESET}")
    print("   Você joga com +1 DADO neste turno. Mais chances de combo!")
    
    print(f"{Cores.VERMELHO}7. CAIXA DE PANDORA 📦{Cores.RESET}")
    print("   Azaração! O oponente jogará com –1 DADO no turno dele.")

    print(f"\n{Cores.AMARELO}8. VELOCINO DOURADO ✨{Cores.RESET} Cura total (100%). Muito raro.")

    input(f"\n{Cores.VERDE}[Enter]{Cores.RESET}")
    
def mostrar_info_deuses():
    """Mostra a lista de personagens jogáveis."""
    limpar_tela()
    print(f"{Cores.NEGRITO}=== 🏛️ PANTHEON (INFO DOS DEUSES) ==={Cores.RESET}\n")
    print("Cada deus possui um Especial ativado com três dados 6.\n")
    
    for classe_deus in TODOS_OS_DEUSES:
        d = classe_deus()
        print(f"{Cores.AMARELO}{d.icone} {d.nome}:{Cores.RESET} {d.descricao}")
        print(f"{Cores.CIANO}{'-'*50}{Cores.RESET}")
    
    input(f"\n{Cores.VERDE}[Pressione Enter para voltar]{Cores.RESET}")

def menu_principal():
    while True:
        limpar_tela()
        print(f"{Cores.CIANO}=======================================")
        print(f"       ⚡ BATTLE OF OLYMPO ⚡")
        print(f"======================================={Cores.RESET}")
        print("1.  ⚔️  JOGAR")
        print("2.  📜  REGRAS (Leia antes de jogar!)")
        print("3.  🎒  ENCICLOPEDIA DOS ITENS")
        print("4. ️ 🏛  CONHECER OS DEUSES")
        print("5.  ❌  SAIR")
        
        escolha = input("\nEscolha uma opção: ")

        if escolha == "1":
            # Inicia o jogo
            BattleOfOlympo().jogar()
            input("\nPressione Enter para voltar ao menu...")
            
        elif escolha == "2":
            mostrar_regras()

        elif escolha == "3":
            mostrar_itens()
            
        elif escolha == "4":
            mostrar_info_deuses()
            
        elif escolha == "5":
            print("Saindo do Olimpo... Que os deuses te acompanhem!")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu_principal()
