import connect
from models import Quote, Author 
import redis
from redis_lru import RedisLRU

client = redis.StrictRedis(host=f"mongodb+srv://user:123456789user1/myDB?retryWrites=true&w=majority&appName=Cluster0", port=6379, password=None)
cache = RedisLRU(client)

@cache
def search_quotes_by_author(author_name):
    author = Author.objects(fullname=author_name).first()
    if author:
        quotes = Quote.objects(author=author)
        for quote in quotes:
            print(quote.text)
    else:
        print("Автор не знайдений")
@cache
def search_quotes_by_tag(tag):
    quotes = Quote.objects(tags=tag)
    for quote in quotes:
        print(quote.text)

def search_quotes_by_tags(tags):
    tags_list = tags.split(',')
    quotes = Quote.objects(tags__in=tags_list)
    for quote in quotes:
        print(quote.text)

if __name__ == "__main__":
    while True:
        command = input("Введіть команду (name: Автор / tag: Тег / tags: Теги): ")
        if command.lower() == 'exit':
            break
        
        parts = command.split(':')
        if len(parts) != 2:
            print("Невірний формат команди")
            continue
        
        search_type, value = parts[0].strip(), parts[1].strip()
        
        if search_type == 'name':
            search_quotes_by_author(value)
        elif search_type == 'tag':
            search_quotes_by_tag(value)
        elif search_type == 'tags':
            search_quotes_by_tags(value)
        else:
            print("Невірний тип пошуку")
