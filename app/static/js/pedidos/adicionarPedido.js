async function loadClientsForSelect() {
    try {
        const response = await fetch('/api/clients');
        if (!response.ok) {
            throw new Error("Erro ao carregar as clientes.");
        }
        
        const clients = await response.json();
        const clientSelect = document.getElementById('client_id');
        clientSelect.innerHTML = '<option value="">Selecione um cliente</option>';

        clients.forEach(client => {
            const option = document.createElement('option');
            option.value = client.id;
            option.textContent = client.name;
            clientSelect.appendChild(option);
        });
    } catch (error) {
        console.error(error);
        alert("Erro ao carregar as clientes.");
    }
}

window.onload = loadClientsForSelect;