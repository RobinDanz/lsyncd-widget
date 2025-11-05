from PyQt6.QtCore import Qt, QPoint, QTimer
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QPixmap


from logwidget.watcher import LogWatcher
from logwidget.const import CHECK_ICON, SYNC_ICON

class LsyncdWidget(QWidget):
    def __init__(self, logfile):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnBottomHint
        )
        
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        self._mouse_dragging = False
        self._drag_position = QPoint()
        
        self.make()
        self.load_style()
        
        self.watcher = LogWatcher(logfile=logfile)
        self.watcher.copy_start.connect(self.on_copy_start)
        self.watcher.copy_end.connect(self.on_copy_end)
        self.watcher.start()
    
    def make(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        
        self.container = QWidget(self)
        self.container.setObjectName('mainContainer')
        
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        self.title = QLabel('File Copy Monitor')
        self.title.setObjectName('title')
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.status = StatusWidget()
        
        layout.addWidget(self.title)
        layout.addWidget(self.status)
        outer_layout.addWidget(self.container)
        
    def load_style(self):
        with open('./assets/styles.qss', 'r') as f:
            self.setStyleSheet(f.read())
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._mouse_dragging = True
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._mouse_dragging and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._mouse_dragging = False
            event.accept()
    
    def on_copy_start(self):
        self.status.animate()
        
    def on_copy_end(self):
        self.status.stop_animate()
        
    def closeEvent(self, event):
        self.watcher.stop()
        self.watcher.wait()
        super().closeEvent(event)
        
class StatusWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # self.dot = QLabel(self)
        # self.dot.setObjectName('dot')
        # self.dot.setFixedSize(16, 16)
        # self.dot.setStyleSheet('border-radius: 8px; background-color: green;')
        
        self.icon = QLabel()
        self.icon.setFixedSize(20, 20)
        self.icon.setScaledContents(True)
        self.icon.setPixmap(QPixmap(CHECK_ICON))
        
        self.label = QLabel('In Sync.', self)
        # self.timer = QTimer(self)
        
        # layout.addWidget(self.dot)
        layout.addWidget(self.icon)
        layout.addWidget(self.label)
        
    # def toggle_opacity(self):
    #     self.visible = not self.visible
    #     self.dot.setVisible(self.visible)
        
    def animate(self):
        self.icon.setPixmap(QPixmap(SYNC_ICON))
        self.label.setText('Processing...')
        # self.timer.start(700)
        
    def stop_animate(self): 
        self.icon.setPixmap(QPixmap(CHECK_ICON))
        self.label.setText('In Sync.')
        
class HeaderWidget(QWidget):
    def __init__(self):
        super().__init__()

class FooterWidget(QWidget):
    def __init__(self):
        super().__init__()