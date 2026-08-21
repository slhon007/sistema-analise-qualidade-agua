import sqlite3

#dados de análises
def salvar_analise(
    nome,
    data,
    temperatura,
    ph,
    oxigenio_dissolvido,
    nitrato,
    nitrito,
    amonia,
    resultado_dureza,
    resultado_turbidez,
    resultado_std,
    resultado_salinidade,
    relatorio
):
    conn = sqlite3.connect("analise_agua.db")
    cursor = conn.cursor()
    
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS analises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            data TEXT,
            temperatura REAL,
            ph REAL,
            oxigenio_dissolvido REAL, 
            nitrato REAL,
            nitrito REAL,
            amonia REAL, 
            resultado_dureza REAL,
            resultado_turbidez REAL,
            resultado_std REAL,
            resultado_salinidade REAL,
            relatorio TEXT 
            
        )""")
        
    cursor.execute(
        """ INSERT INTO analises (
            nome,
            data,
            temperatura,
            ph,
            oxigenio_dissolvido, 
            nitrato,
            nitrito,
            amonia, 
            resultado_dureza,
            resultado_turbidez,
            resultado_std,
            resultado_salinidade,
            relatorio
        )VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            nome,
            data,
            temperatura,
            ph,
            oxigenio_dissolvido, 
            nitrato,
            nitrito,
            amonia, 
            resultado_dureza,
            resultado_turbidez,
            resultado_std,
            resultado_salinidade,
            relatorio
        ))
    
    conn.commit()
    conn.close()
    
def listar_analises():
    
    conn = sqlite3.connect("analise_agua.db")
    conn.row_factory =sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS analises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            data TEXT,
            temperatura REAL,
            ph REAL,
            oxigenio_dissolvido REAL, 
            nitrato REAL,
            nitrito REAL,
            amonia REAL, 
            resultado_dureza REAL,
            resultado_turbidez REAL,
            resultado_std REAL,
            resultado_salinidade REAL,
            relatorio TEXT 
            
        )""")
    
    cursor.execute("SELECT* FROM analises ORDER BY data DESC")
    
    dados = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return dados

def deletar_analise(id):
    
    conn = sqlite3.connect("analise_agua.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM analises WHERE id = ?", (id,))

    conn.commit()
    conn.close()
    
def nome_existe(nome):
    conn = sqlite3.connect("analise_agua.db")
    cursor =  conn.cursor()
    
    cursor.execute("""SELECT 1 FROM analises WHERE nome = ?""", (nome,))
    
    existe = cursor.fetchone() is not None
    conn.commit()
    conn.close()
    
    return existe
    #documentação
def salvar_documentacao(nome, caminho, tipo):
    
    conn = sqlite3.connect("analise_agua.db")
    cursor = conn.cursor()
    
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS documentacao(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            caminho TEXT NOT NULL,
            tipo TEXT NOT NULL
            )""")
    
    cursor.execute("""INSERT INTO documentacao(
        nome,
        caminho,
        tipo)VALUES (?, ?, ?)""",(nome, caminho, tipo))
    
    conn.commit()
    conn.close()
    
def listar_documentacao():
    conn = sqlite3.connect("analise_agua.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""SELECT * FROM documentacao ORDER BY id DESC""")
    
    documentos = cursor.fetchall()
    
    conn.commit()
    conn.close()
    
    return documentos
    
    
def deletar_documentacao(id):
    
    conn = sqlite3.connect("analise_agua.db")
    cursor = conn.cursor()
    
    cursor.execute("""DELETE FROM documentacao WHERE id = ?""", (id,))
    
    conn.commit()
    conn.close()
    
def documento_existe(nome):
    
    conn = sqlite3.connect("analise_agua.db") 
    cursor = conn.cursor()
    
    cursor.execute("""SELECT 1 FROM documentacao WHERE nome = ?""", (nome,))   
    
    existe = cursor.fetchone() is not None

    conn.commit()
    conn.close()
    return existe