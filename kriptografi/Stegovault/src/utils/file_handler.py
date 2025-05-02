def read_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

def write_file(file_path, data):
    with open(file_path, 'wb') as file:
        file.write(data)

def is_valid_file_type(file_path):
    valid_extensions = ['.pdf', '.docx']
    return any(file_path.endswith(ext) for ext in valid_extensions)

def validate_file_path(file_path):
    import os
    return os.path.isfile(file_path) and is_valid_file_type(file_path)