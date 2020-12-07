from django.conf import settings
from django.db import models

# from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    address = models.TextField(null=True , blank=True)
    land_line = models.CharField(max_length=11 , null=True , blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} Profile'

# def user_did_save(sender , instance , created , *args , **kwargs):
#     if created:
#         Profile.objects.get_or_create(user=instance)
#
#
# post_save.connect(user_did_save , sender=User , dispatch_uid="profile_creation")
