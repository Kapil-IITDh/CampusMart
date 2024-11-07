const currentUserId = 1; // Replace with the logged-in user ID
let selectedUserId = null;

// Temporary list of users (Replace this with data fetched from your backend in production)
const temporaryUsers = [
    { user_id: 2, name: 'mridul' },
    { user_id: 3, name: 'manish' },
    { user_id: 4, name: 'kamla' },
    { user_id: 5, name: 'endu pindu' }
];

// Function to load the temporary user list and display it in the sidebar
function loadTemporaryUserList() {
    const userList = document.getElementById('userList');
    userList.innerHTML = ''; // Clear the existing user list

    // Populate the sidebar with the temporary list of users
    temporaryUsers.forEach(user => {
        const userItem = document.createElement('li');
        userItem.classList.add('user-item');
        userItem.textContent = user.name; // Display the user's name
        userItem.onclick = () => selectUser(user.user_id, user.name);
        userList.appendChild(userItem);
    });
}

// Function to select a user and display their chat messages
function selectUser(userId, userName) {
    selectedUserId = userId;
    document.getElementById('chatHeader').textContent = `Chatting with ${userName}`;

    // Highlight the selected user in the sidebar
    const userItems = document.querySelectorAll('.user-item');
    userItems.forEach(item => item.classList.remove('selected'));
    const selectedItem = Array.from(userItems).find(item => item.textContent === userName);
    if (selectedItem) selectedItem.classList.add('selected');

    // Display messages for the selected user
    displayMessages(userId);
}

// Function to display messages between the current user and the selected user
function displayMessages(userId) {
    const messageList = document.getElementById('messageList');
    messageList.innerHTML = ''; // Clear the current message list

    // Sample JSON response simulating chat messages
    const sampleMessages = [
        { sender_id: 1, receiver_id: 2, content: 'code hua?', timestamp: '2024-11-07 10:00:00' },
        { sender_id: 2, receiver_id: 1, content: 'na ni ho payega kl takk', timestamp: '2024-11-07 10:05:00' },
        { sender_id: 1, receiver_id: 2, content: 'are tansion na le, sab ho jayega', timestamp: '2024-11-07 10:10:00' }
    ];

    // Filter and display messages that involve the current user and the selected user
    sampleMessages.forEach(message => {
        if ((message.sender_id === currentUserId && message.receiver_id === userId) ||
            (message.sender_id === userId && message.receiver_id === currentUserId)) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message');
            messageDiv.classList.add(message.sender_id === currentUserId ? 'sent' : 'received');
            messageDiv.textContent = message.content;
            messageList.appendChild(messageDiv);
        }
    });

    // Scroll to the bottom of the message list to show the latest messages
    messageList.scrollTop = messageList.scrollHeight;
}

// Load the temporary user list when the page loads
document.addEventListener('DOMContentLoaded', loadTemporaryUserList);

// Function to call the API and display all users the logged-in user has chatted with

// Function to fetch and display the users the current user has chatted with
async function fetchChatUsers(currentUserId) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/users/${currentUserId}/chats`);
        const users = await response.json();

        if (response.ok) {
            const userList = document.getElementById('userList');
            userList.innerHTML = ''; // Clear existing user list
            // alert("fetched"+users[0].user_name);
            // Display the list of users
            users.forEach(user => {
                const userItem = document.createElement('li');
                userItem.classList.add('user-item');
                userItem.textContent = user.user_name;
                userItem.onclick = () => fetchAndDisplayMessages(currentUserId, user.user_id, user.user_name);
                userList.appendChild(userItem);
            });
        } else {
            console.error('Failed to load user list:', users.error);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Function to fetch and display messages with a selected user
async function fetchAndDisplayMessages(currentUserId, otherUserId, otherUserName) {
    selectedUserId = otherUserId;

    try {
        const response = await fetch(`http://127.0.0.1:5000/messages/${currentUserId}`);
        const messages = await response.json();

        if (response.ok) {
            const messageList = document.getElementById('messageList');
            const chatHeader = document.getElementById('chatHeader');
            messageList.innerHTML = ''; // Clear the current message list
            chatHeader.textContent = `Chat with ${otherUserName}`; // Update the header with the selected user

            // Filter and display messages between the current user and the selected user
            messages.forEach(message => {
                if ((message.senderID === currentUserId && message.receiverID === otherUserId) ||
                    (message.senderID === otherUserId && message.receiverID === currentUserId)) {
                    
                    const messageDiv = document.createElement('div');
                    messageDiv.classList.add('message');
                    messageDiv.classList.add(message.senderID === currentUserId ? 'sent' : 'received');
                    messageDiv.textContent = `${message.senderName}: ${message.content}`;
                    messageList.appendChild(messageDiv);
                }
            });

            // Scroll to the bottom of the message list
            messageList.scrollTop = messageList.scrollHeight;
        } else {
            console.error('Failed to load messages:', messages.error);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}


window.onload = function() {
    fetchChatUsers(currentUserId);
};
function fecth(){
    fetchChatUsers(currentUserId);
}

// Function to send a message and display it in the chat screen
async function sendMessage(currentUserId, receiverId) {
    // Display an alert for debugging purposes
    // alert(`Sender ID: ${currentUserId}, Receiver ID: ${receiverId}`);
    
    // Get the message input element and trim the content
    const messageInput = document.getElementById('messageInput');
    const messageContent = messageInput.value.trim();

    // Check if the message content is not empty
    if (messageContent) {
        try {
            // Send the message to the server using the Fetch API
            const response = await fetch('http://127.0.0.1:5000/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    sender_id: currentUserId,
                    receiver_id: receiverId,
                    message: messageContent
                })
            });

            // Check if the response status is OK (status code 200-299)
            if (response.ok) {
                const result = await response.json();
                console.log(result.message); // Log confirmation message

                // Display the sent message in the chat window
                const messageList = document.getElementById('messageList');
                const messageDiv = document.createElement('div');
                messageDiv.classList.add('message', 'sent');
                messageDiv.textContent = messageContent;
                messageList.appendChild(messageDiv);

                // Scroll to the bottom of the message list to display the new message
                messageList.scrollTop = messageList.scrollHeight;

                // Clear the message input field after sending
                messageInput.value = '';
            } else {
                console.error(`Failed to send message. Status: ${response.status}, ${response.statusText}`);
                alert(`Failed to send message. Please try again.`);
            }
        } catch (error) {
            // Log any errors that occur during the fetch request
            console.error('Error:', error);
            alert('An error occurred while sending the message. Please try again.');
        }
    } else {
        // Alert if the message content is empty
        alert('Please enter a message before sending.');
    }
}


// Event listener for the "Send" button
document.getElementById('sendButton').addEventListener('click', () => {
    const receiverId = selectedUserId; // Replace with the actual selected user ID
    sendMessage(currentUserId, receiverId);
});
