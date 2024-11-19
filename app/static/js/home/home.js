const statuses = [
    { id: "em-espera", title: "🕒 Em Espera" },
    { id: "aceito", title: "👍 Aceito" },
    { id: "recusado", title: "❌ Recusado" },
    { id: "preparando", title: "🍳 Preparando" },
    { id: "pronto", title: "🍽️ Pronto" },
    { id: "saiu-para-entrega", title: "🚚 Saiu para Entrega" },
    { id: "cancelado", title: "🚫 Cancelado" },
    { id: "concluir-pedido", title: "✅ Concluído" },
];

function initializeKanban() {
    const board = document.getElementById("kanban-board");
    statuses.forEach(status => {
        const column = document.createElement("div");
        column.classList.add("kanban-column");
        column.id = status.id;

        column.innerHTML = `
            <h2>${status.title}</h2>
            <div class="kanban-items" ondrop="drop(event)" ondragover="allowDrop(event)"></div>
        `;

        board.appendChild(column);
    });
}

const statusMap = {
    "Espera": "em-espera",
    "Aceito": "aceito",
    "Recusado": "recusado",
    "Preparando": "preparando",
    "Pronto": "pronto",
    "Entrega": "saiu-para-entrega",
    "Cancelado": "cancelado",
    "Concluído": "concluir-pedido",
};

function formatDate(dateString) {
    const date = new Date(dateString);
    date.setHours(date.getHours() + 3);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    
    return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
}

async function loadOrders() {
    try {
        const response = await fetch("/api/orders");
        if (!response.ok) {
            throw new Error("Erro ao carregar pedidos.");
        }

        const orders = await response.json();

        Object.values(statusMap).forEach(columnId => {
            const column = document.querySelector(`#${columnId} .kanban-items`);
            if (column) {
                column.innerHTML = "";
            }
        });

        orders.forEach(order => {
            const mappedStatus = statusMap[order.status];
            if (!mappedStatus) return;
        
            const item = document.createElement("div");
            item.classList.add("kanban-item");
            item.draggable = true;
            item.id = `order-${order.id}`;
            item.ondragstart = drag;
        
            const formattedDate = formatDate(order.created_date);
        
            item.innerHTML = `
                <strong>Pedido #${order.id}</strong><br>
                Cliente: ${order.client ? order.client.name : "Desconhecido"}<br>
                Valor: R$ ${parseFloat(order.amount).toFixed(2)}<br>
                <small>${formattedDate}</small>
            `;
        
            item.onclick = () => {
                window.open(`/pedidos/editar/${order.id}`, '_blank');
            };
        
            const column = document.querySelector(`#${mappedStatus} .kanban-items`);
            if (column) {
                column.appendChild(item);
            }
        });        
    } catch (error) {
        console.error("Erro ao carregar pedidos:", error);
    }
}

function allowDrop(event) {
    event.preventDefault();
}

function drag(event) {
    event.dataTransfer.setData("text", event.target.id);
}

async function drop(event) {
    event.preventDefault();
    const itemId = event.dataTransfer.getData("text");
    const targetColumn = event.target.closest(".kanban-column");

    if (!targetColumn) return;

    const newStatus = targetColumn.id;
    const item = document.getElementById(itemId);

    if (!item) return;

    if (newStatus === "concluir-pedido") {
        if (confirm("Tem certeza de que deseja concluir este pedido?")) {
            item.remove();

            const orderId = itemId.replace("order-", "");

            try {
                const response = await fetch(`/api/orders/status/${orderId}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ status: "Concluído" }),
                });

                if (!response.ok) {
                    const errorText = await response.text();
                    console.error("Erro ao concluir pedido:", errorText);
                    throw new Error("Erro ao concluir pedido");
                }

                console.log("Pedido concluído e excluído com sucesso");
            } catch (error) {
                console.error("Erro ao concluir pedido:", error);
            }
        }
    } else {
        targetColumn.querySelector(".kanban-items").appendChild(item);

        const reverseStatusMap = Object.fromEntries(
            Object.entries(statusMap).map(([key, value]) => [value, key])
        );

        const statusToSave = reverseStatusMap[newStatus];
        if (!statusToSave) return;

        const orderId = itemId.replace("order-", "");

        try {
            const response = await fetch(`/api/orders/status/${orderId}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ status: statusToSave }),
            });

            if (!response.ok) {
                const errorText = await response.text();
                console.error("Erro ao atualizar status no backend:", errorText);
                throw new Error("Erro ao atualizar status no backend.");
            }
        } catch (error) {
            console.error("Erro ao atualizar status:", error);
        }
    }
}

window.onload = () => {
    initializeKanban();
    loadOrders();
};
