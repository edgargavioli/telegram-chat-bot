async function deleteClient(id) {
    if (confirm("Tem certeza de que deseja excluir este cliente?")) {
        const response = await fetch(`/api/clients/${id}`, {
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
    try {
        const response = await fetch('/api/clients');
        if (!response.ok) {
            throw new Error("Erro ao carregar os clientes.");
        }
        const clients = await response.json();
        const tableBody = document.getElementById('clientsTable');
        tableBody.innerHTML = '';

        const editIconUrl = `${window.location.origin}/static/img/editar.png`;
        const deleteIconUrl = `${window.location.origin}/static/img/excluir.png`;

        clients.forEach(client => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${client.id}</td>
                <td>${client.name}</td>
                <td>${client.city}</td>
                <td>${client.is_active === true ? "Sim" : "Não"}</td>
                <td>
                    <a onclick="window.location.href='${window.location.origin}/clientes/editar/${client.id}'"><img src="${editIconUrl}" alt="Editar" class="action-pic"></a>
                    <a onclick="deleteClient(${client.id})"><img src="${deleteIconUrl}" alt="Excluir" class="action-pic"></a>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error(error);
        alert("Erro ao carregar os clientes.");
    }
}

window.onload = loadClients;