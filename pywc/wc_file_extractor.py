
import string

all_symbols = set(string.punctuation)
all_symbols.remove('-')

class WCFileExtractor:

    def __init__(self, file_path):
        self._file_path = file_path

    def extract(self, words_dict={}):

        with open (self._file_path) as file:
            for line in file:
                words = self._line_to_words(line)

                for word in words:
                    self._add_word(word, line, words_dict)


        return words_dict


    def _line_to_words(self, line):

        sentence_no_sym = [s for s in line if s not in all_symbols]
        words = sentence_no_sym.split()
        processed_words = [ w for w in words if w is not '-' ]

        return processed_words


    def _add_word(self, word, line, words_dict):

        if word not in words_dict:
             words_dict[word] = {
                "word_count": 0,
                "files": {
                    self._file_path: []
                }
            }

        words_dict[word]["word_count"] += 1

        wd_f = self._words_dict[word]["word_count"]["files"]

        if self._file_path not in wd_f:
            wd_f[self._file_path] = []

        wd_f[self._file_path].append(line)

