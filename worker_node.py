import pika
import time
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='email_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
     # Convert the received body (the email object) from bytes to a Python object
    email = json.loads(body.decode())  # Using JSON to decode the message
    print(f"Sending email to: {email['recipient']}")
    print(f"Email Body: {email['emailBody']}")
    # Simulate time taken to process the email sending (e.g., contacting SMTP server)
    time.sleep(15)  # Simulate time taken to send an email (e.g., network latency)
    print(f"Email sent to {email['recipient']} successfully!")
    # Acknowledge that the message has been processed
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='email_queue', on_message_callback=callback)

channel.start_consuming()