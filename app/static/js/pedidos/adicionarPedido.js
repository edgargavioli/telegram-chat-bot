async function loadClientsForSelect() {
    try {
        const response = await fetch('/api/clients');
        if (!response.ok) {
            throw new Error("Erro ao carregar os clientes.");
        }

        const clients = await response.json();
        const clientSelect = document.getElementById('client_id');

        if (!clientSelect) {
            console.error("Elemento 'client_id' não encontrado no DOM.");
            return;
        }

        clientSelect.innerHTML = '<option value="" disabled selected>Selecione um cliente</option>';

        clients.forEach(client => {
            const option = document.createElement('option');
            option.value = client.id;
            option.textContent = client.name;
            clientSelect.appendChild(option);
        });
    } catch (error) {
        console.error(error);
        alert("Erro ao carregar os clientes.");
    }
}

async function loadProducts() {
    try {
        const response = await fetch('/api/products');
        if (!response.ok) {
            throw new Error("Erro ao carregar os produtos.");
        }

        const products = await response.json();
        return products.map(product => ({
            id: product.id,
            name: product.name,
            price: product.price
        }));
    } catch (error) {
        console.error(error);
        alert("Erro ao carregar os produtos.");
        return [];
    }
}

function createProductSelect(products) {
    const select = document.createElement('select');
    select.name = "products[]";
    select.classList.add('product-select', 'login-input');
    select.required = true;

    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = 'Selecione um produto';
    defaultOption.disabled = true;
    defaultOption.selected = true;
    select.appendChild(defaultOption);

    products.forEach(product => {
        const option = document.createElement('option');
        option.value = product.id;
        option.textContent = `${product.name} - R$ ${product.price}`;
        option.dataset.price = product.price;
        select.appendChild(option);
    });

    return select;
}

function calculateTotal() {
    const productRows = document.querySelectorAll('.product-item');
    let total = 0;

    productRows.forEach(row => {
        const productSelect = row.querySelector('select');
        const quantityInput = row.querySelector('input[name="quantities[]"]');

        if (productSelect && quantityInput) {
            const selectedOption = productSelect.options[productSelect.selectedIndex];
            const price = parseFloat(selectedOption.dataset.price || 0);
            const quantity = parseInt(quantityInput.value || 0);

            total += price * quantity;
        }
    });

    const totalInput = document.getElementById('amount');
    if (totalInput) {
        totalInput.value = total.toFixed(2);
    }
}

function createProductRow(products) {
    const container = document.createElement('div');
    container.classList.add('product-item');

    const productSelect = createProductSelect(products);
    productSelect.addEventListener('change', calculateTotal);

    const quantityInput = document.createElement('input');
    quantityInput.type = 'number';
    quantityInput.name = 'quantities[]';
    quantityInput.placeholder = 'Quantidade';
    quantityInput.min = 1;
    quantityInput.classList.add('quantity-input', 'login-input');
    quantityInput.required = true;
    quantityInput.addEventListener('input', calculateTotal);

    const removeButton = document.createElement('button');
    removeButton.type = 'button';
    removeButton.textContent = 'Remover';
    removeButton.classList.add('remove-product-btn');
    removeButton.addEventListener('click', () => {
        container.remove();
        calculateTotal();
    });

    container.appendChild(productSelect);
    container.appendChild(quantityInput);
    container.appendChild(removeButton);

    return container;
}

function validateForm(event) {
    const productRows = document.querySelectorAll('.product-item');
    if (productRows.length === 0) {
        alert("É necessário adicionar pelo menos um produto.");
        event.preventDefault();
        return false;
    }
    return true;
}

window.onload = async () => {
    const clientSelect = document.getElementById('client_id');
    if (clientSelect) {
        await loadClientsForSelect();
    } else {
        console.error("Elemento 'client_id' não encontrado no DOM.");
    }

    const productsContainer = document.getElementById('products-container');
    if (productsContainer) {
        const products = await loadProducts();
        const initialRow = createProductRow(products);
        productsContainer.appendChild(initialRow);
    } else {
        console.error("Elemento 'products-container' não encontrado no DOM.");
    }

    const addProductButton = document.getElementById('add-product-btn');
    if (addProductButton) {
        addProductButton.addEventListener('click', async () => {
            const products = await loadProducts();
            const container = document.getElementById('products-container');
            if (container) {
                const productRow = createProductRow(products);
                container.appendChild(productRow);
            } else {
                console.error("Elemento 'products-container' não encontrado no DOM.");
            }
        });
    } else {
        console.error("Elemento 'add-product-btn' não encontrado no DOM.");
    }

    const orderForm = document.querySelector('.product-form-container');
    if (orderForm) {
        orderForm.addEventListener('submit', validateForm);
    } else {
        console.error("Formulário não encontrado no DOM.");
    }
};
