from wcpy import WCExtractorFile

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

    def test_wc_extractor_file_end_to_end_with_files(self):

        extractor = WCExtractorFile(ACTUAL_FILE)
        result_wc = {}
        extractor.extract_wc_from_file(result_wc)

        # Make sure result is not empty
        self.assertTrue(result_wc)

        for o_words in result_wc:

            word_count = result_wc[o_words]["word_count"]
            total_sentences = 0

            o_words_f = result_wc[o_words]["files"]
            for file in o_words_f:
                total_sentences += len(o_words_f[file])

            # Make sure that all the word counts are equal or greater
            # than the number of sentences
            self.assertGreaterEqual(word_count, total_sentences)



    def test_wc_extractor_file_integration_filters(self):

        filter_words=[TEST_WORD]

        openMock = MagicMock()
        openMock.return_value.__enter__.return_value = [TEST_SENTENCE, TEST_SENTENCE_2]
        extractor = WCExtractorFile(TEST_FILE, file_opener=openMock, filter_words=filter_words)

        result_d_words = {}
        expected_d_words = {
            TEST_WORD: {
                "word_count": 2,
                "files": {
                    TEST_FILE: [ TEST_SENTENCE, TEST_SENTENCE_2 ]
                }
            }
        }

        extractor.extract_wc_from_file(result_d_words)
        self.assertEqual(result_d_words, expected_d_words)


    def test_wc_extractor_file_end_to_end_integration(self):

        openMock = MagicMock()
        openMock.return_value.__enter__.return_value = [TEST_SENTENCE, TEST_SENTENCE_2]
        extractor = WCExtractorFile(TEST_FILE, file_opener=openMock, filter_words=[])

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

        extractor.extract_wc_from_file(result_dw)

        self.assertEqual(result_dw, expected_dw)


    def test_extract(self):

        openMock = MagicMock()
        openMock.return_value.__enter__.return_value = [TEST_SENTENCE, TEST_SENTENCE_2]
        extractor = WCExtractorFile(TEST_FILE, file_opener=openMock, filter_words=[])

        add_word_mock = MagicMock()
        extractor._add_word = add_word_mock

        line_to_words_mock = MagicMock(return_value=TEST_SENTENCE)
        extractor._split_line = line_to_words_mock

        result_dw = {}
        extractor.extract_wc_from_file(result_dw)

        expected_line_calls = [call(TEST_SENTENCE), call(TEST_SENTENCE_2)]

        openMock.assert_called_once_with(TEST_FILE)
        line_to_words_mock.assert_has_calls(expected_line_calls)


    def test_line_to_words(self):

        extractor = WCExtractorFile(TEST_FILE, filter_words=[])

        # Test sentence with no symbols
        sentence = "This no symbols"
        l_sentence = ["this", "no", "symbols"]
        l_result = extractor._split_line(sentence)

        self.assertEqual(l_sentence, l_result)

        # Testing more complex sentences with symbols
        sentence_2 = "This, Is. Another; SeNtence... and-works? 1010"
        l_sentence_2 = ["this", "is", "another", "sentence", "and-works", "1010"]
        l_result_2 = extractor._split_line(sentence_2)

        self.assertEqual(l_sentence_2, l_result_2)


    def test_split_line_with_filters(self):

        filter_words=[TEST_WORD]
        extractor = WCExtractorFile(TEST_FILE, filter_words=filter_words)

        result = extractor._split_line(TEST_SENTENCE)

        self.assertEqual(result, [TEST_WORD])


        filter_words=[TEST_WORD]
        extractor = WCExtractorFile(TEST_FILE, filter_words=filter_words)

        result = extractor._split_line(TEST_SENTENCE_2)

        self.assertEqual(result, [TEST_WORD])


    def test_add_single_word(self):

        extractor = WCExtractorFile(TEST_FILE, filter_words=[])

        result_d_words = {}
        expected_d_words = {
            TEST_WORD: {
                "word_count": 1,
                "files": {
                    TEST_FILE: [ TEST_SENTENCE ]
                }
            }
        }

        extractor._add_word(TEST_WORD, TEST_SENTENCE, result_d_words)

        self.assertEqual(result_d_words, expected_d_words)

    def test_add_multiple_words(self):

        extractor = WCExtractorFile(TEST_FILE, filter_words=[])

        result_d_words = {}
        # Testing that adding multiple of the same words
        expected_d_words = {
            TEST_WORD: {
                "word_count": 3,
                "files": {
                    TEST_FILE: [ TEST_SENTENCE, TEST_SENTENCE_2, TEST_SENTENCE ]
                }
            }
        }

        extractor._add_word(TEST_WORD, TEST_SENTENCE, result_d_words)
        extractor._add_word(TEST_WORD, TEST_SENTENCE_2, result_d_words)
        extractor._add_word(TEST_WORD, TEST_SENTENCE, result_d_words)

        self.assertEqual(result_d_words, expected_d_words)


