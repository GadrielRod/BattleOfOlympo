import time
import random
from utils import Cores, limpar_tela, desenhar_dado
from jogador import Jogador
from deuses import TODOS_OS_DEUSES, Kratos

# --- CLASSE PARA A INTELIGÊNCIA ARTIFICIAL ---
class InimigoIA(Jogador):
    """
    IA que simula o comportamento de um jogador humano, tomando decisões 
    baseadas no estado da partida (defesa e dados).
    """
    def __init__(self, nome, deus_escolhido):
        super().__init__(nome, deus_escolhido)

    def decidir_uso_item(self, oponente):
        """Lógica da IA para analisar o inventário e usar itens com pausas visuais."""
        if not self.inventario:
            return
        
        print(f"\n{Cores.CIANO} {self.nome} está analisando itens...{Cores.RESET}")
        time.sleep(1.5)

        for item in self.inventario[:]:
            usar = False
            
            # Prioridade para buffs e debuffs imediatos
            if item in ["Escudo", "Bencao de Hermes", "Caixa de Pandora", "Medusa", "Lanca"]:
                usar = True
            # Itens de cura só se a defesa estiver crítica
            elif item in ["Nectar", "Velocino dourado"] and self.estabilidade <= 70:
                usar = True
            # Ambrosia para finalizar ou empurrar oponente vulnerável
            elif item == "Ambrosia" and oponente.estabilidade <= 50:
                usar = True
            
            if usar:
                print(f"{Cores.CIANO}✨ {self.nome} ativou: {Cores.NEGRITO}{item}{Cores.RESET}!")
                time.sleep(1.2)
                
                idx = self.inventario.index(item)
                self.inventario.pop(idx)
                
                # Execução lógica do efeito do item
                if item == "Nectar": self.curar(25)
                elif item == "Velocino dourado": self.curar(100)
                elif item == "Ambrosia": self.furia_ativa = True
                elif item == "Lanca": self.ataque_extra = True 
                elif item == "Escudo": self.escudo_ativo = True
                elif item == "Bencao de Hermes": self.modificador_dados += 1
                elif item == "Caixa de Pandora": oponente.modificador_dados -= 1
                elif item == "Medusa" and oponente.inventario: 
                    oponente.inventario.pop()
                    print(f"🐍 {oponente.nome} perdeu um item pela Medusa!")
                
                time.sleep(1.0)
                
    def escolher_item_manual(self):
        """
        Sobrescreve a função humana para que a IA escolha o item 
        automaticamente durante o Especial de Atena sem pedir input.
        """
        if len(self.inventario) >= self.max_itens:
            return

        itens_possiveis = [
            "Nectar", "Ambrosia", "Escudo", "Lanca", 
            "Medusa", "Velocino dourado", "Bencao de Hermes", "Caixa de Pandora"
        ]
        
        # Lógica de Sabedoria da IA
        if self.estabilidade <= 60:
            escolha = "Velocino dourado" if self.estabilidade <= 30 else "Nectar"
        else:
            escolha = random.choice(["Lanca", "Bencao de Hermes", "Caixa de Pandora", "Medusa"])
            
        self.inventario.append(escolha)
        print(f"{Cores.CIANO} {self.nome} (Atena) usou sua sabedoria e escolheu: {Cores.NEGRITO}{escolha}{Cores.RESET}")
        time.sleep(1.5)

    def decidir_manter_dados(self, dados):
        """IA escolhe o que manter e informa ao jogador os índices."""
        manter = []
        for i, d in enumerate(dados):
            if d == 6 or d == 1:
                manter.append(i + 1)
        
        # GARANTE QUE A IA SEMPRE MANTENHA ALGO SE NÃO HOUVER 1 OU 6
        if not manter:
            maior = max(dados)
            for i, d in enumerate(dados):
                if d == maior:
                    manter.append(i+1)
                    break

        if dados.count(6) < 2:
            for valor in [6, 5]:
                if dados.count(valor) >= 2:
                    for i, d in enumerate(dados):
                        if d == valor: manter.append(i + 1)

        decisao_str = " ".join(map(str, sorted(list(set(manter)))))
        return decisao_str

