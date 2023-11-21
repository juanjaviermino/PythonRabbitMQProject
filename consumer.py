import pika
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to send an email
def send_email(subject, body, to_email):
    from_email = 'javierarboleda9901@gmail.com'
    password = 'wrgz vyqy qxbq ihcu'  # Be cautious with hardcoding sensitive information

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

# Establish connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the topic exchange
exchange_name = 'topic_exchange'
channel.exchange_declare(exchange=exchange_name, exchange_type='topic')

# Function to process received messages
def callback(ch, method, properties, body):
    message = body.decode('utf-8')
    print(f" [x] Recibido {message}")

    if message.startswith("Subject:"):
        subject_end_index = message.find('\n')
        subject = message[len("Subject:"):subject_end_index].strip()
        body = message[subject_end_index:].strip()
        send_email(subject, body, "jminoarboleda@gmail.com")
    else:
        print("Invalid message format")
    
# Ask the user for the topic to listen to
topic = input("Ingresa el topico a escuchar to (e.g., 'email.info'): ")

# Declare a queue specifically for this topic
queue_name = topic + '_queue'  # Create a unique queue name for this topic
channel.queue_declare(queue=queue_name)

# Bind the queue to the exchange with the specific topic
channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=topic)

# Start consuming the messages from the queue
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print(f' [*] Esperando mensajes en el topico "{topic}". Para salir presiona CTRL+C')
channel.start_consuming()
