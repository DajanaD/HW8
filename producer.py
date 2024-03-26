import pika
import faker
import connect
from models import Contact

def main():
    # Підключення до RabbitMQ
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='contacts')

    # Генератор фейкових даних
    fake = faker.Faker()


    # Кількість контактів, яку ми хочемо згенерувати
    num_contacts = 10

    # Генерація та збереження фейкових контактів у базі даних та відправка їх ідентифікаторів у чергу RabbitMQ
    for _ in range(num_contacts):
        full_name = fake.name()
        email = fake.email()

        # Збереження контакту у базі даних
        contact = Contact(full_name=full_name, email=email).save()

        # Відправлення ідентифікатора контакту у чергу RabbitMQ
        channel.basic_publish(exchange='', routing_key='contacts', body=str(contact.id))

    print(f"{num_contacts} контактів згенеровано та відправлено у чергу RabbitMQ")

    # Закриваємо з'єднання з базою даних та з RabbitMQ
    connection.close()
    

if __name__ == '__main__':
    main()