#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import configparser


def main():
    """Run administrative tasks."""
    config = configparser.ConfigParser()
    config.read('test_from_stori_card/settings.ini')
    debug = config.getboolean('settings', 'DEBUG')
    config_local = config.get('settings', 'config_local_server')
    config_production = config.get('settings', 'config_production_server')
    django_settings_module = config_local if debug else config_production
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', django_settings_module)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