# --- MOTOR PRINCIPAL DO JOGO ---
class BattleOfOlympo:
    def __init__(self, modo="PvP"):
        self.modo = modo
        self.jogadores = []
        self.arena_posicao = 0 
        self.turno_atual = 1

    def selecionar_deus(self, nome_jogador):
        while True:
            print(f"\n{Cores.CIANO}--- Escolha seu deus para {nome_jogador} ---{Cores.RESET}")
            for i, classe_deus in enumerate(TODOS_OS_DEUSES):
                temp = classe_deus()
                print(f"[{i+1}] {temp.icone} {temp.nome}")
            
            entrada = input("Digite o numero (ou segredo): ").strip()
            if entrada.upper() in ["KRATOS", "BOY"]:
                print(f"\n{Cores.VERMELHO}⚠️ FANTASMA DE ESPARTA INVOCADO! ⚠️{Cores.RESET}")
                time.sleep(1)
                return Kratos()

            if entrada.isdigit():
                escolha = int(entrada) - 1
                if 0 <= escolha < len(TODOS_OS_DEUSES):
                    return TODOS_OS_DEUSES[escolha]()
            print("Opção inválida!")

    def iniciar_torneio(self):
        limpar_tela()
        print(f"{Cores.CIANO}=== 🏆 MODO TORNEIO: ASCENSÃO NO OLIMPO ==={Cores.RESET}")
        nome_player = input("Digite seu nome, Campeão: ") or "Campeão"
        deus_player = self.selecionar_deus(nome_player)
        p1 = Jogador(nome_player, deus_player)

        deuses_inimigos = [d() for d in TODOS_OS_DEUSES if d().nome != deus_player.nome]
        random.shuffle(deuses_inimigos)

        for i, deus_ia in enumerate(deuses_inimigos):
            # Reset de estado para cada nova luta do torneio
            self.arena_posicao = 0
            self.turno_atual = 1
            p1.inventario = [] 
            p1.estabilidade = 100
            p1.modificador_dados = 0
            
            p2 = InimigoIA(f" {deus_ia.nome}", deus_ia)
            self.jogadores = [p1, p2]
            
            print(f"\n{Cores.AMARELO}RODADA {i+1} de 7{Cores.RESET}")
            print(f"{Cores.NEGRITO}SEU OPONENTE: {p2.nome}{Cores.RESET}")
            time.sleep(2.5)
            
            venceu = self.jogar()
            if not venceu:
                print(f"\n{Cores.VERMELHO}Você foi derrotado por {deus_ia.nome}. O torneio acabou.{Cores.RESET}")
                return False
        
        print(f"\n{Cores.VERDE}✨ INCRÍVEL! Você derrotou todos e é o novo Semideus ✨{Cores.RESET}")
        return True

    def desenhar_hud(self):
        p1, p2 = self.jogadores[0], self.jogadores[1]
        c1 = Cores.VERDE if p1.estabilidade > 50 else Cores.VERMELHO
        c2 = Cores.VERDE if p2.estabilidade > 50 else Cores.VERMELHO

        print(f"{Cores.CIANO}{'='*60}{Cores.RESET}")
        print(f"{p1.deus.icone} {p1.nome:<20} VS {p2.nome:>20} {p2.deus.icone}")
        print(f"{c1}DEF: {p1.estabilidade}%{Cores.RESET:<21}    {c2}DEF: {p2.estabilidade}%{Cores.RESET:>21}")
        print(f"{Cores.CIANO}{'='*60}{Cores.RESET}")

        trilha = [" . "] * 9
        idx = max(0, min(8, self.arena_posicao + 4))
        trilha[idx] = f"{Cores.AMARELO}[⚡]{Cores.RESET}"
        print(f"\n       (P1) {''.join(trilha)} (P2)")

    def fase_rerrolagem(self, jogador, dados):
        rerrolagens = 2
        while rerrolagens > 0:
            if isinstance(jogador, InimigoIA):
                print(f"\n {jogador.nome} está pensando...")
                time.sleep(1.8)
                decisao = jogador.decidir_manter_dados(dados)
                print(f"\nDados atuais: {' '.join([desenhar_dado(d) for d in dados])}")
                if not decisao:
                    print(f" {jogador.nome} decidiu travar os dados atuais.")
                else:
                    print(f" {jogador.nome} decidiu manter os IDs: {decisao}")
                time.sleep(1.2)
            else:
                print(f"\nDados atuais: {' '.join([desenhar_dado(d) for d in dados])}")
                if any(d==1 for d in dados): print(f"{Cores.VERMELHO}Dados 1 travados!{Cores.RESET}")
                decisao = input(f"[Rerrolagens: {rerrolagens}] Manter IDs (ex: 1 3) ou ENTER: ")
            
            # SE APENAS DER ENTER, ENTENDE QUE QUER MANTER TUDO
            if decisao.strip() == "":
                break
           
            try:
                manteve = [int(x)-1 for x in decisao.split()]
                
                # VERIFICA SE O HUMANO TENTOU ESCOLHER O DADO 1
                if not isinstance(jogador, InimigoIA):
                    tentou_1 = False
                    for idx in manteve:
                        if dados[idx] == 1:
                            tentou_1 = True
                            break
                    if tentou_1:
                        print(f"{Cores.VERMELHO}Dados de valor 1 nao podem ser escolhidos para serem travados, escolha algum outro dado.{Cores.RESET}")
                        continue

                dados = [dados[i] if (i in manteve or dados[i] == 1) else random.randint(1, 6) for i in range(len(dados))]
                rerrolagens -= 1
            except: pass
        return dados

    def resolver_turno(self, atacante, defensor):
        """Processa ações com a regra de pares de faces iguais e Ambrosia funcional."""
        dados = atacante.dados_atuais
        c = {i: dados.count(i) for i in range(1, 7)}
        extra = 0
        
        print(f"\nDados finais: {' '.join([desenhar_dado(d) for d in dados])}")
        print(f"\n{Cores.NEGRITO}--- RESOLUÇÃO DE AÇÕES ---{Cores.RESET}")
        time.sleep(1)

        # 1. Especial (Trio de 6 consome os dados)
        if c[6] >= 3: 
            extra = atacante.deus.ativar_especial(atacante, defensor)
            c[6] -= 3
            time.sleep(1)
        
        # 2. Itens (Par de 2)
        if c[2] >= 2:
            for _ in range(c[2] // 2):
                atacante.ganhar_item()

        # 3. Ataque (Apenas pares de faces iguais: 3-3 ou 4-4)
        atks = (c[3] // 2) + (c[4] // 2)
        if atks > 0:
            dano = (atks * 25) + (25 if atacante.ataque_extra else 0)
            defensor.receber_dano(dano)
            time.sleep(0.8)
        
        # 4. Empurrão (Apenas pares iguais: 5-5 ou 6-6 + Bônus Ambrosia)
        emps = (c[5] // 2) + (c[6] // 2)
        mov = 0
        if emps > 0 or extra > 0:
            forca = defensor.vulnerabilidade + (1 if atacante.furia_ativa else 0)
            mov = (emps * forca) + extra
            print(f"💨 Força do empurrão: {mov} casas.")
        
        # Limpeza
        atacante.furia_ativa = False
        atacante.ataque_extra = False
        atacante.modificador_dados = 0 
        return mov

    def jogar(self):
        while True:
            idx = (self.turno_atual + 1) % 2 
            atacante, defensor = self.jogadores[idx], self.jogadores[1 - idx]
            direcao = 1 if idx == 0 else -1

            limpar_tela(); self.desenhar_hud()   
            print(f"\n🎲 TURNO {self.turno_atual}: {atacante.nome}")
            
            if isinstance(atacante, InimigoIA):
                atacante.decidir_uso_item(defensor)
            else:
                atacante.usar_item(defensor)
            
            qtd = max(1, (3 if self.turno_atual <= 2 else 5) + atacante.modificador_dados)
            atacante.dados_atuais = self.fase_rerrolagem(atacante, atacante.rolar_dados(qtd))

            mov = self.resolver_turno(atacante, defensor)
            self.arena_posicao += (mov * direcao)

            if abs(self.arena_posicao) > 4:
                limpar_tela(); self.desenhar_hud()
                venc = self.jogadores[0].nome if self.arena_posicao > 4 else self.jogadores[1].nome
                print(f"\n{Cores.VERDE}🏆 {venc} VENCEU ESTA PARTIDA!{Cores.RESET}")
                time.sleep(2)
                input(f"\n{Cores.VERDE}[Pressione Enter para seguir]{Cores.RESET}")
                return self.arena_posicao > 4
            
            if not isinstance(atacante, InimigoIA): 
                input(f"\n{Cores.VERDE}[Pressione Enter para seguir]{Cores.RESET}")
            self.turno_atual += 1

    def pvp_inicial(self):
        limpar_tela()
        n1 = input("Nome do Jogador 1 (Esquerda): ")
        d1 = self.selecionar_deus(n1)
        limpar_tela()
        n2 = input("Nome do Jogador 2 (Direita): ")
        d2 = self.selecionar_deus(n2)
        self.jogadores = [Jogador(n1, d1), Jogador(n2, d2)]
        self.jogar()
