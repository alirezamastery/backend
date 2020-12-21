from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


# @receiver(post_save , sender=User)
def user_did_create(sender , instance , created , **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


post_save.connect(user_did_create , sender=User , dispatch_uid="profile_creation")

# @receiver(post_save , sender=User)
# def user_did_save(sender , instance , **kwargs):
#     print('in user_did_save')
#     instance.profile.save()
