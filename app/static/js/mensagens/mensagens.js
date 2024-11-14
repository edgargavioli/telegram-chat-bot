document.querySelector('.message-input').addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

document.querySelector('.send-btn').addEventListener('click', sendMessage);

function sendMessage() {
    const input = document.querySelector('.message-input');
    const messageContent = input.value.trim();
    if (messageContent) {
        const messagesContainer = document.querySelector('.messages-content');
        
        const message = document.createElement('div');
        message.classList.add('message', 'sent');
        message.textContent = messageContent;
        messagesContainer.appendChild(message);

        input.value = '';
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}

function loadContacts() {
    const pageContent = document.querySelector('.page-content');
    pageContent.style.height = '100%';
    fetch('/api/clients')
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao carregar clientes');
            }
            return response.json();
        })
        .then(clients => {
            const contactsList = document.getElementById('contacts-list');
            contactsList.innerHTML = '';

            clients.forEach(client => {
                const listItem = document.createElement('li');
                listItem.onclick = () => {
                    carregarMensagens(client.id);
                }
                listItem.classList.add('contact-item');
                listItem.setAttribute('data-id', client.id);
                listItem.setAttribute('data-name', client.name);
                
                listItem.innerHTML = `
                    <img src="/static/img/icons/user.svg" alt="${client.name}" class="contact-pic">
                    <div class="contact-info">
                        <span class="contact-name">${client.name}</span>
                        <span class="last-message">Última mensagem...</span>
                    </div>
                `;
                
                contactsList.appendChild(listItem);
            });
        })
        .catch(error => {
            console.error(error);
        });
}

function carregarMensagens(clientId) {
    fetch(`/api/clients/${clientId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao carregar dados do cliente');
            }
            return response.json();
        })
        .then(client => {
            const contactName = document.getElementById('contact-name');
            const contactPic = document.getElementById('contact-pic');
            const messageInputContainer = document.querySelector('.message-input-container');

            contactName.textContent = client.name;
            contactPic.style.display = 'block';
            messageInputContainer.style.display = 'flex';

            const messagesContainer = document.querySelector('.messages-content');
            messagesContainer.innerHTML = '';
            const receivedMessage1 = document.createElement('div');
            receivedMessage1.classList.add('message', 'received');
            receivedMessage1.textContent = `address: ${client.address}`;
            messagesContainer.appendChild(receivedMessage1);

            const sentMessage1 = document.createElement('div');
            sentMessage1.classList.add('message', 'sent');
            sentMessage1.textContent = `chat_id: ${client.chat_id}`;
            messagesContainer.appendChild(sentMessage1);

            const receivedMessage2 = document.createElement('div');
            receivedMessage2.classList.add('message', 'received');
            receivedMessage2.textContent = `city: ${client.city}`;
            messagesContainer.appendChild(receivedMessage2);

            const sentMessage2 = document.createElement('div');
            sentMessage2.classList.add('message', 'sent');
            sentMessage2.textContent = `id: ${client.id}`;
            messagesContainer.appendChild(sentMessage2);

            const receivedMessage3 = document.createElement('div');
            receivedMessage3.classList.add('message', 'received');
            receivedMessage3.textContent = `is_active: ${client.is_active}`;
            messagesContainer.appendChild(receivedMessage3);

            const sentMessage3 = document.createElement('div');
            sentMessage3.classList.add('message', 'sent');
            sentMessage3.textContent = `name: ${client.name}`;
            messagesContainer.appendChild(sentMessage3);

            const receivedMessage4 = document.createElement('div');
            receivedMessage4.classList.add('message', 'received');
            receivedMessage4.textContent = `phone_number: ${client.phone_number}`;
            messagesContainer.appendChild(receivedMessage4);

            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        })
        .catch(error => {
            console.error(error);
        });
}

function filterContacts() {
    const searchInput = document.getElementById('search-input').value.toLowerCase();
    const contactItems = document.querySelectorAll('.contact-item');
    
    contactItems.forEach(item => {
        const contactName = item.getAttribute('data-name').toLowerCase();
        if (contactName.indexOf(searchInput) !== -1) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });

    const clearIcon = document.getElementById('clear-icon');
    if (searchInput.length > 0) {
        clearIcon.style.display = 'block';
    } else {
        clearIcon.style.display = 'none';
    }
}

function clearSearch() {
    const searchInput = document.getElementById('search-input');
    searchInput.value = '';
    filterContacts();
}

window.onload = loadContacts;
