import random

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible

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
    ('#111111', "Abnoxious Black"),
    ('#d12f24', "Kinda Red"),
    ('#ffd752', "Warning Yellow"),
    ('#902bd9', "Maybe Purple"),
    ('#f24ea8', "Absolute Pink")
]

@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)

path_and_rename = PathAndRename("viewables")


class Screen(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name of the screen: (Will not be visible on production)")
    background_color = models.CharField(max_length=7, default="#2382BE", choices=screen_colors)
    content_border_color = models.CharField(max_length=7, default="#ffffff", choices=screen_colors)
    scroll_text = models.CharField(max_length=255, verbose_name="Scrolling text")
    time = models.IntegerField(verbose_name="Timeout (for images and HTML pages)", default=5000)
    screen_pin = models.IntegerField(default=random.randint(1000, 9999))
    current_view_id = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Scherm'
        verbose_name_plural = "Schermen"

    def __str__(self):
        return self.name

    def check_view(self, view):
        if view == None:
            self.current_view_id = 0
            return False

        if not view.enabled:
            self.current_view_id = view.id
            return False

        if not self in view.screens.all():
            self.current_view_id = view.id
            return False

        return True

    def get_view(self):
        next_view = Viewable.objects.filter(id__gt=self.current_view_id).order_by('id').first()
        good = False
        while not good:
            good = self.check_view(next_view)
            if not good:
                self.save()
                next_view = Viewable.objects.filter(id__gt=self.current_view_id).order_by('id').first()


        self.current_view_id = next_view.id
        self.save()
        return next_view


class Viewable(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title: (Will not be visible on production)")
    file_type = models.CharField(max_length=3, choices=file_types, default="img")
    file = models.FileField(upload_to=path_and_rename)
    screens = models.ManyToManyField(Screen, blank=True, null=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'dia'
        verbose_name_plural = "dia's"


    def __str__(self):
        return self.title


class Automation(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title: (Short description)")
    datetime = models.DateTimeField(auto_now=False, verbose_name="Execute on:")
    to_enable = models.ManyToManyField(Viewable, blank=True, null=True, verbose_name="Slides to enable:", related_name='to_enable')
    to_disable = models.ManyToManyField(Viewable, blank=True, null=True, verbose_name="Slides to disable:", related_name='to_disable')

    class Meta:
        verbose_name = 'automatisering'
        verbose_name_plural = "automatiseringen"

    def __str__(self):
        return "{} => {}".format(self.title, self.datetime)

    def execute(self, datetime):
        print("executing")
        print("s: {} => o: {}".format(self.datetime, datetime))
        if datetime.date() != self.datetime.date():
            return False

        if (datetime.time().hour < self.datetime.time().hour) or (datetime.time().minute < self.datetime.time().minute):
            return False

        for e in self.to_enable.all():
            e.enabled = True
            e.save()

        for d in self.to_disable.all():
            d.enabled = False
            d.save()


@receiver(post_delete, sender=Viewable)
def delete_file(sender, instance, **kwargs):
    instance.file.delete(False)
