
import re

all_symbols = re.compile('[^a-zA-Z -]')

class WCFileExtractor:

    def __init__(self, file_path, file_opener=open):
        self._file_path = file_path
        self._file_opener = file_opener

    def extract(self, words_dict={}):

        print("HEREEEEEEE")
        with self._file_opener(self._file_path) as file:

            for line in file:
                words = self._line_to_words(line)

                for word in words:
                    self._add_word(word, line, words_dict)


        return words_dict


    def _line_to_words(self, line):

        line_no_sym = all_symbols.sub('', line)
        words = line_no_sym.split()
        processed_words = [ w.lower() for w in words if w is not '-' ]

        return processed_words


    def _add_word(self, word, line, words_dict={}):

        if word not in words_dict:
             words_dict[word] = {
                "word_count": 0,
                "files": {
                    self._file_path: []
                }
            }

        words_dict[word]["word_count"] += 1

        wd_f = words_dict[word]["files"]

        if self._file_path not in wd_f:
            wd_f[self._file_path] = []

        wd_f[self._file_path].append(line)

        return words_dict

