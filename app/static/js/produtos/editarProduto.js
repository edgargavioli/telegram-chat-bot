async function loadCategoriesForSelect() {
    try {
        const response = await fetch('/api/categories');
        if (!response.ok) {
            throw new Error("Erro ao carregar as categorias.");
        }

        const categories = await response.json();
        const categorySelect = document.getElementById('categorySelect');
        const selectedCategoryId = categorySelect.getAttribute('data-selected-category');

        categorySelect.innerHTML = '<option value="">Selecione uma categoria</option>';

        categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category.id;
            option.textContent = category.name;

            if (category.id == selectedCategoryId) {
                option.selected = true;
            }

            categorySelect.appendChild(option);
        });
    } catch (error) {
        console.error(error);
        alert("Erro ao carregar as categorias.");
    }
}

window.onload = loadCategoriesForSelect;
