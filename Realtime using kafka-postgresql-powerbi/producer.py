from confluent_kafka import Producer
import praw


def product_kafka():
    
    reddit = praw.Reddit(client_id='_TqsT-EVDW1p6mMTy33G0g',
                        client_secret='KP5RhpW9YYF8i13rnijJ2KUQ-fLIRg',
                        username='Haunting-Flower1586',
                        password='fawaz123',
                        user_agent='Haunting-Flower1586')

    subreddit = reddit.subreddit('netflix')

    hot_python = subreddit.hot(limit=10)
    for submission in hot_python:
        if not submission.stickied:
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                print(comment.body)

                bootstrap_servers = "127.0.0.1:9092"
                topic = "Netflix"
                producer = Producer({"bootstrap.servers": bootstrap_servers})
                producer.produce(topic, value=comment.body)
                producer.flush()
                print("Message sent to Kafka topic.✅")

teams = product_kafka()
