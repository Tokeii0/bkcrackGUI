"""
输出面板组件 - 用于显示操作结果和进度信息
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QTextBrowser, QPushButton
)
from .styles import OUTPUT_AREA_STYLE, BUTTON_STYLE, SECONDARY_BUTTON_STYLE

class OutputPanelComponent(QWidget):
    # 定义信号
    clear_output_clicked = Signal()
    save_output_clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)
        
        # 输出区域
        self.output_area = QTextBrowser()
        self.output_area.setStyleSheet(OUTPUT_AREA_STYLE)
        self.output_area.setOpenExternalLinks(True)  # 允许打开外部链接
        
        # 按钮区域
        buttons_layout = QHBoxLayout()
        
        # 清空输出按钮
        self.clear_btn = QPushButton("清空输出")
        self.clear_btn.setStyleSheet(SECONDARY_BUTTON_STYLE)
        
        # 保存输出按钮
        self.save_btn = QPushButton("保存输出")
        self.save_btn.setStyleSheet(SECONDARY_BUTTON_STYLE)
        
        # 取消操作按钮
        self.cancel_btn = QPushButton("取消操作")
        self.cancel_btn.setStyleSheet(BUTTON_STYLE)
        self.cancel_btn.hide()  # 默认隐藏取消按钮
        
        buttons_layout.addWidget(self.clear_btn)
        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addStretch(1)  # 添加弹性空间
        buttons_layout.addWidget(self.cancel_btn)
        
        # 添加所有组件到主布局
        main_layout.addWidget(self.output_area, 1)  # 1是拉伸因子
        main_layout.addLayout(buttons_layout)
        
        # 连接信号和槽
        self.clear_btn.clicked.connect(self.clear_output_clicked.emit)
        self.save_btn.clicked.connect(self.save_output_clicked.emit)
        
    def append_output(self, text):
        """添加文本到输出区域"""
        self.output_area.append(text)
        # 滚动到底部
        self.output_area.verticalScrollBar().setValue(
            self.output_area.verticalScrollBar().maximum()
        )
        
    def set_output(self, text):
        """设置输出区域的文本"""
        self.output_area.setPlainText(text)
        # 滚动到底部
        self.output_area.verticalScrollBar().setValue(
            self.output_area.verticalScrollBar().maximum()
        )
        
    def clear_output(self):
        """清空输出区域"""
        self.output_area.clear()
        
    def show_cancel_button(self):
        """显示取消按钮"""
        self.cancel_btn.show()
        
    def hide_cancel_button(self):
        """隐藏取消按钮"""
        self.cancel_btn.hide()
        
    def get_output_text(self):
        """获取输出区域的文本"""
        return self.output_area.toPlainText()
        
    def replace_last_line(self, text):
        """替换最后一行内容，用于动态更新进度"""
        # 获取当前文本
        current_text = self.output_area.toPlainText()
        
        # 如果当前没有文本，直接添加
        if not current_text:
            self.append_output(text)
            return
            
        # 分割成行
        lines = current_text.split('\n')
        
        # 替换最后一行
        if lines and lines[-1].strip():  # 确保最后一行不是空行
            lines[-1] = text
        else:
            # 如果最后一行是空行，添加新行
            lines.append(text)
            
        # 重新组合文本
        new_text = '\n'.join(lines)
        
        # 更新文本区域
        cursor_position = self.output_area.textCursor().position()
        self.output_area.setPlainText(new_text)
        
        # 滚动到底部
        self.output_area.verticalScrollBar().setValue(
            self.output_area.verticalScrollBar().maximum()
        )
