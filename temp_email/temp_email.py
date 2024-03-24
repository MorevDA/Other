import requests
import re
from dataclasses import dataclass
from typing import Dict, List, Optional

__all__ = (
    'FakeEmail',
)


class FakeEmail:
    """ Класс для взаимодействия с API mailslurp.com"""

    base_url = "https://api.mailslurp.com"
    """Базовый адрес для взаимодействия с API"""

    def __init__(self, apy_key, address=None):
        """Создание нового случайного адреса электронной почты.
           :param apy_key: Ключ полученный при регистрации на сервисе mailslurp.com
           :param address: Опциональный параметр, указывается при наличии созданного ранее почтового адреса.
        """

        self.session = requests.session()
        self.headers = {'x-api-key': apy_key}
        self.address = address or self.create_email()
        self.inbox_id = self.address.split('@')[0]

    def create_email(self) -> str:
        """Функция для создания нового почтового ящика"""
        response = self.session.post(f'{self.base_url}/inboxes', headers=self.headers)
        response.raise_for_status()
        return response.json().get('emailAddress')

    def delete_inbox(self) -> int:
        """Функция для удаления почтового ящика"""
        response = self.session.delete(f'{self.base_url}/inboxes/{self.inbox_id}', headers=self.headers)
        response.raise_for_status()
        return response.status_code

    def get_all_emails(self) -> List["'FakeEmail.MessageInfo'"]:
        """Функция для получения списка всех ранее созданных пользователем почтовых ящиков"""
        response = self.session.get(f'{self.base_url}/emails', headers=self.headers)
        response.raise_for_status()
        return [FakeEmail.MessageInfo.from_dict(self, msg) for msg in response.json()['content']]

    def get_email_by_id(self, email_id: str) -> 'FakeEmail.MessageInfo':
        """Функция для получения информации об электронном письме по его id"""
        response = self.session.get(f'{self.base_url}/emails/{email_id}', headers=self.headers)
        return FakeEmail.MessageInfo.from_dict(self, response.json())

    def get_links_in_email(self, email_id: str) -> list[str]:
        """Функция для получения всех ссылок содержащихся в тексте электронного письма по его id"""
        response = self.session.get(f'{self.base_url}/emails/{email_id}/links', headers=self.headers)
        try:
            return response.json()['links']
        except KeyError:
            text = self.get_email_text(email_id)
            return self.get_link_in_text(text)

    def get_url_for_browser(self, email_id: str) -> str:
        """Функция для получения ссылки для просмотра электронного письма в браузере по его id"""
        response = self.session.get(f'{self.base_url}/emails/{email_id}/urls', headers=self.headers)
        return response.json()['plainHtmlBodyUrl']

    def get_email_text(self, email_id: str):
        """Функция для получения текста электронного письма по его id"""
        response = self.session.get(f'{self.base_url}/emails/{email_id}/textLines', headers=self.headers)
        return ",".join(response.json()['lines'])

    def download_attachment(self, email_id, attachment_id: str,
                            path: str = None, file_name: str = None) -> None:
        """Функция для сохранения приложения к электронному письму по id приложения"""
        response = self.session.get(f'{self.base_url}/emails/{email_id}/attachments/{attachment_id}',
                                    headers=self.headers)
        if path and file_name:
            self.write_file(f"{path}/{file_name}", response.content)
        elif file_name:
            self.write_file(file_name, response.content)
        elif path:
            default_file_name = self.get_attachment_metadata(email_id, attachment_id).name
            self.write_file(f'{path}/{default_file_name}', response.content)
        else:
            default_file_name = self.get_attachment_metadata(email_id, attachment_id).name
            self.write_file(default_file_name, response.content)

    def download_all_attachments_in_email(self, email_id, path=None):
        """Функция для сохранения всех приложений к электронному письму по его id"""
        for attachment_id in self.get_email_by_id(email_id).attachment_id:
            self.download_attachment(email_id, attachment_id, path)

    def get_attachment_metadata(self, email_id: str, attachment_id: str) -> 'FakeEmail.Attachment':
        """Функция для получения информации к электронному письму по его id"""
        response = self.session.get(f'{self.base_url}/emails/{email_id}/attachments/{attachment_id}/metadata',
                                    headers=self.headers)
        return FakeEmail.Attachment.from_dict(response.json())

    def wait_for_email(self, timeout: Optional[int] = 60) -> 'FakeEmail.MessageInfo':
        """Метод ожидания поступления новых писем в почтовый ящик"""
        wait_time = timeout * 1000
        response_body = {'inboxId': self.inbox_id, 'timeout': wait_time, 'unreadOnly': True}
        response = self.session.get(f'{self.base_url}/waitForLatestEmail',
                                    headers=self.headers, params=response_body)
        if response:
            return FakeEmail.MessageInfo.from_dict(self, response.json())
        else:
            raise TimeoutError('Timed out waiting for message')

    @staticmethod
    def get_link_in_text(text: str) -> list:
        """Функция для получения списка ссылок содержащегося в тексте"""
        link = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        return link

    @staticmethod
    def write_file(file: str, content: bytes):
        """Функция для сохранения файла"""
        with open(file, "wb") as f:
            f.write(content)

    def __str__(self) -> str:
        return self.address

    @dataclass
    class MessageInfo:
        """Information about a message in the inbox"""
        id: int
        sender: str
        subject: str
        date_str: str
        attachment_id: str
        _mail_instance: 'FakeEmail'

        @classmethod
        def from_dict(cls, mail_instance: 'FakeEmail', msg: Dict[str, any]):
            return cls(
                _mail_instance=mail_instance,
                id=msg['id'],
                sender=msg['from'],
                subject=msg['subject'],
                date_str=msg['createdAt'],
                attachment_id=msg['attachments'] if len(msg.get('attachments')) > 0 else None)

    @dataclass
    class Message:
        pass

    @dataclass
    class Attachment:
        name: str
        content_type: str

        @classmethod
        def from_dict(cls, content_info: dict):
            return cls(
                name=content_info['name'],
                content_type=content_info['contentType'])
