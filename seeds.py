import json
from models import Author, Quote
import connect


# Функція для завантаження авторів з JSON-файлу
def load_authors_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            author = Author(
                fullname=author_data['fullname'],
                born_date=author_data['born_date'],
                born_location=author_data['born_location'],
                description=author_data['description']
            )
            author.save()

# Функція для завантаження цитат з JSON-файлу
def load_quotes_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author_name = quote_data['author']
            author = Author.objects(fullname=author_name).first()
            if author:
                quote = Quote(
                    text=quote_data['quote'],
                    author=author,
                    tags=quote_data['tags']
                )
                quote.save()

if __name__ == "__main__":
    # Шлях до JSON-файлів
    authors_file_path = 'authors.json'
    quotes_file_path = 'quotes.json'

    # Завантаження даних з JSON-файлів
    load_authors_from_json(authors_file_path)
    load_quotes_from_json(quotes_file_path)