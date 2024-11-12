async function deleteUser(id) {
    if (confirm("Tem certeza de que deseja excluir este usuário?")) {
        const response = await fetch(`/api/users/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (response.ok) {
            alert("Usuário excluído com sucesso!");
            window.location.reload();
        } else {
            alert("Erro ao excluir o usuário.");
        }
    }
}

async function loadUsers() {
    try {
        const response = await fetch('/api/users');
        if (!response.ok) {
            throw new Error("Erro ao carregar os usuários.");
        }
        const users = await response.json();
        const tableBody = document.getElementById('usersTable');
        tableBody.innerHTML = '';

        const editIconUrl = `${window.location.origin}/static/img/editar.png`;
        const deleteIconUrl = `${window.location.origin}/static/img/excluir.png`;

        users.forEach(user => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${user.id}</td>
                <td>${user.name}</td>
                <td>${user.username}</td>
                <td>${user.role}</td>
                <td>
                    <a onclick="window.location.href='${window.location.origin}/usuarios/editar/${user.id}'"><img src="${editIconUrl}" alt="Editar" class="action-pic"></a>
                    <a onclick="deleteUser(${user.id})"><img src="${deleteIconUrl}" alt="Excluir" class="action-pic"></a>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error(error);
        alert("Erro ao carregar os usuários.");
    }
}

window.onload = loadUsers;