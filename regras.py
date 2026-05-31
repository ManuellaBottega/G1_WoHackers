import sqlite3
import random
import banco 

# DICIONÁRIOS DE DADOS DO JARDIM

ESPECIES_DISPONIVEIS = {
    "Jiboia": {"rega_dias": 7, "sol_ideal": "meia-sombra"},
    "Samambaia": {"rega_dias": 3, "sol_ideal": "sombra"},
    "Cacto": {"rega_dias": 20, "sol_ideal": "sol_direto"},
    "Espada-de-são-jorge": {"rega_dias": 14, "sol_ideal": "meia-sombra"},
    "Comigo-ninguém-pode": {"rega_dias": 7, "sol_ideal": "sombra"},
    "Suculenta": {"rega_dias": 10, "sol_ideal": "sol_direto"},
    "Trepadeira": {"rega_dias": 4, "sol_ideal": "sol_direto"},
    "Lírio-da-paz": {"rega_dias": 4, "sol_ideal": "sombra"},
    "Costela-de-adão": {"rega_dias": 7, "sol_ideal": "meia-sombra"},
    "Rosa": {"rega_dias": 3, "sol_ideal": "sol_direto"},
    "Orquídea": {"rega_dias": 8, "sol_ideal": "meia-sombra"},
    "Bambu da sorte": {"rega_dias": 5, "sol_ideal": "sombra"}
}

AFINIDADE_INICIAL_ESPECIES = {
    "Jiboia": {
        "Costela-de-adão": 48, "Orquídea": 40, "Espada-de-são-jorge": 35, 
        "Cacto": 10, "Suculenta": 15, "Rosa": 12 
    },
    "Samambaia": {
        "Lírio-da-paz": 48, "Bambu da sorte": 45, "Comigo-ninguém-pode": 38, 
        "Cacto": 2, "Suculenta": 5, "Rosa": 10
    },
    "Cacto": {
        "Suculenta": 48, "Espada-de-são-jorge": 38, 
        "Samambaia": 2, "Lírio-da-paz": 5, "Bambu da sorte": 5, "Orquídea": 8 
    },
    "Espada-de-são-jorge": {
        "Cacto": 38, "Suculenta": 40, "Jiboia": 35, 
        "Lírio-da-paz": 15, "Samambaia": 18 
    },
    "Comigo-ninguém-pode": {
        "Samambaia": 38, "Lírio-da-paz": 42, 
        "Cacto": 5, "Suculenta": 10, "Trepadeira": 12 
    },
    "Suculenta": {
        "Cacto": 48, "Espada-de-são-jorge": 38, "Trepadeira": 35, 
        "Samambaia": 5, "Lírio-da-paz": 8, "Bambu da sorte": 10
    },
    "Trepadeira": {
        "Rosa": 45, "Suculenta": 35, 
        "Samambaia": 10, "Lírio-da-paz": 12, "Orquídea": 15
    },
    "Lírio-da-paz": {
        "Samambaia": 48, "Bambu da sorte": 45, "Comigo-ninguém-pode": 40, 
        "Cacto": 2, "Suculenta": 5, "Rosa": 8
    },
    "Costela-de-adão": {
        "Jiboia": 45, "Orquídea": 40, 
        "Cacto": 10, "Rosa": 15, "Trepadeira": 18
    },
    "Rosa": {
        "Trepadeira": 45, 
        "Cacto": 8, 
        "Samambaia": 5, "Lírio-da-paz": 8 
    },
    "Orquídea": {
        "Costela-de-adão": 42, "Jiboia": 40, 
        "Cacto": 5, "Suculenta": 8, "Rosa": 12
    },
    "Bambu da sorte": {
        "Lírio-da-paz": 45, "Samambaia": 42, "Comigo-ninguém-pode": 38,
        "Cacto": 5, "Suculenta": 8, "Trepadeira": 10
    }
}

# FUNÇÕES DE REGRAS DE RELACIONAMENTO E GERAÇÃO DE PEDIDOS

