from flask import Flask, render_template, request, jsonify
import banco
import regras

app = Flask(__name__)

banco.criar_tabelas()

@app.route('/')
def index():
    """Renderiza a interface principal do chat."""
    return render_template('index.html')

@app.route('/api/cadastrar', methods=['POST'])
def cadastrar_planta():
    dados = request.get_json()
    nome = dados.get('nome')
    especie = dados.get('especie')

    if not nome or not especie:
        return jsonify({"erro": "Nome e espécie são obrigatórios"}), 400

    # NOVA VALIDAÇÃO AQUI
    if especie not in regras.ESPECIES_DISPONIVEIS:
        return jsonify({"erro": "Espécie inválida"}), 400

    try:
        novo_id = regras.cadastrar_nova_planta(nome, especie)
        return jsonify({"sucesso": True, "mensagem": f"{nome} entrou no chat!", "id": novo_id}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/api/plantas', methods=['GET'])
def listar_plantas():
    """Retorna a lista de plantas para o front-end montar a tela."""
    con = banco.conectar_banco()
    cur = con.cursor()
    # Ajustado para selecionar apenas as colunas que realmente existem no banco
    cur.execute("SELECT id, nome_customizado, especie FROM Plantas")
    plantas = cur.fetchall()
    con.close()

    lista_plantas = []
    for p in plantas:
        lista_plantas.append({
            "id": p[0],
            "nome": p[1],
            "especie": p[2]
        })
        
    return jsonify(lista_plantas)

@app.route('/api/turno', methods=['GET'])
def rodar_turno():
    """Gera os pedidos do dia para atualizar o chat e aumenta os dias sem rega."""
    try:
        # A função de regras agora processa o dia, previne frases repetidas e aumenta a sede
        pedidos = regras.finalizar_dia_e_iniciar_turno()
        return jsonify({"pedidos_do_turno": pedidos})
    except Exception as e:
         return jsonify({"erro": str(e)}), 500