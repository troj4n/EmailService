from django.db import models

# Create your models here.
class emailModel(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    cc = models.EmailField()
    bcc = models.EmailField()
    message = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
