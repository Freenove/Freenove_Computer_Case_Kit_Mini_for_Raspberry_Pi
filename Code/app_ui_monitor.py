# app_ui_monitor.py
import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QPen, QColor, QFont


class CircleProgressWidget(QWidget):
    def __init__(self, parent=None, size=100, position=(0, 0),
                 colors=('#4a90e2', '#000000'), progress_width=10):
        super().__init__(parent)
        self.setFixedSize(size, size)  
        self.move(position[0], position[1]) 

        self.progress_color = QColor(colors[0])  
        self.bg_color = QColor(colors[1])  
        self.progress_width = progress_width 
        self.percentage = 0 
        self.label_text = ""  
        self.display_text = None  
        self.label_color = QColor('#FFFFFF')  
        self.display_text_color = QColor('#FFFFFF')  

    def paintEvent(self, event):
        """绘制事件处理器"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  
        painter.setRenderHint(QPainter.TextAntialiasing)  

        margin = 8  
        rect = QRectF(margin, margin,
                      self.width() - 2 * margin,
                      self.height() - 2 * margin)

        pen = QPen(self.bg_color, self.progress_width)  
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.drawEllipse(rect)

        if self.percentage > 0: 
            pen.setColor(self.progress_color)
            painter.setPen(pen)
            span_angle = int(360 * 16 * self.percentage / 100)
            painter.drawArc(rect, 90 * 16, -span_angle)  

        painter.setPen(self.display_text_color) 
        font = QFont('Arial', max(8, int(self.height() * 0.12)))
        font.setBold(True)
        painter.setFont(font)

        if self.display_text is not None: 
            text = self.display_text
        else:  
            text = f"{self.percentage:.1f}%"

        painter.drawText(rect, Qt.AlignCenter, text)

        if self.label_text:  
            painter.setPen(self.label_color)  
            font.setBold(False)
            font.setPointSize(max(6, int(self.height() * 0.08)))
            painter.setFont(font)

            label_rect = QRectF(
                rect.x(),
                rect.y() + rect.height() * 0.5,  
                rect.width(),
                rect.height() * 0.3
            )
            painter.drawText(label_rect, Qt.AlignCenter, self.label_text)

    def draw_progress(self, percentage, label="", display_text=None, label_color=QColor('#FFFFFF'),
                      display_text_color=QColor('#FFFFFF')):
        """
        更新进度条显示
        """
        self.percentage = max(0, min(100, percentage))  
        self.label_text = label
        self.display_text = display_text
        self.label_color = label_color
        self.display_text_color = display_text_color
        self.update()  

    def set_position(self, x, y):
        """设置控件位置"""
        self.move(x, y)


class MonitoringTab(QWidget):
    def __init__(self, width=900, height=600):
        super().__init__()
        self.progress_widgets = [] 

        self.window_width = width  
        self.window_height = height  
        self.color_combinations = [
            ('#FF0000', '#FFD1D1'),  
            ('#00FF00', '#D1F2D1'),  
            ('#0000FF', '#D1F0EE'),  
            ('#FF00FF', '#FFE5B4'), 
            ('#00FFFF', '#D1D1FF'),  
            ('#333333', '#333333'),  
        ]
        self.metric_labels = [
            "CPU Usage",  
            "RAM Usage",  
            "Storage Usage",  
            "CPU Temp",  
            "RPi PWM", 
            "",  
        ]

        self.initUI()  

    def initUI(self):
        self.scale_factor = 0.6  
        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.setStyleSheet("background-color: #333333;") 
        self.setMinimumSize(round(self.window_width*self.scale_factor),
                           round(self.window_height*self.scale_factor))

        width_per_column = (self.window_width - 40) // 3
        height_per_row = (self.window_height - 30) // 2
        self.widget_size = min(width_per_column, height_per_row)
        widget_half_size = self.widget_size // 2

        positions = [
            (1*self.window_width//6-widget_half_size, 1*self.window_height//4-widget_half_size), 
            (3*self.window_width//6-widget_half_size, 1*self.window_height//4-widget_half_size), 
            (5*self.window_width//6-widget_half_size, 1*self.window_height//4-widget_half_size), 
            (1*self.window_width//6-widget_half_size, 3*self.window_height//4-widget_half_size),  
            (3*self.window_width//6-widget_half_size, 3*self.window_height//4-widget_half_size),  
            (5*self.window_width//6-widget_half_size, 3*self.window_height//4-widget_half_size)   
        ]

        for i in range(6):
            progress_widget = CircleProgressWidget(
                size=self.widget_size,
                colors=(self.color_combinations[i][0], self.color_combinations[i][1]),
                progress_width=10
            )
            progress_widget.setParent(self)  
            progress_widget.draw_progress(0, self.metric_labels[i])
            progress_widget.set_position(positions[i][0], positions[i][1])
            
            self.progress_widgets.append(progress_widget)
        self.progress_widgets[5].draw_progress(0, self.metric_labels[5], "")

    def closeEvent(self, event):
        """Handle window close event"""
        event.accept()
    def setCircleProgressValue(self, index, percentage, callword, display_value):
        self.progress_widgets[index].draw_progress(percentage, callword, display_value)

    def setCircleProgressColor(self, index, color_combinations=('#FF6B6B', '#444444')):
        self.progress_widgets[index].progress_color =  QColor(color_combinations[0])
        self.progress_widgets[index].bg_color = QColor(color_combinations[1])
        self.progress_widgets[index].update()

    def setDefaultCircleProgressColor(self):
        for i in range(len(self.color_combinations)):
            self.setCircleProgressColor(i, self.color_combinations[i])

    def resetUiSize(self, width, height):
        self.window_width = width
        self.window_height = height
        self.setGeometry(0, 0, self.window_width, self.window_height)
        self.setMinimumSize(round(self.window_width*self.scale_factor),
                           round(self.window_height*self.scale_factor))

        width_per_column = (width - 40) // 3 
        height_per_row = (height - 30) // 2   
        self.widget_size = min(width_per_column, height_per_row)

        widget_half_size = self.widget_size // 2

        positions = [
            (1*width//6-widget_half_size, 1*height//4-widget_half_size), 
            (3*width//6-widget_half_size, 1*height//4-widget_half_size), 
            (5*width//6-widget_half_size, 1*height//4-widget_half_size),  
            (1*width//6-widget_half_size, 3*height//4-widget_half_size), 
            (3*width//6-widget_half_size, 3*height//4-widget_half_size),  
            (5*width//6-widget_half_size, 3*height//4-widget_half_size)  
        ]

        for i, widget in enumerate(self.progress_widgets):
            widget.setFixedSize(self.widget_size, self.widget_size)
            widget.set_position(positions[i][0], positions[i][1])

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resetUiSize(self.width(), self.height())


if __name__ == "__main__":
    from api_json import ConfigManager
    app = QApplication(sys.argv)
    app_ui_config = ConfigManager()
    screen_direction = app_ui_config.get_value('Monitor', 'screen_orientation')
    if screen_direction == 0:  
        window = MonitoringTab(800, 420)
    elif screen_direction == 1: 
        window = MonitoringTab(480, 740)
    window.show()

    window.setCircleProgressColor(0, ['#FF0000', '#444444'])
    window.setCircleProgressColor(1, ['#00FF00', '#444444'])
    window.setCircleProgressColor(2, ['#0000FF', '#444444'])
    window.setCircleProgressColor(3, ['#FFFF00', '#444444'])
    window.setCircleProgressColor(4, ['#FF00FF', '#444444'])
    window.setCircleProgressColor(5, ['#00FFFF', '#444444'])

    window.setCircleProgressValue(0, 12, "UI 1", "12%")
    window.setCircleProgressValue(1, 24, "UI 2", "24%")
    window.setCircleProgressValue(2, 36, "UI 3", "36%")
    window.setCircleProgressValue(3, 48, "UI 4", "48%")
    window.setCircleProgressValue(4, 60, "UI 5", "60%")
    window.setCircleProgressValue(5, 72, "UI 6", "72%")

    sys.exit(app.exec_())