
from enum import IntEnum

class DIRECTION(IntEnum):
    """
        This class provides the direction in which the WCExtractorProcessor
        class will return the word array. If Descending is provided, then
        the returned array will be sorted in reverse order
    """
    ASCENDING = 0
    DESCENDING = 1

class WCExtractorProcessor:

    def __init__(self, limit=None, direction=DIRECTION.ASCENDING):
        self._limit = limit
        self._direction = direction

    def process_dict_wc_to_list(self, dict_words={}):

        list_words = self._convert_dict_wc_to_list_wc(dict_words)
        sorted_list_words = self._sort_list_wc(list_words)
        cropped_list_words = self._crop_list_wc(sorted_list_words)

        return cropped_list_words

    def _crop_list_wc(self, list_words):
        if self._limit:
            return list_words[:self._limit]

        return list_words

    def _sort_list_wc(self, list_words):
        return sorted(list_words,
                        key=lambda x: x["word_count"],
                        reverse=self._direction)

    def _convert_dict_wc_to_list_wc(self, d_words):
        list_words = []

        for key, value in d_words.items():
            words_obj = {
                "word": key,
                "word_count": value["word_count"],
                "files": value["files"]
            }
            list_words.append(words_obj)

        return list_words



