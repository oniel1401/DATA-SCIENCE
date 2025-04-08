import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from confluent_kafka import Consumer, Producer
from joblib import load
import json

# Télécharger les ressources nécessaires de NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Fonction de prétraitement
def preprocess_text(text):
    text = re.sub(re.compile('<.*?>'), '', text)
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()

    tokens = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words and token.isalpha()]

    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    return ' '.join(tokens)

# Fonction de consommation et de classification
def consume_and_classify():
    bootstrap_servers = "localhost:9092"
    topic = "Netflix"
    outtopic = "Netflix_adapt"
    group_id = "test-group"

    consumer = Consumer({
        "bootstrap.servers": bootstrap_servers,
        "group.id": group_id,
        "auto.offset.reset": "earliest"
    })

    consumer.subscribe([topic])

    model = load('model_lr.joblib')
    vectorizer = load('vectorizer.joblib')

    producer = Producer({"bootstrap.servers": bootstrap_servers})

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        comment = msg.value().decode('utf-8')
        processed_comment = preprocess_text(comment)
        features = vectorizer.transform([processed_comment])
        prediction = model.predict(features)[0]
        sentiment = 'positive' if prediction == 1 else 'negative'
        print('***********************************************************************************************************************************')
        print(f"Comment: {comment}\nSentiment: {sentiment}")
        result = json.dumps({"comment": comment, "sentiment": sentiment})
        producer.produce(outtopic, value=result)
        producer.flush()

    consumer.close()
    producer.close()

consume_and_classify()
