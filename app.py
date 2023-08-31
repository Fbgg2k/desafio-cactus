from flask import Flask, render_template, request, g
import sqlite3
from flask import Flask, render_template, request, g, redirect


app = Flask(__name__)

# Configuração do banco de dados
app.config['DATABASE'] = 'fornecedores.db'


# Rota para a página inicial com botões centralizados
@app.route('/')
def index():
    return render_template('index.html')


# Rota para adicionar fornecedor
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar_fornecedor():
    if request.method == 'POST':
        try:
            razao_social = request.form['razao_social']
            endereco = request.form['endereco']
            contato_nome = request.form['contato_nome']
            contato_email = request.form['contato_email']

            # Lógica para armazenar os dados no banco de dados
            db = get_db()

            # Executar a inserção dos dados na tabela fornecedores
            db.execute(
                'INSERT INTO fornecedores (razao_social, endereco, contato_nome, contato_email) VALUES (?, ?, ?, ?)',
                (razao_social, endereco, contato_nome, contato_email)
            )

            # Commit das mudanças
            db.commit()

            # Redirecionar para a página de consulta após a adição bem-sucedida
            return redirect('/')
        except Exception as e:
            return f'Erro ao adicionar fornecedor: {e}'
            
    return render_template('adicionar.html')


@app.route('/consultar')
def consultar_fornecedores():
    try:
        # Conecte-se ao banco de dados
        db = get_db()

        # Execute a consulta para obter os fornecedores
        cursor = db.execute('SELECT razao_social, endereco, contato_nome, contato_email FROM fornecedores')
        fornecedores = cursor.fetchall()
        
        print(fornecedores)  # Adicione este print para verificar os dados lidos do banco de dados

        return render_template('consultar.html', fornecedores=fornecedores)
    except Exception as e:
        return f'Erro ao consultar fornecedores: {e}'



# Função para conectar-se ao banco de dados
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db


# Resto do código...

# ...

# Função para criar a tabela de fornecedores
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Comando para inicializar o banco de dados
@app.cli.command()
def initdb():
    init_db()
    print('Banco de dados inicializado')

# Resto do código...

if __name__ == '__main__':
    app.run()


