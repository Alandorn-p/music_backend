from django.db import models
import uuid


class Song(models.Model):
    video_id = models.CharField(unique=True, max_length=255)
    title = models.CharField(max_length=255, default="")
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contents = models.BinaryField()
    duration = models.IntegerField()

    def __str__(self) -> str:
        if len(self.title) > 20:
            return self.title[:20]+'...'
        return self.title
