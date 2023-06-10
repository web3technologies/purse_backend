from django.db import models



class PlaidApiError(models.Model):

    error_type = models.CharField(max_length=255)
    error_code = models.CharField(max_length=255, null=True)
    documentation_link = models.CharField(max_length=255, null=True)
    is_login_required = models.BooleanField(default=False)
    

    def __str__(self) -> str:
        return f"{self.error_type} -- {self.error_code if self.error_code else ''}"

