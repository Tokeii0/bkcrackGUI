"""
控制面板组件 - 包含ZIP文件选择、明文文件选择和操作按钮等控件
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QComboBox, QPlainTextEdit, QFileDialog, QTabWidget,
    QFrame, QCheckBox, QSpinBox, QLineEdit, QGroupBox, QFormLayout
)
from .styles import (
    BUTTON_STYLE, SECONDARY_BUTTON_STYLE, LABEL_STYLE, 
    TEXT_BROWSER_STYLE, TEXT_EDIT_STYLE, COMBOBOX_STYLE,
    FRAME_STYLE, TAB_STYLE, CHECKBOX_STYLE
)

class ControlPanelComponent(QWidget):
    # 定义信号
    compressed_file_selected = Signal(str)
    plain_file_selected = Signal(str)
    get_zip_info_clicked = Signal()
    attack_clicked = Signal()
    decrypt_clicked = Signal()
    plain_name_changed = Signal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(15)
        
        # 创建选项卡
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet(TAB_STYLE)
        
        # 基本操作选项卡
        basic_tab = QWidget()
        tab_widget.addTab(basic_tab, "基本操作")
        
        # 高级选项选项卡
        advanced_tab = QWidget()
        tab_widget.addTab(advanced_tab, "高级选项")
        
        # 设置基本操作选项卡的布局
        self.setup_basic_tab(basic_tab)
        
        # 设置高级选项选项卡的布局
        self.setup_advanced_tab(advanced_tab)
        
        # 添加选项卡到主布局
        main_layout.addWidget(tab_widget)
        
        # 添加操作按钮
        self.setup_action_buttons(main_layout)
        
    def setup_basic_tab(self, tab):
        """设置基本操作选项卡"""
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        
        # 压缩包选择区域
        compressed_group = QGroupBox("加密压缩包")
        compressed_layout = QVBoxLayout(compressed_group)
        
        # 压缩包路径显示
        self.compressed_path = QPlainTextEdit()
        self.compressed_path.setReadOnly(True)
        self.compressed_path.setMaximumHeight(60)
        self.compressed_path.setPlaceholderText("请选择加密的ZIP压缩包")
        self.compressed_path.setStyleSheet(TEXT_EDIT_STYLE)
        
        # 压缩包选择按钮
        compressed_btn_layout = QHBoxLayout()
        self.select_compressed_btn = QPushButton("选择压缩包")
        self.select_compressed_btn.setStyleSheet(BUTTON_STYLE)
        self.get_zip_info_btn = QPushButton("查看压缩包信息")
        self.get_zip_info_btn.setStyleSheet(SECONDARY_BUTTON_STYLE)
        
        compressed_btn_layout.addWidget(self.select_compressed_btn)
        compressed_btn_layout.addWidget(self.get_zip_info_btn)
        
        compressed_layout.addWidget(self.compressed_path)
        compressed_layout.addLayout(compressed_btn_layout)
        
        # 压缩包内文件选择
        file_select_layout = QHBoxLayout()
        file_select_layout.addWidget(QLabel("压缩包内文件:"))
        self.plain_name_combo = QComboBox()
        self.plain_name_combo.setStyleSheet(COMBOBOX_STYLE)
        file_select_layout.addWidget(self.plain_name_combo, 1)  # 1是拉伸因子
        
        compressed_layout.addLayout(file_select_layout)
        layout.addWidget(compressed_group)
        
        # 明文文件选择区域
        plaintext_group = QGroupBox("明文文件")
        plaintext_layout = QVBoxLayout(plaintext_group)
        
        # 明文文件路径显示
        self.plain_path = QPlainTextEdit()
        self.plain_path.setReadOnly(True)
        self.plain_path.setMaximumHeight(60)
        self.plain_path.setPlaceholderText("请选择明文文件")
        self.plain_path.setStyleSheet(TEXT_EDIT_STYLE)
        
        # 明文文件选择按钮
        plain_btn_layout = QHBoxLayout()
        self.select_plain_btn = QPushButton("选择明文文件")
        self.select_plain_btn.setStyleSheet(BUTTON_STYLE)
        
        plain_btn_layout.addWidget(self.select_plain_btn)
        plain_btn_layout.addStretch(1)  # 添加弹性空间
        
        plaintext_layout.addWidget(self.plain_path)
        plaintext_layout.addLayout(plain_btn_layout)
        layout.addWidget(plaintext_group)
        
        # 密钥区域
        key_group = QGroupBox("密钥")
        key_layout = QVBoxLayout(key_group)
        
        # 密钥输入框
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("密钥将在攻击成功后自动填充")
        self.key_input.setStyleSheet(TEXT_EDIT_STYLE)
        
        key_layout.addWidget(self.key_input)
        layout.addWidget(key_group)
        
        # 连接信号和槽
        self.select_compressed_btn.clicked.connect(self.select_compressed_file)
        self.get_zip_info_btn.clicked.connect(self.get_zip_info_clicked.emit)
        self.select_plain_btn.clicked.connect(self.select_plain_file)
        self.plain_name_combo.currentIndexChanged.connect(self.plain_name_changed.emit)
        
    def setup_advanced_tab(self, tab):
        """设置高级选项选项卡"""
        layout = QVBoxLayout(tab)
        
        # 创建子选项卡
        advanced_tabs = QTabWidget()
        advanced_tabs.setStyleSheet(TAB_STYLE)
        
        # 基本选项子选项卡
        basic_options_tab = QWidget()
        advanced_tabs.addTab(basic_options_tab, "基本选项")
        
        # 暴力破解子选项卡
        bruteforce_tab = QWidget()
        advanced_tabs.addTab(bruteforce_tab, "暴力破解")
        
        # 恢复密码子选项卡
        recover_tab = QWidget()
        advanced_tabs.addTab(recover_tab, "恢复密码")
        
        # 设置基本选项子选项卡的布局
        self.setup_basic_options_tab(basic_options_tab)
        
        # 设置暴力破解子选项卡的布局
        self.setup_bruteforce_tab(bruteforce_tab)
        
        # 设置恢复密码子选项卡的布局
        self.setup_recover_tab(recover_tab)
        
        # 添加子选项卡到布局
        layout.addWidget(advanced_tabs)
        
    def setup_basic_options_tab(self, tab):
        """设置基本选项子选项卡"""
        layout = QFormLayout(tab)
        layout.setSpacing(10)
        
        # 偏移量选项
        offset_layout = QHBoxLayout()
        self.offset_checkbox = QCheckBox("启用偏移量")
        self.offset_checkbox.setStyleSheet(CHECKBOX_STYLE)
        self.offset_spinbox = QSpinBox()
        self.offset_spinbox.setRange(0, 1000000)
        self.offset_spinbox.setValue(0)
        self.offset_spinbox.setEnabled(False)
        self.offset_spinbox.setStyleSheet(TEXT_EDIT_STYLE)
        
        offset_layout.addWidget(self.offset_checkbox)
        offset_layout.addWidget(self.offset_spinbox)
        offset_layout.addStretch(1)
        
        # 截断大小选项
        truncate_layout = QHBoxLayout()
        self.truncate_checkbox = QCheckBox("启用截断大小")
        self.truncate_checkbox.setStyleSheet(CHECKBOX_STYLE)
        self.truncate_spinbox = QSpinBox()
        self.truncate_spinbox.setRange(1, 1000000)
        self.truncate_spinbox.setValue(1000)
        self.truncate_spinbox.setEnabled(False)
        self.truncate_spinbox.setStyleSheet(TEXT_EDIT_STYLE)
        
        truncate_layout.addWidget(self.truncate_checkbox)
        truncate_layout.addWidget(self.truncate_spinbox)
        truncate_layout.addStretch(1)
        
        # 多线程选项
        jobs_layout = QHBoxLayout()
        self.jobs_checkbox = QCheckBox("启用多线程")
        self.jobs_checkbox.setStyleSheet(CHECKBOX_STYLE)
        self.jobs_spinbox = QSpinBox()
        self.jobs_spinbox.setRange(1, 64)
        self.jobs_spinbox.setValue(4)
        self.jobs_spinbox.setEnabled(False)
        self.jobs_spinbox.setStyleSheet(TEXT_EDIT_STYLE)
        
        jobs_layout.addWidget(self.jobs_checkbox)
        jobs_layout.addWidget(self.jobs_spinbox)
        jobs_layout.addStretch(1)
        
        # 穷举所有解选项
        exhaustive_layout = QHBoxLayout()
        self.exhaustive_checkbox = QCheckBox("穷举所有解")
        self.exhaustive_checkbox.setStyleSheet(CHECKBOX_STYLE)
        
        exhaustive_layout.addWidget(self.exhaustive_checkbox)
        exhaustive_layout.addStretch(1)
        
        # 添加所有选项到布局
        layout.addRow("", offset_layout)
        layout.addRow("", truncate_layout)
        layout.addRow("", jobs_layout)
        layout.addRow("", exhaustive_layout)
        
        # 连接信号和槽
        self.offset_checkbox.stateChanged.connect(
            lambda state: self.offset_spinbox.setEnabled(state == Qt.Checked)
        )
        self.truncate_checkbox.stateChanged.connect(
            lambda state: self.truncate_spinbox.setEnabled(state == Qt.Checked)
        )
        self.jobs_checkbox.stateChanged.connect(
            lambda state: self.jobs_spinbox.setEnabled(state == Qt.Checked)
        )
        
    def setup_bruteforce_tab(self, tab):
        """设置暴力破解子选项卡"""
        layout = QFormLayout(tab)
        layout.setSpacing(10)
        
        # 字符集选择
        charset_layout = QVBoxLayout()
        self.charset_lowercase = QCheckBox("小写字母 (a-z)")
        self.charset_uppercase = QCheckBox("大写字母 (A-Z)")
        self.charset_digits = QCheckBox("数字 (0-9)")
        self.charset_special = QCheckBox("特殊字符 (!@#$...)")
        self.charset_custom = QLineEdit()
        self.charset_custom.setPlaceholderText("自定义字符集")
        
        self.charset_lowercase.setStyleSheet(CHECKBOX_STYLE)
        self.charset_uppercase.setStyleSheet(CHECKBOX_STYLE)
        self.charset_digits.setStyleSheet(CHECKBOX_STYLE)
        self.charset_special.setStyleSheet(CHECKBOX_STYLE)
        self.charset_custom.setStyleSheet(TEXT_EDIT_STYLE)
        
        charset_layout.addWidget(self.charset_lowercase)
        charset_layout.addWidget(self.charset_uppercase)
        charset_layout.addWidget(self.charset_digits)
        charset_layout.addWidget(self.charset_special)
        charset_layout.addWidget(self.charset_custom)
        
        # 密码长度范围
        length_layout = QHBoxLayout()
        self.min_length_spinbox = QSpinBox()
        self.min_length_spinbox.setRange(1, 20)
        self.min_length_spinbox.setValue(1)
        self.min_length_spinbox.setStyleSheet(TEXT_EDIT_STYLE)
        
        self.max_length_spinbox = QSpinBox()
        self.max_length_spinbox.setRange(1, 20)
        self.max_length_spinbox.setValue(8)
        self.max_length_spinbox.setStyleSheet(TEXT_EDIT_STYLE)
        
        length_layout.addWidget(QLabel("最小长度:"))
        length_layout.addWidget(self.min_length_spinbox)
        length_layout.addWidget(QLabel("最大长度:"))
        length_layout.addWidget(self.max_length_spinbox)
        length_layout.addStretch(1)
        
        # 添加所有选项到布局
        layout.addRow("字符集:", charset_layout)
        layout.addRow("密码长度:", length_layout)
        
    def setup_recover_tab(self, tab):
        """设置恢复密码子选项卡"""
        layout = QFormLayout(tab)
        layout.setSpacing(10)
        
        # 字符集选择
        charset_layout = QVBoxLayout()
        self.recover_charset_lowercase = QCheckBox("小写字母 (a-z)")
        self.recover_charset_uppercase = QCheckBox("大写字母 (A-Z)")
        self.recover_charset_digits = QCheckBox("数字 (0-9)")
        self.recover_charset_special = QCheckBox("特殊字符 (!@#$...)")
        self.recover_charset_custom = QLineEdit()
        self.recover_charset_custom.setPlaceholderText("自定义字符集")
        
        self.recover_charset_lowercase.setStyleSheet(CHECKBOX_STYLE)
        self.recover_charset_uppercase.setStyleSheet(CHECKBOX_STYLE)
        self.recover_charset_digits.setStyleSheet(CHECKBOX_STYLE)
        self.recover_charset_special.setStyleSheet(CHECKBOX_STYLE)
        self.recover_charset_custom.setStyleSheet(TEXT_EDIT_STYLE)
        
        charset_layout.addWidget(self.recover_charset_lowercase)
        charset_layout.addWidget(self.recover_charset_uppercase)
        charset_layout.addWidget(self.recover_charset_digits)
        charset_layout.addWidget(self.recover_charset_special)
        charset_layout.addWidget(self.recover_charset_custom)
        
        # 最大密码长度
        max_length_layout = QHBoxLayout()
        self.recover_max_length_spinbox = QSpinBox()
        self.recover_max_length_spinbox.setRange(1, 20)
        self.recover_max_length_spinbox.setValue(10)
        self.recover_max_length_spinbox.setStyleSheet(TEXT_EDIT_STYLE)
        
        max_length_layout.addWidget(QLabel("最大长度:"))
        max_length_layout.addWidget(self.recover_max_length_spinbox)
        max_length_layout.addStretch(1)
        
        # 添加所有选项到布局
        layout.addRow("字符集:", charset_layout)
        layout.addRow("密码长度:", max_length_layout)
        
    def setup_action_buttons(self, layout):
        """设置操作按钮"""
        buttons_layout = QHBoxLayout()
        
        # 攻击按钮
        self.attack_btn = QPushButton("开始攻击")
        self.attack_btn.setStyleSheet(BUTTON_STYLE)
        
        # 解密按钮
        self.decrypt_btn = QPushButton("解密文件")
        self.decrypt_btn.setStyleSheet(SECONDARY_BUTTON_STYLE)
        
        # 主题切换按钮
        self.theme_btn = QPushButton("切换主题")
        self.theme_btn.setStyleSheet(SECONDARY_BUTTON_STYLE)
        
        buttons_layout.addWidget(self.attack_btn)
        buttons_layout.addWidget(self.decrypt_btn)
        buttons_layout.addWidget(self.theme_btn)
        
        layout.addLayout(buttons_layout)
        
        # 连接信号和槽
        self.attack_btn.clicked.connect(self.attack_clicked.emit)
        self.decrypt_btn.clicked.connect(self.decrypt_clicked.emit)
        
    def select_compressed_file(self):
        """选择压缩包文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择加密的ZIP压缩包", "", "ZIP文件 (*.zip)"
        )
        if file_path:
            self.compressed_path.setPlainText(file_path)
            self.compressed_file_selected.emit(file_path)
            
    def select_plain_file(self):
        """选择明文文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择明文文件", "", "所有文件 (*)"
        )
        if file_path:
            self.plain_path.setPlainText(file_path)
            self.plain_file_selected.emit(file_path)
            
    def set_compressed_path(self, path):
        """设置压缩包路径"""
        self.compressed_path.setPlainText(path)
        
    def set_plain_path(self, path):
        """设置明文文件路径"""
        self.plain_path.setPlainText(path)
        
    def set_key(self, key):
        """设置密钥"""
        self.key_input.setText(key)
        
    def get_key(self):
        """获取密钥"""
        return self.key_input.text()
        
    def update_plain_names(self, names):
        """更新明文文件名称下拉框"""
        self.plain_name_combo.clear()
        for name in names:
            self.plain_name_combo.addItem(name)
            
    def get_selected_plain_name(self):
        """获取选中的明文文件名称"""
        return self.plain_name_combo.currentText()
        
    def get_advanced_options(self):
        """获取高级选项设置"""
        options = {
            "offset": self.offset_spinbox.value() if self.offset_checkbox.isChecked() else None,
            "truncate": self.truncate_spinbox.value() if self.truncate_checkbox.isChecked() else None,
            "jobs": self.jobs_spinbox.value() if self.jobs_checkbox.isChecked() else None,
            "exhaustive": self.exhaustive_checkbox.isChecked(),
            "bruteforce": {
                "enabled": any([
                    self.charset_lowercase.isChecked(),
                    self.charset_uppercase.isChecked(),
                    self.charset_digits.isChecked(),
                    self.charset_special.isChecked(),
                    self.charset_custom.text().strip()
                ]),
                "charset": self.get_bruteforce_charset(),
                "min_length": self.min_length_spinbox.value(),
                "max_length": self.max_length_spinbox.value()
            },
            "recover": {
                "enabled": any([
                    self.recover_charset_lowercase.isChecked(),
                    self.recover_charset_uppercase.isChecked(),
                    self.recover_charset_digits.isChecked(),
                    self.recover_charset_special.isChecked(),
                    self.recover_charset_custom.text().strip()
                ]),
                "charset": self.get_recover_charset(),
                "max_length": self.recover_max_length_spinbox.value()
            }
        }
        return options
        
    def get_bruteforce_charset(self):
        """获取暴力破解字符集"""
        charset = ""
        if self.charset_lowercase.isChecked():
            charset += "abcdefghijklmnopqrstuvwxyz"
        if self.charset_uppercase.isChecked():
            charset += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if self.charset_digits.isChecked():
            charset += "0123456789"
        if self.charset_special.isChecked():
            charset += "!@#$%^&*()-_=+[]{}|;:,.<>?/~`"
        charset += self.charset_custom.text()
        return charset
        
    def get_recover_charset(self):
        """获取恢复密码字符集"""
        charset = ""
        if self.recover_charset_lowercase.isChecked():
            charset += "abcdefghijklmnopqrstuvwxyz"
        if self.recover_charset_uppercase.isChecked():
            charset += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if self.recover_charset_digits.isChecked():
            charset += "0123456789"
        if self.recover_charset_special.isChecked():
            charset += "!@#$%^&*()-_=+[]{}|;:,.<>?/~`"
        charset += self.recover_charset_custom.text()
        return charset
