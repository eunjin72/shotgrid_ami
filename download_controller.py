import sys

from PySide2 import *
from PySide2.QtWidgets import *

from ami_handler import ShotgunAction
from download_view import DownloaderView


class DownloaderController(DownloaderView):
    def __init__(self):
        super().__init__()
        self.model = ShotgunAction(sys.argv[1])

        # button clicked event
        self.btn_browse.clicked.connect(self.btn_browse_clicked)
        self.btn_download.clicked.connect(self.btn_download_clicked)
        self.btn_cancel.clicked.connect(self.btn_cancel_clicked)

    def btn_browse_clicked(self):
        dialog = QFileDialog()
        dialog.setDirectory(r'C:\shotgrid')
        self.dir_path = dialog.getExistingDirectory()
        self.line_path.setText(self.dir_path)

    def btn_download_clicked(self):
        self.model.download(self.dir_path)
        self.message_box()

    def btn_cancel_clicked(self):
        self.close()


if __name__ == "__main__":
    app = QApplication()
    dc = DownloaderController()
    sys.exit(app.exec_())