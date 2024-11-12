document.getElementById('client-form').addEventListener('submit', function(event) {
    event.preventDefault();  // Impede o comportamento padrão de envio do formulário

    const form = new FormData(this);  // Pega os dados do formulário

    fetch('/api/clients', {
        method: 'POST',
        body: form  // Envia o FormData diretamente
    })
    .then(response => response.json())  // Trata a resposta como JSON
    .then(data => {
        if (data.message) {
            // Se a resposta contiver uma mensagem de sucesso e a URL de redirecionamento
            window.location.href = data.redirect;  // Redireciona para a página de listagem de clientes
        } else {
            alert('Erro ao adicionar cliente');
        }
    })
    .catch(error => {
        console.error('Erro na requisição:', error);
        alert('Erro ao enviar dados');
    });
});
