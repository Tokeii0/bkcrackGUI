"""
主窗口组件 - 定义应用程序的主窗口布局
"""

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter, 
    QFrame, QLabel, QStatusBar
)
from .styles import COLORS, CARD_STYLE, LABEL_STYLE, STATUSBAR_STYLE

class MainWindowComponent(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        # 设置主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # 创建标题
        title_label = QLabel("BKCrack GUI - ZIP密码破解工具")
        title_label.setStyleSheet(f"font-family: '微软雅黑'; font-size: 16pt; font-weight: bold; color: {COLORS['primary']};")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)
        
        # 左侧面板 - 控制区域
        self.left_panel = QFrame()
        self.left_panel.setObjectName("leftPanel")
        self.left_panel.setStyleSheet(CARD_STYLE)
        self.left_panel.setMinimumWidth(400)
        self.left_panel.setMaximumWidth(500)
        
        # 右侧面板 - 输出区域
        self.right_panel = QFrame()
        self.right_panel.setObjectName("rightPanel")
        self.right_panel.setStyleSheet(CARD_STYLE)
        
        # 添加面板到分割器
        splitter.addWidget(self.left_panel)
        splitter.addWidget(self.right_panel)
        splitter.setSizes([400, 800])  # 设置初始大小
        
        # 添加分割器到主布局
        main_layout.addWidget(splitter, 1)  # 1是拉伸因子，使分割器占据所有可用空间
        
        # 设置左侧面板布局
        left_layout = QVBoxLayout(self.left_panel)
        left_layout.setContentsMargins(10, 10, 10, 10)
        left_layout.setSpacing(15)
        
        # 创建左侧面板的内容占位符
        self.control_container = QFrame()
        left_layout.addWidget(self.control_container)
        
        # 设置右侧面板布局
        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)
        
        # 创建右侧面板的标题
        output_title = QLabel("输出结果")
        output_title.setStyleSheet(LABEL_STYLE)
        right_layout.addWidget(output_title)
        
        # 创建右侧面板的内容占位符
        self.output_container = QFrame()
        right_layout.addWidget(self.output_container, 1)  # 1是拉伸因子
        
        # 创建状态栏
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet(STATUSBAR_STYLE)
        self.status_bar.showMessage("就绪")
        main_layout.addWidget(self.status_bar)
        
    def set_control_widget(self, widget):
        """设置控制区域的小部件"""
        # 清除现有布局
        if self.control_container.layout():
            while self.control_container.layout().count():
                item = self.control_container.layout().takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            self.control_container.layout().deleteLater()
        
        # 创建新布局
        layout = QVBoxLayout(self.control_container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(widget)
        
    def set_output_widget(self, widget):
        """设置输出区域的小部件"""
        # 清除现有布局
        if self.output_container.layout():
            while self.output_container.layout().count():
                item = self.output_container.layout().takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            self.output_container.layout().deleteLater()
        
        # 创建新布局
        layout = QVBoxLayout(self.output_container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(widget)
        
    def update_status(self, message):
        """更新状态栏消息"""
        self.status_bar.showMessage(message)
