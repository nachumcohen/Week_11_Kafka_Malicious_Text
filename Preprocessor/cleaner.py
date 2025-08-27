import re
import string
import nltk
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords

# Download required NLTK resources (only needed once per environment)
nltk.download('stopwords')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

class Cleaner:

    def __init__(self , text):
        self.text = text

    def remove_punctuation(self):
        # Remove standard punctuation marks (, . ! ?)
        translator = str.maketrans('', '', string.punctuation)
        self.text = self.text.translate(translator)

    def remove_special_marks(self):
        # Remove any non-alphanumeric characters except spaces
        self.text = re.sub(r'[^a-zA-Z0-9\s]', '', self.text)

    def remove_whitespace(self):
        # Replace multiple spaces/newlines with a single space
        self.text = " ".join(self.text.split())

    def remove_stopwords(self):
        # Remove common words like "is", "the", "and"
        stop_words = set(stopwords.words("english"))
        word_tokens = word_tokenize(self.text)
        filtered_text = [word for word in word_tokens if word not in stop_words]
        self.text = ' '.join(filtered_text)

    def text_to_lower(self):
        # Convert all characters to lowercase
        self.text = self.text.lower()

    def lemma_words(self):
        # Reduce words to their base form
        word_tokens = word_tokenize(self.text)
        lemmas = [lemmatizer.lemmatize(word) for word in word_tokens]
        self.text = ' '.join(lemmas)

    def return_self_text(self):
        return self.text