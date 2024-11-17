import pika
import sys
import json 


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='email_queue', durable=True)

# Get the name argument (if provided) or use 'customer' as default
name = sys.argv[1] if len(sys.argv) > 1 else "customer"

# Create a personalized email object
email_message = {
    'recipient': f'{name}@gmail.com', 
    'emailBody': f'Dear {name},\n\nYour order has been successfully placed. Thank you for shopping with us!'  
}

# Send the email message to the queue
channel.basic_publish(
    exchange='',
    routing_key='email_queue',
    body=json.dumps(email_message),  # Convert the email object to JSON
    properties=pika.BasicProperties(
        delivery_mode=pika.DeliveryMode.Persistent  # Ensure the message persists in case RabbitMQ crashes
    )
)
print(f" [x] Sent order confirmation email to {email_message['recipient']}")
connection.close()