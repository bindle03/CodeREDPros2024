// // collect DOMs
// let mediaRecorder, chunks = [], audioURL = ''

// // mediaRecorder setup for audio
// if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia){
//     console.log('mediaDevices supported..')

//     navigator.mediaDevices.getUserMedia({
//         audio: true
//     }).then(stream => {
//         mediaRecorder = new MediaRecorder(stream)

//         mediaRecorder.ondataavailable = (e) => {
//             chunks.push(e.data)
//         }

//         mediaRecorder.onstop = async () => {
//             const blob = new Blob(chunks, {'type': 'audio/wav; codecs=opus'})
            
//             chunks = []
        
//             document.getElementById('audio').src = URL.createObjectURL(blob)
//             document.getElementById('audio').play()


//             let reader = new FileReader()
//             reader.readAsDataURL(blob)
//             reader.onloadend = async () => {
//                 let base64data = reader.result

//                 await fetch('/record', {
//                     method: 'POST',
//                     headers: {
//                         'Content-Type': 'application/json'
//                     },
//                     body: JSON.stringify({
//                         'audio': base64data
//                     })
//                 }).then(response => {
//                     return response.json()
//                 }).then(data => {
//                     if (data['status'] === 'success') {
//                         document.getElementById('input-text').value = data['transcript']
//                     }
//                 }).catch(error => {
//                     console.log('Following error has occured : ',error)
//                 })
//             }
            
//         }

        
//     }).catch(error => {
//         console.log('Following error has occured : ',error)
//     })
// }

// const record = () => {
//     mediaRecorder.start()
    
// }

// const stopRecording = () => {
//     mediaRecorder.stop()
// }



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

document.getElementById('mic').addEventListener('click', () => {

    const mic = document.getElementById('mic');
    const status = mic.getAttribute('status');
    if (status === 'off') {
        mic.setAttribute('status', 'on');
        mic.classList.add('fa-microphone-slash');
        mic.classList.remove('fa-microphone');
        recognition.start();
    } else {
        mic.setAttribute('status', 'off');
        mic.classList.add('fa-microphone');
        mic.classList.remove('fa-microphone-slash');
        recognition.stop();
    }
});