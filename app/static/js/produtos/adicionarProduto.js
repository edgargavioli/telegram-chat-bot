async function loadCategoriesForSelect() {
    try {
        const response = await fetch('/api/categories');
        if (!response.ok) {
            throw new Error("Erro ao carregar as categorias.");
        }
        
        const categories = await response.json();
        const categorySelect = document.getElementById('categorySelect');
        categorySelect.innerHTML = '<option value="" disabled selected>Selecione uma categoria</option>';

        categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category.id;
            option.textContent = category.name;
            categorySelect.appendChild(option);
        });
    } catch (error) {
        console.error(error);
        alert("Erro ao carregar as categorias.");
    }
}

window.onload = loadCategoriesForSelect;