import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageFilter, ImageEnhance
import threading

def process_image(image_path, output_folder, filters):
    try:
        img = Image.open(image_path)
        
        if "sharpness" in filters:
            img = ImageEnhance.Sharpness(img).enhance(7.0)
        if "sepia" in filters:
            img = img.convert('L').filter(ImageFilter.CONTOUR)
        if "resize" in filters:
            img = img.resize((100, 100))
        
        # Сохраняем обработанное изображение в выходную папку
        img.save(os.path.join(output_folder, 'processed_' + os.path.basename(image_path)))
    except Exception as e:
        print(f"Ошибка обработки {image_path}: {str(e)}")

def process_images_in_thread(input_folder, output_folder, filters):
    image_paths = [os.path.join(input_folder, filename) for filename in os.listdir(input_folder)]

    # Создаем выходную папку, если её нет
    os.makedirs(output_folder, exist_ok=True)

    for path in image_paths:
        # Запускаем обработку изображения в отдельном потоке
        threading.Thread(target=process_image, args=(path, output_folder, filters)).start()

def browse_input_folder():
    input_folder = filedialog.askdirectory()
    input_folder_var.set(input_folder)

def browse_output_folder():
    output_folder = filedialog.askdirectory()
    output_folder_var.set(output_folder)

def start_processing():
    input_folder = input_folder_var.get()
    output_folder = output_folder_var.get()
    
    # Получаем выбранные фильтры
    selected_filters = []
    if sharpness_var.get():
        selected_filters.append("sharpness")
    if sepia_var.get():
        selected_filters.append("sepia")
    if resize_var.get():
        selected_filters.append("resize")
    
    process_images_in_thread(input_folder, output_folder, selected_filters)

if __name__ == "__main__":
    # Создаем главное окно
    root = tk.Tk()
    root.title("Обработка изображений")

    # Переменные для хранения путей к входной и выходной папкам
    input_folder_var = tk.StringVar()
    output_folder_var = tk.StringVar()

    # Выбор входной папки
    input_folder_label = tk.Label(root, text="Выберите входную папку:")
    input_folder_label.pack()
    input_folder_entry = tk.Entry(root, textvariable=input_folder_var, width=40)
    input_folder_entry.pack()
    input_folder_button = tk.Button(root, text="Обзор", command=browse_input_folder)
    input_folder_button.pack()

    # Выбор выходной папки
    output_folder_label = tk.Label(root, text="Выберите выходную папку:")
    output_folder_label.pack()
    output_folder_entry = tk.Entry(root, textvariable=output_folder_var, width=40)
    output_folder_entry.pack()
    output_folder_button = tk.Button(root, text="Обзор", command=browse_output_folder)
    output_folder_button.pack()

    # Флажки для выбора фильтров
    sharpness_var = tk.BooleanVar()
    sharpness_checkbox = tk.Checkbutton(root, text="Увеличение резкости", variable=sharpness_var)
    sharpness_checkbox.pack()
    
    sepia_var = tk.BooleanVar()
    sepia_checkbox = tk.Checkbutton(root, text="Сепия", variable=sepia_var)
    sepia_checkbox.pack()
    
    resize_var = tk.BooleanVar()
    resize_checkbox = tk.Checkbutton(root, text="Уменьшение размера", variable=resize_var)
    resize_checkbox.pack()

    # Кнопка для обработки изображений
    process_button = tk.Button(root, text="Обработать изображия", command=start_processing)
    process_button.pack()

    root.mainloop()
