import re
import matplotlib.pyplot as plt

from pymongo import MongoClient
from collections import Counter
from wordcloud import WordCloud


class DataVisualization:
    def __init__(self, word_limit=10, plt_visual=False, wordcloud_visual=False):
        self.word_limit = word_limit
        self.plt_visual = plt_visual
        self.wordcloud_visual = wordcloud_visual

        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['haktan_ozer']
        self.read_collection = self.db['news']
        self.save_collection = self.db['word_frequency']
        self.word_counts = None
        self.most_common_words = None

    def get_word_counts(self):
        """
        This method gets word counts from database
        :return:
        """
        all_texts = [doc['text'] for doc in self.read_collection.find()]
        all_text_combined = ' '.join(all_texts)
        words = re.findall(r'\w+', all_text_combined.lower())
        self.word_counts = Counter(words)

    def plt_visualization(self):
        """
        This method visualizes word counts with matplotlib
        :return: save plot as png file
        """
        most_common_words = self.word_counts.most_common(10)
        words, counts = zip(*most_common_words)
        plt.bar(words, counts, color='skyblue')
        plt.xlabel('Words')
        plt.ylabel('Frequencies')
        plt.title('Most Common Words')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('word_frequencies.png')
        plt.show()

    def wordcloud_visualization(self):
        """
        This method visualizes word counts with wordcloud
        :return: save plot as png file
        """
        most_common_words = dict(self.word_counts.most_common(100))
        wordcloud = (WordCloud(width=800, height=400, background_color='white').
                     generate_from_frequencies(most_common_words))
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Wordcloud')
        plt.show()
        wordcloud.to_file('wordcloud.png')

    def results(self):
        """
        This method prints most common words and visualizes word counts
        """

        self.get_word_counts()
        self.most_common_words = self.word_counts.most_common(self.word_limit)

        if not self.plt_visual and not self.wordcloud_visual:
            print("Most common words:")

            for word, count in self.most_common_words:
                print(f"{word}: {count}")

                self.save_collection.insert_one({'word': word, 'count': count})

        if self.plt_visual:
            self.plt_visualization()

        if self.wordcloud_visual:
            self.wordcloud_visualization()


if __name__ == '__main__':
    d_visualization = DataVisualization(word_limit=10, plt_visual=False, wordcloud_visual=False)
    d_visualization.results()
