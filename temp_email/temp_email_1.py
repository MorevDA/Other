import requests
from dataclasses import dataclass
from typing import Dict, List


class FakeEmail:
    base_url = "https://api.mailslurp.com"
    session = requests.session()

    def __init__(self, apy_key, address=None):
        self.headers = {'x-api-key': apy_key, 'content-type': 'application/json'}
        self.address = address or self.create_email()
        self.inbox_id = self.address.split('@')[0]

    def create_email(self) -> str:
        response = self.session.post(f'{self.base_url}/inboxes', headers=self.headers)
        response.raise_for_status()
        return response.json().get('emailAddress')

    def delete_inbox(self) -> int:
        response = self.session.delete(f'{self.base_url}/inboxes/{self.inbox_id}', headers=self.headers)
        response.raise_for_status()
        return response.status_code

    def get_all_emails(self) -> List["'FakeEmail.MessageInfo'"]:
        response = self.session.get(f'{self.base_url}/emails', headers=self.headers)
        response.raise_for_status()
        return [FakeEmail.MessageInfo.from_dict(self, msg) for msg in response.json()['content']]

    def get_email_by_id(self, email_id: str) -> 'FakeEmail.MessageInfo':
        response = self.session.get(f'{self.base_url}/emails/{email_id}', headers=self.headers)
        return FakeEmail.MessageInfo.from_dict(self, response.json())

    def get_links_in_email(self, email_id: str) -> list[str] | str:
        response = self.session.get(f'{self.base_url}/emails/{email_id}/links', headers=self.headers)
        try:
            return response.json()['links']
        except KeyError:
            return ("Email content is not HTML. Please use the method 'get_url_for_browser' to view content in your "
                    "browser.")

    def get_url_for_browser(self, email_id: str) -> str:
        response = self.session.get(f'{self.base_url}/emails/{email_id}/urls', headers=self.headers)
        return response.json()['plainHtmlBodyUrl']

    def get_email_text(self, email_id: str):
        response = self.session.get(f'{self.base_url}/emails/{email_id}/textLines', headers=self.headers)
        return ",".join(response.json()['lines'])

    def download_attachment(self, email_id, attachment_id: str,
                            path: str = None, file_name: str = None) -> bytes:
        response = self.session.get(f'{self.base_url}/emails/{email_id}/attachments/{attachment_id}',
                                    headers=self.headers)
        if path and file_name:
            self.write_file(f"{path + file_name}", response.content)
        elif file_name:
            self.write_file(file_name, response.content)
        else:
            default_file_name = self.get_attachment_metadata(email_id, attachment_id).name
            self.write_file(default_file_name, response.content)

    def get_attachment_metadata(self, email_id: str, attachment_id: str):
        response = self.session.get(f'{self.base_url}/emails/{email_id}/attachments/{attachment_id}/metadata',
                                    headers=self.headers)
        return FakeEmail.Content.from_dict(response.json())

    @staticmethod
    def write_file(file: str, content: bytes):
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
    class Content:
        name: str
        content_type: str

        @classmethod
        def from_dict(cls, content_info: dict):
            return cls(
                name=content_info['name'],
                content_type=content_info['contentType'])
