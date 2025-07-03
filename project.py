from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QCheckBox, QLineEdit,
    QSpinBox, QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog, QSpacerItem, QSizePolicy, QGridLayout, QFrame
)
from PyQt5.QtCore import Qt
import sys

class TrendDataExtractor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trend Data Extraction")
        self.setGeometry(100, 100, 1300, 550)

        self.setStyleSheet("""
            QWidget {
                font-family: Arial;
                font-size: 11px;
                          
            }

            QLabel {
                font-weight: bold;
                margin-right: 4px;
                          
            }

            QComboBox, QLineEdit, QSpinBox {
              
                border-radius: 3px;
                border: 1px solid #aaa;
                min-width: 30px;
                font-size: 11px;
                margin-top: 2px;
                margin-bottom: 2px;
            }

            QCheckBox {
                margin-left: 0px;
                margin-right: 6px;
            }

            QPushButton {
                padding: 3px 8px;
                border-radius: 4px;
                background-color: #4472C4;
                color: white;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #365F91;
            }

            QPushButton#IconButton {
                background-color: transparent;
                border: none;
                font-size: 16px;
            }

            QLineEdit {
                min-width: 100px;
            }

            QLabel#TitleLabel {
                background-color: #f7bd65;
                border-top: 2px solid #888;
                border-bottom: 2px solid #888;
                border-left: none;
                border-right: none;
                border-radius: 0px;
            }

            QFrame#FinalFrame {
                background-color: #f7bd65;
                border-top: 2px solid #888;
                border-bottom: 2px solid #888;
                border-left: none;
                border-right: none;
                border-radius: 0px;
            }
        """)

        wrapper_layout = QVBoxLayout()
        main_layout = QVBoxLayout()

        title_frame = QFrame()
        title_layout = QVBoxLayout()
        title = QLabel("Trend Data Extraction")
        title.setObjectName("TitleLabel")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 6px;")
        title_layout.addWidget(title)
        title_frame.setLayout(title_layout)
        main_layout.addWidget(title_frame)

        line2_layout = QHBoxLayout()
        line2_layout.setSpacing(8)

        self.system_combo = QComboBox()
        self.system_combo.addItems(["A", "B"])
        line2_layout.addWidget(QLabel("System:"))
        line2_layout.addWidget(self.system_combo)

        self.sublist_combo = QComboBox()
        self.sublist_combo.addItems(["Sublist 1", "Sublist 2"])
        line2_layout.addWidget(QLabel("Sublist:"))
        line2_layout.addWidget(self.sublist_combo)

        self.exclude_sparse_cb = QCheckBox("Exclude Spares")
        line2_layout.addWidget(self.exclude_sparse_cb)

        self.all_tags_cb = QCheckBox()
        line2_layout.addWidget(QLabel("All Tags:"))
        line2_layout.addWidget(self.all_tags_cb)

        self.select_tags_cb = QCheckBox()
        line2_layout.addWidget(QLabel("Select Tags:"))
        line2_layout.addWidget(self.select_tags_cb)

        self.trend_tags_combo = QComboBox()
        self.trend_tags_combo.addItems(["0 tag(s) selected"])
        line2_layout.addWidget(QLabel("Trend Tags:"))
        line2_layout.addWidget(self.trend_tags_combo)

        self.filter_tag_combo = QComboBox()
        self.filter_tag_combo.addItems(["Filter A", "Filter B"])
        line2_layout.addWidget(QLabel("Filter Tag:"))
        line2_layout.addWidget(self.filter_tag_combo)

        main_layout.addLayout(line2_layout)

        datetime_layout = QVBoxLayout()
        grid = QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(5)
        grid.setContentsMargins(0, 0, 0, 0)

        labels = ["Day", "Month", "Year", "Hour", "Minute", "Second"]
        for col, label in enumerate(labels):
            lbl = QLabel(label)
            lbl.setAlignment(Qt.AlignCenter)
            grid.addWidget(lbl, 0, col + 1)
        grid.addWidget(QLabel("To"), 0, len(labels) + 1)
        for col, label in enumerate(labels):
            lbl = QLabel(label)
            lbl.setAlignment(Qt.AlignCenter)
            grid.addWidget(lbl, 0, len(labels) + col + 2)
       

        grid.addWidget(QLabel("From:"), 1, 0)
        for col, label in enumerate(labels):
            widget = self.create_widget_for_time(label)
            grid.addWidget(widget, 1, col + 1)

        grid.addWidget(QLabel("To:"), 1, len(labels) + 1)
        for col, label in enumerate(labels):
            widget = self.create_widget_for_time(label)
            grid.addWidget(widget, 1, len(labels) + col + 2)

        grid.addWidget(QLineEdit("Deployment version:"), 0, len(labels)*2 + 2)
        
        datetime_layout.addLayout(grid)
        main_layout.addLayout(datetime_layout)

        final_frame = QFrame()
        final_frame.setObjectName("FinalFrame")
        final_layout = QHBoxLayout()

        final_layout.addWidget(QLabel("Live:"))
        self.live_combo = QComboBox()
        self.live_combo.addItems(["Live A", "Live B"])
        final_layout.addWidget(self.live_combo)

        final_layout.addWidget(QLabel("Backup:"))
        self.backup_combo = QComboBox()
        self.backup_combo.addItems(["Backup A", "Backup B"])
        final_layout.addWidget(self.backup_combo)

        final_layout.addWidget(QLabel("DBPath:"))
        self.dbpath_button = QPushButton("📁")
        self.dbpath_button.setObjectName("IconButton")
        self.dbpath_button.setFixedWidth(30)
        self.dbpath_button.clicked.connect(self.select_db_folder)
        self.dbpath_line = QLineEdit()

        final_layout.addWidget(self.dbpath_button)
        final_layout.addWidget(self.dbpath_line)

        final_layout.addWidget(QLabel("OutputPath:"))
        self.output_button = QPushButton("📁")
        self.output_button.setObjectName("IconButton")
        self.output_button.setFixedWidth(30)
        self.output_button.clicked.connect(self.select_output_path)
        self.outputpath_line = QLineEdit()

        final_layout.addWidget(self.output_button)
        final_layout.addWidget(self.outputpath_line)

        self.extract_button = QPushButton("Extract")
        final_layout.addWidget(self.extract_button)

        final_frame.setLayout(final_layout)
        main_layout.addWidget(final_frame)

        main_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        wrapper_layout.addLayout(main_layout)
        self.setLayout(wrapper_layout)

    def create_widget_for_time(self, label):
        if label == "Month":
            combo = QComboBox()
            combo.setFixedWidth(60)
            combo.addItems(["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"])
            return combo
        elif label == "Year":
            spin = QSpinBox()
            spin.setFixedWidth(65)
            spin.setRange(2000, 2100)
            spin.setValue(2025)
            return spin
        elif label == "Day":
            spin = QSpinBox()
            spin.setFixedWidth(45)
            spin.setRange(1, 31)
            return spin
        else:
            spin = QSpinBox()
            spin.setFixedWidth(45)
            spin.setRange(0, 59)
            return spin

    def select_db_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select DB Folder")
        if folder:
            self.dbpath_line.setText(folder)

    def select_output_path(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Select Output File", "", "All Files (*)")
        if file_path:
            self.outputpath_line.setText(file_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrendDataExtractor()
    window.show()
    sys.exit(app.exec_())
