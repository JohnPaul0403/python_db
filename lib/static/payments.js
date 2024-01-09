import Auth from "./auth_model.js";

document.addEventListener(
    'DOMContentLoaded',
    async () => {
        let socket = io.connect('http://' + location.host);
        let token = ""
        let auth = new Auth()
        const payments = Square.payments(auth.app_id, auth.id_location);
        const card = await payments.card();
        await card.attach('#card-container');
    
        const cardButton = document.getElementById('card-button');
        cardButton.addEventListener('click', async () => {
            const statusContainer = document.getElementById('payment-status-container');
    
            try {
                statusContainer.innerHTML = "Processing payment...";
                const result = await card.tokenize();
                if (result.status === 'OK') {
                    token = result.token
                    socket.emit('token', token)
                    console.log(`Payment token is ${result.token}`);
                    statusContainer.innerHTML = "Payment Successful";
                } else {
                    let errorMessage = `Tokenization failed with status: ${result.status}`;
                    if (result.errors) {
                    errorMessage += ` and errors: ${JSON.stringify(
                        result.errors
                    )}`;
                    }
        
                    throw new Error(errorMessage);
                }
            } catch (e) {
            console.error(e);
            statusContainer.innerHTML = "Payment Failed";
            }
        });

        socket.on('connect', () => {
            console.log('connected');
        })

        socket.on('disconnect', () => {
            console.log('disconnected');
        })
    }
)