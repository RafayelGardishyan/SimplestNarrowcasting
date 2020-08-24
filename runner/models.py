import random

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.
file_types = [
    ("img", "Image"),
    ("vdo", "Video"),
    ("pge", "HTML Page")
]

screen_colors = [
    ("#14B4A0", "Praedinius Green"),
    ("#2382BE", "Praedinius Blue"),
    ('#EEEEEE', "Normal White"),
    ('#111111', "Abnoxious Black")
]


class Viewable(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title: (Will not be visible on production)")
    file_type = models.CharField(max_length=3, choices=file_types, default="img")
    file = models.FileField(upload_to="viewables")
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Screen(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name of the screen: (Will not be visible on production)")
    background_color = models.CharField(max_length=7, default="#2382BE", choices=screen_colors)
    content_border_color = models.CharField(max_length=7, default="#ffffff", choices=screen_colors)
    scroll_text = models.CharField(max_length=255, verbose_name="Scrolling text")
    time = models.IntegerField(verbose_name="Timeout (for images and HTML pages)", default=5000)
    screen_pin = models.IntegerField(default=random.randint(1000, 9999))
    current_view_id = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_view(self):
        next_view = Viewable.objects.filter(id__gt=self.current_view_id).order_by('id').first()
        if next_view == None:
            self.current_view_id = 0
            self.save()
            next_view = Viewable.objects.filter(id__gt=self.current_view_id).order_by('id').first()

        if not next_view.enabled:
            self.current_view_id = next_view.id
            self.save()
            next_view = Viewable.objects.filter(id__gt=self.current_view_id).order_by('id').first()

        self.current_view_id = next_view.id
        self.save()
        return next_view

@receiver(post_delete, sender=Viewable)
def delete_file(sender, instance, **kwargs):
    instance.file.delete(False)
