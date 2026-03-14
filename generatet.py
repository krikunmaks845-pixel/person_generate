import sys
import csv
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QLineEdit, QVBoxLayout, QScrollArea, QDialog, QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QLinearGradient, QColor
from person_generate.generate import generate_multiple


class VioletGradientWidget(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        gradient = QLinearGradient(0, 0, 0, self.height())

        gradient.setColorAt(0.0, QColor(15, 12, 41))
        gradient.setColorAt(0.3, QColor(48, 35, 74))
        gradient.setColorAt(0.6, QColor(95, 61, 118))
        gradient.setColorAt(1.0, QColor(146, 83, 161))

        painter.fillRect(self.rect(), gradient)

class ExportDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Export format")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout(self)

        self.csv_btn = QPushButton("CSV")
        self.json_btn = QPushButton("JSON")

        layout.addWidget(self.csv_btn)
        layout.addWidget(self.json_btn)

        self.csv_btn.clicked.connect(lambda: self.done(1))
        self.json_btn.clicked.connect(lambda: self.done(2))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Human Generator")
        self.setGeometry(100, 100, 1300, 900)

        self.violet_widget = VioletGradientWidget()
        self.setCentralWidget(self.violet_widget)
        button = QPushButton("Export", self.violet_widget)
        button.move(10, 10)
        button.show()
        button.clicked.connect(self.export_clicked)

        self.count_input = QLineEdit("100", self.violet_widget)
        self.count_input.move(950, 710)
        self.count_input.show()
        self.count_input.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.count_input.setStyleSheet("""
                QLineEdit {
                    background-color: rgba(20, 15, 45, 80);
                    border-radius: 12px;
                }

                QLineEdit QWidget {
                    background: transparent;
                    color: #E6DFFF;
                }
                """)
        button2 = QPushButton("Згенерувати", self.violet_widget)
        button2.move(968, 735)
        button2.show()

        scroll = QScrollArea(self.violet_widget)
        scroll.setWidgetResizable(True)

        content = QWidget(self.violet_widget)
        content.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        scroll.setStyleSheet("""
        QScrollArea {
            background-color: rgba(20, 15, 45, 80);
            border-radius: 12px;
        }

        QScrollArea QWidget {
            background: transparent;
            color: #E6DFFF;
        }
        """)

        self.results_layout = QVBoxLayout(content)

        scroll.setWidget(content)
        scroll.move(700, 100)

        scroll.setMinimumWidth(600)
        scroll.setMinimumHeight(600)
        scroll.show()



        self.generate_button = button2
        self.generate_button.clicked.connect(self.generate_clicked)

    def clear_results(self):
        while self.results_layout.count():
            item = self.results_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def generate_clicked(self):
        text = self.count_input.text()
        if not text:
            return

        count = int(text)
        people = generate_multiple(count)
        self.clear_results()
        self.generated_people = people

        for person in people:
            label = QLabel(
                f"{person['name']} | {person['age']} | {person['email']}"
            )
            label.setStyleSheet("color: #E6DFFF; font-size: 14px;")
            self.results_layout.addWidget(label)

    def export_clicked(self):
        if not hasattr(self, "generated_people"):
            return
        dialog = ExportDialog()
        result = dialog.exec()

        if result == 1:
            self.export_csv()
        elif result == 2:
            self.export_json()

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save CSV", "", "CSV Files (*.csv)"
            )

        if not path:
            return

        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file, fieldnames=["name", "age", "email"]
                )
            writer.writeheader()
            writer.writerows(self.generated_people)

    def export_json(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save JSON", "", "JSON Files (*.json)"
            )

        if not path:
                return

        with open(path, "w", encoding="utf-8") as file:
                json.dump(self.generated_people, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())