def cadastrar_nova_planta(nome_customizado, especie, nome_arquivo_foto='default_planta.png'):
    local_inicial = ESPECIES_DISPONIVEIS[especie]["sol_ideal"]
    
    # Usando a função do banco.py
    conexao = banco.conectar_banco()
    cursor = conexao.cursor()

    cursor.execute('''
        INSERT INTO Plantas (nome_customizado, especie, dias_sem_rega, local_atual, foto_perfil, ja_atendida)
        VALUES (?, ?, 0, ?, ?, 0)
    ''', (nome_customizado, especie, local_inicial, nome_arquivo_foto))
    
    nova_planta_id = cursor.lastrowid

    cursor.execute("SELECT id, especie FROM Plantas WHERE id != ?", (nova_planta_id,))
    outras_plantas = cursor.fetchall()
    
    for planta in outras_plantas:
        id_antiga, especie_antiga = planta
        
        afinidade_base_nova = AFINIDADE_INICIAL_ESPECIES.get(especie, {}).get(especie_antiga, 25)
        afinidade_base_antiga = AFINIDADE_INICIAL_ESPECIES.get(especie_antiga, {}).get(especie, 25)
        
        afinidade_nova_para_antiga = max(0, min(50, afinidade_base_nova + random.randint(-15, 15)))
        afinidade_antiga_para_nova = max(0, min(50, afinidade_base_antiga + random.randint(-15, 15)))
        
        cursor.execute('INSERT INTO Relacionamentos VALUES (?, ?, ?)', (nova_planta_id, id_antiga, afinidade_nova_para_antiga))
        cursor.execute('INSERT INTO Relacionamentos VALUES (?, ?, ?)', (id_antiga, nova_planta_id, afinidade_antiga_para_nova))

    conexao.commit()
    conexao.close()
    return nova_planta_id

def gerar_frases_planta(planta, outra_planta):
    nome, especie, dias_sem_rega, local_atual = planta
    necessidades = ESPECIES_DISPONIVEIS[especie]
    
    nome_alvo = outra_planta[0] if outra_planta else "sua vizinha"
    local_alvo = outra_planta[1] if outra_planta else None

    if nome_alvo == nome and outra_planta:
        nome_alvo = f"a outra {nome_alvo}"
    
    acoes_boas, acoes_ruins = [], []

    if dias_sem_rega >= necessidades["rega_dias"]:
        acoes_ruins.extend(["Tô morrendo de sede, me rega logo!", "Acho que esqueceram de mim, quero água."])
    else:
        acoes_boas.append("Por favor, me dê um pouco de água.")

    lugares_ruins = [l for l in set(e["sol_ideal"] for e in ESPECIES_DISPONIVEIS.values()) if l != necessidades["sol_ideal"]]

    if local_atual == necessidades["sol_ideal"]:
        if local_alvo == local_atual:
            acoes_ruins.extend([
                f"Tire a {nome_alvo} daqui, ela está roubando minha luz!", 
                f"A presença da {nome_alvo} tá me fazendo murchar, tira ela daqui."
            ])
        
        if lugares_ruins:
            lugar_aleatorio = random.choice(lugares_ruins)
            acoes_ruins.append(f"Tô enjoada daqui, me coloque na {lugar_aleatorio}.")
            if local_alvo == local_atual:
                acoes_ruins.append(f"Manda a {nome_alvo} para a {lugar_aleatorio}, não suporto olhar pra ela!")
    else:
        acoes_boas.append(f"Me coloque na {necessidades['sol_ideal']}, por favor.")
        if local_alvo != local_atual:
            acoes_ruins.append(f"Se eu vou ficar nesse lugar horrível, traga a {nome_alvo} pra sofrer comigo!")

    frases_ruins = [
        "Me coloque na geladeira, não suporto mais esse clima.", 
        f"Jogue a planta {nome_alvo} da janela para ver se ela voa.", 
        f"Acho que a planta {nome_alvo} ficaria ótima como espanador de pó."
    ]
    if local_alvo == local_atual:
        frases_ruins.append(f"Tira a planta {nome_alvo} de perto de mim, a presença dela me enoja.")
    
    frases_boas = [
        "Aprecie a minha beleza estonteante.", 
        f"Faça roupinhas de crochê combinando para mim e para a planta {nome_alvo}."
    ]
    if local_alvo != local_atual:
        frases_boas.append(f"Coloque a gente mais perto, adoro a planta {nome_alvo}!")

    acoes_ruins.append(random.choice(frases_ruins))
    acoes_boas.append(random.choice(frases_boas))

    return acoes_boas, acoes_ruins

