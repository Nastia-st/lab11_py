import nltk

try:
    # Перевірка наявності необхідних ресурсів
    _ = nltk.corpus.gutenberg.words('shakespeare-caesar.txt')
    _ = nltk.corpus.stopwords.words('english')
except LookupError:
    # Завантаження, якщо ресурси відсутні
    print("Завантажуємо необхідні корпуси NLTK...")
    nltk.download(['gutenberg', 'stopwords', 'punkt'])

print("NLTK та корпуси готові до використання.")
import nltk
from nltk.corpus import gutenberg
from nltk.corpus import stopwords
import string
from collections import Counter
import matplotlib.pyplot as plt

# Завантаження та підготовка даних 
try:
    words = gutenberg.words('shakespeare-caesar.txt')
except LookupError:
    print("Завантаження необхідних корпусів NLTK...")
    nltk.download(['gutenberg', 'stopwords', 'punkt'])
    words = gutenberg.words('shakespeare-caesar.txt')

word_count = len(words)
print(f"\nКількість слів у тексті: {word_count:,}")

# Аналіз 10 найбільш вживаних слів 
all_words_raw = [word.lower() for word in words]
word_freq_raw = Counter(all_words_raw)
top_10_raw = word_freq_raw.most_common(10)
words_raw = [item[0] for item in top_10_raw]
counts_raw = [item[1] for item in top_10_raw]
print("\nТоп-10 слів (із пунктуацією та стоп-словами)")
for word, count in top_10_raw:
    print(f"'{word}': {count:,}")

# Побудова діаграми
plt.figure(figsize=(10, 5))
plt.bar(words_raw, counts_raw, color='skyblue')
plt.title('Топ-10 слів у тексті (сирий)', fontsize=14)
plt.show()

# Аналіз 10 найбільш вживаних слів (Очищений текст)
english_stopwords = set(stopwords.words('english'))
punctuation_set = set(string.punctuation)

# Фільтрація
filtered_words = [
    word.lower()
    for word in words
    if word.lower() not in english_stopwords and word not in punctuation_set and word.isalnum()
]

# Повторний підрахунок частоти
word_freq_filtered = Counter(filtered_words)
top_10_filtered = word_freq_filtered.most_common(10)
words_filtered = [item[0] for item in top_10_filtered]
counts_filtered = [item[1] for item in top_10_filtered]
print("\nТоп-10 слів (після видалення стоп-слів та пунктуації)")
for word, count in top_10_filtered:
    print(f"'{word}': {count:,}")

# Побудова діаграми (Очищений текст)
plt.figure(figsize=(10, 5))
plt.bar(words_filtered, counts_filtered, color='coral')
plt.title('Топ-10 слів у тексті (очищений)', fontsize=14)
plt.show()