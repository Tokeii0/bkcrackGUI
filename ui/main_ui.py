"""
主UI文件 - 整合所有UI组件
"""

from PySide6.QtWidgets import QMainWindow
from .components.main_window import MainWindowComponent
from .components.control_panel import ControlPanelComponent
from .components.output_panel import OutputPanelComponent
from .components.theme_manager import ThemeManager

class MainUI(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        # 设置窗口标题和大小
        self.setWindowTitle("BKCrack GUI - ZIP密码破解工具")
        self.resize(1200, 800)
        
        # 创建主窗口组件
        self.main_window = MainWindowComponent()
        self.setCentralWidget(self.main_window)
        
        # 创建控制面板组件
        self.control_panel = ControlPanelComponent()
        self.main_window.set_control_widget(self.control_panel)
        
        # 创建输出面板组件
        self.output_panel = OutputPanelComponent()
        self.main_window.set_output_widget(self.output_panel)
        
        # 创建主题管理器
        self.theme_manager = ThemeManager()
        self.theme_manager.apply_theme()  # 应用默认主题
        
        # 连接主题切换按钮
        self.control_panel.theme_btn.clicked.connect(self.toggle_theme)
        
    def toggle_theme(self):
        """切换主题"""
        is_dark = self.theme_manager.toggle_theme()
        if is_dark:
            self.control_panel.theme_btn.setText("切换到亮色主题")
        else:
            self.control_panel.theme_btn.setText("切换到暗色主题")
            
    def update_status(self, message):
        """更新状态栏消息"""
        self.main_window.update_status(message)
