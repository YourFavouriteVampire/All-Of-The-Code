import sys
import os
import pandas as pd
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QFileDialog,
    QVBoxLayout, QWidget, QSizePolicy, QToolBar, QDialog, QHBoxLayout, QScrollArea, QSplitter
)

class AuthManager:
    @staticmethod
    def authenticate(username, password):
        return username == "root" and password == "root"

class EntryCard(QLabel):
    def __init__(self, entry_info):
        super().__init__()
        self.setStyleSheet("background-color: lightblue; font-size: 14px; padding: 10px; border: 1px solid gray;")
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(200, 350)

        image_path = entry_info.get('image_path', 'default_image.png')
        pixmap = QPixmap(image_path).scaledToHeight(200)
        self.setPixmap(pixmap)

        text_info = self.format_entry_info(entry_info)
        text_label = QLabel(text_info)
        text_label.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        # Use a QSplitter to divide the EntryCard into two sections
        splitter = QSplitter(Qt.Vertical)

        # Create labels for the image and text
        image_label = QLabel()
        image_label.setPixmap(pixmap)

        # Add the image label to the top section
        splitter.addWidget(image_label)

        # Add a stretch to create the 2:1 ratio
        splitter.setSizes([2, 1])

        # Add the text label to the bottom section
        splitter.addWidget(text_label)

        # Set the layout of the EntryCard to QVBoxLayout
        layout = QVBoxLayout(self)
        layout.addWidget(splitter)

    def format_entry_info(self, entry_info):
        return f"ID: {entry_info['id']}\n" \
               f"Name: {entry_info['name']}\n" \
               f"Phone: {entry_info['phone']}\n" \
               f"CNIC: {entry_info['cnic']}\n" \
               f"Gender: {entry_info['gender']}\n" \
               f"DOB: {entry_info['dob']}"


class EntryInputDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Enter Entry Information")
        self.setFixedSize(500, 650)

        layout = QVBoxLayout(self)

        self.name_input = QLineEdit()
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)

        self.phone_input = QLineEdit()
        layout.addWidget(QLabel("Phone Number:"))
        layout.addWidget(self.phone_input)

        self.cnic_input = QLineEdit()
        layout.addWidget(QLabel("CNIC Number:"))
        layout.addWidget(self.cnic_input)

        self.gender_input = QLineEdit()
        layout.addWidget(QLabel("Gender:"))
        layout.addWidget(self.gender_input)

        self.dob_input = QLineEdit()
        layout.addWidget(QLabel("Date of Birth:"))
        layout.addWidget(self.dob_input)

        self.image_path_input = QLineEdit()
        layout.addWidget(QLabel("Image Path:"))
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.image_path_input)
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_image)
        image_layout.addWidget(browse_button)
        layout.addLayout(image_layout)

        create_button = QPushButton("Create Entry")
        create_button.clicked.connect(self.accept)
        layout.addWidget(create_button)

    def get_entry_info(self):
        return {
            'id': str(self.generate_unique_id()).zfill(4),
            'name': self.name_input.text(),
            'phone': self.phone_input.text(),
            'cnic': self.cnic_input.text(),
            'gender': self.gender_input.text(),
            'dob': self.dob_input.text(),
            'image_path': self.image_path_input.text()
        }

    def generate_unique_id(self):
        return len(main_window.cards_layout)

    def browse_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)", options=options)
        if file_path:
            self.image_path_input.setText(file_path)

class SearchEntryDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Search Entry")
        self.setFixedSize(300, 100)

        layout = QVBoxLayout(self)

        id_label = QLabel("Enter Entry ID:")
        self.id_input = QLineEdit()
        layout.addWidget(id_label)
        layout.addWidget(self.id_input)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_entry)
        layout.addWidget(search_button)

    def search_entry(self):
        entry_id = self.id_input.text()
        main_window.search_entry_by_id(entry_id)
        self.accept()

class ExportImportDialog(QDialog):
    def __init__(self, export_mode=True):
        super().__init__()

        self.export_mode = export_mode

        if self.export_mode:
            self.setWindowTitle("Export Data")
        else:
            self.setWindowTitle("Import Data")

        self.setFixedSize(400, 150)

        layout = QVBoxLayout(self)

        self.folder_path_input = QLineEdit()
        layout.addWidget(QLabel("Folder Path:"))
        layout.addWidget(self.folder_path_input)

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_folder)
        layout.addWidget(browse_button)

        action_button_text = "Export" if self.export_mode else "Import"
        action_button = QPushButton(action_button_text)
        action_button.clicked.connect(self.accept)
        layout.addWidget(action_button)

    def browse_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder_path = QFileDialog.getExistingDirectory(self if self.export_mode else None,
                                                       "Select Folder",
                                                       os.path.expanduser("~") + "/Desktop",
                                                       options=options)
        if folder_path:
            self.folder_path_input.setText(folder_path)

    def get_folder_path(self):
        return self.folder_path_input.text()

class ImportDataDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Import Data")
        self.setFixedSize(400, 150)

        layout = QVBoxLayout(self)

        self.file_path_input = QLineEdit()
        layout.addWidget(QLabel("File Path:"))
        layout.addWidget(self.file_path_input)

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_file)
        layout.addWidget(browse_button)

        action_button = QPushButton("Import")
        action_button.clicked.connect(self.accept)
        layout.addWidget(action_button)

        self.file_path_input.returnPressed.connect(action_button.click)

    def browse_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Excel File", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        if file_path:
            self.file_path_input.setText(file_path)

    def get_file_path(self):
        return self.file_path_input.text()

