import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from moviepy import VideoFileClip


def compress_video(input_path, target_width=1280, target_bitrate="500k"):
    """
    Сжимает видео: изменяет разрешение и bitrate (совместимо с MoviePy v2.0+)
    :param input_path: путь к исходному видео
    :param target_width: желаемая ширина (высота рассчитается пропорционально)
    :param target_bitrate: bitrate для сжатия (например, "500k" = 500 Kbps)
    :return: путь к сжатому файлу
    """
    print(f"Загружаем видео: {input_path}")
    clip = VideoFileClip(input_path)

    # Вычисляем новую высоту пропорционально
    aspect_ratio = clip.h / clip.w
    target_height = int(target_width * aspect_ratio)

    # Масштабируем видео (новый способ в v2.0)
    resized_clip = clip.resized(width=target_width)

    output_path = os.path.splitext(input_path)[0] + "_compressed.mp4"

    print(f"Сжимаем видео... Новое разрешение: {target_width}x{target_height}, bitrate: {target_bitrate}")

    # Запись с указанием параметров кодирования
    resized_clip.write_videofile(
        output_path,
        codec='libx264',
        audio_codec='aac',
        bitrate=target_bitrate,
        preset='medium',
        ffmpeg_params=['-crf', '23']  # CRF 18-28: чем меньше — тем лучше качество
    )

    # Освобождаем ресурсы
    clip.close()
    resized_clip.close()

    original_size = os.path.getsize(input_path) / (1024*1024)  # MB
    compressed_size = os.path.getsize(output_path) / (1024*1024)  # MB
    reduction = ((original_size - compressed_size) / original_size) * 100

    print(f"\n✅ Готово!")
    print(f"Исходный размер: {original_size:.2f} MB")
    print(f"Сжатый размер: {compressed_size:.2f} MB")
    print(f"Сокращение: {reduction:.1f}%")

    return output_path


def main():
    # Скрываем главное окно Tkinter
    Tk().withdraw()

    # Открываем диалог выбора файла
    print("Выберите видеофайл для сжатия...")
    video_path = askopenfilename(
        title="Выберите видео",
        filetypes=[
            ("Видео файлы", "*.mp4 *.mov *.avi *.mkv *.wmv"),
            ("MP4", "*.mp4"),
            ("MOV", "*.mov"),
            ("AVI", "*.avi"),
            ("MKV", "*.mkv"),
            ("WMV", "*.wmv"),
            ("Все файлы", "*.*")
        ]
    )

    if not video_path:
        print("Файл не выбран. Программа завершена.")
        return

    # Проверка расширения
    valid_exts = ('.mp4', '.mov', '.avi', '.mkv', '.wmv')
    if not video_path.lower().endswith(valid_exts):
        print(f"Неподдерживаемый формат: {video_path}. Поддерживаются: {valid_exts}")
        return

    # Сжимаем
    compress_video(video_path)


if __name__ == "__main__":
    main()