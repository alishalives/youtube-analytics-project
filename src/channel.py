import os
from googleapiclient.discovery import build
import json


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('API_key')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self._channel_id = channel_id
        self.__channel = Channel.youtube.channels().list(id=self._channel_id, part='snippet,statistics').execute()

        self.title = self.__channel['items'][0]['snippet']['title']
        self.description = self.__channel['items'][0]['snippet']['description']
        self.url = self.__channel['items'][0]['snippet']['thumbnails']['default']['url']
        self.followers_count = self.__channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.__channel['items'][0]['statistics']['videoCount']
        self.view_count = self.__channel['items'][0]['statistics']['viewCount']

    def print_info(self) -> str:
        """Выводит в консоль информацию о канале."""
        channel = Channel.youtube.channels().list(id=self._channel_id, part='snippet,statistics').execute()
        return json.dumps(channel, indent=2, ensure_ascii=False)

    @property
    def channel_id(self):
        """
        Метод геттер для защищенного поля channel_id
        """
        return self._channel_id

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self, filename):
        """
        Создание json-файла с атрибутами класса
        """
        data = {
            "channel_id": self._channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriber_count": self.followers_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }
        with open(filename, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

