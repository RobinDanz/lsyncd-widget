from PyQt6.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve
from PyQt6.QtWidgets import QLabel, QWidget, QGraphicsColorizeEffect, QGraphicsOpacityEffect, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QColor

from logwidget.watcher import LogWatcher

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
        
        self.dot = QLabel(self)
        self.dot.setObjectName('dot')
        self.dot.setFixedSize(16, 16)
        self.dot.setStyleSheet('border-radius: 8px; background-color: green;')
        
        self.opacity = QGraphicsOpacityEffect()
        self.opacity.setOpacity(1)
        self.dot.setGraphicsEffect(self.opacity)
        
        self.animation = QPropertyAnimation(self.opacity, b'opacity', self)
        self.animation.setDuration(1500)
        self.animation.setStartValue(0)
        self.animation.setKeyValueAt(0.5, 1)
        self.animation.setEndValue(0)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.setLoopCount(-1)
        
        self.label = QLabel('In Sync.', self)
        
        layout.addWidget(self.dot)
        layout.addWidget(self.label)
        
        
    def animate(self):
        self.dot.setStyleSheet("border-radius: 8px; background-color: red;")
        # self.effect.setColor(QColor("red"))
        self.label.setText('Processing...')
        self.animation.start()
        
    def stop_animate(self):
        self.animation.stop()
        self.opacity.setOpacity(1)
        self.dot.setStyleSheet("border-radius: 8px; background-color: green;")
        self.label.setText('In Sync.')
        
class HeaderWidget(QWidget):
    def __init__(self):
        super().__init__()

class FooterWidget(QWidget):
    def __init__(self):
        super().__init__()