class LoginPage(QMainWindow):
    show_main_window_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login Page")
        self.setFixedSize(300, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)

        self.create_login_widgets(layout)

    def create_login_widgets(self, layout):
        username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)

        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if AuthManager.authenticate(username, password):
            self.show_main_window_signal.emit()
            self.close()
        else:
            self.show_login_error_message("Invalid username or password")

    def show_login_error_message(self, message):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.warning(self, "Login Failed", message)

class BaseWindow(QMainWindow):
    def create_toolbar_button(self, text, slot):
        button = QPushButton(text)
        button.clicked.connect(slot)
        return button
    
class FolderWidget(BaseWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Folder")
        self.setGeometry(100, 100, 800, 600)

        central_widget = self.create_central_widget()
        self.setCentralWidget(central_widget)

        self.create_toolbar()

    def create_central_widget(self):
        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)

        self.folder_layout = QVBoxLayout()
        self.folder_content = QWidget()
        self.folder_layout.addWidget(self.folder_content)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.folder_content)

        central_layout.addLayout(self.folder_layout)
        return central_widget

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        go_back_button = self.create_toolbar_button("Go Back", self.go_back)
        toolbar.addWidget(go_back_button)

    def go_back(self):
        self.close()

class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 800, 600)

        self.entry_count = 0

        central_widget = self.create_central_widget()
        self.setCentralWidget(central_widget)

        self.create_toolbar()

    def create_central_widget(self):
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: white;")
        central_layout = QVBoxLayout(central_widget)
        self.cards_layout = QHBoxLayout()
        central_layout.addLayout(self.cards_layout)
        return central_widget

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        create_entry_button = self.create_toolbar_button("Create Entry", self.create_entry)
        search_entry_button = self.create_toolbar_button("Search Entry", self.show_search_dialog)
        export_data_button = self.create_toolbar_button("Export Data", self.export_data)
        import_data_button = self.create_toolbar_button("Import Data", self.import_data)

        new_folder_button = self.create_toolbar_button("New Folder", self.create_folder)
        toolbar.addWidget(new_folder_button)

        toolbar.addSeparator()
        toolbar.addWidget(create_entry_button)
        toolbar.addWidget(search_entry_button)
        toolbar.addWidget(export_data_button)
        toolbar.addWidget(import_data_button)

    def create_toolbar_button(self, text, slot):
        button = QPushButton(text)
        button.clicked.connect(slot)
        return button

    def create_entry(self):
        input_dialog = EntryInputDialog()
        if input_dialog.exec_() == QDialog.Accepted:
            entry_info = input_dialog.get_entry_info()
            self.add_entry_card(entry_info)

    def add_entry_card(self, entry_info):
        card = EntryCard(entry_info)
        self.cards_layout.addWidget(card)

    def show_search_dialog(self):
        search_dialog = SearchEntryDialog()
        search_dialog.exec_()

    def search_entry_by_id(self, entry_id):
        print(f"Searching for entry with ID: {entry_id}")

    def export_data(self):
        export_dialog = ExportImportDialog(export_mode=True)
        if export_dialog.exec_() == QDialog.Accepted:
            folder_path = export_dialog.get_folder_path()
            self.export_to_excel(folder_path)

    def import_data(self):
        import_dialog = ImportDataDialog()
        if import_dialog.exec_() == QDialog.Accepted:
            file_path = import_dialog.get_file_path()
            self.import_from_excel(file_path)

    def export_to_excel(self, folder_path):
        if folder_path:
            data = {'ID': [], 'Name': [], 'Phone': [], 'CNIC': [], 'Gender': [], 'DOB': [], 'Image_Path': []}

            for i in range(self.cards_layout.count()):
                card = self.cards_layout.itemAt(i).widget()
                entry_info = card.format_entry_info(entry_info)
                data['ID'].append(entry_info['id'])
                data['Name'].append(entry_info['name'])
                data['Phone'].append(entry_info['phone'])
                data['CNIC'].append(entry_info['cnic'])
                data['Gender'].append(entry_info['gender'])
                data['DOB'].append(entry_info['dob'])
                data['Image_Path'].append(entry_info.get('image_path', 'default_image.png'))

            df = pd.DataFrame(data)
            file_path = os.path.join(folder_path, "exported_data.xlsx")
            df.to_excel(file_path, index=False)

    def import_from_excel(self, file_path):
        if file_path and os.path.exists(file_path):
            df = pd.read_excel(file_path)

            for index, row in df.iterrows():
                entry_info = {
                    'id': str(row['ID']).zfill(4),
                    'name': str(row['Name']),
                    'phone': str(row['Phone']),
                    'cnic': str(row['CNIC']),
                    'gender': str(row['Gender']),
                    'dob': str(row['DOB']),
                    'image_path': str(row['Image_Path'])
                }
                self.add_entry_card(entry_info)

    def create_folder(self):
        folder_widget = FolderWidget(self)
        folder_widget.show()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_page = LoginPage()
    main_window = MainWindow()

    login_page.show_main_window_signal.connect(main_window.show)

    login_page.show()
    sys.exit(app.exec())