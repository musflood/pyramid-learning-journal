from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Unicode,
)

from .meta import Base
from datetime import datetime
from markdown import markdown


class Entry(Base):
    """Create a table for journal entries."""

    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    body = Column(Unicode)
    creation_date = Column(DateTime)

    def __init__(self, creation_date=None, *args, **kwargs):
        """Initialize a new journal entry with current date."""
        super(Entry, self).__init__(*args, **kwargs)
        self.creation_date = creation_date
        if not creation_date:
            self.creation_date = datetime.now()

    def to_dict(self):
        """Take all model attributes and render them as a dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'creation_date': self.creation_date.strftime('%A, %B %d, %Y, %I:%M %p')
        }

    def to_html_dict(self):
        """Take all model attributes and render them as a dict with html."""
        attr = self.to_dict()
        attr['body'] = markdown(attr['body'])
        return attr