def classificar_acoes(id_planta):
    con = banco.conectar_banco()
    cur = con.cursor()
    cur.execute("SELECT nome_customizado, especie, dias_sem_rega, local_atual FROM Plantas WHERE id = ?", (id_planta,))
    planta = cur.fetchone()
    
    cur.execute("SELECT nome_customizado, local_atual FROM Plantas WHERE id != ? ORDER BY RANDOM() LIMIT 1", (id_planta,))
    outra_planta = cur.fetchone()
    con.close()

    if not planta:
        return [], []
        
    return gerar_frases_planta(planta, outra_planta)

def pegar_acao_unica(lista_acoes, pedidos_usados):
    if not lista_acoes:
        return ""
    random.shuffle(lista_acoes)
    for acao in lista_acoes:
        texto_base = acao.split('(')[0].strip() if '(' in acao else acao.strip()
        if texto_base not in pedidos_usados:
            pedidos_usados.add(texto_base)
            return acao
    return lista_acoes[0]

def gerar_pedido_turno(id_p1, pedidos_usados):
    con = banco.conectar_banco()
    cur = con.cursor()
    
    cur.execute("SELECT nome_customizado, ja_atendida FROM Plantas WHERE id = ?", (id_p1,))
    res_p1 = cur.fetchone()
    
    if not res_p1 or res_p1[1] == 1:
        con.close()
        return None
        
    nome_p1 = res_p1[0]
    
    cur.execute("SELECT id, nome_customizado FROM Plantas WHERE id != ? ORDER BY RANDOM() LIMIT 1", (id_p1,))
    p2 = cur.fetchone()
    
    if not p2:
        boas_p1, ruins_p1 = classificar_acoes(id_p1)
        con.close()
        if boas_p1: return random.choice(boas_p1)
        return None

    id_p2, nome_p2 = p2

    cur.execute("SELECT nivel_afinidade FROM Relacionamentos WHERE planta_origem_id = ? AND planta_destino_id = ?", (id_p1, id_p2))
    rela_p1p2 = cur.fetchone()[0]

    cur.execute('''
        SELECT R1.planta_destino_id 
        FROM Relacionamentos R1
        JOIN Relacionamentos R2 ON R1.planta_destino_id = R2.planta_destino_id
        WHERE R1.planta_origem_id = ? AND R1.nivel_afinidade > 35
          AND R2.planta_origem_id = ? AND R2.nivel_afinidade > 35
    ''', (id_p1, id_p2))
    alvo_ciume = cur.fetchone()
    
    boas_p1, ruins_p1 = classificar_acoes(id_p1)
    con.close()

    if alvo_ciume:
        ruins_p1.append(f"Essa {nome_p2} é uma grande de uma talarica!")

    if rela_p1p2 < 25:
        if ruins_p1: return pegar_acao_unica(ruins_p1, pedidos_usados)
    elif rela_p1p2 > 35:
        if boas_p1: return pegar_acao_unica(boas_p1, pedidos_usados)
    else:
        todas_acoes = boas_p1 + ruins_p1
        if todas_acoes: return pegar_acao_unica(todas_acoes, pedidos_usados)

    return None

