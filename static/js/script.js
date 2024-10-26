document.getElementById('produto-form').addEventListener('submit', function(e) {
    e.preventDefault(); // Previne o comportamento padrão do form

    const nome = document.getElementById('nome').value;
    const quantidade = document.getElementById('quantidade').value;
    const preco = document.getElementById('preco').value;
    const mensagemErro = document.getElementById('mensagem-erro');

    // Verificar se todos os campos estão preenchidos
    if (!nome || !quantidade || !preco) {
        mensagemErro.style.display = 'block'; // Mostra a mensagem de erro
        return; // Para a execução aqui se os campos não estiverem preenchidos
    }

    mensagemErro.style.display = 'none'; // Oculta a mensagem de erro se os campos estiverem preenchidos

    // Enviando dados ao backend (Python/Flask)
    fetch('/adicionar_produto', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nome, quantidade, preco }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Redireciona para a página de produtos após adicionar
            window.location.href = '/produtos';
        } else {
            alert('Erro ao adicionar produto');
        }
    });
});
