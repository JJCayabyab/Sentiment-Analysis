# do not use any module or library
# extraction of tweets using tweepy
# clean the tweets using finite automata procedure
# used regex to create scored based lexical to detect the good and bad words
# used the score to be the output of the program

class SentimentDFA:
    def __init__(self):
        # Define states
        self.states = {'q0', 'q1'}

        # Define transitions
        self.transitions = {
            'q0': {'good': 'q1', 'bad': 'q1'},
            'q1': {'good': 'q1', 'bad': 'q1'},
        }

        # Define accepting states
        self.accepting_states = {'q1'}

    def analyze_sentiment(self, text):
        words = text.lower().split()
        current_state = 'q0'

        for word in words:
            if word in self.transitions.get(current_state, {}):
                current_state = self.transitions[current_state][word]
            else:
                # Handle unknown words or reset to the initial state
                current_state = 'q0'

        if current_state in self.accepting_states:
            return "Positive"
        else:
            return "Negative"

# Example usage
if __name__ == "__main__":
    sentiment_dfa = SentimentDFA()

    input_text = input("Enter a text for sentiment analysis: ")
    result = sentiment_dfa.analyze_sentiment(input_text)

    print(f"Sentiment: {result}")
