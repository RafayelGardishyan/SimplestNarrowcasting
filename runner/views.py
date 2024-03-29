import json
import requests

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core import serializers

from runner.models import Screen, Automation


def screen(request, screen_id):
    try:
        screen = Screen.objects.get(pk=screen_id)
    except Screen.DoesNotExist:
        return redirect('/')

    context = {
        "screen": screen
    }
    return render(request, "screen.html", context)


def internal_metadata(request, screen_pin):
    return HttpResponse(serializers.serialize("json", [Screen.objects.get(screen_pin=screen_pin)]), content_type="text/plain")


def get_weather():
    response = requests.get("http://api.weatherapi.com/v1/current.json?key=d4e994c56a6a45aba08105348200910&q=53.220638,6.571441")
    response = response.json()

    temp = int(response["current"]["temp_c"])
    icon = response["current"]["condition"]["icon"][2:]

    return {"temp": temp, "icon": icon}


def get_next_image(request, screen_id):
    try:
        screen = Screen.objects.get(pk=screen_id)
    except Screen.DoesNotExist:
        return redirect('/')



    response = requests.get("http://worldtimeapi.org/api/timezone/Europe/Amsterdam")
    response = response.json()

    from datetime import datetime

    a = datetime.strptime(response["datetime"][:-6], "%Y-%m-%dT%H:%M:%S.%f")

    for atmn in Automation.objects.all():
        atmn.execute(a)

    time = (str(a.hour) if len(str(a.hour)) == 2 else "0" + str(a.hour)) + ":" + (str(a.minute) if len(str(a.minute)) == 2 else "0" + str(a.minute))

    view = screen.get_view()
    return HttpResponse(json.dumps(
        {
            "type": view.file_type,
            "url": view.file.url,
            "sctext": screen.scroll_text,
            "time": time,
            "weather": get_weather(),
            "screen": json.loads(serializers.serialize("json", [screen]))
        }), content_type='text/plain')


def index(request):
    if request.method == "POST":
        pin = int(request.POST["pin"])
        try:
            screen = Screen.objects.get(screen_pin=pin)
        except Screen.DoesNotExist:
            return redirect('/')

        return redirect('/view/screen/{}'.format(screen.pk))

    return render(request, "index.html", {})