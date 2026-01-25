import time
import random
from utils import Cores, limpar_tela, desenhar_dado
from jogador import Jogador
from deuses import TODOS_OS_DEUSES, Kratos

class BattleOfOlympo:
    def __init__(self):
        self.jogadores = []
        self.arena_posicao = 0 
        self.turno_atual = 1
        self.setup_inicial()

    def selecionar_deus(self, nome_jogador):
        while True:
            print(f"\n{Cores.CIANO}--- Escolha seu deus para {nome_jogador} ---{Cores.RESET}")
            for i, classe_deus in enumerate(TODOS_OS_DEUSES):
                temp = classe_deus()
                print(f"[{i+1}] {temp.icone} {temp.nome}")
            
            entrada = input("Digite o numero (ou segredo): ").strip()
            
            if entrada.upper() == "KRATOS" or entrada.upper() == "BOY":
                print(f"\n{Cores.VERMELHO}⚠️  FANTASMA DE ESPARTA INVOCADO! ⚠️{Cores.RESET}")
                time.sleep(1)
                return Kratos()

            if entrada.isdigit():
                escolha = int(entrada) - 1
                if 0 <= escolha < len(TODOS_OS_DEUSES):
                    return TODOS_OS_DEUSES[escolha]()
            
            print("Inválido!")

    def setup_inicial(self):
        limpar_tela()
        print(f"{Cores.NEGRITO}--- PREPARACAO ---{Cores.RESET}")
        n1 = input("Nome P1 (Esq): ") or "Jogador 1"
        d1 = self.selecionar_deus(n1)
        p1 = Jogador(n1, d1)
        limpar_tela()
        n2 = input("Nome P2 (Dir): ") or "Jogador 2"
        d2 = self.selecionar_deus(n2)
        p2 = Jogador(n2, d2)
        self.jogadores = [p1, p2]
        limpar_tela()
        print("A Batalha vai comecar...")
        time.sleep(2)

    def desenhar_hud(self):
        p1, p2 = self.jogadores[0], self.jogadores[1]
        c1 = Cores.VERDE if p1.estabilidade > 50 else (Cores.AMARELO if p1.estabilidade > 0 else Cores.VERMELHO)
        c2 = Cores.VERDE if p2.estabilidade > 50 else (Cores.AMARELO if p2.estabilidade > 0 else Cores.VERMELHO)

        print(f"{Cores.CIANO}{'='*60}{Cores.RESET}")
        print(f"{p1.deus.icone} {p1.nome:<20} VS {p2.nome:>20} {p2.deus.icone}")
        print(f"{c1}DEF: {p1.estabilidade}%{Cores.RESET:<21}    {c2}DEF: {p2.estabilidade}%{Cores.RESET:>21}")
        
        # Mostra buffs ativos no HUD
        buff_p1 = f"(Mod Dados: {p1.modificador_dados:+d})" if p1.modificador_dados != 0 else ""
        buff_p2 = f"(Mod Dados: {p2.modificador_dados:+d})" if p2.modificador_dados != 0 else ""
        
        print(f"🎒 {len(p1.inventario)} Item(s) {buff_p1:<12}  🎒 {len(p2.inventario)} Item(s) {buff_p2:>12}")
        print(f"{Cores.CIANO}{'='*60}{Cores.RESET}")

    def desenhar_arena(self):
        trilha = [" . "] * 9
        idx = max(0, min(8, self.arena_posicao + 4))
        trilha[idx] = f"{Cores.AMARELO}[⚡]{Cores.RESET}"
        
        arena_visual = "".join(trilha)
        print(f"\n       {Cores.AZUL}(P1){Cores.RESET} {arena_visual} {Cores.VERMELHO}(P2){Cores.RESET}")
        
        if self.arena_posicao > 0: msg = f"P1 empurrando! Falta {5 - self.arena_posicao}"
        elif self.arena_posicao < 0: msg = f"P2 empurrando! Falta {5 + self.arena_posicao}"
        else: msg = "Centro"
        print(f"       {Cores.AMARELO}{msg}{Cores.RESET}")

    def fase_rerrolagem(self, dados):
        rerrolagens = 2
        while rerrolagens > 0:
            print(f"\n{Cores.NEGRITO}>>> SEUS DADOS:{Cores.RESET}")
            print(f"ID:    {'  '.join([f' {i+1} ' for i in range(len(dados))])}")
            print(f"VALOR: {'  '.join([desenhar_dado(d) for d in dados])}")
            
            if all(d == 1 for d in dados):
                print(f"{Cores.VERMELHO}Tudo 1! Travado.{Cores.RESET}")
                break

            print(f"\n[Rerrolagens: {rerrolagens}] ID para MANTER (ex: 1 3).")
            print(f"{Cores.VERDE}[ENTER] = PULA (Aceita tudo){Cores.RESET}")
            decisao = input("Opção: ")
            
            if decisao.strip() == "": break
            
            try:
                indices_manter = [int(x)-1 for x in decisao.split()]
                indices_finais = []
                for i, valor in enumerate(dados):
                    if valor == 1:
                        if i not in indices_manter: print(f"Dado {i+1} (1) mantido.")
                        indices_finais.append(i)
                    elif i in indices_manter:
                        indices_finais.append(i)
                
                if not indices_finais and len(dados) > 0:
                    print("Mantenha ao menos 1!")
                    continue
                
                novos = []
                for i in range(len(dados)):
                    if i in indices_finais: novos.append(dados[i])
                    else: novos.append(random.randint(1, 6))
                dados = novos
                rerrolagens -= 1
            except: print("Erro numérico.")
        return dados

    def resolver_turno(self, atacante, defensor):
        dados = atacante.dados_atuais
        contagem = {i: dados.count(i) for i in range(1, 7)}
        empurrao_extra = 0
        
        print(f"\n{Cores.NEGRITO}--- RESOLUÇÃO ---{Cores.RESET}")

        # 1. Especial
        if contagem[6] >= 3:
            empurrao_extra += atacante.deus.ativar_especial(atacante, defensor)
            contagem[6] -= 3

        # 2. Itens (Atena escolhe, outros aleatório)
        pares_dois = contagem[2] // 2
        if pares_dois > 0:
            for _ in range(pares_dois): atacante.ganhar_item()

        # 3. Ataque
        num_ataques = (contagem[3] + contagem[4]) // 2
        if num_ataques > 0:
            dano = num_ataques * 25
            if atacante.ataque_extra:
                print(f"{Cores.MAGENTA}Lança: +25% Dano!{Cores.RESET}")
                dano += 25
            print(f"⚔️  ATAQUE! {dano}% dano.")
            defensor.receber_dano(dano)
        else: print("⚔️  Sem ataques.")

        # 4. Empurrao
        num_empurroes = (contagem[5] + contagem[6]) // 2
        movimento_total = 0
        if num_empurroes > 0 or empurrao_extra > 0:
            forca = defensor.vulnerabilidade + (1 if atacante.furia_ativa else 0)
            movimento_total = (num_empurroes * forca) + empurrao_extra
            print(f"💨 EMPURRÃO! Total: {movimento_total} casas.")
        else: print("💨 Sem empurrões.")
        
        # Reset de buffs DESTE JOGADOR no final do turno
        atacante.furia_ativa = False
        atacante.ataque_extra = False
        atacante.modificador_dados = 0 # Reseta Hermes (Pandora continua no inimigo)
        
        input(f"\n{Cores.VERDE}[Enter para continuar]{Cores.RESET}")
        return movimento_total

    def jogar(self):
        rodando = True
        while rodando:
            idx = (self.turno_atual + 1) % 2 
            atacante = self.jogadores[idx]
            defensor = self.jogadores[1 - idx]
            direcao = 1 if idx == 0 else -1 

            limpar_tela()
            self.desenhar_hud()   
            self.desenhar_arena() 
            
            print(f"\n🎲 TURNO {self.turno_atual}: {atacante.nome} ({atacante.deus.nome})")
            
            # Fase Item
            atacante.usar_item(defensor)
            
            # CALCULO DE DADOS COM MODIFICADORES
            base = 3 if self.turno_atual <= 2 else 5
            qtd_final = base + atacante.modificador_dados
            # Garante no mínimo 1 dado (para não bugar se levar muita Pandora)
            qtd_final = max(1, qtd_final)
            
            if atacante.modificador_dados != 0:
                print(f"{Cores.MAGENTA}Modificador de Dados Ativo: {atacante.modificador_dados:+d}{Cores.RESET}")
            
            print(f"Rolando {qtd_final} dados...")
            
            # Rolar
            atacante.dados_atuais = atacante.rolar_dados(qtd_final)
            atacante.dados_atuais = self.fase_rerrolagem(atacante.dados_atuais)

            # Resolver
            mov = self.resolver_turno(atacante, defensor)
            self.arena_posicao += (mov * direcao)

            # Vitoria
            if self.arena_posicao > 4:
                limpar_tela()
                self.desenhar_arena()
                print(f"\n{Cores.VERDE}🏆 {self.jogadores[0].nome} VENCEU! 🏆{Cores.RESET}")
                rodando = False
            elif self.arena_posicao < -4:
                limpar_tela()
                self.desenhar_arena()
                print(f"\n{Cores.VERDE}🏆 {self.jogadores[1].nome} VENCEU! 🏆{Cores.RESET}")
                rodando = False
            
            if rodando: self.turno_atual += 1
