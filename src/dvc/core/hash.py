import hashlib
from pathlib import Path


class FileHasher():
    """
    Hash content of any given file
    """

    def md5(self,
            file_path: Path) -> str:
        """
        Extract content from a file and hash its output

        :param file_path: Pathlib Path
        :return: string
        """
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
