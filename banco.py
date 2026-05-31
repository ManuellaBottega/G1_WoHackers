import sqlite3

def conectar_banco():
    conexao = sqlite3.connect('banco_jardim.db')
    return conexao

def criar_tabelas():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Plantas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_customizado TEXT NOT NULL,
            especie TEXT NOT NULL,
            dias_sem_rega INTEGER DEFAULT 0,
            local_atual TEXT NOT NULL,
            foto_perfil TEXT DEFAULT 'default_planta.png',
            ja_atendida INTEGER DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Relacionamentos (
            planta_origem_id INTEGER,
            planta_destino_id INTEGER,
            nivel_afinidade INTEGER DEFAULT 25,
            PRIMARY KEY (planta_origem_id, planta_destino_id),
            FOREIGN KEY (planta_origem_id) REFERENCES Plantas (id),
            FOREIGN KEY (planta_destino_id) REFERENCES Plantas (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Historico_Acoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dia_do_jogo INTEGER NOT NULL,
            planta_id INTEGER,
            acao_realizada TEXT NOT NULL,
            FOREIGN KEY (planta_id) REFERENCES Plantas (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Controle_Dias (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            dia_atual INTEGER DEFAULT 1
        )
    ''')

    cursor.execute("INSERT OR IGNORE INTO Controle_Dias (id, dia_atual) VALUES (1, 1)")

    conexao.commit()
    conexao.close()

if __name__ == '__main__':
    criar_tabelas()