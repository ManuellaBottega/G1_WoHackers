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
    """Recebe os dados do front-end e cadastra uma nova planta."""
    dados = request.get_json()
    nome = dados.get('nome')
    especie = dados.get('especie')

    if not nome or not especie:
        return jsonify({"erro": "Nome e espécie são obrigatórios"}), 400

    try:
        # Removido o parâmetro 'vaso' que causava erro de assinatura
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
    """Gera os pedidos do dia para atualizar o chat."""
    con = banco.conectar_banco()
    cur = con.cursor()
    cur.execute("SELECT id FROM Plantas")
    plantas_existentes = cur.fetchall()
    con.close()

    pedidos = []
    for p in plantas_existentes:
        id_planta = p[0]
        pedido_texto = regras.gerar_pedido_turno(id_planta)
        
        if pedido_texto:
            pedidos.append({
                "id_planta": id_planta,
                "mensagem": pedido_texto
            })

    return jsonify({"pedidos_do_turno": pedidos})

if __name__ == '__main__':
    app.run(debug=True, port=5000)