from django.db.models.signals import post_save
from django.dispatch import receiver
from repository.models_list.models import Hospital


@receiver(post_save, sender=Hospital)
def create_hospital(sender, instance=None, created=False, **kwargs):
    if created:
        hos_name = instance.hos_name
        instance.hos_name = hos_name + "test signals"
        instance.save()