import pathlib


class Paths:
    """
     Various methods for working with paths within the project folder

        root_path: returns the root path to the working folder

        file_exists: returns True or False depeding on the existence of the
        filename provided
    """

    @staticmethod
    def root_path():
        return pathlib.Path.cwd()

    @staticmethod
    def file_exists(filename):
        return pathlib.Path(filename).exists()

    def create_file(filename):
        """
        create_file summary:
            Creates a file of the filename provided

        Args:
            filename (str): The file name to be created
        """

        try:
            if not pathlib.Path(filename).is_file():
                pathlib.Path(filename).touch()

        except OSError as e:
            return f"Error: {e.strerror}"

    def delete_file(filename):
        """
        delete_file summary:
            Deletes a file of the filename provided if it exists

        Args:
            filename (str): The file name to be deleted
        """
        
        try:
            if pathlib.Path(filename).exists():
                pathlib.Path(filename).unlink()
        except OSError as e:
            return f"Error: {e.strerror}"

    def create_folder(folder):
        """
        create_folder summary:
            Creates a folder of the name provided

        Args:
            folder (str): The folder name to be created
        """

        try:
            if not pathlib.Path(folder).is_dir():
                pathlib.Path(folder).mkdir(parents=True, exist_ok=True)

        except OSError as e:
            return f"Error: {e.strerror}"

    def delete_folder(folder):
        """
        delete_folder summary:
            Deletes/Removes a folder of the name provided if it exists

        Args:
            folder (str): The folder name to be created
        """

        try:
            if pathlib.Path(folder):
                pathlib.Path(folder).rmdir()

        except OSError as e:
            return f"Error: {e.strerror}"
