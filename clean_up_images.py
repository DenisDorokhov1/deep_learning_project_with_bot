import os
from PIL import Image

IMAGES_DIR = "images"

removed = 0
checked = 0

for filename in os.listdir(IMAGES_DIR):
    path = os.path.join(IMAGES_DIR, filename)

    if not os.path.isfile(path):
        continue

    checked += 1

    try:
        with Image.open(path) as img:
            img.verify()  # проверяет целостность файла
    except Exception as e:
        print(f"❌ Удаляю битый файл: {filename} ({e})")
        os.remove(path)
        removed += 1

print("\nГотово.")
print(f"Проверено файлов: {checked}")
print(f"Удалено битых: {removed}")
