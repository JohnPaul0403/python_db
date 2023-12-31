document.addEventListener(
    'DOMContentLoaded',
    () => {
        const socket = io({autoConnect: false});

        socket.on('message', (data) => {
            console.log(data)
        })
    }
)