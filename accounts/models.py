from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class VulnTrackAccounts(AbstractUser):
    class Roles(models.TextChoices):
        RESEARCHER = "researcher","RESEARCHER",
        MODERATOR = "moderator","MODERATOR",
        ADMIN = "admin","ADMIN",
    role = models.CharField(max_length=20,
                            choices=Roles,
                            default=Roles.RESEARCHER)




