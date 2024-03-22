import pika
import connect 
from models import Contact
import sys

def main():
    # Підключення до RabbitMQ
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority&appName=Cluster0", port=5672, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue='contacts')

    def send_email(contact_id):
        # Імітація надсилання email
        print(f"Email sent to contact with id: {contact_id}")

        # Оновлення логічного поля "sent" у контакту
        contact = Contact.objects(id=contact_id).first()
        if contact:
            contact.sent = True
            contact.save()
            print(f"Contact with id {contact_id} marked as sent")

    def callback(ch, method, properties, body):
        contact_id = body.decode()
        send_email(contact_id)

    channel.basic_consume(queue='contacts', on_message_callback=callback, auto_ack=True)

    print('Consumer стартує. Очікування повідомлень...')

    channel.start_consuming()

    # Закриваємо з'єднання з базою даних та з RabbitMQ
    connection.close()

    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)