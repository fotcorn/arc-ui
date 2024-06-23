import os
import json
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from app.models import Dataset, Task


class Command(BaseCommand):
    help = "Import a dataset into the database"

    def add_arguments(self, parser):
        parser.add_argument("dataset_name", type=str, help="Name of the dataset")
        parser.add_argument(
            "dataset_path", type=str, help="Path to the dataset directory"
        )

    def handle(self, *args, **options):
        dataset_name = options["dataset_name"]
        dataset_path = options["dataset_path"]

        if not os.path.isdir(dataset_path):
            raise CommandError(f"The path '{dataset_path}' is not a valid directory.")

        json_files = [f for f in os.listdir(dataset_path) if f.endswith(".json")]
        if not json_files:
            raise CommandError(f"No JSON files found in '{dataset_path}'.")

        existing_dataset = Dataset.objects.filter(name=dataset_name).first()
        if existing_dataset:
            choice = input(
                "Dataset already exists. Choose an option:\n"
                "a) Cancel\n"
                "b) Delete and recreate dataset\n"
                "c) Add non-existing tasks to dataset\n"
                "Enter your choice (a/b/c): "
            ).lower()

            if choice == "a":
                self.stdout.write(self.style.WARNING("Operation cancelled."))
                return
            elif choice == "b":
                existing_dataset.delete()
                dataset = Dataset.objects.create(name=dataset_name)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Deleted existing dataset and created new one: {dataset_name}"
                    )
                )
            elif choice == "c":
                dataset = existing_dataset
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Adding non-existing tasks to dataset: {dataset_name}"
                    )
                )
            else:
                raise CommandError("Invalid choice. Operation cancelled.")
        else:
            dataset = Dataset.objects.create(name=dataset_name)
            self.stdout.write(
                self.style.SUCCESS(f"Created new dataset: {dataset_name}")
            )

        tasks_created = 0
        tasks_skipped = 0

        with transaction.atomic():
            for json_file in json_files:
                task_name = os.path.splitext(json_file)[0]
                file_path = os.path.join(dataset_path, json_file)

                if Task.objects.filter(name=task_name, dataset=dataset).exists():
                    tasks_skipped += 1
                    continue

                with open(file_path, "r") as f:
                    data = json.load(f)

                Task.objects.create(
                    name=task_name,
                    dataset=dataset,
                    train=data.get("train", []),
                    test=data.get("test", []),
                )
                tasks_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Import completed. {tasks_created} tasks created, {tasks_skipped} tasks skipped."
            )
        )
