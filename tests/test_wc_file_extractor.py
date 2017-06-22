from pywc import WCFileExtractor

import unittest
from unittest.mock import MagicMock, call

TEST_WORD = "TEST_WORD"
TEST_FILE = "TEST_FILE"
TEST_SENTENCE = "TEST_SENTENCE"
TEST_SENTENCE_2 = "TEST_SENTENCE_2"

class TestWCFileExtractor(unittest.TestCase):

    def setUp(self):

        self._openMock = MagicMock()
        self._openMock.__iter__.return_value = [TEST_SENTENCE, TEST_SENTENCE_2]

        self._extractor = WCFileExtractor(TEST_FILE, self._openMock)

    def test_extract(self):

        add_word_mock = MagicMock()
        self._extractor._add_word = add_word_mock

        line_to_words_mock = MagicMock(side_effects=[TEST_SENTENCE, TEST_SENTENCE_2])
        self._extractor._line_to_words = line_to_words_mock

        wd = {}
        self._extractor.extract(wd)

        expected_line_calls = [call(TEST_SENTENCE), call(TEST_SENTENCE_2)]

        self._openMock.assert_called_with(TEST_FILE)
        line_to_words_mock.assert_has_calls(expected_line_calls)


    def test_line_to_words(self):

        # Test sentence with no symbols
        sentence = "This no symbols"
        l_sentence = ["this", "no", "symbols"]
        l_result = self._extractor._line_to_words(sentence)

        self.assertEqual(l_sentence, l_result)

        # Testing more complex sentences with symbols
        sentence_2 = "This, Is. Another; SeNtence... and-works?"
        l_sentence_2 = ["this", "is", "another", "sentence", "and-works"]
        l_result_2 = self._extractor._line_to_words(sentence_2)

        self.assertEqual(l_sentence_2, l_result_2)



    def test_add_single_word(self):
        words_dict = {}
        expected_words_dict = {
            TEST_WORD: {
                "word_count": 1,
                "files": {
                    TEST_FILE: [ TEST_SENTENCE ]
                }
            }
        }

        result_words_dict = self._extractor._add_word(TEST_WORD, TEST_SENTENCE, words_dict)

        self.assertEqual(result_words_dict, expected_words_dict)

    def test_add_multiple_words(self):
        words_dict = {}
        # Testing that adding multiple of the same words
        expected_words_dict = {
            TEST_WORD: {
                "word_count": 3,
                "files": {
                    TEST_FILE: [ TEST_SENTENCE, TEST_SENTENCE_2, TEST_SENTENCE ]
                }
            }
        }

        result_words_dict = self._extractor._add_word(TEST_WORD, TEST_SENTENCE, words_dict)
        result_words_dict = self._extractor._add_word(TEST_WORD, TEST_SENTENCE_2, words_dict)
        result_words_dict = self._extractor._add_word(TEST_WORD, TEST_SENTENCE, words_dict)

        self.assertEqual(result_words_dict, expected_words_dict)



