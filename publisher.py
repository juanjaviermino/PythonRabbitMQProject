import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

exchange_name = 'topic_exchange'
channel.exchange_declare(exchange=exchange_name, exchange_type='topic')

channel.queue_declare(queue='email_queue')
channel.queue_bind(exchange=exchange_name, queue='email_queue', routing_key='email.*')

topic = input("Ingresa el topico (e.g., 'email.info'): ")  # Routing key pattern e.g., 'email.info'
subject = input("Ingresa el titulo del mail: ")
body = input("Ingresa el cuerpo del email: ")

message = f"Subject: {subject}\n\n{body}"
channel.basic_publish(exchange=exchange_name,
                      routing_key=topic,  
                      body=message)
print(f" [x] Email enviado al topico '{topic}'")

connection.close()
