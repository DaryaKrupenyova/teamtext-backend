from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Collaborators(models.Model):
    user = models.ForeignKey(to=User, related_name="collaborators",
                             on_delete=models.CASCADE, null=False, blank=False)
    document = models.ForeignKey(to="Document", related_name="collaborators",
                                 on_delete=models.CASCADE, null=False, blank=False)
    role = models.CharField(default="editor", max_length=45, null=False, blank=False)

    class Meta:
        db_table = "collaborators"
        verbose_name = "collaborators"
        verbose_name_plural = "collaborators"

    def __str__(self):
        return f"{self.user} works on {self.document}"


class Document(models.Model):
    title = models.CharField(default="DOCUMENT_TITLE", max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    sharing_token = models.TextField(null=True, blank=True)
    users = models.ManyToManyField(to=User, through="Collaborators", related_name="documents")

    class Meta:
        db_table = "document"
        verbose_name = "document"
        verbose_name_plural = "documents"

    def __str__(self):
        return f"Document {self.title}"
