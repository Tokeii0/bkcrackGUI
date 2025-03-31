"""
主题管理器 - 处理亮色和暗色主题的切换
"""

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication

# 亮色主题颜色
LIGHT_COLORS = {
    "primary": "#0078d4",
    "primary_hover": "#1a86d9",
    "primary_pressed": "#006cbe",
    "background": "#f5f5f5",
    "card_background": "#ffffff",
    "text": "#333333",
    "text_secondary": "#666666",
    "border": "#cccccc",
    "border_hover": "#999999",
    "success": "#28a745",
    "warning": "#ffc107",
    "error": "#dc3545",
    "disabled": "#cccccc",
    "disabled_text": "#666666"
}

# 暗色主题颜色
DARK_COLORS = {
    "primary": "#0078d4",
    "primary_hover": "#1a86d9",
    "primary_pressed": "#006cbe",
    "background": "#1e1e1e",
    "card_background": "#2d2d2d",
    "text": "#e0e0e0",
    "text_secondary": "#a0a0a0",
    "border": "#555555",
    "border_hover": "#777777",
    "success": "#28a745",
    "warning": "#ffc107",
    "error": "#dc3545",
    "disabled": "#555555",
    "disabled_text": "#888888"
}

class ThemeManager(QObject):
    # 定义信号
    theme_changed = Signal(bool)  # True表示暗色主题，False表示亮色主题
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_dark_theme = False  # 默认使用亮色主题
        
    def toggle_theme(self):
        """切换主题"""
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()
        self.theme_changed.emit(self.is_dark_theme)
        return self.is_dark_theme
        
    def apply_theme(self):
        """应用主题"""
        colors = DARK_COLORS if self.is_dark_theme else LIGHT_COLORS
        
        # 应用主应用样式
        app_style = f"""
            QWidget {{ 
                background-color: {colors['background']}; 
                color: {colors['text']}; 
            }}
        """
        
        # 应用按钮样式
        button_style = f"""
            QPushButton {{ 
                background-color: {colors['primary']}; 
                color: white; 
                border-radius: 4px; 
                padding: 5px 10px;
                font-family: '微软雅黑'; 
                font-size: 10pt; 
                font-weight: bold;
            }}
            QPushButton:hover {{ 
                background-color: {colors['primary_hover']}; 
            }}
            QPushButton:pressed {{ 
                background-color: {colors['primary_pressed']}; 
            }}
            QPushButton:disabled {{ 
                background-color: {colors['disabled']}; 
                color: {colors['disabled_text']}; 
            }}
        """
        
        # 应用次要按钮样式
        secondary_button_style = f"""
            QPushButton {{ 
                background-color: {colors['card_background']}; 
                color: {colors['text']}; 
                border: 1px solid {colors['border']}; 
                border-radius: 4px; 
                padding: 5px 10px;
                font-family: '微软雅黑'; 
                font-size: 10pt; 
                font-weight: bold;
            }}
            QPushButton:hover {{ 
                background-color: {colors['background']}; 
                border: 1px solid {colors['border_hover']}; 
            }}
            QPushButton:pressed {{ 
                background-color: {colors['background']}; 
            }}
            QPushButton:disabled {{ 
                background-color: {colors['disabled']}; 
                color: {colors['disabled_text']}; 
            }}
        """
        
        # 应用标签样式
        label_style = f"""
            QLabel {{ 
                color: {colors['text']}; 
                font-family: '微软雅黑'; 
                font-size: 10pt; 
                font-weight: bold;
            }}
        """
        
        # 应用文本浏览器样式
        text_browser_style = f"""
            QTextBrowser {{ 
                background-color: {colors['card_background']}; 
                color: {colors['text']}; 
                border: 1px solid {colors['border']}; 
                border-radius: 3px; 
                padding: 5px;
                font-family: 'Consolas'; 
                font-size: 9pt;
            }}
        """
        
        # 应用文本编辑样式
        text_edit_style = f"""
            QPlainTextEdit, QLineEdit {{ 
                background-color: {colors['card_background']}; 
                color: {colors['text']}; 
                border: 1px solid {colors['border']}; 
                border-radius: 3px; 
                padding: 5px;
                font-family: 'Consolas'; 
                font-size: 9pt;
            }}
        """
        
        # 应用下拉框样式
        combobox_style = f"""
            QComboBox {{ 
                background-color: {colors['card_background']}; 
                color: {colors['text']}; 
                border: 1px solid {colors['border']}; 
                border-radius: 3px; 
                padding: 5px; 
                font-family: 'Consolas'; 
                font-size: 9pt;
            }}
            QComboBox:hover {{ 
                border: 1px solid {colors['border_hover']}; 
            }}
            QComboBox::drop-down {{ 
                subcontrol-origin: padding; 
                subcontrol-position: top right; 
                width: 20px; 
                border-left: 1px solid {colors['border']}; 
            }}
            QComboBox QAbstractItemView {{ 
                background-color: {colors['card_background']}; 
                color: {colors['text']}; 
                selection-background-color: {colors['primary']}; 
                selection-color: white; 
                border: 1px solid {colors['border']}; 
            }}
        """
        
        # 应用框架样式
        frame_style = f"""
            QFrame {{ 
                background-color: {colors['card_background']}; 
                border: 1px solid {colors['border']}; 
                border-radius: 4px; 
            }}
        """
        
        # 应用选项卡样式
        tab_style = f"""
            QTabWidget::pane {{ 
                border: 1px solid {colors['border']}; 
                background-color: {colors['card_background']}; 
            }}
            QTabWidget::tab-bar {{ 
                left: 5px; 
            }}
            QTabBar::tab {{ 
                background: {colors['background']}; 
                color: {colors['text']}; 
                padding: 8px 12px; 
                margin-right: 2px; 
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                border: 1px solid {colors['border']};
                border-bottom: none;
            }}
            QTabBar::tab:selected {{ 
                background: {colors['primary']}; 
                color: white; 
            }}
            QTabBar::tab:hover:!selected {{ 
                background: {colors['background']}; 
                border: 1px solid {colors['border_hover']}; 
                border-bottom: none;
            }}
        """
        
        # 应用复选框样式
        checkbox_style = f"""
            QCheckBox {{ 
                color: {colors['text']}; 
                font-family: 'Consolas'; 
                font-size: 9pt;
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
            }}
            QCheckBox::indicator:unchecked {{
                border: 1px solid {colors['border']};
                background-color: {colors['card_background']};
            }}
            QCheckBox::indicator:checked {{
                border: 1px solid {colors['primary']};
                background-color: {colors['primary']};
            }}
        """
        
        # 应用进度条样式
        progressbar_style = f"""
            QProgressBar {{
                border: 1px solid {colors['border']};
                border-radius: 3px;
                background-color: {colors['card_background']};
                text-align: center;
                color: {colors['text']};
            }}
            QProgressBar::chunk {{
                background-color: {colors['primary']};
                width: 10px;
            }}
        """
        
        # 应用分组框样式
        groupbox_style = f"""
            QGroupBox {{
                border: 1px solid {colors['border']};
                border-radius: 4px;
                margin-top: 1ex;
                font-family: '微软雅黑';
                font-size: 10pt;
                font-weight: bold;
                color: {colors['text']};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
            }}
        """
        
        # 应用滚动条样式
        scrollbar_style = f"""
            QScrollBar:vertical {{
                border: none;
                background: {colors['background']};
                width: 10px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {colors['border']};
                min-height: 20px;
                border-radius: 5px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar:horizontal {{
                border: none;
                background: {colors['background']};
                height: 10px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::handle:horizontal {{
                background: {colors['border']};
                min-width: 20px;
                border-radius: 5px;
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
        """
        
        # 应用所有样式
        QApplication.instance().setStyleSheet(
            app_style + 
            button_style + 
            secondary_button_style + 
            label_style + 
            text_browser_style + 
            text_edit_style + 
            combobox_style + 
            frame_style + 
            tab_style + 
            checkbox_style + 
            progressbar_style + 
            groupbox_style + 
            scrollbar_style
        )
        
    def is_dark(self):
        """是否是暗色主题"""
        return self.is_dark_theme
