async function loadOrders() {
    try {
        const response = await fetch('/api/orders');
        if (!response.ok) {
            throw new Error("Erro ao carregar os pedidos.");
        }
        const orders = await response.json();
        const tableBody = document.getElementById('ordersTable');
        tableBody.innerHTML = '';

        const editIconUrl = `${window.location.origin}/static/img/editar.png`;
        const deleteIconUrl = `${window.location.origin}/static/img/excluir.png`;

        orders.forEach(order => {
            const row = document.createElement('tr');

            //const formattedDate = formatDate(order.created_date);

            const formattedAmount = Number(order.amount).toFixed(2);
            row.innerHTML = `
                <td>${order.id}</td>
                <td>${order.client.name}</td>
                <td>${order.created_date}</td>
                <td>${order.status}</td>
                <td>R$ ${formattedAmount}</td>
                <td>
                    <a onclick="window.location.href='${window.location.origin}/pedidos/editar/${order.id}'"><img src="${editIconUrl}" alt="Editar" class="action-pic"></a>
                    <a onclick="deleteOrder(${order.id})"><img src="${deleteIconUrl}" alt="Excluir" class="action-pic"></a>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error(error);
        alert("Erro ao carregar os pedidos.");
    }
}

async function deleteOrder(id) {
    if (confirm("Tem certeza de que deseja excluir este produto?")) {
        const response = await fetch(`/api/orders/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (response.ok) {
            alert("Pedido excluído com sucesso!");
            loadOrders();
        } else {
            alert("Erro ao excluir o pedido.");
        }
    }
}

window.onload = loadOrders;
