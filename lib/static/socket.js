document.addEventListener(
    'DOMContentLoaded',
    () => {
        var socket = io.connect('http://' + location.host);

        function messageText(text) {
            const messages = document.getElementById('messages');
            messages.innerHTML += '<div><strong>' + text + ':</strong></div>';
        }

        socket.on('connect', () => {
            console.log('connected');
        })

        socket.on('Bot Response', (data) => {
            messageText(data);
            console.log(data)
        })

        document.getElementById('form').onsubmit = ev => {
            const textField = document.getElementById('text');
            const assistant_id = document.getElementById("assistant_id").innerHTML
            messageText(textField.value)
            ev.preventDefault();
            socket.emit('message', [textField.value, assistant_id]);
            textField.value = '';
        }
    }
)