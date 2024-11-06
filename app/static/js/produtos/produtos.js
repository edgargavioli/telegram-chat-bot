async function loadProducts() {
    try {
        const response = await fetch('/api/products');
        if (!response.ok) {
            throw new Error("Erro ao carregar os produtos.");
        }
        const products = await response.json();
        const tableBody = document.getElementById('productsTable');
        tableBody.innerHTML = '';

        const editIconUrl = `${window.location.origin}/static/img/editar.png`;
        const deleteIconUrl = `${window.location.origin}/static/img/excluir.png`;

        products.forEach(product => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${product.id}</td>
                <td>${product.name}</td>
                <td>${product.description}</td>
                <td>R$ ${product.price}</td>
                <td>${product.category ? product.category.name : 'Sem categoria'}</td>
                <td>
                    <a onclick="window.location.href='${window.location.origin}/produtos/editar/${product.id}'"><img src="${editIconUrl}" alt="Editar" class="action-pic"></a>
                    <a onclick="deleteProduct(${product.id})"><img src="${deleteIconUrl}" alt="Excluir" class="action-pic"></a>
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
        const response = await fetch(`/api/products/${id}`, {
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
