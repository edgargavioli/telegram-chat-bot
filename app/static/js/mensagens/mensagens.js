const messagesContainer = document.querySelector('.messages-content');
const sendBtn = document.querySelector('.send-btn');

let mensagem = [];

function loadAllMessagesFirstTime(){
    fetch('/api/messages', {
        method: 'GET',
    }).then(response => {
        return response.json();
    }).then(messages => {
        messages.forEach(msg => {
            mensagem.push(msg);
        });
    }).catch(error => {
        console.error(error);
    });
}

loadAllMessagesFirstTime();

socket.on('new_message', (msg_back) => {
    const chatAtivo = document.querySelector('.contact-item.active')?.getAttribute('data-chat-id');

    mensagem.push(msg_back);

    if (msg_back.chat_id == chatAtivo) {
        const message = document.createElement('div');
        message.classList.add('message', 'received');
        message.textContent = msg_back.message;

        messagesContainer.appendChild(message);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    } else {
        const contactItem = document.querySelector(`.contact-item[data-chat-id="${msg_back.chat_id}"]`);

        if (contactItem) {
            const lastMessageElem = contactItem.querySelector('.last-message');
            lastMessageElem.textContent = msg_back.message;

            contactItem.classList.add('new_message');
        }
    }
});


document.querySelector('.message-input').addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

sendBtn.addEventListener('click', sendMessage);

function fetchMessages(chatId, messageContent, type) {
    fetch('/api/messages/send', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            chat_id: chatId,
            message: messageContent,
            type: type
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
            fetchMessages(chatId, messageContent, 'transmitir');
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

        fetchMessages(activeContact.getAttribute('data-chat-id'), messageContent, 'sent');
        mensagem.push({chat_id: Number(activeContact.getAttribute('data-chat-id')), message: messageContent, type: 'sent'});

        const lastMessageElem = activeContact.querySelector('.last-message');
        lastMessageElem.textContent = messageContent;

        const message = document.createElement('div');
        message.classList.add('message', 'sent');
        message.textContent = messageContent;
        messagesContainer.appendChild(message);

        input.value = '';
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

}

function lastMessageChatId(chat_id){
    let lastMessage = '';
    mensagem.forEach(msg => {
        if(msg.chat_id === chat_id) {
            lastMessage = msg.message;
        }
    });
    return lastMessage;
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
                        <span class="last-message">${lastMessageChatId(client.chat_id)}</span>
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

            let lastMessage = '';

            mensagem.forEach(msg => {
                if(msg.chat_id === client.chat_id) {
                    const message = document.createElement('div');
                    message.classList.add('message', msg.type);
                    message.textContent = msg.message;
                    messagesContainer.appendChild(message);

                    lastMessage = msg.message;
                }
            });

            const contactItem = document.querySelector(`.contact-item[data-chat-id="${client.chat_id}"]`);
            const lastMessageElem = contactItem.querySelector('.last-message');
            lastMessageElem.textContent = lastMessage;

            if (contactItem) {
                contactItem.classList.remove('new_message');
            }

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
