import os
import random
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import banco
import regras

app = Flask(__name__)

# Configuração do diretório onde as fotos das plantas serão salvas
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limita o upload a 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Garante que as pastas 'static' e 'static/uploads' existam
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

banco.criar_tabelas()

def arquivo_permitido(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/cadastrar', methods=['POST'])
def cadastrar_planta():
    # Usamos request.form porque formulários com arquivos usam multipart/form-data
    nome = request.form.get('nome')
    especie = request.form.get('especie')

    if not nome or not especie:
        return jsonify({"erro": "Nome e espécie são obrigatórios"}), 400

    if especie not in regras.ESPECIES_DISPONIVEIS:
        return jsonify({"erro": "Espécie inválida"}), 400

    # Processamento do upload do arquivo de imagem
    nome_arquivo_salvo = 'default_planta.png'
    if 'foto' in request.files:
        arquivo = request.files['foto']
        if arquivo and arquivo.filename != '' and arquivo_permitido(arquivo.filename):
            extensao = arquivo.filename.rsplit('.', 1)[1].lower()
            # Gera um nome seguro unindo o nome da planta a um número aleatório
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
    # Buscando a coluna foto_perfil do banco
    cur.execute("SELECT id, nome_customizado, especie, foto_perfil FROM Plantas")
    plantas = cur.fetchall()
    con.close()

    lista_plantas = []
    for p in plantas:
        lista_plantas.append({
            "id": p[0],
            "nome": p[1],
            "especie": p[2],
            # Retorna o caminho correto para o front-end renderizar na tag <img src="...">
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
    for p in plantas_existentes:
        id_planta = p[0]
        # O seu regras.py já recebe 'pedidos_usados' aqui. Para fins de compatibilidade,
        # criamos um set temporário por requisição para evitar travamentos
        pedidos_usados_temp = set()
        pedido_texto = regras.gerar_pedido_turno(id_planta, pedidos_usados_temp)
        
        if pedido_texto:
            pedidos.append({
                "id_planta": id_planta,
                "mensagem": pedido_texto
            })

    return jsonify({"pedidos_do_turno": pedidos})

# ... (Mantenha as rotas /api/regar e /api/mover idênticas)

if __name__ == '__main__':
    app.run(debug=True, port=5000)