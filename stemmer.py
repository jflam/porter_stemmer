# Implementation of the Porter Stemming Algorithm based on implementation from
# https://tartarus.org/martin/PorterStemmer/python.txt

VOWELS = 'aeiou'

class Stemmer:
    j: int 
    k: int
    word: str
    
    def is_consonant(self, i):
        if self.word[i] in VOWELS:
            return False
        
        if self.word[i] != 'y':
            return True

        # Special case 'y' - vowel if preceded by consonant 
        if i > 0 and self.is_consonant(i-1):
            return False
        else:
            return True

    def has_vowel_in_stem(self):
        for i in range(self.j + 1):
            if not self.is_consonant(i):
                return True
        return False

    def has_double_consonant(self, i):
        if i < 1:
            return False
        if self.word[i] != self.word[i-1]:
            return False
        return self.is_consonant(i)

    def has_cvc(self, i):
        if (i < 2 
            or not self.is_consonant(i) 
            or self.is_consonant(i-1) 
            or not self.is_consonant(i-2)):
            return False
        ch = self.word[i]
        if ch == "w" or ch == "x" or ch == "y":
            return False
        return True

    def m(self):
        """Calculate the number of consonant sequences (VC) in the word."""
        consonant_sequences = 0
        i = 0
        while True:
            if i > self.j:
                return consonant_sequences
            if not self.is_consonant(i):
                break
            i += 1
        i += 1
        while True:
            while True:
                if i > self.j:
                    return consonant_sequences
                if self.is_consonant(i):
                    break 
                i += 1
            i += 1
            consonant_sequences += 1
            while True:
                if i > self.j:
                    return consonant_sequences
                if not self.is_consonant(i):
                    break
                i += 1
            i += 1

    def ends_with(self, s: str):
        """Efficient test if self.word ends in s. Side effect is that 
        self.j is set for future operations that mutate the string"""

        length = len(s)
        if s[length - 1] != self.word[self.k]:
            return False 
        if length > self.k + 1:
            return False 
        if self.word[self.k - length + 1:self.k + 1] != s:
            return False 
        self.j = self.k - length
        return True
    
    def replace_with(self, s: str):
        """Insert s at the insertion point in the string determined by an
        earlier call to ends."""

        length = len(s)
        self.word = self.word[:self.j+1] + s + self.word[self.j+length+1:]
        self.k = self.j + length

    def truncate(self, count: int):
        self.k -= count 

    def r(self, s: str):
        if self.m() > 0:
            self.replace_with(s)

    def step1a(self):
        if self.ends_with("s"):
            if self.ends_with("sses"):
                self.truncate(2)
            elif self.ends_with("ies"):
                self.truncate(2)
            elif self.word[self.k - 1] != 's':
                self.truncate(1)

    def step1b(self):
        if self.ends_with("eed"):
            if self.m() > 0:
                self.truncate(1)
        elif ((self.ends_with("ed") or self.ends_with("ing")) 
              and self.has_vowel_in_stem()):
            self.k = self.j
            if self.ends_with("at"):
                self.replace_with("ate")
            elif self.ends_with("bl"):
                self.replace_with("ble")
            elif self.ends_with("iz"):
                self.replace_with("ize")
            elif self.has_double_consonant(self.k):
                self.truncate(1)
                ch = self.word[self.k]
                if ch == "l" or ch == "s" or ch == "z":
                    self.truncate(-1)
            elif (self.m() == 1 and self.has_cvc(self.k)):
                self.replace_with("e")
    
    def step1c(self):
        if self.ends_with("y") and self.has_vowel_in_stem():
            self.word = self.word[:self.k] + "i" + self.word[self.k+1:]

    step2_rules = {
        "a": [("ational", "ate"),
              ("itional", "tion")],
        "c": [("enci", "ence"),
              ("anci", "ance")],
        "e": [("izer", "ize")],
        "l": [("bli", "ble"),
              ("alli", "al"),
              ("entli", "ent"),
              ("eli", "e"),
              ("ousli", "ous")],
        "o": [("ization", "ize"),
              ("ation", "ate"),
              ("ator", "ate")],
        "s": [("alism", "al"),
              ("iveness", "ive"),
              ("fulness", "ful"),
              ("ousness", "ous")],
        "t": [("aliti", "al"),
              ("iviti", "ive"),
              ("biliti", "ble")],
        "g": [("logi", "log")]
    }

    def step2(self):
        for letter, transforms in self.step2_rules.items():
            if self.word[self.k-1] == letter:
                for transform in transforms:
                    if self.ends_with(transform[0]):
                        self.r(transform[1])

    step3_rules = {
        "e": [("icate", "ic"),
              ("ative", ""),
              ("alize", "al")],
        "i": [("iciti", "ic")],
        "l": [("ical", "ic"),
              ("ful", "")],
        "s": [("ness", "")]
    }

    def step3(self):
        for letter, transforms in self.step3_rules.items():
            if self.word[self.k] == letter:
                for transform in transforms:
                    if self.ends_with(transform[0]):
                        self.r(transform[1])
        
    step4_rules = {
        "a": [("al", None)],
        "c": [("ance", None),
              ("ence", None)],
        "e": [("er", None)],
        "i": [("ic", None)],
        "l": [("able", None),
              ("ible", None)],
        "n": [("ant", None),
              ("ement", None),
              ("ment", None),
              ("ent", None)],
        "o": [("ion", lambda c: c == "s" or c == "t"),
              ("ou", None)],
        "s": [("ism", None)],
        "t": [("ate", None),
              ("iti", None)],
        "u": [("ous", None)],
        "v": [("ive", None)],
        "z": [("ize", None)]
    }

    def step4(self):
        for letter, transforms in self.step4_rules.items():
            if self.word[self.k-1] == letter:
                for transform in transforms:
                    if transform[1] is None:
                        if self.ends_with(transform[0]):
                            if self.m() > 1:
                                self.k = self.j
                            return
                    else:
                        if (self.ends_with(transform[0])
                            and transform[1](self.word[self.j])):
                            if self.m() > 1:
                                self.k = self.j
                            return

    def step5(self):
        self.j = self.k
        if self.word[self.k] == "e":
            a = self.m()
            if a > 1 or (a == 1 and not self.has_cvc(self.k-1)):
                self.truncate(1)
        if (self.word[self.k] == "l" 
            and self.has_double_consonant(self.k) 
            and self.m() > 1):
            self.truncate(1)

    def stem(self, word: str):
        self.word = word
        self.k = len(word) - 1

        if self.k <= 1:
            return self.word

        self.step1a()
        self.step1b()
        self.step1c()
        self.step2()
        self.step3()
        self.step4()
        self.step5()
        return self.word[:self.k + 1]