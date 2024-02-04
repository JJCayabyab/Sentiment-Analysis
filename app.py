from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify
import csv

app = Flask(__name__)

class SentimentAnalyzer:
    def __init__(self, positive_lexicon, negative_lexicon):
        self.positive_fsm = self.build_fsm(positive_lexicon)
        self.negative_fsm = self.build_fsm(negative_lexicon)

    def build_fsm(self, lexicon):
        fsm = {}
        for word in lexicon:
            current_state = fsm
            for char in word:
                current_state = current_state.setdefault(char, {})
            current_state['is_end'] = True
        return fsm

    def analyze_sentiment(self, text):
        words = text.split()  # Split the text into words
        positive_score = sum(self.check_fsm(word, self.positive_fsm) for word in words)
        negative_score = sum(self.check_fsm(word, self.negative_fsm) for word in words)

        if positive_score > negative_score:
            return "Positive"
        elif positive_score < negative_score:
            return "Negative"
        else:
            return "Neutral"

    def check_fsm(self, word, fsm):
        score = 0
        for char in word:
            if char in fsm:
                fsm = fsm[char]
                if 'is_end' in fsm:
                    score += 1
            else:
                fsm = self.positive_fsm  # Reset to initial state for the next word
        return score

# Load positive and negative lexicons from text files
with open('positive.txt', 'r') as file:
    positive_lexicon = file.read().splitlines()

with open('negative.txt', 'r') as file:
    negative_lexicon = file.read().splitlines()

# Initialize the SentimentAnalyzer
sentiment_analyzer = SentimentAnalyzer(positive_lexicon, negative_lexicon)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form.get('text')
    file = request.files.get('file')

    if not text and not file:
        return redirect(url_for('index'))

    try:
        if file:
            # Process CSV file
            results = process_csv(file)
            return jsonify(results)
        else:
            # Process text input
            result = {'text': text, 'lexicon': sentiment_analyzer.analyze_sentiment(text)}
            return jsonify([result])
    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({'error': str(e)}), 500


def process_csv(file):
    results = []
    reader = csv.DictReader(file.read().decode('utf-8').splitlines())
    
    for row in reader:
        text = row['message']
        lexicon = sentiment_analyzer.analyze_sentiment(text)
        results.append({'text': text, 'lexicon': lexicon})
    
    return results

if __name__ == '__main__':
    app.run(debug=True)
