from flask import Flask, render_template, request, jsonify
from PIL import Image, ImageOps, ImageDraw
import io
import numpy as np
import cv2

app = Flask(__name__)

def preprocess_image(image):
    # Конвертируем изображение в градации серого и инвертируем цвета
    image = image.convert('L')
    image = ImageOps.invert(image)
    image = image.resize((28, 28), Image.ANTIALIAS)
    image = np.array(image)
    image = image / 255.0
    image = image.reshape(1, 28, 28, 1)
    return image

def draw_boxes(image, boxes, labels):
    draw = ImageDraw.Draw(image)
    for box, label in zip(boxes, labels):
        draw.rectangle(box, outline="red", width=2)
        draw.text((box[0], box[1] - 10), str(label), fill="red")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file in request'}), 400

    file = request.files['image']
    image = Image.open(file.stream)
    image.save('no_boxes.png')

    # Пример простой обработки изображения для поиска контуров цифр
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    boxes = []
    labels = []

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 10 and h > 10:  # Исключаем слишком маленькие контуры
            boxes.append((x, y, x + w, y + h))
            labels.append('?')  # В данном примере не выполняется реальное распознавание

    draw_boxes(image, boxes, labels)

    # Конвертируем изображение обратно в байты для отправки обратно клиенту
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    return jsonify({'message': 'Image processed successfully', 'image': img_byte_arr.decode('latin1')})

if __name__ == '__main__':
    app.run(debug=True)
