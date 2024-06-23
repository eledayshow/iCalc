const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let drawing = false;

resizeCanvas();

window.addEventListener('resize', resizeCanvas);
canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mousemove', draw);

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

function startDrawing(event) {
    drawing = true;
    draw(event);  // Начинаем рисовать сразу при нажатии
}

function stopDrawing() {
    drawing = false;
    ctx.beginPath();  // Заканчиваем текущий путь, чтобы линии не соединялись
}

function draw(event) {
    if (!drawing) return;
    
    ctx.lineWidth = 5;
    ctx.lineCap = 'round';
    ctx.strokeStyle = 'black';
    
    ctx.lineTo(event.clientX, event.clientY);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(event.clientX, event.clientY);
}

function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function sendImage() {
    canvas.toBlob((blob) => {
        const formData = new FormData();
        formData.append('image', blob, 'canvas.png');

        fetch('/process_image', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            const img = new Image();
            img.src = 'data:image/png;base64,' + btoa(data.image);
            document.body.appendChild(img);
        })
        .catch(error => console.error('Error:', error));
    });
}
