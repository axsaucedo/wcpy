from pywc import WCExtractorFile

import unittest
from unittest.mock import MagicMock, call

ACTUAL_FILE = "tests/test_data/doc1.txt"
TEST_FILE = "TEST_FILE"
TEST_SENTENCE = "TEST SENTENCE"
TEST_SENTENCE_2 = "TEST SENTENCE TWO"
TEST_WORD = "test"
TEST_WORD_2 = "sentence"
TEST_WORD_3 = "two"
TEST_WORD_COUNT = 2
TEST_WORD_COUNT_2 = 2
TEST_WORD_COUNT_3 = 1

class TestWCExtractorFile(unittest.TestCase):

    def setUp(self):

        self._openMock = MagicMock()
        self._openMock.return_value.__enter__.return_value = [TEST_SENTENCE, TEST_SENTENCE_2]

        self._extractor = WCExtractorFile(TEST_FILE, self._openMock)

    def test_wc_extractor_file_end_to_end_with_files(self):

        extractor = WCExtractorFile(ACTUAL_FILE)
        result_wc = {}
        extractor.extract_wc_from_file()

        for o_words in result_wc:

            word_count = result_wc[o_words]["word_count"]
            total_sentences = 0

            o_words_f = result_wc[o_words]["files"]
            for file in o_words_f:
                total_sentences += len(o_words_f[file])

            # Make sure that all the word counts are equal or greater
            # than the number of sentences
            self.assertGreaterEqual(word_count, total_sentences)


    def test_wc_extractor_file_end_to_end_integration(self):

        result_dw = {}
        expected_dw = {
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

        self._extractor.extract_wc_from_file(result_dw)

        self.assertEqual(result_dw, expected_dw)


    def test_extract(self):

        add_word_mock = MagicMock()
        self._extractor._add_word = add_word_mock

        line_to_words_mock = MagicMock(return_value=TEST_SENTENCE)
        self._extractor._split_line = line_to_words_mock

        result_dw = {}
        self._extractor.extract_wc_from_file(result_dw)

        expected_line_calls = [call(TEST_SENTENCE), call(TEST_SENTENCE_2)]

        self._openMock.assert_called_once_with(TEST_FILE)
        line_to_words_mock.assert_has_calls(expected_line_calls)


    def test_line_to_words(self):

        # Test sentence with no symbols
        sentence = "This no symbols"
        l_sentence = ["this", "no", "symbols"]
        l_result = self._extractor._split_line(sentence)

        self.assertEqual(l_sentence, l_result)

        # Testing more complex sentences with symbols
        sentence_2 = "This, Is. Another; SeNtence... and-works? 1010"
        l_sentence_2 = ["this", "is", "another", "sentence", "and-works", "1010"]
        l_result_2 = self._extractor._split_line(sentence_2)

        self.assertEqual(l_sentence_2, l_result_2)



    def test_add_single_word(self):
        d_words = {}
        expected_d_words = {
            TEST_WORD: {
                "word_count": 1,
                "files": {
                    TEST_FILE: [ TEST_SENTENCE ]
                }
            }
        }

        result_d_words = self._extractor._add_word(TEST_WORD, TEST_SENTENCE, d_words)

        self.assertEqual(result_d_words, expected_d_words)

    def test_add_multiple_words(self):
        d_words = {}
        # Testing that adding multiple of the same words
        expected_d_words = {
            TEST_WORD: {
                "word_count": 3,
                "files": {
                    TEST_FILE: [ TEST_SENTENCE, TEST_SENTENCE_2, TEST_SENTENCE ]
                }
            }
        }

        result_d_words = self._extractor._add_word(TEST_WORD, TEST_SENTENCE, d_words)
        result_d_words = self._extractor._add_word(TEST_WORD, TEST_SENTENCE_2, d_words)
        result_d_words = self._extractor._add_word(TEST_WORD, TEST_SENTENCE, d_words)

        self.assertEqual(result_d_words, expected_d_words)


