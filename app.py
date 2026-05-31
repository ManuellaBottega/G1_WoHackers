import os
import random
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import banco
import regras

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
banco.criar_tabelas()

def arquivo_permitido(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/cadastrar', methods=['POST'])
def cadastrar_planta():
    nome = request.form.get('nome')
    especie = request.form.get('especie')

    if not nome or not especie:
        return jsonify({"erro": "Nome e espécie são obrigatórios"}), 400

    if especie not in regras.ESPECIES_DISPONIVEIS:
        return jsonify({"erro": "Espécie inválida"}), 400

    nome_arquivo_salvo = 'default_planta.png'
    if 'foto' in request.files:
        arquivo = request.files['foto']
        if arquivo and arquivo.filename != '' and arquivo_permitido(arquivo.filename):
            extensao = arquivo.filename.rsplit('.', 1)[1].lower()
            nome_seguro = secure_filename(f"{nome}_{random.randint(100, 999)}.{extensao}")
            caminho_completo = os.path.join(app.config['UPLOAD_FOLDER'], nome_seguro)
            arquivo.save(caminho_completo)
            nome_arquivo_salvo = nome_seguro

    try:
        novo_id = regras.cadastrar_nova_planta(nome, especie, nome_arquivo_salvo)
        return jsonify({"sucesso": True, "mensagem": f"{nome} entrou no chat!", "id": novo_id}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/api/plantas', methods=['GET'])
def listar_plantas():
    con = banco.conectar_banco()
    cur = con.cursor()
    cur.execute("SELECT id, nome_customizado, especie, foto_perfil FROM Plantas")
    plantas = cur.fetchall()
    con.close()

    lista_plantas = []
    for p in plantas:
        lista_plantas.append({
            "id": p[0],
            "nome": p[1],
            "especie": p[2],
            "foto_url": f"/static/uploads/{p[3]}" if p[3] != 'default_planta.png' else "/static/default_planta.png"
        })
        
    return jsonify(lista_plantas)

@app.route('/api/turno', methods=['GET'])
def rodar_turno():
    con = banco.conectar_banco()
    cur = con.cursor()
    cur.execute("SELECT id FROM Plantas")
    plantas_existentes = cur.fetchall()
    con.close()

    pedidos = []
    pedidos_usados_temp = set() 
    for p in plantas_existentes:
        id_planta = p[0]
        pedido_texto = regras.gerar_pedido_turno(id_planta, pedidos_usados_temp)
        
        if pedido_texto:
            pedidos.append({
                "id_planta": id_planta,
                "mensagem": pedido_texto
            })

    return jsonify({"pedidos_do_turno": pedidos})

@app.route('/api/atender/<int:id_planta>', methods=['POST'])
def atender_pedido(id_planta):
    dados = request.get_json()
    mensagem = dados.get('mensagem', '')
    
    try:
        sucesso, msg_retorno = regras.processar_atendimento(id_planta, mensagem)
        return jsonify({"sucesso": sucesso, "mensagem": msg_retorno}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    
@app.route('/api/avancar-dia', methods=['POST'])
def avancar_dia():
    try:
        pedidos = regras.finalizar_dia_e_iniciar_turno()
        return jsonify({"sucesso": True, "pedidos_do_turno": pedidos}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    
#Você encontrou um pedaço do codigo do diario secreto! Tire o comentarios desses lugares para ler as relacões dos membros do jardim:

#1. Na parte de baixo do HTML, tem um bloco comentado que começa com "<!--" e termina com "-->". Dentro dele, tem o código do modal do diário secreto. Descomente ele para ativar o botão e a janela do diário.
#2. No final do script, tem uma função chamada "abrirDiarioSecreto" e outra chamada "fecharModalDiario". Elas estão comentadas, descomente elas para ativar a funcionalidade de abrir e fechar o diário secreto.
#3. No arquivo app.py, tem um endpoint comentado chamado "/api/diario". Descomente ele para ativar a funcionalidade de buscar os dados do diário secreto.
#4. Após rodar o código, clique no olho que apareceu no canto da tela!

# @app.route('/api/diario', methods=['GET'])
# def buscar_diario():
#     con = banco.conectar_banco()
#     cur = con.cursor()
    
    # cur.execute('''
    #     SELECT H.dia_do_jogo, P.nome_customizado, H.acao_realizada 
    #     FROM Historico_Acoes H
    #     JOIN Plantas P ON H.planta_id = P.id
    #     ORDER BY H.id DESC LIMIT 15
    # ''')
    # historico = [{"dia": r[0], "nome": r[1], "acao": r[2]} for r in cur.fetchall()]
    
    # cur.execute('''
    #     SELECT P1.nome_customizado, P2.nome_customizado, R.nivel_afinidade
    #     FROM Relacionamentos R
    #     JOIN Plantas P1 ON R.planta_origem_id = P1.id
    #     JOIN Plantas P2 ON R.planta_destino_id = P2.id
    #     ORDER BY R.nivel_afinidade DESC
    # ''')
    # relacionamentos = []
    # for r in cur.fetchall():
    #     if r[2] > 35:
    #         status = "ama"
    #     elif r[2] < 20:
    #         status = "odeia"
    #     else:
    #         status = "neutro"
            

    #     if status != "neutro":
    #         relacionamentos.append({"planta_origem": r[0], "planta_destino": r[1], "status": status, "nivel": r[2]})
            
#    con.close()
#    return jsonify({"historico": historico, "relacionamentos": relacionamentos}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)