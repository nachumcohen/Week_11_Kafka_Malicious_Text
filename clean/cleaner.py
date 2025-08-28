import re
import string
import nltk
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords

# Download required NLTK resources (only needed once per environment)
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

lemmatizer = WordNetLemmatizer()

class Cleaner:


    def remove_punctuation(self , text):
        # Remove standard punctuation marks (, . ! ?)
        translator = str.maketrans('', '', string.punctuation)
        text = text.translate(translator)
        return text

    def remove_special_marks(self , text):
        # Remove any non-alphanumeric characters except spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return text

    def remove_whitespace(self , text):
        # Replace multiple spaces/newlines with a single space
        text = " ".join(text.split())
        return text

    def remove_stopwords(self ,text):
        # Remove common words like "is", "the", "and"
        stop_words = set(stopwords.words("english"))
        word_tokens = word_tokenize(text)
        filtered_text = [word for word in word_tokens if word not in stop_words]
        text = ' '.join(filtered_text)
        return text

    def text_to_lower(self,text):
        # Convert all characters to lowercase
        text = text.lower()
        return text

    def lemma_words(self,text):
        # Reduce words to their base form
        word_tokens = word_tokenize(text)
        lemmas = [lemmatizer.lemmatize(word) for word in word_tokens]
        text = ' '.join(lemmas)
        return text

    def get_clean_text(self,text):
        text = self.remove_punctuation(text)
        text = self.remove_special_marks(text)
        text = self.remove_whitespace(text)
        text = self.remove_stopwords(text)
        text = self.text_to_lower(text)
        text = self.lemma_words(text)

        return text