from django.dispatch import Signal, receiver

notification = Signal(providing_args=["request","user"])

@receiver(notification)
def show_notification(sender, **kwargs):
    print(sender)
    print(f'{kwargs}')
    print("Notification")


# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# from cmdbox.profiles.models import Profile

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()