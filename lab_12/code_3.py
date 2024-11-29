import cv2
import numpy as np
from tkinter import Tk, filedialog
import os

def image_to_bit_array(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Не вдалося завантажити зображення.")
    _, binary_img = cv2.threshold(img, 127, 1, cv2.THRESH_BINARY)
    bit_array = binary_img.flatten()
    return bit_array

def hide_image_in_video(video_path, image_path, output_path):
    try:
        bit_array = image_to_bit_array(image_path)
    except Exception as e:
        print(f"Помилка: {e}")
        return

    bit_index = 0 

    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print("Не вдалося відкрити відеофайл.")
        return

    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    if len(bit_array) > frame_width * frame_height * total_frames:
        print("Недостатньо місця у відео для приховування зображення!")
        video.release()
        return

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    frame_count = 0
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % 50 == 0:
            print(f"Опрацьовано кадрів: {frame_count}/{total_frames}")

        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                if bit_index < len(bit_array):
                    frame[i, j, 0] = (frame[i, j, 0] & 0xFE) | bit_array[bit_index]
                    bit_index += 1
                else:
                    break
            if bit_index >= len(bit_array):
                break

        out.write(frame)

    video.release()
    out.release()
    print(f"Зображення успішно приховано у відеофайлі: {output_path}")

def main():
    Tk().withdraw() 

    base_dir = r"/Users/mukha/Documents/Унік/3й курс/Сем 1/зпд/code/lab_12"

    video_path = filedialog.askopenfilename(
        initialdir=os.path.join(base_dir, "Original Files"),
        title="Оберіть відеофайл",
        filetypes=[("Відеофайли", "*.mp4 *.avi")]
    )
    if not video_path:
        print("Відеофайл не вибрано!")
        return

    image_path = filedialog.askopenfilename(
        initialdir=os.path.join(base_dir, "Original Files"),
        title="Оберіть зображення для приховування",
        filetypes=[("Зображення PNG", "*.png")]
    )
    if not image_path:
        print("Зображення не вибрано!")
        return

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    suggested_filename = f"{video_name}_with_{image_name}.avi"

    output_path = filedialog.asksaveasfilename(
        initialdir=os.path.join(base_dir, "Changed files"),
        title="Оберіть місце для збереження файлу",
        initialfile=suggested_filename,
        defaultextension=".avi",
        filetypes=[("Відеофайли AVI", "*.avi")]
    )
    if not output_path:
        print("Місце для збереження не вибрано!")
        return

    hide_image_in_video(video_path, image_path, output_path)
    print(f"Файл збережено за адресою: {output_path}")

if __name__ == "__main__":
    main()
