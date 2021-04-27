from mongoengine.document import Document
from mongoengine.fields import StringField, URLField, DateField


class Episode(Document):
    page_url = URLField(unique=True, required=True)
    date = DateField()
    title = StringField(required=True)
    description = StringField()
    mp3_url = URLField()

    def __repr__(self):
        return f"Episode ({self.date}): \n{self.title}"
