import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QFrame,
    QStackedWidget, QComboBox, QCheckBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QImage, QFont, QPalette, QColor
import qrcode
from io import BytesIO


class QRCodeGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('QR Code Generator')
        self.resize(600, 800)  # Initial size
        self.setMinimumSize(500, 600)  # Minimum size to prevent UI from being crushed

        # Modern color scheme
        self.bg_color = '#f5f5f5'
        self.primary_color = '#6366f1'
        self.secondary_color = '#8b5cf6'
        self.success_color = '#10b981'
        self.text_color = '#1f2937'
        self.card_bg = '#ffffff'
        self.wifi_color = '#f59e0b'

        # Variables
        self.qr_image = None
        self.current_mode = None

        # Setup UI
        self.init_ui()

    def init_ui(self):
        # Central widget with stacked layout for multiple screens
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        self.header = QWidget()
        self.header.setFixedHeight(100)
        self.header.setStyleSheet(f'background-color: {self.primary_color};')
        header_layout = QVBoxLayout(self.header)

        self.title_label = QLabel('QR Code Generator')
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont('Segoe UI', 28, QFont.Weight.Bold))
        self.title_label.setStyleSheet('color: white; padding: 20px;')
        header_layout.addWidget(self.title_label)

        main_layout.addWidget(self.header)

        # Stacked widget for different screens
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget, 1)

        # Create screens
        self.mode_selection_screen = self.create_mode_selection_screen()
        self.url_mode_screen = self.create_url_mode_screen()
        self.wifi_mode_screen = self.create_wifi_mode_screen()
        self.preview_screen = self.create_preview_screen()

        # Add screens to stacked widget
        self.stacked_widget.addWidget(self.mode_selection_screen)
        self.stacked_widget.addWidget(self.url_mode_screen)
        self.stacked_widget.addWidget(self.wifi_mode_screen)
        self.stacked_widget.addWidget(self.preview_screen)

        # Show mode selection by default
        self.show_mode_selection()

    def create_mode_selection_screen(self):
        '''Create the initial mode selection screen'''
        screen = QWidget()
        screen.setStyleSheet(f'background-color: {self.bg_color};')
        layout = QVBoxLayout(screen)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Welcome message
        welcome_label = QLabel('Choose QR Code Type')
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setFont(QFont('Segoe UI', 18, QFont.Weight.Bold))
        welcome_label.setStyleSheet(f'color: {self.text_color}; padding: 20px;')
        layout.addWidget(welcome_label)

        # URL Mode Button
        url_btn = QPushButton('📱 URL / Text Mode')
        url_btn.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        url_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        url_btn.setMinimumHeight(120)
        url_btn.setStyleSheet(f'''
            QPushButton {{
                background-color: {self.primary_color};
                color: white;
                border: none;
                border-radius: 12px;
                padding: 20px;
            }}
            QPushButton:hover {{
                background-color: {self.secondary_color};
            }}
            QPushButton:pressed {{
                background-color: #7c3aed;
            }}
        ''')
        url_btn.clicked.connect(self.show_url_mode)
        layout.addWidget(url_btn)

        # WiFi Mode Button
        wifi_btn = QPushButton('📶 WiFi Mode')
        wifi_btn.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        wifi_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        wifi_btn.setMinimumHeight(120)
        wifi_btn.setStyleSheet(f'''
            QPushButton {{
                background-color: {self.wifi_color};
                color: white;
                border: none;
                border-radius: 12px;
                padding: 20px;
            }}
            QPushButton:hover {{
                background-color: #d97706;
            }}
            QPushButton:pressed {{
                background-color: #b45309;
            }}
        ''')
        wifi_btn.clicked.connect(self.show_wifi_mode)
        layout.addWidget(wifi_btn)

        layout.addStretch()

        return screen

    def create_url_mode_screen(self):
        '''Create the URL/Text mode screen'''
        screen = QWidget()
        screen.setStyleSheet(f'background-color: {self.bg_color};')
        layout = QVBoxLayout(screen)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Back button
        back_btn = QPushButton('← Back')
        back_btn.setFont(QFont('Segoe UI', 11))
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.setStyleSheet('''
            QPushButton {
                background-color: transparent;
                color: #6b7280;
                border: none;
                text-align: left;
                padding: 5px;
            }
            QPushButton:hover {
                color: #374151;
            }
        ''')
        back_btn.clicked.connect(self.show_mode_selection)
        layout.addWidget(back_btn)

        # Input card
        input_card = self.create_card()
        input_layout = QVBoxLayout(input_card)
        input_layout.setContentsMargins(25, 25, 25, 25)
        input_layout.setSpacing(15)

        # Input label
        input_label = QLabel('Enter text or URL')
        input_label.setFont(QFont('Segoe UI', 13, QFont.Weight.Bold))
        input_label.setStyleSheet(f'color: {self.text_color};')
        input_layout.addWidget(input_label)

        # Text entry
        self.url_text_entry = QLineEdit()
        self.url_text_entry.setFont(QFont('Segoe UI', 12))
        self.url_text_entry.setPlaceholderText('Enter text or URL to generate QR code...')
        self.url_text_entry.setStyleSheet(f'''
            QLineEdit {{
                padding: 12px;
                border: 2px solid #e5e7eb;
                border-radius: 6px;
                background-color: white;
                color: {self.text_color};
            }}
            QLineEdit:focus {{
                border: 2px solid #6366f1;
            }}
        ''')
        input_layout.addWidget(self.url_text_entry)

        # Preview button
        url_preview_btn = QPushButton('Preview QR Code')
        url_preview_btn.setFont(QFont('Segoe UI', 12, QFont.Weight.Bold))
        url_preview_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        url_preview_btn.setStyleSheet(f'''
            QPushButton {{
                background-color: {self.primary_color};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 14px;
            }}
            QPushButton:hover {{
                background-color: {self.secondary_color};
            }}
            QPushButton:pressed {{
                background-color: #7c3aed;
            }}
        ''')
        url_preview_btn.clicked.connect(lambda: self.preview_qr_code('url'))
        input_layout.addWidget(url_preview_btn)

        layout.addWidget(input_card)
        layout.addStretch()

        return screen

    def create_wifi_mode_screen(self):
        '''Create the WiFi mode screen'''
        screen = QWidget()
        screen.setStyleSheet(f'background-color: {self.bg_color};')
        layout = QVBoxLayout(screen)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        # Back button
        back_btn = QPushButton('← Back')
        back_btn.setFont(QFont('Segoe UI', 11))
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.setStyleSheet('''
            QPushButton {
                background-color: transparent;
                color: #6b7280;
                border: none;
                text-align: left;
                padding: 5px;
            }
            QPushButton:hover {
                color: #374151;
            }
        ''')
        back_btn.clicked.connect(self.show_mode_selection)
        layout.addWidget(back_btn)

        # WiFi Input card
        wifi_card = self.create_card()
        wifi_layout = QVBoxLayout(wifi_card)
        wifi_layout.setContentsMargins(20, 20, 20, 20)
        wifi_layout.setSpacing(10)

        # SSID
        ssid_label = QLabel('WiFi Network Name (SSID)')
        ssid_label.setFont(QFont('Segoe UI', 11, QFont.Weight.Bold))
        ssid_label.setStyleSheet(f'color: {self.text_color}; margin-top: 5px;')
        wifi_layout.addWidget(ssid_label)

        self.wifi_ssid_entry = QLineEdit()
        self.wifi_ssid_entry.setFont(QFont('Segoe UI', 11))
        self.wifi_ssid_entry.setPlaceholderText('Enter WiFi network name...')
        self.wifi_ssid_entry.setMinimumHeight(40)
        self.wifi_ssid_entry.setStyleSheet(f'''
            QLineEdit {{
                padding: 10px;
                border: 2px solid #e5e7eb;
                border-radius: 6px;
                background-color: white;
                color: {self.text_color};
            }}
            QLineEdit:focus {{
                border: 2px solid {self.wifi_color};
            }}
        ''')
        wifi_layout.addWidget(self.wifi_ssid_entry)

        # Password
        password_label = QLabel('WiFi Password')
        password_label.setFont(QFont('Segoe UI', 11, QFont.Weight.Bold))
        password_label.setStyleSheet(f'color: {self.text_color}; margin-top: 8px;')
        wifi_layout.addWidget(password_label)

        self.wifi_password_entry = QLineEdit()
        self.wifi_password_entry.setFont(QFont('Segoe UI', 11))
        self.wifi_password_entry.setPlaceholderText('Enter WiFi password...')
        self.wifi_password_entry.setMinimumHeight(40)
        self.wifi_password_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.wifi_password_entry.setStyleSheet(f'''
            QLineEdit {{
                padding: 10px;
                border: 2px solid #e5e7eb;
                border-radius: 6px;
                background-color: white;
                color: {self.text_color};
            }}
            QLineEdit:focus {{
                border: 2px solid {self.wifi_color};
            }}
        ''')
        wifi_layout.addWidget(self.wifi_password_entry)

        # Show password checkbox
        self.show_password_check = QCheckBox('Show password')
        self.show_password_check.setFont(QFont('Segoe UI', 10))
        self.show_password_check.setStyleSheet(f'color: {self.text_color}; margin-bottom: 5px;')
        self.show_password_check.stateChanged.connect(self.toggle_password_visibility)
        wifi_layout.addWidget(self.show_password_check)

        # Encryption type
        encryption_label = QLabel('Security Type')
        encryption_label.setFont(QFont('Segoe UI', 11, QFont.Weight.Bold))
        encryption_label.setStyleSheet(f'color: {self.text_color}; margin-top: 8px;')
        wifi_layout.addWidget(encryption_label)

        self.wifi_encryption_combo = QComboBox()
        self.wifi_encryption_combo.setFont(QFont('Segoe UI', 11))
        self.wifi_encryption_combo.setMinimumHeight(40)
        self.wifi_encryption_combo.addItems(['WPA/WPA2', 'WEP', 'No Password'])
        self.wifi_encryption_combo.setStyleSheet(f'''
            QComboBox {{
                padding: 10px;
                border: 2px solid #e5e7eb;
                border-radius: 6px;
                background-color: white;
                color: {self.text_color};
            }}
            QComboBox:focus {{
                border: 2px solid {self.wifi_color};
            }}
            QComboBox::drop-down {{
                border: none;
                padding-right: 10px;
            }}
            QComboBox QAbstractItemView {{
                background-color: white;
                color: {self.text_color};
                selection-background-color: {self.wifi_color};
                selection-color: white;
            }}
        ''')
        wifi_layout.addWidget(self.wifi_encryption_combo)

        # Preview button
        wifi_preview_btn = QPushButton('Preview QR Code')
        wifi_preview_btn.setFont(QFont('Segoe UI', 11, QFont.Weight.Bold))
        wifi_preview_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        wifi_preview_btn.setMinimumHeight(45)
        wifi_preview_btn.setStyleSheet(f'''
            QPushButton {{
                background-color: {self.wifi_color};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                margin-top: 10px;
            }}
            QPushButton:hover {{
                background-color: #d97706;
            }}
            QPushButton:pressed {{
                background-color: #b45309;
            }}
        ''')
        wifi_preview_btn.clicked.connect(lambda: self.preview_qr_code('wifi'))
        wifi_layout.addWidget(wifi_preview_btn)

        layout.addWidget(wifi_card)
        layout.addStretch()

        return screen

    def create_card(self):
        '''Create a card widget with modern styling'''
        card = QFrame()
        card.setStyleSheet(f'''
            QFrame {{
                background-color: {self.card_bg};
                border-radius: 8px;
                border: 1px solid #e5e7eb;
            }}
        ''')
        return card

    def create_preview_screen(self):
        '''Create the QR code preview screen'''
        screen = QWidget()
        screen.setStyleSheet(f'background-color: {self.bg_color};')
        layout = QVBoxLayout(screen)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(20)

        # Back button
        back_btn = QPushButton('← Back')
        back_btn.setFont(QFont('Segoe UI', 11))
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.setStyleSheet('''
            QPushButton {
                background-color: transparent;
                color: #6b7280;
                border: none;
                text-align: left;
                padding: 5px;
            }
            QPushButton:hover {
                color: #374151;
            }
        ''')
        back_btn.clicked.connect(self.close_preview)
        layout.addWidget(back_btn)

        # QR Code display card
        qr_card = self.create_card()
        qr_layout = QVBoxLayout(qr_card)
        qr_layout.setContentsMargins(30, 30, 30, 30)
        qr_layout.setSpacing(20)

        # Preview label
        self.preview_title = QLabel('QR Code Preview')
        self.preview_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_title.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        self.preview_title.setStyleSheet(f'color: {self.text_color};')
        qr_layout.addWidget(self.preview_title)

        # QR Code display area
        self.preview_qr_display = QLabel()
        self.preview_qr_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_qr_display.setMinimumHeight(400)
        self.preview_qr_display.setStyleSheet('''
            QLabel {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 6px;
            }
        ''')
        qr_layout.addWidget(self.preview_qr_display, 1)

        # Save button
        self.preview_save_btn = QPushButton('💾 Save QR Code')
        self.preview_save_btn.setFont(QFont('Segoe UI', 12, QFont.Weight.Bold))
        self.preview_save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.preview_save_btn.setMinimumHeight(50)
        self.preview_save_btn.setStyleSheet(f'''
            QPushButton {{
                background-color: {self.success_color};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 14px;
            }}
            QPushButton:hover {{
                background-color: #059669;
            }}
            QPushButton:pressed {{
                background-color: #047857;
            }}
        ''')
        self.preview_save_btn.clicked.connect(self.save_qr_code)
        qr_layout.addWidget(self.preview_save_btn)

        layout.addWidget(qr_card, 1)

        return screen

    def show_mode_selection(self):
        '''Show the mode selection screen'''
        self.stacked_widget.setCurrentWidget(self.mode_selection_screen)
        self.title_label.setText('QR Code Generator')
        self.header.setStyleSheet(f'background-color: {self.primary_color};')
        self.current_mode = None

    def show_url_mode(self):
        '''Show the URL/Text mode screen'''
        self.stacked_widget.setCurrentWidget(self.url_mode_screen)
        self.title_label.setText('URL / Text Mode')
        self.header.setStyleSheet(f'background-color: {self.primary_color};')
        self.current_mode = 'url'
        # Reset URL mode
        self.url_text_entry.clear()
        self.qr_image = None

    def show_wifi_mode(self):
        '''Show the WiFi mode screen'''
        self.stacked_widget.setCurrentWidget(self.wifi_mode_screen)
        self.title_label.setText('WiFi Mode')
        self.header.setStyleSheet(f'background-color: {self.wifi_color};')
        self.current_mode = 'wifi'
        # Reset WiFi mode
        self.wifi_ssid_entry.clear()
        self.wifi_password_entry.clear()
        self.wifi_encryption_combo.setCurrentIndex(0)
        self.show_password_check.setChecked(False)
        self.qr_image = None

    def close_preview(self):
        '''Close preview and return to the mode screen'''
        if self.current_mode == 'url':
            self.show_url_mode()
        elif self.current_mode == 'wifi':
            self.show_wifi_mode()
        else:
            self.show_mode_selection()

    def toggle_password_visibility(self, state):
        '''Toggle password visibility'''
        if state:
            self.wifi_password_entry.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.wifi_password_entry.setEchoMode(QLineEdit.EchoMode.Password)

    def preview_qr_code(self, mode):
        '''Generate and preview QR code based on mode'''
        if mode == 'url':
            data = self.url_text_entry.text().strip()

            if not data:
                QMessageBox.warning(self, 'Warning', 'Please enter text or URL for the QR code!')
                return

            preview_title = 'URL/Text QR Code'

        elif mode == 'wifi':
            ssid = self.wifi_ssid_entry.text().strip()
            password = self.wifi_password_entry.text()
            encryption_index = self.wifi_encryption_combo.currentIndex()

            if not ssid:
                QMessageBox.warning(self, 'Warning', 'Please enter WiFi network name (SSID)!')
                return

            # Map encryption type
            encryption_map = {
                0: 'WPA',  # WPA/WPA2
                1: 'WEP',  # WEP
                2: 'nopass'  # No Password
            }
            encryption = encryption_map[encryption_index]

            # Create WiFi QR code data in standard format
            # Format: WIFI:T:WPA;S:mynetwork;P:mypassword;;
            if encryption == 'nopass':
                data = f'WIFI:T:nopass;S:{ssid};;'
            else:
                if not password:
                    QMessageBox.warning(self, 'Warning', 'Please enter WiFi password!')
                    return
                data = f'WIFI:T:{encryption};S:{ssid};P:{password};;'

            preview_title = 'WiFi QR Code'

        else:
            return

        try:
            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            # Generate QR code image
            self.qr_image = qr.make_image(fill_color='black', back_color='white')

            # Convert PIL image to QPixmap
            buffer = BytesIO()
            self.qr_image.save(buffer, format='PNG')
            buffer.seek(0)

            qimage = QImage()
            qimage.loadFromData(buffer.read())
            pixmap = QPixmap.fromImage(qimage)

            # Scale to fit display area while maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(
                450, 450,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            # Display QR code in preview screen
            self.preview_qr_display.setPixmap(scaled_pixmap)
            self.preview_title.setText(preview_title)

            # Show preview screen
            self.stacked_widget.setCurrentWidget(self.preview_screen)
            self.title_label.setText('Preview')

            # Set header color based on mode
            if mode == 'url':
                self.header.setStyleSheet(f'background-color: {self.primary_color};')
            else:
                self.header.setStyleSheet(f'background-color: {self.wifi_color};')

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to generate QR code: {str(e)}')

    def save_qr_code(self):
        if not self.qr_image:
            QMessageBox.warning(self, 'Warning', 'No QR code to save!')
            return

        # Open native file dialog (PyQt6 uses native dialogs on all platforms)
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            'Save QR Code',
            'qrcode.png',
            'PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*.*)'
        )

        if file_path:
            try:
                self.qr_image.save(file_path)
                QMessageBox.information(self, 'Success', f'QR Code saved to:\n{file_path}')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to save QR code: {str(e)}')


def main():
    app = QApplication(sys.argv)

    # Set application-wide font
    app.setFont(QFont('Segoe UI', 10))

    window = QRCodeGeneratorApp()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
