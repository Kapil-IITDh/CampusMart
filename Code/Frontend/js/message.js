const currentUserId =  getUserId(); // Replace with the logged-in user ID
let selectedUserId = getSellerIdFromUrl() || null; // Get seller ID if passed in URL

// Function to get the seller ID from the URL
function getSellerIdFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    const sellerId = urlParams.get('seller_id');
    console.log('Extracted seller_id:', sellerId); // Debugging line
    return sellerId;
}
function getUserId(){
    // Retrieve the 'user' item from localStorage
    const user = localStorage.getItem('user');
    if (user) {
        const userData = JSON.parse(user);
        const userID = userData.userID;
        console.log('User ID:', userID);
        // alert(userID);
        return userID;
    } else {
        console.log('No user data found in localStorage.');
    }

}
// Load the user list and auto-start chat with the seller if applicable
document.addEventListener('DOMContentLoaded', loadUserList);

// Function to load the user list or display "No chat started yet" if none exist
async function loadUserList() {
    // alert("loaduser");
    const userList = document.getElementById('userList');
    userList.innerHTML = ''; // Clear existing user list
    // alert(currentUserId);
    // alert(selectedUserId);
    try {
        const response = await fetch(`http://127.0.0.1:5000/users/${currentUserId}/chats`);
        const users = await response.json();

        if (response.ok && users.length > 0) {
            users.forEach(user => {
                const userItem = document.createElement('li');
                userItem.classList.add('user-item');
                userItem.textContent = user.user_name;
                userItem.onclick = () => fetchAndDisplayMessages(currentUserId, user.user_id, user.user_name);
                userList.appendChild(userItem);
            });

            // Auto-start chat with the seller if provided via URL
            if (selectedUserId) {
                const seller = users.find(user => user.user_id === parseInt(selectedUserId));
                if (seller) {
                    selectUser(seller.user_id, seller.user_name);
                } else {
                    // Add a placeholder seller item to start a chat
                    const sellerItem = document.createElement('li');
                    sellerItem.classList.add('user-item');
                    sellerItem.textContent = 'Seller';
                    sellerItem.onclick = () => selectUser(selectedUserId, 'Seller');
                    userList.appendChild(sellerItem);
                    selectUser(selectedUserId, 'Seller');
                }
            }
        } else {
            // Show "No chat started yet" if no chats are found
            const noChatItem = document.createElement('li');
            noChatItem.textContent = 'No chat started yet';
            noChatItem.classList.add('no-chat');
            userList.appendChild(noChatItem);
        }
    } catch (error) {
        console.error('Error fetching user list:', error);
    }
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

// Function to fetch and display messages with a selected user
async function fetchAndDisplayMessages(currentUserId, otherUserId, otherUserName) {
    selectedUserId = otherUserId;

    try {
        const response = await fetch(`http://127.0.0.1:5000/messages/${currentUserId}`);
        const messages = await response.json();

        if (response.ok && messages.length > 0) {
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
            const messageList = document.getElementById('messageList');
            messageList.innerHTML = '<p>No messages found.</p>'; // Display if no messages are found
        }
    } catch (error) {
        console.error('Error fetching messages:', error);
    }
}

// Function to send a message and display it in the chat screen
async function sendMessage(currentUserId, receiverId) {
    const messageInput = document.getElementById('messageInput');
    const messageContent = messageInput.value.trim();

    if (messageContent) {
        try {
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

            if (response.ok) {
                const result = await response.json();
                console.log(result.message);

                const messageList = document.getElementById('messageList');
                const messageDiv = document.createElement('div');
                messageDiv.classList.add('message', 'sent');
                messageDiv.textContent = messageContent;
                messageList.appendChild(messageDiv);

                messageList.scrollTop = messageList.scrollHeight;
                messageInput.value = '';
            } else {
                console.error('Failed to send message:', response.status, response.statusText);
                alert('Failed to send message. Please try again.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while sending the message. Please try again.');
        }
    } else {
        alert('Please enter a message before sending.');
    }
}
function startMessagePolling() {
    if (selectedUserId) {
        setInterval(() => {
            fetchAndDisplayMessages(currentUserId, selectedUserId);
            

        }, 500); // Poll every 5 seconds
    }
}

// Event listener for the "Send" button
document.getElementById('sendButton').addEventListener('click', () => {
    if (selectedUserId) {
        sendMessage(currentUserId, selectedUserId);
    } else {
        alert('No user selected for the chat.');
    }
});
