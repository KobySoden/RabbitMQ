import pika

def connect():
    #connect to broker
    connection = pika.BlockingConnection(pika.ConnectionParameters('IP'))
    return connection.channel()

    
def send(msg, channel, q):
    #create a topic to send messages to
    channel.queue_declare(queue=q)

    channel.basic_publish(exchange='',
                        routing_key=q,
                        body=msg)

    print(" [x] Sent " + msg)

def recieve(q):
    channel.queue_declare(queue=q)

    def callback(ch, method, properties, body):
        #do something
        print(" [x] Received %r" % body)
        #stop consuming loop
        channel.stop_consuming()

    channel.basic_consume(queue=q,
                        auto_ack=True, #remove this for manual message delation after consumption
                        on_message_callback=callback)

    channel.start_consuming()

if __name__ == "__main__":
    channel = connect()
    send('https://www.google.com', channel, 'hello')
    channel.close()

    channel = connect()
    recieve('hello')
    channel.close()
