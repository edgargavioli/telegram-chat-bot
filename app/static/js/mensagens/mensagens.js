const messagesContainer = document.querySelector('.messages-content');
const sendBtn = document.querySelector('.send-btn');

const socket = io('http://localhost:5000');

let mensagem = [];

socket.on('new_message', (msg_back) => {
    // Obtém o ID do chat ativo
    let chatAtivo = document.querySelector('.contact-item.active').getAttribute('data-chat-id');
    
    // Adiciona a mensagem recebida no array de mensagens
    mensagem.push(msg_back);
    console.log(msg_back);
    console.log(chatAtivo);
    
    // Verifica se a mensagem recebida é do chat ativo
    if (msg_back.chat_id == chatAtivo) {
        // Cria um novo elemento de mensagem recebida
        const message = document.createElement('div');
        message.classList.add('message', 'received');
        message.textContent = msg_back.message;
        
        // Adiciona a nova mensagem ao contêiner de mensagens
        messagesContainer.appendChild(message);

        // Rola a área de mensagens para baixo (para mostrar a nova mensagem)
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
});

document.querySelector('.message-input').addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

sendBtn.addEventListener('click', sendMessage);

function fetchMessages(chatId, messageContent) {
    fetch('/api/messages/send', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            chat_id: chatId,
            message: messageContent
        })
    }).catch(error => {
        console.error(error);
    });
}

function sendMessage() {
    const input = document.querySelector('.message-input');
    const messageContent = input.value.trim();
    const liqeuquero = document.querySelectorAll('.contact-item');

    if(sendBtn.classList.contains('transmitir-btn')) {
        liqeuquero.forEach(li => {
            const chatId = li.getAttribute('data-chat-id');
            fetchMessages(chatId, messageContent);
        })
        const message = document.createElement('div');
        message.classList.add('message', 'sent');
        message.textContent = messageContent;
        messagesContainer.appendChild(message);
        input.value = '';
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        return
    }

    if (messageContent) {
        const activeContact = document.querySelector('.contact-item.active');

        fetchMessages(activeContact.getAttribute('data-chat-id'), messageContent);

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
                listItem.setAttribute('data-chat-id', client.chat_id);
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
            sendBtn.classList.remove('transmitir-btn');
            const contactName = document.getElementById('contact-name');
            const contactPic = document.getElementById('contact-pic');
            const messageInputContainer = document.querySelector('.message-input-container');
            const lis = document.querySelectorAll('.contact-item');

            lis.forEach(li => {
                if (li.getAttribute('data-id') === clientId.toString()) {
                    li.classList.add('active');
                } else {
                    li.classList.remove('active');
                }
            })

            contactName.textContent = client.name;
            contactPic.style.display = 'block';
            messageInputContainer.style.display = 'flex';

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

            mensagem.forEach(msg => {
                if(msg.chat_id === client.chat_id) {
                    const message = document.createElement('div');
                    message.classList.add('message', 'received');
                    message.textContent = msg.message;
                    messagesContainer.appendChild(message);
                }
            });

            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        })
        .catch(error => {
            console.error(error);
        });
}

function transmitir() {
    sendBtn.classList.add('transmitir-btn');
    const contactName = document.getElementById('contact-name');
    const messageInputContainer = document.querySelector('.message-input-container');

    contactName.textContent = 'Transmissão';
    messageInputContainer.style.display = 'flex';

    messagesContainer.innerHTML = '';

    messagesContainer.scrollTop = messagesContainer.scrollHeight;
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
