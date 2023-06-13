import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit
from PyQt5.QtCore import Qt
from urllib.parse import urlparse
import platform

class DragAndDrop(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Drag and Drop')
        self.resize(300, 150)
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        for url in urls:
            file_path = url.toLocalFile()
            if file_path.endswith(".url"):
                extracted_url = self.extract_url_from_url_file(file_path)
                if extracted_url:
                    self.append_to_file("urls.txt", extracted_url)
            else:
                self.append_to_file("urls.txt", url.toString())
        event.acceptProposedAction()

    def extract_url_from_url_file(self, file_path):
        if platform.system() == "Windows":
            with open(file_path, "r") as infile:
                for line in infile:
                    if line.startswith('URL='):
                        url = line[4:].strip()
                        return url
        elif platform.system() == "Darwin":
            # macOS specific code to extract URL from .webloc files
            with open(file_path, "r") as infile:
                for line in infile:
                    if line.startswith('<string>'):
                        url = line.strip("<string>").strip("</").strip()
                        return url
        elif platform.system() == "Linux":
            # Linux specific code to extract URL from .desktop files
            with open(file_path, "r") as infile:
                for line in infile:
                    if line.startswith("URL="):
                        url = line.strip("URL=").strip()
                        return url
        return None

    def append_to_file(self, filename, content):
        with open(filename, "a") as outfile:
            outfile.write(content + ",\n")

def main():
    app = QApplication(sys.argv)
    demo = DragAndDrop()
    demo.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
