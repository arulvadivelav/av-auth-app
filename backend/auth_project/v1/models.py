from django.db import models


# Create your models here.
class EmailVerification(models.Model):
    class Meta:
        db_table = "v1_email_verification"

    email = models.EmailField(null=False)
    otp = models.CharField(max_length=6)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
