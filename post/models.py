from datetime import datetime

from django.db import models
from mongoengine import Document, EmbeddedDocument, fields


class EmbeddedFile(EmbeddedDocument):
    filename = fields.StringField()
    doc = fields.FileField(required=True)


class Comments(EmbeddedDocument):
    post_id = fields.StringField(required=True)
    user_id = fields.StringField(required=True)
    content = fields.StringField(required=True)
    created_at = fields.DateTimeField(default=datetime.now())
    file = fields.EmbeddedDocumentField(EmbeddedFile, blank=True)


class Post(Document):
    user_id = fields.StringField(required=True)
    title = fields.StringField(required=True, max_length=100)
    description = fields.StringField(default='')
    created_at = fields.DateTimeField(default=datetime.now())
    comments = fields.EmbeddedDocumentListField(Comments)
