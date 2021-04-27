from mongoengine.document import Document
from mongoengine.queryset import queryset_manager
from mongoengine.fields import StringField, URLField, DateField


class Episode(Document):
    page_url = URLField(unique=True, required=True)
    date = DateField()
    title = StringField(required=True)
    description = StringField()
    mp3_url = URLField()

    def __repr__(self):
        return f"Episode ({self.date}): \n{self.title}"

    @queryset_manager
    def missing_audio(doc_cls, queryset):
        """Return all episodes that don't have an MP3 url set yet"""
        return queryset.filter(mp3_url=None)
