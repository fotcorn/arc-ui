#!/bin/bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py import_dataset "ARC Training" /app/datasets/ARC-AGI/data/training/
docker-compose exec web python manage.py import_dataset "ARC Evaluation" /app/datasets/ARC-AGI/data/evaluation/
docker-compose exec web python manage.py createsuperuser
