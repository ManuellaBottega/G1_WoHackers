import sqlite3
import random

ESPECIES_DISPONIVEIS = {
    "Jiboia": {"rega_dias": 7, "sol_ideal": "meia-sombra"},
    "Samambaia": {"rega_dias": 3, "sol_ideal": "sombra"},
    "Cacto": {"rega_dias": 20, "sol_ideal": "sol_direto"}
}

AFINIDADE_INICIAL_ESPECIES = {
    "Cacto": {"Samambaia": 5, "Jiboia": 40},
    "Samambaia": {"Cacto": 10, "Jiboia": 25},
    "Jiboia": {"Cacto": 35, "Samambaia": 20}
}

def conectar():
    return sqlite3.connect('banco_jardim.db')

def cadastrar_nova_planta(nome_customizado, especie, nome_arquivo_foto='default_planta.png'):
    local_inicial = ESPECIES_DISPONIVEIS[especie]["sol_ideal"]
    
    conexao = conectar()
    cursor = conexao.cursor()

    # Incluindo a foto_perfil no INSERT
    cursor.execute('''
        INSERT INTO Plantas (nome_customizado, especie, dias_sem_rega, local_atual, foto_perfil)
        VALUES (?, ?, 0, ?, ?)
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

def classificar_acoes(id_planta):
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT nome_customizado, especie, dias_sem_rega, local_atual FROM Plantas WHERE id = ?", (id_planta,))
    planta = cur.fetchone()
    
    cur.execute("SELECT nome_customizado FROM Plantas WHERE id != ? ORDER BY RANDOM() LIMIT 1", (id_planta,))
    outra_planta = cur.fetchone()
    con.close()

    if not planta:
        return [], []

    nome, especie, dias_sem_rega, local_atual = planta
    necessidades = ESPECIES_DISPONIVEIS[especie]
    
    nome_alvo = outra_planta[0] if outra_planta else "sua vizinha"
    
    acoes_boas = []
    acoes_ruins = []

    # Corrigido: Reclama de sede se os dias sem rega atingiram ou passaram do limite
    if dias_sem_rega >= necessidades["rega_dias"]:
        acoes_ruins.append(f"Tô morrendo de sede, me rega logo! ({nome})")
        acoes_ruins.append(f"Acho que esqueceram de mim, quero água. ({nome})")
    else:
        acoes_boas.append(f"Por favor, me dê um pouco de água. ({nome})")

    if local_atual == necessidades["sol_ideal"]:
        acoes_ruins.append(f"Me tire daqui, quero ir para outro lugar! ({nome})")
        lugares_possiveis = [esp["sol_ideal"] for esp in ESPECIES_DISPONIVEIS.values()]
        lugares_ruins = [lugo for lugo in lugares_possiveis if lugo != necessidades["sol_ideal"]]
        acoes_ruins.append(f"Me coloque na {random.choice(lugares_ruins)}. ({nome})")
    else:
        acoes_boas.append(f"Me coloque na {necessidades['sol_ideal']}. ({nome})")
        lugares_possiveis = [esp["sol_ideal"] for esp in ESPECIES_DISPONIVEIS.values()]
        lugares_ruins = [lugo for lugo in lugares_possiveis if lugo != necessidades["sol_ideal"]]
        acoes_ruins.append(f"Me mude para a {random.choice(lugares_ruins)}. ({nome})")

    frases_ruins_absurdas = [
        f"Coloque a planta {nome} na geladeira.",
        f"Use as folhas de {nome} para fazer bem-me-quer, mal-me-quer.",
        f"Verifique o alcance de arremesso da planta {nome_alvo} jogando ela da janela.",
        f"Acho que {nome} ficaria ótima sendo usada como espanador de pó."
    ]
    
    frases_boas_absurdas = [
        f"Aprecie a beleza estonteante da planta {nome}.",
        f"Leve a planta {nome} para dar uma volta de carrinho de mão no quarteirão.",
        f"Faça roupinhas de crochê sob medida para a planta {nome}.",
        f"Coloque uma música clássica para {nome} ouvir enquanto fotossintetiza."
    ]

    acoes_ruins.append(random.choice(frases_ruins_absurdas))
    acoes_boas.append(random.choice(frases_boas_absurdas))

    return acoes_boas, acoes_ruins

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
    con = conectar()
    cur = con.cursor()
    
    cur.execute("SELECT nome_customizado FROM Plantas WHERE id = ?", (id_p1,))
    res_p1 = cur.fetchone()
    if not res_p1:
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
    
    cur.execute("SELECT nivel_afinidade FROM Relacionamentos WHERE planta_origem_id = ? AND planta_destino_id = ?", (id_p2, id_p1))
    rela_p2p1 = cur.fetchone()[0]

    cur.execute('''
        SELECT R1.planta_destino_id 
        FROM Relacionamentos R1
        JOIN Relacionamentos R2 ON R1.planta_destino_id = R2.planta_destino_id
        WHERE R1.planta_origem_id = ? AND R1.nivel_afinidade > 35
          AND R2.planta_origem_id = ? AND R2.nivel_afinidade > 35
    ''', (id_p1, id_p2))
    alvo_ciume = cur.fetchone()
    
    boas_p1, ruins_p1 = classificar_acoes(id_p1)
    boas_p2, ruins_p2 = classificar_acoes(id_p2)
    con.close()

    if alvo_ciume:
        rela_p1p2 = 10
        rela_p2p1 = 10
        ruins_p1.append(f"Fica longe, o amor da minha vida prefere a mim! ({nome_p1})")
        ruins_p2.append(f"Sua presença me enoja, você nunca vai ter quem você quer. ({nome_p2})")

    if rela_p1p2 < 20 and rela_p2p1 > 30:
        if ruins_p2: return f"{nome_p2}: {pegar_acao_unica(ruins_p2, pedidos_usados)}"
    elif rela_p2p1 < 20 and rela_p1p2 > 30:
        if ruins_p1: return f"{nome_p1}: {pegar_acao_unica(ruins_p1, pedidos_usados)}"
    elif rela_p1p2 < 20:
        if ruins_p2: return f"{nome_p1}: Ei humano, {pegar_acao_unica(ruins_p2, pedidos_usados).lower()}"
    elif rela_p1p2 > 30:
        if boas_p2: return f"{nome_p1}: Humano, {pegar_acao_unica(boas_p2, pedidos_usados).lower()}"
    elif rela_p2p1 < 20:
        if ruins_p1: return f"{nome_p2}: Que tal se você {pegar_acao_unica(ruins_p1, pedidos_usados).lower()}?"
    elif rela_p2p1 > 30:
        if boas_p1: return f"{nome_p2}: Faça um favor e {pegar_acao_unica(boas_p1, pedidos_usados).lower()}"
    else:
        if boas_p1: 
            return f"{nome_p1}: {pegar_acao_unica(boas_p1, pedidos_usados)}"
    return None

def finalizar_dia_e_iniciar_turno():
    # Cria o controle de pedidos limpo apenas para este turno
    pedidos_usados = set() 
    
    con = conectar()
    cur = con.cursor()
    cur.execute("UPDATE Plantas SET dias_sem_rega = dias_sem_rega + 1")
    
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

def registrar_acao_historico(id_planta, acao):
    con = conectar()
    cur = con.cursor()
    
    cur.execute("SELECT COALESCE(MAX(dia_do_jogo), 1) FROM Historico_Acoes")
    resultado = cur.fetchone()
    dia_atual = resultado[0] if resultado else 1

    cur.execute('''
        INSERT INTO Historico_Acoes (dia_do_jogo, planta_id, acao_realizada)
        VALUES (?, ?, ?)
    ''', (dia_atual, id_planta, acao))
    
    con.commit()
    con.close()

def regar_planta(id_planta):
    con = conectar()
    cur = con.cursor()
    cur.execute("UPDATE Plantas SET dias_sem_rega = 0 WHERE id = ?", (id_planta,))
    con.commit()
    con.close()
    
    registrar_acao_historico(id_planta, "Humano regou a planta")
    return True

def mover_planta(id_planta, novo_local):
    lugares_validos = [esp["sol_ideal"] for esp in ESPECIES_DISPONIVEIS.values()]
    if novo_local not in lugares_validos:
        raise ValueError("Local inválido para as regras do jardim")
        
    con = conectar()
    cur = con.cursor()
    cur.execute("UPDATE Plantas SET local_atual = ? WHERE id = ?", (novo_local, id_planta))
    con.commit()
    con.close()
    
    registrar_acao_historico(id_planta, f"Humano moveu a planta para {novo_local}")
    return True