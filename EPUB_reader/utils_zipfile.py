import zipfile

import utils_log


class zipfile_shell:
    def __init__(self, zip_file_name, file_name):
        self.zip_file_name = zip_file_name
        self.zip_file = zipfile.ZipFile(self.zip_file_name)
        self.file = self.zip_file.open(file_name)

    def __enter__(self):
        return self.file

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.file.close()
        self.zip_file.close()
        if exc_tb is not None:
            utils_log.get_logger(__name__).log(40, exc_value)
