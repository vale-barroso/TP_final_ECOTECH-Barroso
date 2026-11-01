"""Levanta un servidor local para ver el panel en el navegador.

Uso:  python ver_panel.py
Luego abrir:  http://127.0.0.1:8000/
"""
import sys

import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.urls import path

settings.configure(
    DEBUG=True,
    SECRET_KEY="clave-solo-para-demo",
    ALLOWED_HOSTS=["*"],
    ROOT_URLCONF=__name__,
    INSTALLED_APPS=["sustentabilidad"],
    TEMPLATES=[{
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    }],
)
django.setup()

from sustentabilidad.views import vista_panel_sustentabilidad

urlpatterns = [path("", vista_panel_sustentabilidad)]

if __name__ == "__main__":
    execute_from_command_line([sys.argv[0], "runserver", "--noreload"])