import os
import glob
import pathlib

ROOT_DIR = os.path.join(pathlib.Path(__file__).parent.parent.parent)

SOURCES_SEARCH = os.path.join(ROOT_DIR, "data", "raw", "*sources*.txt")
TEXT_FOLDERS_SEARCH = os.path.join(ROOT_DIR, "data", "raw", "*/")

sources_files = glob.glob(SOURCES_SEARCH)
text_folders = glob.glob(TEXT_FOLDERS_SEARCH)

for folder in text_folders:
    text_files = glob.glob(os.path.join(folder, "*.txt"))
