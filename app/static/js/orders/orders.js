async function loadProducts() {
    try {
        const response = await fetch('/api/orders');
        if (!response.ok) {
            throw new Error("Erro ao carregar os produtos.");
        }
        const orders = await response.json();
        const tableBody = document.getElementById('ordersTable');
        tableBody.innerHTML = '';

        const editIconUrl = `${window.location.origin}/static/img/editar.png`;
        const deleteIconUrl = `${window.location.origin}/static/img/excluir.png`;

        orders.forEach(orders => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${orders.id}</td>
                <td>${orders.client.name}</td>
                <td>${orders.created_date}</td>
                <td>R$ ${orders.status}</td>
                <td>${orders.amount}</td>
                <td>
                    <a onclick="window.location.href='${window.location.origin}/produtos/editar/${orders.id}'"><img src="${editIconUrl}" alt="Editar" class="action-pic"></a>
                    <a onclick="deleteProduct(${orders.id})"><img src="${deleteIconUrl}" alt="Excluir" class="action-pic"></a>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error(error);
        alert("Erro ao carregar os produtos.");
    }
}

async function deleteProduct(id) {
    if (confirm("Tem certeza de que deseja excluir este produto?")) {
        const response = await fetch(`/api/orders/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (response.ok) {
            alert("Produto excluído com sucesso!");
            loadProducts();
        } else {
            alert("Erro ao excluir o produto.");
        }
    }
}

window.onload = loadProducts;
