async function loadClientsForSelect() {
    try {
        const response = await fetch('/api/clients');
        if (!response.ok) {
            throw new Error("Erro ao carregar os clientes.");
        }

        const clients = await response.json();
        const clientSelect = document.getElementById('client_id');
        const selectedClientId = clientSelect.getAttribute('data-selected-client');

        clientSelect.innerHTML = '<option value="" disabled selected>Selecione um cliente</option>';

        clients.forEach(client => {
            const option = document.createElement('option');
            option.value = client.id;
            option.textContent = client.name;

            if (client.id == selectedClientId) {
                option.selected = true;
            }

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
    select.classList.add('product-select');
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
    quantityInput.classList.add('quantity-input');
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

document.getElementById('client_id').addEventListener('change', function () {
    const selectedClientId = this.value;
    const viewClientLink = document.getElementById('view-client-link');

    if (selectedClientId) {
        viewClientLink.href = `/clientes/editar/${selectedClientId}`;
        viewClientLink.style.display = 'inline';
    } else {
        viewClientLink.href = '#';
        viewClientLink.style.display = 'none';
    }
});

window.addEventListener('load', () => {
    const clientSelect = document.getElementById('client_id');
    const selectedClientId = clientSelect.getAttribute('data-selected-client');
    const viewClientLink = document.getElementById('view-client-link');

    if (selectedClientId) {
        viewClientLink.href = `/clientes/editar/${selectedClientId}`;
        viewClientLink.style.display = 'inline';
    }
});

window.onload = async function () {
    await loadClientsForSelect();
    const products = await loadProducts();

    const productsContainer = document.getElementById('products-container');
    const addProductButton = document.getElementById('add-product-btn');

    initializeExistingRows();

    if (addProductButton) {
        addProductButton.addEventListener('click', () => {
            const productRow = createProductRow(products);
            productsContainer.appendChild(productRow);
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

function initializeExistingRows() {
    const existingRows = document.querySelectorAll('.product-item');
    existingRows.forEach(row => {
        const productSelect = row.querySelector('.product-select');
        const quantityInput = row.querySelector('.quantity-input');

        if (productSelect) {
            productSelect.addEventListener('change', calculateTotal);
        }

        if (quantityInput) {
            quantityInput.addEventListener('input', calculateTotal);
        }
    });

    initializeRemoveButtons();
}

function initializeRemoveButtons() {
    const existingRemoveButtons = document.querySelectorAll('.remove-product-btn');
    existingRemoveButtons.forEach(button => {
        button.removeEventListener('click', handleRemoveButton);
        button.addEventListener('click', handleRemoveButton);
    });
}

function handleRemoveButton(event) {
    const button = event.currentTarget;
    const productItem = button.closest('.product-item');

    if (productItem) {
        productItem.remove();
        calculateTotal();
    }
}