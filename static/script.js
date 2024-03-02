const form = document.querySelector('.message-form');

document.querySelector('textarea').addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      form.dispatchEvent(new Event('submit'));
    }
});

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const inputText = document.getElementById('input-text').value;
    
    if (inputText === "") return;

    const chatContainer = document.querySelector('.chat-container');

    // Add user message to chat
    const userMessage = document.createElement('div');
    userMessage.classList.add('chat-message');
    userMessage.innerHTML = `
        <div class="chat-message-content user-message">
            <span>${inputText}</span>
        </div>
    `;
    
    chatContainer.appendChild(userMessage);
    document.getElementById('input-text').value = "";
    document.querySelector('#submit-btn').disabled = true;
    document.querySelector('.logo').src = "static/images/loading.gif"
    chatContainer.scrollTo({top: chatContainer.scrollHeight, behavior: 'smooth'})

    fetch('/send', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({inputText: inputText})
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)


        if (data['missing']) {
            const botMessage = document.createElement('div');
            botMessage.classList.add('chat-message');
            botMessage.innerHTML = `
                <div class="chat-message-content bot-message">
                    <span>${data.message}</span>
                </div>
            `;
            chatContainer.appendChild(botMessage);
            document.querySelector('#submit-btn').disabled = false;
            document.querySelector('.logo').src = "static/images/vpt_logo.jpg"
            return;
        }

        if (data['best_flights'].length == 0) {
            const botMessage = document.createElement('div');
            botMessage.classList.add('chat-message');
            botMessage.innerHTML = `
                <div class="chat-message-content bot-message">
                    <span>${data.message}</span>
                </div>
            `;
            chatContainer.appendChild(botMessage);
            document.querySelector('#submit-btn').disabled = false;
            document.querySelector('.logo').src = "static/images/vpt_logo.jpg"
            return;
        }

        console.log(data)
        
        
        data = data['best_flights'];              
        for (let i = 0; i < data.length; i++) {
            
            const botMessage = document.createElement('div');
            botMessage.classList.add('chat-message');
            
            // Cast price to a number
            let price = data[i]['price']['grandTotal'];
            
            let segments = data[i]['itineraries'][0]['segments'];
            let numberOfSegments = segments.length;
            const totalDuration = data[i]['itineraries'][0]['duration'].match(/^PT(?:([0-9]+)H)?(?:([0-9]+)M)?$/);
            
            
            const messageBlock = document.createElement('div');
            messageBlock.classList.add('chat-message-content');
            messageBlock.classList.add('bot-message');
            
            let itinerariesBlock = document.createElement('div');
            itinerariesBlock.classList.add('itineraries-block');

            for (let j in segments) {
                if (j != 0) {
                    itinerariesBlock.innerHTML += `<div class="divider"></div>`
                }
                
                // https://content.airhex.com/content/logos/airlines_SU_100_100_s.png

                const formatedDeparture = new Date(segments[j]['departure']['at'])
                const formatedArrival = new Date(segments[j]['arrival']['at'])
                const duration = segments[j]['duration'].match(/^PT(?:([0-9]+)H)?(?:([0-9]+)M)?$/);
                const timezone = new Date().toLocaleTimeString('en-US', { timeZoneName: 'short' }).split(' ')[2];

                
                let imgLink = `<img class="airline-logo" src="https://content.airhex.com/content/logos/airlines_${segments[j]['carrierCode'].substring(0, 2)}_100_100_s.png" />`

                if (j > 0 && segments[j]['carrierCode'].substring(0, 2) == segments[j - 1]['carrierCode'].substring(0, 2)) {
                    imgLink = '';
                }

                itinerariesBlock.innerHTML += `
                    ${imgLink}
                    <div class="timeline-block">
                        <div class="depart flight-info">
                            <p>Depart ${segments[j]['departure']['iataCode']}</p>
                            <p>${formatedDeparture.getHours() < 10 ? "0" + formatedDeparture.getHours() : formatedDeparture.getHours()}:${formatedDeparture.getMinutes() < 10 ? "0" + formatedDeparture.getMinutes() : formatedDeparture.getMinutes()} ${timezone}</p>
                            <p>${formatedDeparture.getMonth() + 1}/${formatedDeparture.getDate()}/${formatedDeparture.getFullYear()}</p>
                        </div>
                        <div>
                            <span style="font-size: 5vw; max-width: 20px">&#8594;</span>
                            ${numberOfSegments > 1 ? `<p class="segment-time">${duration[1] ? Number(duration[1]) + " hours" : ""} ${Number(duration[2])} minutes</p>` : ''}
                        </div>
                        <div class="arrive flight-info">
                            <p>Arrival ${segments[j]['arrival']['iataCode']}</p>
                            <p>${formatedArrival.getHours() < 10 ? "0" + formatedArrival.getHours(): formatedArrival.getHours()}:${formatedArrival.getMinutes() < 10 ? "0" + formatedArrival.getMinutes() : formatedArrival.getMinutes()} ${timezone}</p>
                            <p>${formatedArrival.getMonth() + 1}/${formatedArrival.getDate()}/${formatedArrival.getFullYear()}</p>
                        </div>        
                    </div>
                `;
            }

            itinerariesBlock.innerHTML += `<div class="summary-block"><p><span class="title">Grand Price</span>: ${price} USD</p><p><span class="title">Total Duration</span>: ${totalDuration[1] ? Number(totalDuration[1]) + " hours" : ""} ${Number(totalDuration[2])} minutes</p></div>`

            messageBlock.appendChild(itinerariesBlock);

            botMessage.appendChild(messageBlock);
            chatContainer.appendChild(botMessage);

            document.querySelector('#submit-btn').disabled = false;
            document.querySelector('.logo').src = "static/images/vpt_logo.jpg"
            chatContainer.scrollTo({top: chatContainer.scrollHeight, behavior: 'smooth'})
            
        }

    })
    .catch((error) => {
        console.error('Error:', error);
    });
    chatContainer.scrollTo({top: chatContainer.scrollHeight, behavior: 'smooth'})
    
});


const recognition = new webkitSpeechRecognition();
recognition.continuous = true;
recognition.interimResults = true;
recognition.lang = 'en-US';

recognition.onresult = (event) => {
    if (event.results[0][0].cofidence < 0.7) {
        return
    }
    
    document.getElementById('input-text').value = (event.results[0][0].transcript)
}

const mic = document.getElementById('mic');
const micOff = async () => {
    mic.setAttribute('status', 'off');
    mic.classList.add('fa-microphone');
    mic.classList.remove('fa-microphone-slash');
    recognition.stop();
}

const micOn = async () => {
    mic.setAttribute('status', 'on');
    mic.classList.add('fa-microphone-slash');
    mic.classList.remove('fa-microphone');
    recognition.start();
}

mic.addEventListener('click', () => {
    document.getElementById('mic').getAttribute('status') === 'off' ? micOn() : micOff();
});


