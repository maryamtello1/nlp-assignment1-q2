import string
import re
import math
import sys

def process_text(text):
    # Split text into sentences by '.', '?', or '"', and get rid of extra spaces
    sentences = re.split(r'[\.\?"?]+', text)
    return [re.sub(r'[^\w\s\']', '', sentence).strip() for sentence in sentences if sentence.strip()]

def count_unigrams(sentences):
    word_freq = {}
    for sentence in sentences:
        for word in sentence.split():
            if word not in word_freq:
                word_freq[word] = 1
            else:
                word_freq[word] += 1
    return word_freq

def count_bigrams(sentences):
    bigram_freq = {}
    for sentence in sentences:
        words = sentence.split()
        i = 0
        while i < len(words) - 1:
            # Correctly handle apostrophes in words like "king's"
            # Check if the next word is 's and merge it with the current word
            if words[i + 1] == "'s":
                words[i] += "'s"
                i += 1 # Skip the next word as it is merged
            if i + 1 < len(words): # Ensure there is a next word to form a bigram
                bigram = words[i] + " " + words[i + 1]
                if bigram not in bigram_freq:
                    bigram_freq[bigram] = 1
                else:
                    bigram_freq[bigram] += 1
            i += 1
    return bigram_freq

def chi_square(unigram_counts, bigram_counts, total_bigrams, total_unigrams):
    results = {}
    for bigram, bigram_count in bigram_counts.items():
        word1, word2 = bigram.split()
        #A: the frequency of the bigram.
        A = bigram_count
        #B :  frequency of the first word in the bigram occurring without the second word.
        B = unigram_counts[word1] - bigram_count
        #C:frequency of the second word in the bigram occurring without the first word.
        C = unigram_counts[word2] - bigram_count
        # D:  the number of times neither of the words in the bigram occur together.
        D = total_bigrams - (A + B + C)

        #chi square formula
        chi_sq_value = (total_unigrams * (A*D - B*C)**2) / ((A + C)*(B + D)*(A + B)*(C + D))
        results[bigram] = chi_sq_value
    return results

def calculate_pmi(unigram_counts, bigram_counts, total_unigrams):
    results = {}
    for bigram, count in bigram_counts.items():
        word1, word2 = bigram.split()
        #P(x) and P(y) are the probabilities of the individual words.
        p_x = unigram_counts[word1] / total_unigrams
        p_y = unigram_counts[word2] / total_unigrams
        #P(x,y) = the probability of the bigram (joint probability).
        p_xy = count / total_unigrams
        pmi = math.log2(p_xy / (p_x * p_y))
        results[bigram] = pmi
    return results

def main(measure):
    with open("Collocations", "r") as f:
        text = f.read()

    sentences = process_text(text)
    unigram_counts = count_unigrams(sentences)
    bigram_counts = count_bigrams(sentences)
    total_unigrams = sum(unigram_counts.values())
    total_bigrams = sum(bigram_counts.values())

    if measure == "chi-square":
        results = chi_square(unigram_counts, bigram_counts, total_bigrams, total_unigrams)
    elif measure == "PMI":
        results = calculate_pmi(unigram_counts, bigram_counts, total_unigrams)
    else:
        raise ValueError("Invalid measure type. Use 'chi-square' or 'PMI'.")

    # Output the top 20 results sorted by score
    sorted_results = sorted(results.items(), key=lambda item: item[1], reverse=True)[:20]
    for bigram, score in sorted_results:
        print(f"{bigram} {score}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: % python Collocations.py <file> <measure>")
    else:
        _, filename, measure = sys.argv
        main(measure)


