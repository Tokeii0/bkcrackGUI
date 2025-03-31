"""
样式定义文件 - 包含应用程序的所有样式定义
"""

# 颜色定义
COLORS = {
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

# 字体定义
FONTS = {
    "title": "font-family: '微软雅黑'; font-size: 10pt; font-weight: bold;",
    "content": "font-family: 'Consolas'; font-size: 9pt;",
    "small": "font-family: 'Consolas'; font-size: 8pt;",
}

# 组件样式
BUTTON_STYLE = f"""
    QPushButton {{ 
        background-color: {COLORS['primary']}; 
        color: white; 
        border-radius: 4px; 
        padding: 5px 10px;
        {FONTS['title']}
    }}
    QPushButton:hover {{ 
        background-color: {COLORS['primary_hover']}; 
    }}
    QPushButton:pressed {{ 
        background-color: {COLORS['primary_pressed']}; 
    }}
    QPushButton:disabled {{ 
        background-color: {COLORS['disabled']}; 
        color: {COLORS['disabled_text']}; 
    }}
"""

SECONDARY_BUTTON_STYLE = f"""
    QPushButton {{ 
        background-color: {COLORS['card_background']}; 
        color: {COLORS['text']}; 
        border: 1px solid {COLORS['border']}; 
        border-radius: 4px; 
        padding: 5px 10px;
        {FONTS['title']}
    }}
    QPushButton:hover {{ 
        background-color: {COLORS['background']}; 
        border: 1px solid {COLORS['border_hover']}; 
    }}
    QPushButton:pressed {{ 
        background-color: {COLORS['background']}; 
    }}
    QPushButton:disabled {{ 
        background-color: {COLORS['disabled']}; 
        color: {COLORS['disabled_text']}; 
    }}
"""

LABEL_STYLE = f"""
    QLabel {{ 
        color: {COLORS['text']}; 
        {FONTS['title']}
    }}
"""

TEXT_BROWSER_STYLE = f"""
    QTextBrowser {{ 
        background-color: {COLORS['card_background']}; 
        color: {COLORS['text']}; 
        border: 1px solid {COLORS['border']}; 
        border-radius: 3px; 
        padding: 5px;
        {FONTS['content']}
    }}
"""

TEXT_EDIT_STYLE = f"""
    QPlainTextEdit {{ 
        background-color: {COLORS['card_background']}; 
        color: {COLORS['text']}; 
        border: 1px solid {COLORS['border']}; 
        border-radius: 3px; 
        padding: 5px;
        {FONTS['content']}
    }}
"""

COMBOBOX_STYLE = f"""
    QComboBox {{ 
        background-color: {COLORS['card_background']}; 
        color: {COLORS['text']}; 
        border: 1px solid {COLORS['border']}; 
        border-radius: 3px; 
        padding: 5px; 
        {FONTS['content']}
    }}
    QComboBox:hover {{ 
        border: 1px solid {COLORS['border_hover']}; 
    }}
    QComboBox::drop-down {{ 
        subcontrol-origin: padding; 
        subcontrol-position: top right; 
        width: 20px; 
        border-left: 1px solid {COLORS['border']}; 
    }}
    QComboBox QAbstractItemView {{ 
        background-color: {COLORS['card_background']}; 
        color: {COLORS['text']}; 
        selection-background-color: {COLORS['primary']}; 
        selection-color: white; 
        border: 1px solid {COLORS['border']}; 
    }}
"""

FRAME_STYLE = f"""
    QFrame {{ 
        background-color: {COLORS['card_background']}; 
        border: 1px solid {COLORS['border']}; 
        border-radius: 4px; 
    }}
"""

TAB_STYLE = f"""
    QTabWidget::pane {{ 
        border: 1px solid {COLORS['border']}; 
        background-color: {COLORS['card_background']}; 
    }}
    QTabWidget::tab-bar {{ 
        left: 5px; 
    }}
    QTabBar::tab {{ 
        background: {COLORS['background']}; 
        color: {COLORS['text']}; 
        padding: 8px 12px; 
        margin-right: 2px; 
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        border: 1px solid {COLORS['border']};
        border-bottom: none;
    }}
    QTabBar::tab:selected {{ 
        background: {COLORS['primary']}; 
        color: white; 
    }}
    QTabBar::tab:hover:!selected {{ 
        background: {COLORS['background']}; 
        border: 1px solid {COLORS['border_hover']}; 
        border-bottom: none;
    }}
"""

CHECKBOX_STYLE = f"""
    QCheckBox {{ 
        color: {COLORS['text']}; 
        {FONTS['content']}
    }}
    QCheckBox::indicator {{
        width: 16px;
        height: 16px;
    }}
    QCheckBox::indicator:unchecked {{
        border: 1px solid {COLORS['border']};
        background-color: {COLORS['card_background']};
    }}
    QCheckBox::indicator:checked {{
        border: 1px solid {COLORS['primary']};
        background-color: {COLORS['primary']};
    }}
"""

# 主应用样式
APP_STYLE = f"""
    QWidget {{ 
        background-color: {COLORS['background']}; 
    }}
"""

# 卡片样式
CARD_STYLE = f"""
    QFrame.card {{ 
        background-color: {COLORS['card_background']}; 
        border-radius: 8px; 
        border: 1px solid {COLORS['border']}; 
        padding: 10px; 
    }}
"""

# 状态栏样式
STATUSBAR_STYLE = f"""
    QStatusBar {{ 
        background-color: {COLORS['background']}; 
        color: {COLORS['text']}; 
        border-top: 1px solid {COLORS['border']}; 
    }}
"""

# 输出区域样式
OUTPUT_AREA_STYLE = f"""
    QTextBrowser {{ 
        background-color: {COLORS['card_background']}; 
        color: {COLORS['text']}; 
        border: 1px solid {COLORS['border']}; 
        border-radius: 4px; 
        padding: 10px;
        {FONTS['content']}
    }}
"""