def finalizar_dia_e_iniciar_turno():
    pedidos_usados = set() 
    
    con = banco.conectar_banco()
    cur = con.cursor()
    
    cur.execute("UPDATE Controle_Dias SET dia_atual = dia_atual + 1 WHERE id = 1")
    cur.execute("UPDATE Plantas SET dias_sem_rega = dias_sem_rega + 1, ja_atendida = 0")
    
    cur.execute("SELECT planta_origem_id, planta_destino_id, nivel_afinidade FROM Relacionamentos")
    para_atualizar = cur.fetchall()
    
    for rel in para_atualizar:
        p_origem, p_destino, afinidade_atual = rel
        nova_afinidade = afinidade_atual + random.randint(-4, 4)
        nova_afinidade = max(0, min(50, nova_afinidade)) 
        
        cur.execute('''
            UPDATE Relacionamentos SET nivel_afinidade = ? 
            WHERE planta_origem_id = ? AND planta_destino_id = ?
        ''', (nova_afinidade, p_origem, p_destino))
    
    cur.execute("SELECT id FROM Plantas")
    plantas = cur.fetchall()
    con.commit()
    con.close()

    novas_mensagens = []
    for planta in plantas:
        mensagem = gerar_pedido_turno(planta[0], pedidos_usados)
        if mensagem:
            novas_mensagens.append({
                "id_planta": planta[0],
                "mensagem": mensagem
            })
            
    return novas_mensagens

def registrar_acao_historico(id_planta, acao, cur=None, con=None):
    fechar_no_fim = False
    if cur is None:
        con = banco.conectar_banco()
        cur = con.cursor()
        fechar_no_fim = True
        
    cur.execute("SELECT dia_atual FROM Controle_Dias WHERE id = 1")
    resultado = cur.fetchone()
    dia_atual = resultado[0] if resultado else 1

    cur.execute('''
        INSERT INTO Historico_Acoes (dia_do_jogo, planta_id, acao_realizada)
        VALUES (?, ?, ?)
    ''', (dia_atual, id_planta, acao))
    
    if fechar_no_fim:
        con.commit()
        con.close()

def interpretar_mensagem(mensagem):
    msg_lower = mensagem.lower()
    intencoes = {
        "agua": any(p in msg_lower for p in ["água", "sede", "rega"]),
        "local": next((l for l in ["sombra", "meia-sombra", "sol_direto"] if l in msg_lower), None),
        "treta": any(p in msg_lower for p in ["tira", "roubando", "enoja", "longe", "janela", "espanador", "sofrer", "talarica"])
    }
    return intencoes, msg_lower

def processar_atendimento(id_planta, mensagem):
    intencoes, msg_lower = interpretar_mensagem(mensagem)
    acao_realizada = f"Atendeu: {mensagem}"
    
    con = banco.conectar_banco()
    cur = con.cursor()
    cur.execute("UPDATE Plantas SET ja_atendida = 1 WHERE id = ?", (id_planta,))

    if intencoes["agua"]:
        cur.execute("UPDATE Plantas SET dias_sem_rega = 0 WHERE id = ?", (id_planta,))
        acao_realizada += " 💧"

    if intencoes["local"]:
        cur.execute("UPDATE Plantas SET local_atual = ? WHERE id = ?", (intencoes["local"], id_planta))
        acao_realizada += f" ☀️ ({intencoes['local']})"

    cur.execute("SELECT id, nome_customizado FROM Plantas WHERE id != ?", (id_planta,))
    todas_outras = cur.fetchall()

    for id_outra, nome_outra in todas_outras:
        if len(nome_outra) > 1 and nome_outra.lower() in msg_lower:
            cur.execute("SELECT nivel_afinidade FROM Relacionamentos WHERE planta_origem_id = ? AND planta_destino_id = ?", (id_planta, id_outra))
            res = cur.fetchone()
            
            if res:
                nova_afinidade = max(0, res[0] - 15) if intencoes["treta"] else min(50, res[0] + 15)
                acao_realizada += f" | 💔 Treta com {nome_outra}" if intencoes["treta"] else f" | 💖 Amizade com {nome_outra}"
                
                cur.execute('''
                    UPDATE Relacionamentos SET nivel_afinidade = ? 
                    WHERE (planta_origem_id = ? AND planta_destino_id = ?) 
                       OR (planta_origem_id = ? AND planta_destino_id = ?)
                ''', (nova_afinidade, id_planta, id_outra, id_outra, id_planta))

    con.commit()
    con.close()

    registrar_acao_historico(id_planta, acao_realizada)
    return True, "Pedido processado com inteligência!"