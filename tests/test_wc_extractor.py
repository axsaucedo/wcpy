from pywc.wc_extractor import WCExtractor
from pywc.wc_extractor_processor import WCExtractorProcessor, DIRECTION

import unittest
from unittest.mock import MagicMock, call

class TestWCExtractorFile(unittest.TestCase):

    def test_wc_extractor_file_end_to_end_with_files(self):

        extractor = WCExtractor(direction=DIRECTION.DESCENDING, limit=1)
        extractor.extract_wc_and_display(["tests/test_data"])