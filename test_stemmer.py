from stemmer import Stemmer
from timeit import default_timer as timer

with open('data/words.txt', 'r') as rf:
    words = rf.read().splitlines()

with open('data/expected.txt', 'r') as rf:
    expected = rf.read().splitlines()

print(f"words == {len(words)} expected == {len(expected)}")
assert len(words) == len(expected)

start = timer()
stemmer = Stemmer()
errors = 0
for i, word in enumerate(words):
    if not expected[i] == stemmer.stem(word):
        errors += 1
end = timer()

print(f"ELAPSED TIME {end-start:.2f}s CORRECT: {len(words)-errors}/{len(words)}")
print(f"PERCENTAGE CORRECT: {(len(words)-errors)/len(words)*100:.2f}")