import sys
from os import path, scandir, makedirs, replace

file_types = {'Documents': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx', '.doc', '.odt', '.xls', '.csv', '.eml', '.rtf'],
              'Images': ['.jpg', '.jpeg', '.png', '.gif'],
              'Videos': ['.mp4', '.avi', '.mov', '.mpeg', '.mpg'],
              'Audio': ['.mp3', '.wav', '.wma', '.midi', '.mid'],
              'Virtual': ['.ova', '.vdi', '.iso'],
              'Packets': ['.zip', '.rar', '.tar', '.7z', '.gz', '.bin'],
              'eBooks': ['.epub', '.mobi'],
              'Code': ['.html', '.py', '.java', '.cpp', '.c', '.cs', '.php', '.swift', '.css', '.js', '.asm', '.jnlp', '.xml', '.sql']
              }


def distrFiles(sourceDir):
    for file in scandir(sourceDir):
        if file.is_file():
            fileExt = path.splitext(file.name)[1].lower()
            for dirName, extensions in file_types.items():
                if fileExt in extensions:
                    directory = path.join(sourceDir, dirName)
                    makedirs(directory, exist_ok=True)
                    newPath = path.join(directory, file.name)
                    replace(file.path, newPath)


def main():
    if len(sys.argv) > 2 or len(sys.argv) == 1:
        raise Exception("The usage must be: fileOrganizer.py /path/to/dir")
    elif not path.exists(sys.argv[1]):
        raise Exception("Path to directory doesn't exist")
    sourceDir = sys.argv[1]
    distrFiles(sourceDir)


if __name__ == "__main__":
    main()
