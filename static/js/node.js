const express = require('express');
const path = require('path');

const app = express();
const PORT = 3000;

// Definindo EJS como motor de template
app.set('view engine', 'ejs');

// Servindo arquivos estáticos (CSS, JS)
app.use(express.static(path.join(__dirname, 'static')));

// Usando body-parser para processar o formulário
app.use(express.urlencoded({ extended: true }));

// Página inicial com o formulário para adicionar produtos
app.get('/', (req, res) => {
    res.render('index');
});

// Redireciona para produtos após adicionar
app.post('/adicionar_produto', (req, res) => {
    const { nome, quantidade, preco } = req.body;
    console.log(`Produto Adicionado: ${nome}, Quantidade: ${quantidade}, Preço: ${preco}`);

    // Redireciona para a página de produtos após adicionar o produto
    res.redirect('/produtos');
});

// Página de exibição de produtos
app.get('/produtos', (req, res) => {
    // Suponhamos que você tenha uma lista de produtos, que pode ser vinda de um banco de dados
    const produtos = [
        { nome: 'Produto 1', quantidade: 10, preco: 50.00 },
        { nome: 'Produto 2', quantidade: 5, preco: 100.00 }
    ];

    res.render('produtos', { produtos });
});

app.listen(PORT, () => {
    console.log(`Servidor Node.js rodando na porta ${PORT}`);
});
