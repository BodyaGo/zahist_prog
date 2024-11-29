from PIL import Image
import wave
import numpy as np
from tkinter import Tk, filedialog
import os

def audio_to_byte_array(audio_path):
    try:
        with wave.open(audio_path, "rb") as audio_file:
            frames = bytearray(audio_file.readframes(audio_file.getnframes()))
        print(f"Зчитано {len(frames)} байтів з аудіофайлу.")
        return frames
    except Exception as e:
        print(f"Помилка зчитування аудіофайлу: {e}")
        return None

def hide_audio_in_image(image_path, audio_path, output_path):
    audio_bytes = audio_to_byte_array(audio_path)
    if audio_bytes is None:
        print("Не вдалося завантажити аудіофайл.")
        return
    
    img = Image.open(image_path).convert("RGB") 
    pixels = np.array(img)

    if len(audio_bytes) * 8 > pixels.size:
        print("Недостатньо місця в зображенні для приховування аудіофайлу!")
        return

    audio_index = 0
    for i, pixel in enumerate(pixels.reshape(-1, 3)):
        if audio_index >= len(audio_bytes):
            break
        for color in range(3):
            if audio_index >= len(audio_bytes):
                break
            bit = (audio_bytes[audio_index] >> (7 - (audio_index % 8))) & 0x01
            pixel[color] = (pixel[color] & 0xFE) | bit
            audio_index += 1

    stego_image = Image.fromarray(pixels)
    try:
        stego_image.save(output_path, compress_level=0)
        print(f"Аудіофайл успішно закодовано у зображенні: {output_path}")
    except Exception as e:
        print(f"Помилка збереження зображення: {e}")

def main():
    Tk().withdraw()

    base_dir = r"/Users/mukha/Documents/Унік/3й курс/Сем 1/зпд/code/lab_12"

    image_path = filedialog.askopenfilename(
        initialdir=os.path.join(base_dir, "Original Files"),
        title="Оберіть зображення для кодування",
        filetypes=[("Зображення PNG", "*.png")]
    )
    if not image_path:
        print("Зображення не вибрано!")
        return

    audio_path = filedialog.askopenfilename(
        initialdir=os.path.join(base_dir, "Original Files"),
        title="Оберіть аудіофайл (wav)",
        filetypes=[("WAV файли", "*.wav")]
    )
    if not audio_path:
        print("Аудіофайл не вибрано!")
        return

    audio_name = os.path.splitext(os.path.basename(audio_path))[0]
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    suggested_filename = f"{image_name}_with_{audio_name}.png"

    output_path = filedialog.asksaveasfilename(
        initialdir=os.path.join(base_dir, "Changed files"),
        title="Оберіть місце для збереження файлу",
        initialfile=suggested_filename,
        defaultextension=".png",
        filetypes=[("PNG файли", "*.png")]
    )

    if not output_path:
        print("Місце для збереження не вибрано!")
        return
    
    hide_audio_in_image(image_path, audio_path, output_path)
    print(f"Файл збережено за адресою: {output_path}")

if __name__ == "__main__":
    main()
