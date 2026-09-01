import sys
import os
import platform
import subprocess
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QPushButton, QFileDialog, QListWidget, QHBoxLayout,
                               QLabel, QComboBox, QGroupBox, QGridLayout, QSlider,
                               QMessageBox, QDialog, QTextEdit)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaDevices, QVideoFrame
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QPixmap, QIcon, QDesktopServices

# --- RESOURCE PATH HELPER (FOR PYINSTALLER ICON & DATA BUNDLING) ---
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

DONATION_URL = "https://kreosus.com/mitratheatre/about"

# --- MODERN DARK THEME QSS ---
STYLE_SHEET = """
QMainWindow, QWidget {
    background-color: #1E1E1E;
    color: #FFFFFF;
    font-family: 'Segoe UI', Arial, sans-serif;
}
QGroupBox {
    font-weight: bold;
    border: 2px solid #3F3F46;
    border-radius: 8px;
    margin-top: 15px;
    padding-top: 15px;
    font-size: 14px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 10px;
    color: #9CDCFE;
    bottom: 5px;
}
QListWidget {
    background-color: #2D2D30;
    border: 1px solid #3F3F46;
    border-radius: 8px;
    padding: 5px;
    font-size: 14px;
    outline: none;
}
QListWidget::item { padding: 8px; border-radius: 4px; }
QListWidget::item:selected { background-color: #007ACC; color: white; }
QListWidget::item:hover { background-color: #3F3F46; }
QPushButton {
    background-color: #333337;
    color: white;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 8px 12px;
    font-size: 13px;
    font-weight: bold;
}
QPushButton:hover { background-color: #3F3F46; border: 1px solid #007ACC; }
QPushButton:pressed { background-color: #007ACC; }
QPushButton#loadBtn { background-color: #007ACC; border: none; }
QPushButton#loadBtn:hover { background-color: #0098FF; }
QPushButton#infoBtn { background-color: #4CAF50; border: none; padding: 6px 14px; }
QPushButton#infoBtn:hover { background-color: #45a049; }
QPushButton#donateBtn { background-color: #E91E63; border: none; padding: 6px 14px; }
QPushButton#donateBtn:hover { background-color: #d81558; }
QPushButton#blankBtn { background-color: #2E7D32; border: 1px solid #4CAF50; padding: 8px 12px; }
QPushButton#blankBtn:checked { background-color: #C62828; border: 1px solid #EF5350; }
QLabel { font-size: 13px; }
QComboBox {
    background-color: #2D2D30; border: 1px solid #3F3F46;
    border-radius: 6px; padding: 6px; color: white;
}
#previewLabel {
    background-color: #000000;
    border: 2px solid #555555;
}
QSlider::groove:horizontal {
    border: 1px solid #3A3939; height: 8px; background: #201F1F; margin: 2px 0; border-radius: 4px;
}
QSlider::handle:horizontal {
    background: #007ACC; border: 1px solid #007ACC; width: 14px; height: 14px; margin: -4px 0; border-radius: 7px;
}
QSlider::groove:vertical {
    border: 1px solid #3A3939; width: 8px; background: #201F1F; margin: 0 2px; border-radius: 4px;
}
QSlider::handle:vertical {
    background: #4CAF50; border: 1px solid #4CAF50; width: 14px; height: 14px; margin: 0 -4px; border-radius: 7px;
}
"""

class EulaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("End-User License Agreement (EULA)")
        self.resize(700, 500)
        
        layout = QVBoxLayout(self)
        
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        
        eula_path = resource_path("EULA.txt")
        try:
            with open(eula_path, "r", encoding="utf-8") as file:
                self.text_edit.setText(file.read())
        except Exception as e:
            self.text_edit.setText(
                f"Error: EULA.txt could not be loaded.\nDetails: {str(e)}\n\n"
                "Software provided as-is. Governed by the laws of Türkiye, jurisdiction in Antalya."
            )
            
        layout.addWidget(self.text_edit)
        
        self.close_btn = QPushButton("Close", self)
        self.close_btn.clicked.connect(self.accept)
        layout.addWidget(self.close_btn)

class ClickableSlider(QSlider):
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self.orientation() == Qt.Orientation.Horizontal:
                val = self.minimum() + ((self.maximum() - self.minimum()) * event.position().x()) / self.width()
                self.setValue(int(val))
                self.sliderMoved.emit(int(val))

class DisplayWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Projector Display")
        self.setStyleSheet("background-color: black;")
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.video_widget = QVideoWidget()
        self.layout.addWidget(self.video_widget)
        self.video_widget.hide()

class ControlWindow(QMainWindow):
    def __init__(self, display_window):
        super().__init__()
        self.display_window = display_window
        self.setWindowTitle("Mitra Theatre")
        self.resize(1000, 750)

        # State variable for the screen feed switch
        self.is_screen_blanked = False

        # --- DUAL MEDIA ENGINE SETUP ---
        self.video_player = QMediaPlayer()
        self.video_audio_output = QAudioOutput()
        self.video_player.setAudioOutput(self.video_audio_output)
        
        self.video_player.setVideoOutput(self.display_window.video_widget)
        self.display_window.video_widget.videoSink().videoFrameChanged.connect(self.process_video_frame)

        self.audio_player = QMediaPlayer()
        self.audio_only_output = QAudioOutput()
        self.audio_player.setAudioOutput(self.audio_only_output)
        
        self.video_audio_output.setVolume(0.5)
        self.audio_only_output.setVolume(0.5)

        self.playlist = []
        self.available_audio_devices = QMediaDevices.audioOutputs()

        # --- UI CONSTRUCTION ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Top Header: Device Selector & App Info
        device_layout = QHBoxLayout()
        device_layout.addWidget(QLabel("Master Output Device:"))
        self.device_combo = QComboBox()
        for device in self.available_audio_devices:
            self.device_combo.addItem(device.description())
        device_layout.addWidget(self.device_combo)
        
        device_layout.addStretch() 

        self.btn_info = QPushButton("Info")
        self.btn_info.setObjectName("infoBtn")
        self.btn_info.clicked.connect(self.show_info)
        device_layout.addWidget(self.btn_info)

        self.btn_donate = QPushButton("Donate")
        self.btn_donate.setObjectName("donateBtn")
        self.btn_donate.clicked.connect(self.open_donation_page)
        device_layout.addWidget(self.btn_donate)
        
        main_layout.addLayout(device_layout)

        # Middle Grid Layout
        grid = QGridLayout()
        main_layout.addLayout(grid)

        # --- DECK A (VIDEO) ---
        deck_a_group = QGroupBox("Deck A: Visuals & Video")
        deck_a_layout = QHBoxLayout(deck_a_group)
        
        deck_a_controls_layout = QVBoxLayout()
        self.lbl_deck_a_status = QLabel("Currently Loaded: None")
        self.lbl_deck_a_status.setStyleSheet("color: #4CAF50; font-weight: bold;")
        deck_a_controls_layout.addWidget(self.lbl_deck_a_status)

        self.lbl_preview = QLabel()
        self.lbl_preview.setObjectName("previewLabel")
        self.lbl_preview.setFixedSize(320, 180) 
        self.lbl_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        deck_a_controls_layout.addWidget(self.lbl_preview)

        seek_a_layout = QHBoxLayout()
        self.lbl_time_a = QLabel("00:00 / 00:00")
        self.slider_seek_a = ClickableSlider(Qt.Orientation.Horizontal)
        self.slider_seek_a.setRange(0, 100)
        seek_a_layout.addWidget(self.lbl_time_a)
        seek_a_layout.addWidget(self.slider_seek_a)
        deck_a_controls_layout.addLayout(seek_a_layout)

        # Action Buttons Row inside Deck A
        btn_layout_a = QHBoxLayout()
        self.btn_load_a = QPushButton("Load")
        self.btn_load_a.setObjectName("loadBtn")
        self.btn_playpause_a = QPushButton("▶ Play")
        self.btn_stop_a = QPushButton("■ Stop")
        
        # Blank Screen toggle placed directly in Deck A control bar
        self.btn_blank = QPushButton("LIVE")
        self.btn_blank.setObjectName("blankBtn")
        self.btn_blank.setCheckable(True)
        self.btn_blank.clicked.connect(self.toggle_blank_screen)

        btn_layout_a.addWidget(self.btn_load_a)
        btn_layout_a.addWidget(self.btn_playpause_a)
        btn_layout_a.addWidget(self.btn_stop_a)
        btn_layout_a.addWidget(self.btn_blank)
        deck_a_controls_layout.addLayout(btn_layout_a)
        
        deck_a_layout.addLayout(deck_a_controls_layout)

        vol_a_layout = QVBoxLayout()
        vol_a_layout.addWidget(QLabel("Vol"), alignment=Qt.AlignmentFlag.AlignHCenter)
        self.slider_vol_a = QSlider(Qt.Orientation.Vertical)
        self.slider_vol_a.setRange(0, 100)
        self.slider_vol_a.setValue(50)
        vol_a_layout.addWidget(self.slider_vol_a, alignment=Qt.AlignmentFlag.AlignHCenter)
        deck_a_layout.addLayout(vol_a_layout)

        grid.addWidget(deck_a_group, 0, 0)

        # --- DECK B (AUDIO) ---
        deck_b_group = QGroupBox("Deck B: Background Music")
        deck_b_layout = QHBoxLayout(deck_b_group)
        
        deck_b_controls_layout = QVBoxLayout()
        self.lbl_deck_b_status = QLabel("Currently Loaded: None")
        self.lbl_deck_b_status.setStyleSheet("color: #FF9800; font-weight: bold;")
        deck_b_controls_layout.addWidget(self.lbl_deck_b_status)
        deck_b_controls_layout.addStretch()

        seek_b_layout = QHBoxLayout()
        self.lbl_time_b = QLabel("00:00 / 00:00")
        self.slider_seek_b = ClickableSlider(Qt.Orientation.Horizontal)
        self.slider_seek_b.setRange(0, 100)
        seek_b_layout.addWidget(self.lbl_time_b)
        seek_b_layout.addWidget(self.slider_seek_b)
        deck_b_controls_layout.addLayout(seek_b_layout)

        btn_layout_b = QHBoxLayout()
        self.btn_load_b = QPushButton("Load")
        self.btn_load_b.setObjectName("loadBtn")
        self.btn_playpause_b = QPushButton("▶ Play")
        self.btn_stop_b = QPushButton("■ Stop")
        btn_layout_b.addWidget(self.btn_load_b)
        btn_layout_b.addWidget(self.btn_playpause_b)
        btn_layout_b.addWidget(self.btn_stop_b)
        deck_b_controls_layout.addLayout(btn_layout_b)
        
        deck_b_layout.addLayout(deck_b_controls_layout)

        vol_b_layout = QVBoxLayout()
        vol_b_layout.addWidget(QLabel("Vol"), alignment=Qt.AlignmentFlag.AlignHCenter)
        self.slider_vol_b = QSlider(Qt.Orientation.Vertical)
        self.slider_vol_b.setRange(0, 100)
        self.slider_vol_b.setValue(50)
        self.slider_vol_b.setStyleSheet("QSlider::handle:vertical { background: #FF9800; border: 1px solid #FF9800; }")
        vol_b_layout.addWidget(self.slider_vol_b, alignment=Qt.AlignmentFlag.AlignHCenter)
        deck_b_layout.addLayout(vol_b_layout)

        grid.addWidget(deck_b_group, 1, 0)

        # --- MASTER PLAYLIST ---
        playlist_group = QGroupBox("Master Playlist")
        playlist_layout = QVBoxLayout(playlist_group)
        self.list_widget = QListWidget()
        playlist_layout.addWidget(self.list_widget)
        self.btn_add = QPushButton("+ Add Files to Library")
        playlist_layout.addWidget(self.btn_add)
        
        grid.addWidget(playlist_group, 0, 1, 2, 1) 
        grid.setColumnStretch(0, 1) 
        grid.setColumnStretch(1, 1) 

        # --- CONNECTIONS ---
        self.device_combo.currentIndexChanged.connect(self.change_audio_device)
        self.btn_add.clicked.connect(self.add_media)
        
        # Playlist interaction: Smart double-click loading
        self.list_widget.itemDoubleClicked.connect(self.handle_playlist_doubleclick)
        
        self.btn_load_a.clicked.connect(self.load_deck_a)
        self.btn_playpause_a.clicked.connect(self.toggle_play_a)
        self.btn_stop_a.clicked.connect(self.stop_a)
        self.slider_vol_a.valueChanged.connect(self.set_volume_a)
        self.slider_seek_a.sliderMoved.connect(self.set_position_a)
        self.video_player.positionChanged.connect(self.position_changed_a)
        self.video_player.durationChanged.connect(self.duration_changed_a)
        self.video_player.mediaStatusChanged.connect(self.check_video_status)

        self.btn_load_b.clicked.connect(self.load_deck_b)
        self.btn_playpause_b.clicked.connect(self.toggle_play_b)
        self.btn_stop_b.clicked.connect(self.stop_b)
        self.slider_vol_b.valueChanged.connect(self.set_volume_b)
        self.slider_seek_b.sliderMoved.connect(self.set_position_b)
        self.audio_player.positionChanged.connect(self.position_changed_b)
        self.audio_player.durationChanged.connect(self.duration_changed_b)

    # --- BLANK SCREEN CONTROL ---
    def toggle_blank_screen(self):
        self.is_screen_blanked = self.btn_blank.isChecked()
        if self.is_screen_blanked:
            self.btn_blank.setText("BLACK")
            self.display_window.video_widget.hide()
            self.lbl_preview.clear()
        else:
            self.btn_blank.setText("LIVE")
            if not self.video_player.source().isEmpty() and self.video_player.playbackState() != QMediaPlayer.PlaybackState.StoppedState:
                self.display_window.video_widget.show()

    # --- DEVICE, PLAYLIST & INFO ---
    def show_info(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("About Mitra Theatre")
        dialog_layout = QVBoxLayout(dialog)

        header_layout = QHBoxLayout()
        title_label = QLabel("<h2>Mitra Theatre</h2>")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        icon_file = resource_path("icon.ico")
        if os.path.exists(icon_file):
            pixmap = QPixmap(icon_file)
            if not pixmap.isNull():
                icon_label = QLabel()
                icon_label.setPixmap(pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                header_layout.addWidget(icon_label)

        dialog_layout.addLayout(header_layout)

        details_label = QLabel(
            "<p><b>Version:</b> 1.2.10</p>"
            "<p>&copy; 2026 Özgün Ersin. All Rights Reserved.</p>"
            "<p>A professional dual-deck media controller designed for seamless presentations and live events.</p>"
            "<h3>Changelog</h3>"
            "<ul style='margin-top: 0px; margin-bottom: 10px;'>"
            "<li><b>v1.2:</b> Smart double-click loading (Video -> Deck A, Audio -> Deck B), enhanced LIVE/BLACK screen toggle, Changelog added.</li>"
            "<li><b>v1.1:</b> Output Blanking switch added, EULA file integration, UI refinements.</li>"
            "</ul>"
            "<p><small>This proprietary software utilizes the PySide6 toolkit, which is licensed under the LGPL v3.</small></p>"
            f'<p>If you find Mitra Theatre useful, consider <a href="{DONATION_URL}">supporting its development</a>.</p>'
        )
        details_label.setWordWrap(True)
        details_label.setOpenExternalLinks(True)
        dialog_layout.addWidget(details_label)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(dialog.accept)

        btn_eula = QPushButton("View EULA")
        btn_eula.clicked.connect(lambda: [dialog.accept(), self.open_eula()])

        btn_donate = QPushButton("Donate")
        btn_donate.clicked.connect(self.open_donation_page)

        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_eula)
        btn_layout.addWidget(btn_donate)
        dialog_layout.addLayout(btn_layout)

        dialog.exec()

    def open_donation_page(self):
        QDesktopServices.openUrl(QUrl(DONATION_URL))

    def open_eula(self):
        eula_dialog = EulaDialog(self)
        eula_dialog.exec()

    def change_audio_device(self, index):
        if 0 <= index < len(self.available_audio_devices):
            selected_device = self.available_audio_devices[index]
            self.video_audio_output.setDevice(selected_device)
            self.audio_only_output.setDevice(selected_device)

    def add_media(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Media", "", "Media Files (*.mp4 *.avi *.mkv *.mov *.mp3 *.wav)"
        )
        for f in files:
            self.playlist.append(f)
            self.list_widget.addItem(os.path.basename(f))

    def handle_playlist_doubleclick(self, item):
        selected = self.list_widget.currentRow()
        if selected >= 0:
            file_path = self.playlist[selected]
            # Check file extension to route audio to Deck B, everything else to Deck A
            ext = os.path.splitext(file_path)[1].lower()
            if ext in ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a']:
                self.load_deck_b()
            else:
                self.load_deck_a()

    def format_time(self, ms):
        s = round(ms / 1000)
        m, s = divmod(s, 60)
        return f"{m:02d}:{s:02d}"

    # --- DECK A LOGIC ---
    def load_deck_a(self):
        selected = self.list_widget.currentRow()
        if selected >= 0:
            file_path = self.playlist[selected]
            self.video_player.setSource(QUrl.fromLocalFile(file_path))
            self.lbl_deck_a_status.setText(f"Loaded: {os.path.basename(file_path)}")
            self.video_player.stop() 
            self.display_window.video_widget.hide()
            self.lbl_preview.clear() 
            self.btn_playpause_a.setText("▶ Play")

    def toggle_play_a(self):
        if self.video_player.source().isEmpty():
            return
        if self.video_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.video_player.pause()
            self.btn_playpause_a.setText("▶ Play")
        else:
            if not self.is_screen_blanked:
                self.display_window.video_widget.show()
            self.video_player.play()
            self.btn_playpause_a.setText("⏸ Pause")

    def stop_a(self):
        self.video_player.stop()
        self.display_window.video_widget.hide()
        self.lbl_preview.clear()
        self.btn_playpause_a.setText("▶ Play")

    def set_volume_a(self, volume):
        self.video_audio_output.setVolume(volume / 100.0)

    def set_position_a(self, position):
        self.video_player.setPosition(position)

    def position_changed_a(self, position):
        self.slider_seek_a.setValue(position)
        duration = self.video_player.duration()
        self.lbl_time_a.setText(f"{self.format_time(position)} / {self.format_time(duration)}")

    def duration_changed_a(self, duration):
        self.slider_seek_a.setRange(0, duration)

    def check_video_status(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.display_window.video_widget.hide()
            self.btn_playpause_a.setText("▶ Play")

    def process_video_frame(self, frame: QVideoFrame):
        if self.is_screen_blanked:
            self.lbl_preview.clear()
            return

        if frame.isValid():
            image = frame.toImage()
            if not image.isNull():
                pixmap = QPixmap.fromImage(image)
                scaled_pixmap = pixmap.scaled(self.lbl_preview.size(), 
                                              Qt.AspectRatioMode.KeepAspectRatio, 
                                              Qt.TransformationMode.SmoothTransformation)
                self.lbl_preview.setPixmap(scaled_pixmap)

    # --- DECK B LOGIC ---
    def load_deck_b(self):
        selected = self.list_widget.currentRow()
        if selected >= 0:
            file_path = self.playlist[selected]
            self.audio_player.setSource(QUrl.fromLocalFile(file_path))
            self.lbl_deck_b_status.setText(f"Loaded: {os.path.basename(file_path)}")
            self.audio_player.stop()
            self.btn_playpause_b.setText("▶ Play")

    def toggle_play_b(self):
        if self.audio_player.source().isEmpty():
            return
        if self.audio_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.audio_player.pause()
            self.btn_playpause_b.setText("▶ Play")
        else:
            self.audio_player.play()
            self.btn_playpause_b.setText("⏸ Pause")

    def stop_b(self):
        self.audio_player.stop()
        self.btn_playpause_b.setText("▶ Play")

    def set_volume_b(self, volume):
        self.audio_only_output.setVolume(volume / 100.0)

    def set_position_b(self, position):
        self.audio_player.setPosition(position)

    def position_changed_b(self, position):
        self.slider_seek_b.setValue(position)
        duration = self.audio_player.duration()
        self.lbl_time_b.setText(f"{self.format_time(position)} / {self.format_time(duration)}")

    def duration_changed_b(self, duration):
        self.slider_seek_b.setRange(0, duration)

    # --- CLEAN SHUTDOWN FIX ---
    def closeEvent(self, event):
        self.display_window.close()
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE_SHEET)

    icon_file = resource_path("icon.ico")
    if os.path.exists(icon_file):
        app.setWindowIcon(QIcon(icon_file))

    display = DisplayWindow()
    screens = app.screens()

    if len(screens) > 1:
        second_screen = screens[1]
        display.setGeometry(second_screen.geometry())
        display.showFullScreen()
    else:
        display.resize(800, 600)
        display.show()

    controller = ControlWindow(display)
    controller.setGeometry(screens[0].geometry().x() + 100, screens[0].geometry().y() + 100, 1000, 750)
    
    if os.path.exists(icon_file):
        controller.setWindowIcon(QIcon(icon_file))
        
    controller.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
