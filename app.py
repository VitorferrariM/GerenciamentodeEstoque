from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
import psycopg2

app = Flask(__name__)

# Configuração do banco de dados (com os dados do Render)
DB_HOST = 'dpg-cs99jt23esus739cjlrg-a.oregon-postgres.render.com'
DB_NAME = 'extensao_5i4j'
DB_USER = 'extensao_5i4j_user'
DB_PASS = '0KA1KZfXAMMq6nl6Ofs1d0sdfdKNcMKG'

# Função para obter conexão com o banco de dados
def get_db_connection():
    try:
        print("Conectando ao banco de dados...")
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=5432
        )
        print("Conexão bem-sucedida!")
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {str(e)}")
        return None

# Função para garantir que a pasta de imagens exista
def ensure_upload_folder():
    upload_folder = 'static/img'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
        print(f"Pasta '{upload_folder}' criada com sucesso!")

# Rota para exibir a página inicial
@app.route('/')
def index():
    return render_template('index.html')  # Renderizando o template da página inicial

# Rota para exibir o formulário de adicionar produto
@app.route('/adicionar')
def adicionar_produto():
    return render_template('adicionar_produto.html')  # Renderizando o template do formulário

# Rota para processar o envio do produto (POST)
@app.route('/adicionar_produto', methods=['POST'])
def adicionar_produto_processar():
    try:
        print("Recebendo dados do formulário...")

        # Verificar se o arquivo imagem foi enviado
        if 'imagem' not in request.files:
            print("Erro: Imagem não enviada.")
            return jsonify({'success': False, 'message': 'Imagem não enviada'})

        # Receber os dados do formulário
        nome = request.form['nome']
        quantidade = request.form['quantidade']
        preco = request.form['preco']
        imagem = request.files['imagem']

        print(f"Nome: {nome}, Quantidade: {quantidade}, Preço: {preco}, Imagem: {imagem.filename}")

        if nome and quantidade and preco and imagem:
            # Garantir que o diretório de upload exista
            ensure_upload_folder()

            # Salvar a imagem na pasta estática
            imagem_path = os.path.join('static/img', imagem.filename)
            imagem.save(imagem_path)
            print(f"Imagem salva em: {imagem_path}")

            # Conectar ao banco e inserir os dados
            conn = get_db_connection()
            if conn is None:
                return jsonify({'success': False, 'message': 'Erro ao conectar ao banco de dados'})

            cur = conn.cursor()

            # Inserir produto no banco de dados
            cur.execute('INSERT INTO produtos (nome, quantidade, preco, imagem) VALUES (%s, %s, %s, %s)',
                        (nome, quantidade, preco, imagem.filename))
            conn.commit()

            # Fechar conexão
            cur.close()
            conn.close()

            print("Produto adicionado com sucesso.")
            return jsonify({'success': True, 'message': 'Produto adicionado com sucesso'})

        # Se algum campo não estiver preenchido
        print("Erro: Dados incompletos.")
        return jsonify({'success': False, 'message': 'Dados incompletos'})

    except Exception as e:
        print(f"Erro: {str(e)}")  # Captura e exibe o erro
        return jsonify({'success': False, 'message': 'Erro ao processar a requisição'})

# Rota para exibir os produtos cadastrados
@app.route('/produtos.html')
def ver_produtos():
    try:
        # Conectar ao banco de dados
        conn = get_db_connection()
        if conn is None:
            print("Conexão falhou.")
            return jsonify({'success': False, 'message': 'Erro ao conectar ao banco de dados'})

        cur = conn.cursor()
        
        # Obter os produtos cadastrados
        cur.execute('SELECT id, nome, quantidade, preco, imagem FROM produtos')
        produtos = cur.fetchall()
        
        # Fechar conexão
        cur.close()
        conn.close()

        if not produtos:
            print("Nenhum produto encontrado.")
        
        # Renderizar o template com a lista de produtos
        return render_template('produtos.html', produtos=produtos)

    except Exception as e:
        print(f"Erro ao exibir produtos: {str(e)}")  # Mostrar a mensagem de erro
        return jsonify({'success': False, 'message': 'Erro ao exibir produtos'})

# Rota para excluir um produto
@app.route('/excluir/<int:produto_id>', methods=['POST'])
def excluir_produto(produto_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({'success': False, 'message': 'Erro ao conectar ao banco de dados'})

        cur = conn.cursor()
        cur.execute("DELETE FROM produtos WHERE id = %s", (produto_id,))
        conn.commit()

        cur.close()
        conn.close()
        return redirect(url_for('ver_produtos'))  # Redireciona de volta para a página de produtos

    except Exception as e:
        print(f"Erro ao excluir produto: {str(e)}")
        return jsonify({'success': False, 'message': 'Erro ao excluir produto'})

if __name__ == '__main__':
    app.run(debug=True)
