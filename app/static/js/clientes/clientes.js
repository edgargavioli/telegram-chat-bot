async function deleteClient(id) {
    if (confirm("Tem certeza de que deseja excluir este cliente?")) {
        const response = await fetch(`/api/clients/${id}`, { // Corrigido o uso de crase
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (response.ok) {
            alert("Cliente excluído com sucesso!");
            window.location.reload();
        } else {
            alert("Erro ao excluir o cliente.");
        }
    }
}

async function loadClients() {

    const editIconUrl = `${window.location.origin}/static/img/editar.png`;
    const deleteIconUrl = `${window.location.origin}/static/img/excluir.png`;

    try {
        const response = await fetch('/api/clients'); // Corrigido o endpoint
        if (!response.ok) {
            throw new Error("Erro ao carregar os clientes.");
        }
        const clients = await response.json();
        const tableBody = document.getElementById('clienteTable'); // Corrigido o ID no HTML
        tableBody.innerHTML = '';

        clients.forEach(client => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${client.id}</td>
                <td>${client.chat_id}</td>
                <td>${client.name}</td>
                <td>${client.phone_number}</td>
                <td>${client.city}</td>
                <td>${client.address}</td>
                <td>
                    <button onclick="editClient(${client.id})">
                     <img src="${editIconUrl}" alt="Editar" class="action-pic">
                     </button>
                    <button onclick="deleteClient(${client.id})">
                     <img src="${deleteIconUrl}" alt="Excluir" class="action-pic">
                    </button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error(error);
        alert("Erro ao carregar os clientes.");
    }
}
    function editClient(id){
        window.location.href =  `/clientes/editar/${id}`;
    }
