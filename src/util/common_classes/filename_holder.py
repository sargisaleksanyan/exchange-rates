import os

MAIN_FOLDER = os.path.abspath('')
TOOLS_FOLDER_NAME = 'tools'


def make_file_path_for_tool(file: str):
    # return os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', TOOLS_FOLDER_NAME + '/', file)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', TOOLS_FOLDER_NAME + '/', file)


class FileNames:
    proxyFileName = make_file_path_for_tool('proxy.txt')
