from PIL import Image
import numpy as np
import wave
from tkinter import Tk, filedialog
import os

def image_to_bit_array(image_path):
    try:
        img = Image.open(image_path).convert("1")  # Чорно-біле зображення (1 біт на піксель)
        bit_array = np.array(img).flatten()
        print(f"Бітовий масив зображення завантажено успішно: {len(bit_array)} біт")
        return bit_array
    except Exception as e:
        print(f"Помилка завантаження зображення: {e}")
        return None

def hide_data_in_audio(audio_path, image_path, output_path):
    bit_array = image_to_bit_array(image_path)
    if bit_array is None:
        return
    try:
        with wave.open(audio_path, "rb") as audio_file:
            params = audio_file.getparams()
            frames = bytearray(audio_file.readframes(audio_file.getnframes()))

        if len(bit_array) > len(frames):
            print("Недостатньо місця в аудіофайлі для приховування зображення!")
            return
        
        for i, bit in enumerate(bit_array):
            frames[i] = (frames[i] & 0xFE) | bit 

        with wave.open(output_path, "wb") as steg_audio:
            steg_audio.setparams(params)
            steg_audio.writeframes(frames)

        print(f"Зображення успішно приховано у файлі {output_path}")

    except Exception as e:
        print(f"Помилка обробки аудіофайлу: {e}")

def main():
    Tk().withdraw()

    base_dir = r"/Users/mukha/Documents/Унік/3й курс/Сем 1/зпд/code/lab_12"
    try:
        audio_path = filedialog.askopenfilename(
            initialdir=os.path.join(base_dir, "Original Files"),
            title="Оберіть аудіофайл (wav)",
            filetypes=[("WAV файли", "*.wav")]
        )
        if not audio_path:
            raise ValueError("Аудіофайл не вибрано")

        image_path = filedialog.askopenfilename(
            initialdir=os.path.join(base_dir, "Original Files"),
            title="Оберіть зображення для приховування",
            filetypes=[("Зображення PNG", "*.png")]
        )
        if not image_path:
            raise ValueError("Зображення не вибрано")

        print(f"Розмір аудіофайлу: {os.path.getsize(audio_path)} байт")
        print(f"Розмір зображення: {os.path.getsize(image_path)} байт")

        output_filename = f"{os.path.splitext(os.path.basename(image_path))[0]}_in_{os.path.splitext(os.path.basename(audio_path))[0]}.wav"
        output_path = filedialog.asksaveasfilename(
            initialdir=os.path.join(base_dir, "Changed files"),
            title="Оберіть місце для збереження файлу",
            initialfile=output_filename,
            defaultextension=".wav",
            filetypes=[("WAV файли", "*.wav")]
        )
        if not output_path:
            raise ValueError("Не обрано шлях для збереження")

        hide_data_in_audio(audio_path, image_path, output_path)

    except Exception as e:
        print(f"Помилка: {e}")

if __name__ == "__main__":
    main()
