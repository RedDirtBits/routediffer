import pathlib


class Paths:
    """
     Static methods that point to various resources within the project folder

    Returns:
        path: root path and paths to various project resources
    """

    @staticmethod
    def root_path():
        return pathlib.Path.cwd()

    @staticmethod
    def file_exists(filename):
        return pathlib.Path(filename).exists()

    def create_file(filename):

        try:
            if not pathlib.Path(filename).is_file():
                pathlib.Path(filename).touch()

        except OSError as e:
            return f"Error: {e.strerror}"

    def delete_file(filename):
        
        try:
            if pathlib.Path(filename).exists():
                pathlib.Path(filename).unlink()
        except OSError as e:
            return f"Error: {e.strerror}"

    def create_folder(folder):

        try:
            if not pathlib.Path(folder).is_dir():
                pathlib.Path(folder).mkdir(parents=True, exist_ok=True)

        except OSError as e:
            return f"Error: {e.strerror}"

    def delete_folder(folder):

        try:
            if pathlib.Path(folder):
                pathlib.Path(folder).rmdir()

        except OSError as e:
            return f"Error: {e.strerror}"
