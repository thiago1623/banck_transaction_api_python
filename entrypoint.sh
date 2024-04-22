#!/bin/sh

cp settings.ini test_from_stori_card/test_from_stori_card/
pip install -qr /app/test_from_stori_card/requirements.txt --exists-action w

# run Django server
cd test_from_stori_card/
python manage.py runserver 0.0.0.0:8000
