// Grab elements, create settings, etc.
window.addEventListener('load', function() {
 
var video = document.getElementById('video_in');
var video_out = document.getElementById('video_out');
const captureVideoButton = document.getElementById('start-button');
const stopVideoButton = document.getElementById('stop-button');
const goHomeSafeButton = document.getElementById('detect')

// Get access to the camera!
captureVideoButton.onclick = function() {
if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    // Not adding `{ audio: true }` since we only want video now
    navigator.mediaDevices.getUserMedia({ video: [50,50]}).then(function(stream) {
        // video.src = window.URL.createObjectURL(stream);
        // console.log(video)
        
        video.srcObject = stream;
        video.play();
    });
}
}
const getFrame = () => {
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0);
            const data = canvas.toDataURL('image/png', 0.7);
            return data;
        }

const WS_URL = 'ws://127.0.0.1:8000/ws/detect';
const FPS = 10;
const ws = new WebSocket(WS_URL);

ws.onopen = () => {
    console.log(`Connected to ${WS_URL}`);
    
}

goHomeSafeButton.onclick = function() {
	console.log('goHomeSafeButton clicked')
	window.sendFrame = setInterval(() => {
                ws.send(getFrame());
            }, 1000 / FPS);
}
ws.onmessage = function(e){
console.log('Data Received!')
video_out.src = e.data
// video_out.play()

}
stopVideoButton.onclick = function() {
	video.srcObject = new MediaStream();
}
ws.onclose = () => {
	console.log(`Disconnected to ${WS_URL}`);
	clearInterval(window.sendFrame)
}
})


