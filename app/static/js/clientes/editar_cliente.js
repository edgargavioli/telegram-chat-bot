async function loadClientData(id) {
    try {
        const response = await fetch(`/api/clients/${id}`);
        const client = await response.json();

        document.getElementById('chat_id').value = client.chat_id;
        document.getElementById('name').value = client.name;
        document.getElementById('phone_number').value = client.phone_number;
        document.getElementById('city').value = client.city;
        document.getElementById('address').value = client.address;
    } catch (error) {
        console.error("Erro ao carregar os dados do cliente:", error);
    }
}

document.getElementById('edit-client-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const clientId = window.location.pathname.split('/').pop();
    const formData = new FormData(this);

    try {
        const response = await fetch(`/api/clients/${clientId}`, {
            method: 'PUT',
            body: formData
        });
        const data = await response.json();

        if (response.ok) {
            alert("Cliente atualizado com sucesso!");
            window.location.href = "/clientes";
        } else {
            alert("Erro ao atualizar o cliente.");
        }
    } catch (error) {
        console.error("Erro ao enviar dados:", error);
    }
});

// Carregar os dados do cliente na abertura da página
document.addEventListener("DOMContentLoaded", () => {
    const clientId = window.location.pathname.split('/').pop();
    loadClientData(clientId);
});
