from flask import Flask, render_template, request, jsonify, abort
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
        words = text.lower().split()  # Convert to lowercase and split the text into words
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
                fsm = self.positive_fsm  # Reset to the initial state for the next word
        return score

# Load positive and negative lexicons from text files
try:
    with open('positive.txt', 'r') as file:
        positive_lexicon = file.read().splitlines()

    with open('negative.txt', 'r') as file:
        negative_lexicon = file.read().splitlines()

    # Initialize the SentimentAnalyzer
    sentiment_analyzer = SentimentAnalyzer(positive_lexicon, negative_lexicon)
except FileNotFoundError as e:
    print(f"Error: {e}")
    # Handle the missing file error appropriately
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    # Handle other potential exceptions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/sentiment', methods=['POST'])
def analyze_sentiment():
    try:
        data = request.get_json()

        if 'file' in request.files:
            # Handle CSV file input
            file = request.files['file']
            if file and file.filename.endswith('.csv'):
                messages = []
                reader = csv.DictReader(file)
                for row in reader:
                    if 'message' in row:
                        messages.append(row['message'])
                results = [{'message': message, 'sentiment': sentiment_analyzer.analyze_sentiment(message)} for message in messages]
                return jsonify({'results': results})
            else:
                return jsonify({'error': 'Invalid file format'}), 400
        elif 'text' in data:
            # Handle text input
            text = data['text']
            sentiment = sentiment_analyzer.analyze_sentiment(text)
            return jsonify({'message': text, 'sentiment': sentiment})
        else:
            return jsonify({'error': 'Invalid input format'}), 400
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        abort(500)
    
@app.route('/api/upload_csv', methods=['POST'])
def upload_csv():
    file = request.files['file']
    if file and file.filename.endswith('.csv'):
        # Assuming the CSV file has a 'message' column
        messages = []
        reader = csv.DictReader(file)
        for row in reader:
            if 'message' in row:
                messages.append(row['message'])
        results = [{'message': message, 'sentiment': sentiment_analyzer.analyze_sentiment(message)} for message in messages]
        return jsonify({'results': results})
    else:
        return jsonify({'error': 'Invalid file format'}), 400

if __name__ == '__main__':
    app.run(debug=True)