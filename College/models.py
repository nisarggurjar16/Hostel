from django.db import models

class ContactForm(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    subject = models.CharField(max_length=128, null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name + ' <> ' + self.subject



