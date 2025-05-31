import os

class FileManager:
    TEMP_DIR = "temp"

    @staticmethod
    def ensure_temp_dir():
        if not os.path.exists(FileManager.TEMP_DIR):
            os.makedirs(FileManager.TEMP_DIR)

    @staticmethod
    def get_temp_path(filename):
        FileManager.ensure_temp_dir()
        return os.path.join(FileManager.TEMP_DIR, filename)

    @staticmethod
    def save_file(filename, data):
        path = FileManager.get_temp_path(filename)
        with open(path, 'wb') as f:
            f.write(data)
        return path

    @staticmethod
    def delete_file(filename):
        path = FileManager.get_temp_path(filename)
        if os.path.exists(path):
            os.remove(path)

    @staticmethod
    def delete_files(*filenames):
        for filename in filenames:
            FileManager.delete_file(filename)
