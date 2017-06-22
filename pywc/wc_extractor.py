
from pywc.wc_extractor_processor import WCExtractorProcessor, DIRECTION
from pywc.wc_extractor_file import WCExtractorFile

import glob, os

class PathNotValidException(Exception):
    def __init__(self, path):
        Exception.__init__(self, "Path provided is not valid: " + str(path))

class WCExtractor:

    def __init__(self, limit=None, direction=DIRECTION.ASCENDING,
                    extractor_file=WCExtractorFile, dict_words={},
                    extractor_processor=WCExtractorProcessor, file_extension=".txt"):

        self._dict_words = dict_words
        self._file_extension = file_extension
        self._limit = limit
        self._direction = direction
        self._extractor_processor = extractor_processor
        self._extractor_file = extractor_file


    def extract_wc_and_display(self, paths):

        result_dict = self._dict_words

        self._check_all_root_paths_valid(paths)
        all_file_paths = self._extract_all_paths(paths)

        for path in all_file_paths:
            extractor_file = self._extractor_file(path)
            extractor_file.extract_wc_from_file(result_dict)

        extractor_processor = self._extractor_processor(limit=self._limit, direction=self._direction)
        result_list = extractor_processor.process_dict_wc_to_list(result_dict)

        self._display_results(result_list)


    def _check_all_root_paths_valid(self, paths):
        for path in paths:
            if not os.path.exists(path):
                raise PathNotValidException(path)

    def _extract_all_paths(self, paths):
        """
            Traverses all folders and subfolders recurisvely, and expands the paths
                the paths must be valid, and can be checked with the
                _check_all_root_paths_valid funciton. If they don't exist it will be
                skipped.
        """
        all_file_paths = []
        for path in paths:
            if not os.path.exists(path):
                continue


            abs_path = os.path.abspath(path)

            if os.path.isdir(abs_path):
                sub_paths = self._expand_folder_paths(abs_path)
                all_file_paths.extend(sub_paths)
            else:
                all_file_paths.append(abs_path)


        return all_file_paths


    def _expand_folder_paths(self, folder_path):
        all_sub_paths = []

        if not os.path.exists(folder_path):
            return all_sub_paths

        glob_extension = "**/*" + self._file_extension
        glob_path = os.path.join(folder_path, glob_extension)

        for sub_path in glob.iglob(glob_path, recursive=True):
            all_sub_paths.append(sub_path)

        return all_sub_paths


    def _display_results(self, list_wc):

        rows = []
        for obj_word in list_wc:
            word = obj_word["word"]
            wc = str(obj_word["word_count"])
            files = []
            sentences = []

            for file_name in obj_word["files"]:
                files.append(file_name.split("/")[-1])
                file_sentences = obj_word["files"][file_name]

                for sentence in file_sentences:
                    sentences.append(sentence)

            rows.append([word, wc, ", ".join(files)])

        widths = [ len(max(columns, key=len)) for columns in zip(*rows) ]

        header, data = rows[0], rows[1:]
        print(
            ' | '.join( format(title, "%ds" % width) for width, title in zip(widths, header) )
            )

        print( '-+-'.join( '-' * width for width in widths ) )

        for row in data:
            print(" | ".join( format(cdata, "%ds" % width) for width, cdata in zip(widths, row) ))



