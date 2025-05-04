# Get-Content input.txt | python spell_checker.py
import sys
import re
from collections import Counter

# Read the corpus and build dictionary
def load_corpus(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    text = text.lower()
    words = re.findall(r"[a-z'-]+", text)
    return Counter(words)

# Generate one-edit-away words
def edits1(word):
    """Generate all possible edits 1 edit away from word"""
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word)+1)]
    
    # Deletion (remove one character)
    deletes = [L + R[1:] for L, R in splits if R]
    
    # Insertion (add one character)
    inserts = [L + c + R for L, R in splits for c in letters]
    
    # Replacement (change one character)
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    
    # Transposition (swap adjacent characters)
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    
    # Return combined set of all possible edits
    return set(deletes + inserts + replaces + transposes)

# Correct a word
def correct(word, word_freq):
    """Return best correction for potentially misspelled word"""
    word = word.lower()  # Convert input to lowercase
    
    # If word is already in dictionary, return it
    if word in word_freq:
        return word
    
    # Generate all possible 1-edit candidates
    candidates = edits1(word)
    
    # Filter candidates to only those in our dictionary
    valid = [w for w in candidates if w in word_freq]
    
    if not valid:
        return word  # No suggestions found
    
    # Select candidate with highest frequency, then alphabetical order
    return min(valid, key=lambda w: (-word_freq[w], w))

# Main program
if __name__ == "__main__":
    word_freq = load_corpus("corpus.txt")  # Ensure this is in same folder
    n = int(sys.stdin.readline())
    for _ in range(n):
        word = sys.stdin.readline().strip()
        print(correct(word, word_freq))

















'''
Algorithm
Step-by-Step Process for the Spell Checker:

Corpus Processing:
Read the corpus file line by line until "END-OF-CORPUS" is encountered.
Extract words using regex [a-z'-]+ to include apostrophes and hyphens.
Build a frequency dictionary (word_freq) using Counter to track how often each word appears.

Input Handling:
Read the number of test words (N).
For each input word:
Convert it to lowercase for case-insensitive matching.

Correction Logic:
If the word exists in word_freq, return it as correct.
If not, generate all possible 1-edit candidates (deletions, insertions, replacements, transpositions).
Filter candidates to retain only those present in word_freq.
If no valid candidates exist, return the original word.
Else, select the candidate with:
Highest frequency in the corpus.
Alphabetical order (if frequencies are tied).

Theory Paragraph (NLP Connection)
Spell checking is a fundamental Natural Language Processing (NLP) task that addresses noisy text input caused by human typing errors. This problem demonstrates a basic NLP pipeline:

Corpus-Based Language Model: The frequency dictionary built from the corpus acts as a statistical language model, prioritizing words that appear more frequently in real-world usage.

Edit Distance: The 1-edit candidates (insertions, deletions, replacements, transpositions) model common typographical errors using the Damerau-Levenshtein edit distance, a standard NLP technique for string matching.

Ranking: Corrections are ranked by frequency (a proxy for likelihood) and alphabetically, mimicking how NLP systems balance statistical and linguistic patterns.

This qualifies as an NLP task because it processes natural language text, applies linguistic rules (word structure), and uses statistical methods (frequency analysis) to improve text quality—core principles of NLP systems like autocorrect and search engines.
'''
