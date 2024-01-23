import MdParser from "./parse_model.js";

document.addEventListener(
    'DOMContentLoaded',
    () => {
        var socket = io.connect('http://' + location.host);
        let username = ""
        let assistant_id = ""
        let assistant_name = ""

        function messageText(sender, text) {
            const mdParser = MdParser(text)
            const messages = document.getElementById('messages');
            messages.innerHTML += '<div><strong>' + sender + ': </strong>' + mdParser.parse() + '</div>';
        }

        socket.on('connect', () => {
            console.log('connected');
        })

        socket.on('disconnect', () => {
            console.log('disconnected');
        })

        socket.on('Username', 
            (data) => {
                console.log(data)
                username = data
            })

        socket.on('assistant',
            (data) => {
                console.log(data)
                assistant_id = data["assistant_id"]
                assistant_name = data["name"]
                //document.getElementById("assistant_id").innerHTML = data.assistant_id
                document.getElementById("assistant_name").innerHTML = assistant_name
                console.log(assistant_name)
            }
        )

        socket.on('Bot Response', (data) => {
            messageText(assistant_name, data);
            console.log(data)
        })

        document.getElementById('form').onsubmit = ev => {
            const textField = document.getElementById('text');
            messageText(username, textField.value)
            ev.preventDefault();    
            socket.emit('message', [textField.value, assistant_id]);
            textField.value = '';
        }
    }
)