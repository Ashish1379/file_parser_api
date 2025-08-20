from django.db import models
import uuid
# Create your models here.
class Files(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=108)
    file = models.FileField(upload_to="files/")
    status = models.CharField(
        max_length=20,
        choices=[("uploading", "Uploading"),
                 ("processing", "Processing"),
                 ("ready", "Ready"),
                 ("failed", "Failed")],
        default="uploading"
    )
    progress = models.IntegerField(default=0)
    parsed_content = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename