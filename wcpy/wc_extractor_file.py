
import re
from nltk.tokenize import word_tokenize

# This regex removes
all_symbols_re = re.compile("(^[A-Z]\.|[^a-zA-Z '-]|''|--)")

class PathNotValidException(Exception):
    def __init__(self, path):
        Exception.__init__(self, "Path provided is not valid: " + str(path))

class WCExtractorFile:

    def __init__(self, file_path, file_opener=open, filter_words=[]):
        self._file_path = file_path
        self._file_opener = file_opener
        self._filter_words = set(filter_words)

    def extract_wc_from_file(self, d_words={}):
        """
        TODO: Add Docs
        """

        with self._file_opener(self._file_path) as file:

            for line in file:
                already_added_words = set()
                words = self._split_line(line)

                for word in words:

                    add_sentence = True

                    if word not in already_added_words:
                        already_added_words.add(word)
                    else:
                        add_sentence = False

                    self._add_word(word, line, d_words, add_sentence=add_sentence)


    def _split_line(self, line):

        try:
            words_with_symbols = word_tokenize(line)
            words = [ w.lower() for w in words_with_symbols if any(char.isalpha() or char.isdigit() for char in w) ]

        except:
            print("No 'punkdt' dataset found. Quality is worse, please download with: python -c \"import nltk; nltk.download('punkt')\"")
            line_no_sym = all_symbols_re.sub(' ', line)
            words = line_no_sym.split()

        if len(self._filter_words) > 0:
            words = [w for w in words if w in self._filter_words]

        processed_words = [ w.lower() for w in words if w not in '-' ]

        return processed_words


    def _add_word(self, word, line, d_words={}, add_sentence=True):

        if word not in d_words:
             d_words[word] = {
                "word_count": 0,
                "files": {
                    self._file_path: []
                }
            }

        d_words[word]["word_count"] += 1

        dw_f = d_words[word]["files"]

        if self._file_path not in dw_f:
            dw_f[self._file_path] = []

        if add_sentence:
            dw_f[self._file_path].append(line)


