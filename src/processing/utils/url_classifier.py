import pandas as pd
import re
import nltk
from sklearn.exceptions import ConvergenceWarning
from sklearn.utils._testing import ignore_warnings
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from urllib.parse import urlparse
from contextlib import suppress

DEFAULT_DATAPATH = "../datasets/urldata.csv"


class URLClassifier:
    """
    Classifier is based on this guide written by Faizan Ahmad:
    - https://www.kdnuggets.com/2016/10/machine-learning-detect-malicious-urls.html

    The data-set used was obtained from the following kaggle notebook written by Siddharth Kumar:
    - https://www.kaggle.com/siddharthkumar25/detect-malicious-url-using-ml

    A URL Classifier which uses a large dataset of pre-labeled malicious and benign URLs
    to classify URLs using a TF-IDF Vectorizer and Logistic Regression model.
    """
    def __init__(self, datapath=None, verbose=True):
        nltk.download('stopwords', quiet=True)
        self.stoplist = stopwords.words('english') + ['http', 'https']
        print("- [URL Classifier] Loading malicious URL dataset")
        self.url_df = pd.read_csv(datapath if datapath else DEFAULT_DATAPATH)
        self.tfidf_vec = TfidfVectorizer(tokenizer=self.gen_tokens)
        self.model = LogisticRegression()
        self.setup()

    @ignore_warnings(category=ConvergenceWarning)
    def setup(self):
        """
        Fit and transform classification model using vectorized
        dataset and calculate accuracy score on testing dataset using trained model.
        """
        print("- [URL Classifier] Generating tokens: this may take some time...")
        url_df_vecs = self.tfidf_vec.fit_transform(self.url_df["url"])
        url_df_labels = self.url_df["label"]

        print("- [URL Classifier] Training and testing on dataset.")
        x_train, x_test, y_train, y_test = train_test_split(
            url_df_vecs,
            url_df_labels,
            test_size=0.25,
            random_state=192837
        )
        self.model.fit(x_train, y_train)
        accuracy_score = self.model.score(x_test, y_test) * 100

        print(f"- [URL Classifier] Classifier Accuracy: {accuracy_score:.2f}%")

    def gen_tokens(self, url):
        """
        Generate TFIDF Vector tokens from a provided URL.
        This methid invokes stop-words removal, e.g. tokens "and", "is", "com", "http", etc...

        Args:
            url (str): The URL to be tokenized

        Returns:
            list: A list of tokens extracted from a given URL
        """
        url_info = urlparse(url)
        tokens = set(re.findall(r"[\w']+", url))
        tokens.add(url_info.hostname)

        with suppress(Exception):
            if url_info.port:
                tokens.add(str(url_info.port))

        return [t for t in tokens if t is not None and t not in self.stoplist]

    def classify_urls(self, urls):
        """
        Classifies a list of URLs, labelling each URL as 'benign' or 'malicious'

        Args:
            urls (list): A list of URLs (strings) to be classified

        Returns:
            None - The URL list contains an invalid or empty URL
            list - A list of string labels representing classification of each URL.
                A URL label can be either 'malicious' or 'benign'.

        """
        if any(not url or '.' not in url for url in urls):
            return None

        vec_urls = self.tfidf_vec.transform(urls)
        return self.model.predict(vec_urls)
