from wcpy import WCExtractorProcessor, DIRECTION

import unittest
from unittest.mock import MagicMock, call

class TestWCExtractorProcessor(unittest.TestCase):

    def test_convert(self):
        extractor = WCExtractorProcessor()

        l_result = extractor._convert_dict_wc_to_list_wc(T_WD)

        self.assertEqual(len(l_result), len(T_WD))

        # Make sure that all the objects in the list are the present
        for o_word in T_WD_LIST:
            found = None
            for result_o_word in l_result:
                if result_o_word["word"] == o_word["word"]:
                    found = result_o_word
                    break
            self.assertTrue(found)
            self.assertEqual(o_word, result_o_word)


    def test_convert_edge_cases(self):

        # Test empty dictionary
        extractor = WCExtractorProcessor()
        r_array = extractor._convert_dict_wc_to_list_wc({})

        self.assertEquals(r_array, [])

    def test_extractor_processor_integration(self):

        extractor = WCExtractorProcessor(direction=DIRECTION.ASCENDING)
        l_result = extractor.process_dict_wc_to_list(T_WD)

        self.assertEqual(l_result, T_WD_LIST_SORTED)


        extractor = WCExtractorProcessor(direction=DIRECTION.DESCENDING)
        l_result = extractor.process_dict_wc_to_list(T_WD)

        self.assertEqual(l_result, T_WD_LIST_REVERSED)


        extractor = WCExtractorProcessor(direction=DIRECTION.DESCENDING, limit=2)
        l_result = extractor.process_dict_wc_to_list(T_WD)

        self.assertEqual(l_result, T_WD_LIST_REVERSED[:2])


T_WD = {
    "word": {
        "word_count": 1,
        "files": {
            "TEST_FILE": [ "TEST_SENTENCE", "TEST_SENTENCE_2" ]
        }
    },
    "another": {
        "word_count": 5,
        "files": {
            "TEST_FILE": [ "TEST_SENTENCE", "TEST_SENTENCE_2" ]
        }
    },
    "final": {
        "word_count": 10,
        "files": {
            "TEST_FILE": [ "TEST_SENTENCE_2" ]
        }
    }
}

T_WD_LIST = [
    {
        "word": "word",
        "word_count": 1,
        "files": {
            "TEST_FILE": [ "TEST_SENTENCE", "TEST_SENTENCE_2" ]
        }
    },
    {
        "word": "final",
        "word_count": 10,
        "files": {
            "TEST_FILE": [ "TEST_SENTENCE_2" ]
        }
    },
    {
        "word": "another",
        "word_count": 5,
        "files": {
            "TEST_FILE": [ "TEST_SENTENCE", "TEST_SENTENCE_2" ]
        }
    }
]

T_WD_LIST_SORTED = [
    {
        "word": "word",
        "word_count": 1,
        "files": {
            "TEST_FILE": [ "TEST_SENTENCE", "TEST_SENTENCE_2" ]
        }
    },
    {
        "word": "another",
        "word_count": 5,
        "files": {
            "TEST_FILE": [ "TEST_SENTENCE", "TEST_SENTENCE_2" ]
        }
    },
    {
        "word": "final",
        "word_count": 10,
        "files": {
            "TEST_FILE": [ "TEST_SENTENCE_2" ]
        }
    }
]

T_WD_LIST_REVERSED = list(reversed(T_WD_LIST_SORTED))


