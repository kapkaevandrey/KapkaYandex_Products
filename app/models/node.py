from sqlalchemy import Column, String, Text

from app.models import NodeBase


class Node(NodeBase):

    def __repr__(self):
        return (f'Проект - "{self.name}" осталось собрать '
                f'{self.full_amount} руб.')
