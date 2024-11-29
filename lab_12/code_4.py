import cv2
import numpy as np
from tkinter import Tk, filedialog
import os

def video_to_bit_array(video_path):
    with open(video_path, 'rb') as file:
        video_bytes = file.read()

    bits = np.unpackbits(np.frombuffer(video_bytes, dtype=np.uint8))
    return bits.tolist()

def hide_video_in_image(image_path, video_path, output_path):
    bit_array = video_to_bit_array(video_path)
    video_size = len(bit_array)

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Не вдалося завантажити зображення")

    available_bits = img.size 
    print(f"Розмір відео у бітах: {video_size}")
    print(f"Доступно бітів у зображенні: {available_bits}")

    if video_size > available_bits:
        raise ValueError(f"Недостатньо місця у зображенні: потрібно {video_size} біт, доступно {available_bits} біт")
    
    flattened_img = img.ravel()
    for i in range(video_size):
        flattened_img[i] = (flattened_img[i] & 0xFE) | bit_array[i]

    modified_img = flattened_img.reshape(img.shape)

    cv2.imwrite(output_path, modified_img)
    print(f"Відео успішно вбудовано у зображення")
    print(f"Використано {video_size} біт із {available_bits} доступних")

def main():
    """Головна функція з покращеною діагностикою."""
    try:
        base_dir = r"/Users/mukha/Documents/Унік/3й курс/Сем 1/зпд/code/lab_12"

        image_path = filedialog.askopenfilename(
            title="Оберіть PNG-зображення",
            filetypes=[("PNG зображення", "*.png")],
            initialdir=os.path.join(base_dir, "Original Files")
        )
        if not image_path:
            raise ValueError("Зображення не обрано")

        video_path = filedialog.askopenfilename(
            title="Оберіть відеофайл",
            filetypes=[("Відео", "*.mp4 *.avi")],
            initialdir=os.path.join(base_dir, "Original Files")
        )
        if not video_path:
            raise ValueError("Відео не обрано")

        print(f"Розмір зображення: {os.path.getsize(image_path)} байт")
        print(f"Розмір відео: {os.path.getsize(video_path)} байт")

        output_filename = f"{os.path.splitext(os.path.basename(image_path))[0]}_with_{os.path.splitext(os.path.basename(video_path))[0]}"
        output_path = filedialog.asksaveasfilename(
            title="Зберегти результат",
            initialfile=output_filename,
            defaultextension=".png",
            filetypes=[("PNG зображення", "*.png")],
            initialdir=os.path.join(base_dir, "Changed files")
        )
        if not output_path:
            raise ValueError("Не обрано шлях для збереження")

        hide_video_in_image(image_path, video_path, output_path)
        print(f"Файл збережено за адресою: {output_path}")

    except Exception as e:
        print(f"Помилка: {e}")

if __name__ == "__main__":
    main()
