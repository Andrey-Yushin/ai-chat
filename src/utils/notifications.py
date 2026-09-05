
import os       # Библиотека для работы с операционной системой и переменными окружения
import smtplib  # Библиотека для работы с почтой
from email.mime.text import MIMEText
from email.header import Header
from dotenv import load_dotenv  # Библиотека для загрузки переменных окружения из .env файла
from utils.logger import AppLogger  # Импорт собственного логгера для отслеживания работы (будет рассмотрен в следующей части урока)

# Загрузка переменных окружения из .env файла при импорте модуля
load_dotenv()

class EmailNotification:
    """
    Класс для отправки уведомлений о балансе на почту.
    """

    def __init__(self):
        """
        Инициализация почтовых уведомлений.

        Raises:
            ValueError: Если email не найден в переменных окружения
        """

        # Инициализация логгера для отслеживания работы клиента
        self.logger = AppLogger()

        self.email_address = os.getenv("EMAIL_ADDRESS")  # Электронная почта отправителя
        self.email_pass = os.getenv("EMAIL_PASS")  # Пароль от почты отправителя
        self.email_recipient = os.getenv("EMAIL_RECIPIENT")  # Электронная почта получателя

        # Проверяем наличие email отправителя
        if not self.email_address:
            self.logger.error("Email address not found in .env")
            raise ValueError("Email address not found in .env")

        # Проверяем наличие пароля от почты отправителя
        if not self.email_pass:
            self.logger.error("Email password not found in .env")
            raise ValueError("Email password not found in .env")

        # Проверяем наличие email получателя
        if not self.email_recipient:
            self.logger.error("Your email address not found in .env")
            raise ValueError("Your email address not found in .env")

        self.logger.info("EmailNotification initialized successfully")

    def send_balance_notification(self, message: str,
                                  subject: str = "Остаток бюджета AITunnel"):
        """
        Отправка уведомления по почте.

        Args:
            message (str): Текст сообщения для отправки
            subject (str): Тема уведомления

        Returns:
            bool: True если отправлено, False при ошибке
        """
        try:
            # Создаём объект письма с UTF-8 кодировкой
            msg = MIMEText(message, 'plain', 'utf-8')
            msg['Subject'] = Header(subject, 'utf-8')  # Кодируем тему
            msg['From'] = self.email_address
            msg['To'] = self.email_recipient

            # Подключаемся к серверу электронной почты при отправке
            smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
            # Включение шифрования
            smtpObj.starttls()
            # Авторизация
            smtpObj.login(self.email_address, self.email_pass)

            # Отправляем
            smtpObj.send_message(msg)
            smtpObj.quit()

            self.logger.info(f"Email notification sent to {self.email_recipient}")
            return True

        except ConnectionError as e:
            self.logger.error(f"Connection error: {e}")
            return False
        except smtplib.SMTPException as e:
            self.logger.error(f"SMTP error: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
            return False
