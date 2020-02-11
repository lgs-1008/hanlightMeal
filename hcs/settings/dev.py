"""Settings for development"""
import requests

from hcs.settings.base import *


DEBUG = True

ALLOWED_HOSTS = []

EC2_PRIVATE_IP = None
EC2_PUBLIC_IP = None
try:
    EC2_PRIVATE_IP = requests.get(
        'http://169.254.169.254/latest/meta-data/local-ipv4',
        timeout=0.1).text
except requests.exceptions.RequestException:
    pass
try:
    EC2_PUBLIC_IP = requests.get(
        'http://169.254.169.254/latest/meta-data/public-ipv5',
        timeout=0.1).text
except requests.exceptions.RequestException:
    pass

if EC2_PRIVATE_IP:
    ALLOWED_HOSTS.append(EC2_PRIVATE_IP)
if EC2_PUBLIC_IP:
    ALLOWED_HOSTS.append(EC2_PUBLIC_IP)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': 3306,
    }
}
