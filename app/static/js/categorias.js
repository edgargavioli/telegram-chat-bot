async function deleteCategory(id) {
    if (confirm("Tem certeza de que deseja excluir esta categoria?")) {
        const response = await fetch(`/api/categories/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (response.ok) {
            alert("Categoria excluída com sucesso!");
            window.location.reload();
        } else {
            alert("Erro ao excluir a categoria.");
        }
    }
}

async function loadCategories() {
    try {
        const response = await fetch('/api/categories');
        if (!response.ok) {
            throw new Error("Erro ao carregar as categorias.");
        }
        const categories = await response.json();
        const tableBody = document.getElementById('categoriesTable');
        tableBody.innerHTML = '';

        const editIconUrl = `${window.location.origin}/static/img/editar.png`;
        const deleteIconUrl = `${window.location.origin}/static/img/excluir.png`;

        categories.forEach(category => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${category.id}</td>
                <td>${category.name}</td>
                <td>
                    <a onclick="window.location.href='${window.location.origin}/categorias/editar/${category.id}'"><img src="${editIconUrl}" alt="Editar" class="action-pic"></a>
                    <a onclick="deleteCategory(${category.id})"><img src="${deleteIconUrl}" alt="Excluir" class="action-pic"></a>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error(error);
        alert("Erro ao carregar as categorias.");
    }
}

window.onload = loadCategories;