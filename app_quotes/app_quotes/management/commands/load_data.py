import json
from django.core.management.base import BaseCommand, CommandError
from app_quotes.models import Quote
from app_author.models import Author


class Command(BaseCommand):
    help = "Load data from quotes.json and authors.json"

    def handle(self, *args, **kwargs):
        try:
            with open("authors.json", "r", encoding="utf-8") as authors_file:
                authors_data = json.load(authors_file)

            with open("quotes.json", "r", encoding="utf-8") as quotes_file:
                quotes_data = json.load(quotes_file)

            # Create a dictionary of authors to avoid duplicates
            authors_dict = {}
            for author_data in authors_data:
                author, created = Author.objects.get_or_create(
                    fullname=author_data["fullname"],
                    defaults={
                        "born_date": author_data["born_date"],
                        "born_location": author_data["born_location"],
                        "description": author_data["description"],
                    },
                )
                authors_dict[author.fullname] = author

            # Create quotes and associate them with authors
            for quote_data in quotes_data:
                author = authors_dict[quote_data["author"]]
                Quote.objects.create(
                    quote=quote_data["quote"],
                    author=author,
                    tags=", ".join(
                        quote_data["tags"]
                    ),  # Store tags as a comma-separated string
                )

            self.stdout.write(self.style.SUCCESS("Data loaded successfully"))

        except FileNotFoundError as e:
            raise CommandError(f"File not found: {e.filename}")
        except json.JSONDecodeError as e:
            raise CommandError(f"Error decoding JSON: {e}")
        except Exception as e:
            raise CommandError(f"An error occurred: {e}")
