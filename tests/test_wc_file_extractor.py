from pywc import WCFileExtractor

import unittest
from unittest.mock import MagicMock, call

ACTUAL_FILE = "test_data/doc1.txt"
TEST_FILE = "TEST_FILE"
TEST_SENTENCE = "TEST SENTENCE"
TEST_SENTENCE_2 = "TEST SENTENCE TWO"
TEST_WORD = "test"
TEST_WORD_2 = "sentence"
TEST_WORD_3 = "two"
TEST_WORD_COUNT = 2
TEST_WORD_COUNT_2 = 2
TEST_WORD_COUNT_3 = 1

class TestWCFileExtractor(unittest.TestCase):

    def setUp(self):

        self._openMock = MagicMock()
        self._openMock.return_value.__enter__.return_value = [TEST_SENTENCE, TEST_SENTENCE_2]

        self._extractor = WCFileExtractor(TEST_FILE, self._openMock)

    def test_wc_file_extractor_end_to_end_with_files(self):
        extractor = WCFileExtractor(ACTUAL_FILE)
        result = extractor.extract()


    def test_wc_file_extractor_end_to_end_integration(self):

        wd = {}
        expected_wd = {
            TEST_WORD: {
                "word_count": TEST_WORD_COUNT,
                "files": {
                    TEST_FILE: [ TEST_SENTENCE, TEST_SENTENCE_2 ]
                }
            },
            TEST_WORD_2: {
                "word_count": TEST_WORD_COUNT_2,
                "files": {
                    TEST_FILE: [ TEST_SENTENCE, TEST_SENTENCE_2 ]
                }
            },
            TEST_WORD_3: {
                "word_count": TEST_WORD_COUNT_3,
                "files": {
                    TEST_FILE: [ TEST_SENTENCE_2 ]
                }
            }
        }

        result_wd = self._extractor.extract(wd)

        self.assertEqual(result_wd, expected_wd)


    def test_extract(self):

        add_word_mock = MagicMock()
        self._extractor._add_word = add_word_mock

        line_to_words_mock = MagicMock(return_value=TEST_SENTENCE)
        self._extractor._line_to_words = line_to_words_mock

        wd = {}
        self._extractor.extract(wd)

        expected_line_calls = [call(TEST_SENTENCE), call(TEST_SENTENCE_2)]

        self._openMock.assert_called_once_with(TEST_FILE)
        line_to_words_mock.assert_has_calls(expected_line_calls)


    def test_line_to_words(self):

        # Test sentence with no symbols
        sentence = "This no symbols"
        l_sentence = ["this", "no", "symbols"]
        l_result = self._extractor._line_to_words(sentence)

        self.assertEqual(l_sentence, l_result)

        # Testing more complex sentences with symbols
        sentence_2 = "This, Is. Another; SeNtence... and-works? 1010"
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



