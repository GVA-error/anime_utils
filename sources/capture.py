import os
import keyboard
import pyperclip
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QPen, QIcon, QAction
from PyQt6.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu
from configparser import ConfigParser

from paddleocr import PaddleOCR

import sys

BORDER = 20
PEN_BORDER = 30
os.environ["FLAGS_use_mkldnn"] = "0"

class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self._resizing = False
        self._last_button = None
        self._resize_edges = None
        self._start_pos = None
        self._start_geometry = None
        self._handling = False
        # Default settings
        self.capture_hotkey = "alt"
        self.exit_hotkey = "f11"
        self.language = "japan"
        self.start_hidden = True

        self.read_config()
        self.add_tray()
        self.add_square()
        self.add_ocr()
        self.add_hotkeys()


    def add_hotkeys(self):
        keyboard.add_hotkey(self.exit_hotkey, lambda : sys.exit(0))
        keyboard.add_hotkey(self.capture_hotkey, self.make_screen)

    def add_ocr(self):
        self.ocr = PaddleOCR(
            lang="japan",
            device="cpu",
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=True,
            text_detection_model_name="PP-OCRv5_mobile_det",
            text_recognition_model_name="PP-OCRv5_mobile_rec",
        )

    def add_square(self):
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(400, 300)

    def add_tray(self):
        tray = QSystemTrayIcon(self)
        tray.setIcon(QIcon("resources/icon.ico"))

        menu = QMenu()

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(QApplication.quit)

        menu.addAction(exit_action)

        tray.setContextMenu(menu)
        tray.show()
        self.tray = tray

    def read_config(self):
        config = ConfigParser()
        config.read("config.ini")
        self.capture_hotkey = config["hotkeys"]["capture"]
        self.exit_hotkey = config["hotkeys"]["exit"]
        self.language = config["ocr"]["language"]
        self.start_hidden = config.getboolean("app", "start_hidden")

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen()
        pen.setWidth(PEN_BORDER)
        painter.setPen(pen)
        painter.drawRect(self.rect())

    def make_screen(self):
        if self._handling:
            return
        if self._resizing:
            return
        self._handling = True
        screen = QApplication.primaryScreen()
        pixmap = screen.grabWindow(
            0,
            self.x(),
            self.y(),
            self.width(),
            self.height()
        )
        pixmap.save("capture.png")
        result = self.ocr.predict("capture.png")
        text = []
        for line in result:
            text.append(' '.join(line["rec_texts"]))
        cb_text = '\n'.join(text)
        pyperclip.copy(cb_text)
        self._handling = False
        print(text)


    def _get_edges(self, pos):
        x = pos.x()
        y = pos.y()

        left = x <= BORDER
        right = x >= self.width() - BORDER
        top = y <= BORDER
        bottom = y >= self.height() - BORDER

        return left, right, top, bottom

    def mousePressEvent(self, event):
        if event.button() not in [Qt.MouseButton.LeftButton, Qt.MouseButton.RightButton]:
            return
        self._last_button = event.button()

        edges = self._get_edges(event.pos())

        if any(edges):
            self._resizing = True
            self._resize_edges = edges
            self._start_pos = event.globalPosition().toPoint()
            self._start_geometry = self.geometry()

    def mouseMoveEvent(self, event):
        if not self._resizing:
            return

        delta = event.globalPosition().toPoint() - self._start_pos

        left, right, top, bottom = self._resize_edges

        rect = QRect(self._start_geometry)

        if self._last_button == Qt.MouseButton.RightButton:
            rect.setLeft(rect.left() + delta.x())
            rect.setRight(rect.right() + delta.x())
            rect.setTop(rect.top() + delta.y())
            rect.setBottom(rect.bottom() + delta.y())
        else:
            if left:
                rect.setLeft(rect.left() + delta.x())
            if right:
                rect.setRight(rect.right() + delta.x())
            if top:
                rect.setTop(rect.top() + delta.y())
            if bottom:
                rect.setBottom(rect.bottom() + delta.y())

        min_width = 50
        min_height = 50

        if rect.width() >= min_width and rect.height() >= min_height:
            self.setGeometry(rect)

    def mouseReleaseEvent(self, event):
        self._resizing = False
        self._resize_edges = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = Overlay()
    overlay.show()
    sys.exit(app.exec())