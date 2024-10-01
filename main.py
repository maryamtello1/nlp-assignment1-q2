import string
import re


def process_text(text):
    # Split text into sentences by '.', '?', or '"', and get rid of extra spaces
    sentences = re.split(r'[\.\?"?]+', text)
    return [re.sub(r'[^\w\s\']', '', sentence).strip() for sentence in sentences if sentence.strip()]


def count_unigrams(words):
    word_freq = {}
    for word in words:
        if word not in word_freq:
            word_freq[word] = 1
        else:
            word_freq[word] += 1
    return word_freq


def count_bigrams(sentences):
    bigram_freq = {}
    for sentence in sentences:
        words = sentence.split()
        # Correctly handle apostrophes in words like "king's"
        i = 0
        while i < len(words) - 1:
            current_word = words[i]
            next_word = words[i + 1]
            # Check if the next word is 's and merge it with the current word
            if next_word == "'s":
                current_word += "'s"
                i += 1  # Skip the next word as it is merged
            if i + 1 < len(words):  # Ensure there is a next word to form a bigram
                bigram = current_word + " " + words[i + 1]
                if bigram not in bigram_freq:
                    bigram_freq[bigram] = 1
                else:
                    bigram_freq[bigram] += 1
            i += 1
    return bigram_freq

def write_frequencies_to_file(filename, freq_dict):
    with open(filename, "w", encoding="utf-8") as file:
        for key, value in sorted(freq_dict.items(), key=lambda item: item[1], reverse=True):
            file.write(f"{key}: {value}\n")


if __name__ == '__main__':
    with open("Collocations", "r") as f:
        paragraph = f.read()


    # Process the text to remove punctuation and split into words
    sentences = process_text(paragraph)

    # Count unigrams and bigrams
    unigram_counts = count_unigrams(sentences)
    bigram_counts = count_bigrams(sentences)

    # print("Unigrams:", unigram_counts)
    write_frequencies_to_file("bigram_counts.txt", bigram_counts)


