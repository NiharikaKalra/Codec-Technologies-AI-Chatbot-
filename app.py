from flask import Flask, render_template, request, jsonify
import sqlite3
import nltk
from nltk.tokenize import word_tokenize
from datetime import datetime

# 1. NLTK 
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

app = Flask(__name__)

# 2. SQLite 
def setup_database():
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_msg TEXT,
            bot_reply TEXT,
            time TEXT
        )
    ''')
    conn.commit()
    conn.close()

# 3. chatboat ques ans
responses = {
    "hi": "Hello! Welcome to Codec Technologies. How can I help you?",
    "hello": "Hi there! Ask me anything about our internship or courses.",
    "name": "I am Vrinda, an AI Support Assistant built by [Niharika Kalra]].",
    "developer": "This chatbot was developed by [Niharika Kalra] during the Python Developer Internship.",
    "internship": "This is a 1-Month Python Developer Internship. You need to complete any 2 projects.",
    "project": "You can choose any 2 projects from the list of 10 and upload them to GitHub.",
    "certificate": "You will get your certificate after submitting your GitHub links via email.",
    "submit": "Send your GitHub project links and your full name to vaishali@codectechnologies.in.",
    "bye": "Goodbye! Best of luck with your internship."
}

# 4. user message answer finder
def find_reply(message):
    
    words = word_tokenize(message.lower())
    
    for word in words:
        if word in responses:
            return responses[word]
            
    return "Sorry, I didn't understand. Try asking about: internship, project, submit, or certificate."

# 5. showing home page of website
@app.route('/')
def home():
    return render_template('index.html')

# 6. take messages and give answer
@app.route('/ask', methods=['POST'])
def ask():
    user_text = request.json.get('message', '')
    reply = find_reply(user_text)
    
    # बातचीत को डेटाबेस में सेव करना
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO logs (user_msg, bot_reply, time) VALUES (?, ?, ?)", 
                   (user_text, reply, current_time))
    conn.commit()
    conn.close()
    
    return jsonify({'reply': reply})

if __name__ == '__main__':
    setup_database()
    app.run(debug=True)
