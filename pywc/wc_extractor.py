
from pywc.wc_extractor_processor import WCExtractorProcessor, DIRECTION
from pywc.wc_extractor_file import WCExtractorFile

import glob, os

class PathNotValidException(Exception):
    def __init__(self, path):
        Exception.__init__(self, "Path provided is not valid: " + str(path))

class InvalidColumnException(Exception):
    def __init__(self, col):
        Exception.__init__(self, "Column provided is not valid: " + str(col) + ". Valid columns are: " + str(VALID_COLUMNS))

VALID_COLUMNS = ["word", "count", "files", "sentences"]
VALID_COLUMNS_SET = set(VALID_COLUMNS)


class WCExtractor:

    def __init__(self, limit=None, direction=DIRECTION.ASCENDING,
                    extractor_file=WCExtractorFile, filter_words=[],
                    extractor_processor=WCExtractorProcessor, file_extension="txt"):

        # TODO: Check for valid file extension
        self._file_extension = file_extension
        self._limit = limit
        self._direction = direction
        self._extractor_processor = extractor_processor
        self._extractor_file = extractor_file
        self._filter_words = filter_words


    def generate_wc_dict(self, paths):

        result_dict = {}

        self._check_all_root_paths_valid(paths)
        all_file_paths = self._extract_all_paths(paths)

        for path in all_file_paths:
            extractor_file = self._extractor_file(path, filter_words=self._filter_words)
            extractor_file.extract_wc_from_file(result_dict)

        return result_dict


    def generate_wc_list(self, paths):

        dict_wc = self.generate_wc_dict(paths)

        extractor_processor = self._extractor_processor(limit=self._limit, direction=self._direction)
        result_list = extractor_processor.process_dict_wc_to_list(dict_wc)

        return result_list


    def display_wc_table(self, paths, char_limit=50, columns=None):

        list_wc = self.generate_wc_list(paths)
        headers, rows = self._generate_table(list_wc, char_limit=char_limit, columns=columns)

        self._print_table_ascii(headers, rows)


    def _check_all_root_paths_valid(self, paths):
        for path in paths:
            if not os.path.exists(path):
                raise PathNotValidException(path)

            # TODO: Add support for globbed files
            if "*" in path:
                raise PathNotValidException("Globbed paths (*) are not supported, please just select the folder: " + str(path))


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

        glob_extension = "**/*." + self._file_extension
        glob_path = os.path.join(folder_path, glob_extension)

        for sub_path in glob.iglob(glob_path, recursive=True):
            all_sub_paths.append(sub_path)

        return all_sub_paths


    def _generate_table(self, list_wc, char_limit=50, columns=None):

        # We first check that the columns are valid
        if columns and len(columns):
            columns = [ col.lower() for col in columns ]
            for col in columns:
                if col not in VALID_COLUMNS_SET:
                    raise InvalidColumnException(col)

        # Creating a printable set of rows
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

            # Format documents and sentences for printing
            str_files = ", ".join(files)
            str_sentences = ", ".join(sentences)

            # Truncate all the inputs to the char_limit
            # TODO: This could be made more efficient by using
            #   'continue' in the loop when char_limit is exceeded
            if char_limit:
                if char_limit < 5:
                    print("WARNING: Minimum char limit must be above 5. Changing to 5.")
                    # We substract 3 to add the '...' truncations
                    char_trunc = char_limit - 3
                str_files = str_files[:char_limit] + "..." if len(str_files) > char_limit else str_files
                str_sentences = str_sentences[:char_limit] + "..." if len(str_sentences) > char_limit else str_sentences

            # Note: if column becomes longer, it will be necessary
            #   to create a set to improve time complexity
            if columns and len(columns):
                row_cols = []
                if VALID_COLUMNS[0] in columns:
                    row_cols.append(word)
                if VALID_COLUMNS[1] in columns:
                    row_cols.append(wc)
                if VALID_COLUMNS[2] in columns:
                    row_cols.append(str_files)
                if VALID_COLUMNS[3] in columns:
                    row_cols.append(str_sentences)

                rows.append(row_cols)
            else:
                rows.append([ word, wc, str_files, str_sentences ])

        # We define the headers
        headers = columns if columns and len(columns) else VALID_COLUMNS
        print(headers)
        print(rows)
        return headers, rows

    def _print_table_ascii(self, headers, rows):

        # Here, get the max_widths of all the data
        #   To do this, first transpose / group all strings by columns.
        #   Then get the strings with the most number of chars in each columns.
        #   Finally count the number of characters in the longest string.
        #   Those are our max_widths
        max_widths = [ len(max(columns, key=len)) for columns in zip(*rows, headers) ]

        # First we create a row divider
        #   Print a number of dashes relative to the width of each column
        #   by using the * python operator.
        #   The separator of each is also 3 characters long, same as above
        print(' ', '-+-'.join( '-' * width for width in max_widths ) )

        # Now print the headers
        #   Using Python's format functionality, as it allows us to specify a
        #   standard width, which will make our table consistent and symmetric
        #   In this case, our width is 'max_width', and we print the title within that
        #   and separate each of the strings by a pipe symbol '|'
        print('|',' | '.join( format(title, "%ds" % max_width) for max_width, title in zip(max_widths, headers) ), '|')

        # Another row divider
        print('|', '-+-'.join( '-' * width for width in max_widths ) )

        # Now print all the data
        #   This uses a similar approach as the print map used above
        #   when printing the headers
        for row in rows:
            print('|', " | ".join( format(cdata, "%ds" % width) for width, cdata in zip(max_widths, row) ), '|')

        # Final row divider
        print(' ', '-+-'.join( '-' * width for width in max_widths ) )


