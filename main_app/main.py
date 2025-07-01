import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
from PIL import Image, ImageFilter
import os


def send_email_with_image():
    # Конфигурация
    sender_email = "ваша_почта@gmail.com"
    app_password = "16-значный пароль приложения"  # ← Вставьте сюда пароль приложения!
    recipient_email = "ваша_почта@gmail.com"
    image_path = "processed.jpg"

    # Проверка файла
    if not os.path.exists(image_path):
        print(f"❌ Файл {image_path} не найден!")
        return

    # Создаем письмо
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = Header("Обработанное изображение", 'utf-8')

    # Текст письма
    msg.attach(MIMEText("Ваше изображение готово!", 'plain', 'utf-8'))

    # Вложение изображения
    with open(image_path, 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-Disposition', 'attachment',
                       filename=Header("result.jpg", 'utf-8').encode())
        msg.attach(img)

    # Отправка
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        print("Письмо успешно отправлено!")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    send_email_with_image()