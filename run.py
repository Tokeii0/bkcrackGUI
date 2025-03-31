"""
BKCrack GUI - ZIP密码破解工具
主程序文件 - 整合所有UI组件和功能
"""

import os
import sys
import subprocess
import threading
from PySide6.QtCore import Qt, QThread, Signal, QObject
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox
from ui.main_ui import MainUI

# 创建一个工作线程类用于执行耗时操作
class WorkerThread(QThread):
    # 定义信号
    resultReady = Signal(str)
    progressUpdate = Signal(str)  # 进度更新信号
    
    def __init__(self, command):
        super().__init__()
        self.command = command
        self.process = None
        self.terminated = False
    
    def run(self):
        try:
            # 创建子进程，并捕获输出
            self.process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # 读取输出并发送进度更新信号
            output_lines = []
            for line in iter(self.process.stdout.readline, ''):
                if self.terminated:
                    break
                output_lines.append(line)
                self.progressUpdate.emit(line)
            
            # 等待进程结束
            self.process.wait()
            
            # 发送完整输出
            self.resultReady.emit(''.join(output_lines))
        except Exception as e:
            self.resultReady.emit(f"执行命令时出错: {str(e)}")
    
    def terminate(self):
        """终止线程和子进程"""
        self.terminated = True
        if self.process:
            self.process.terminate()
        super().terminate()


class BKCrackGUI(QObject):
    def __init__(self):
        super().__init__()
        # 启用调试输出
        self.debug = True
        # 初始化UI
        self.ui = MainUI()
        
        # 初始化变量
        self.compressedZipPath = ''  # 用于存储被加密的压缩包路径
        self.plainFilePath = ''  # 用于存储明文路径
        self.compressedFileNames = []  # 用于存储压缩包内的文件名列表
        self.plain_file_paths = {}  # 用于存储明文文件名和路径的映射
        
        # 初始化线程变量
        self.worker_thread = None
        
        # 加载明文文件
        self.loadPlainFiles()
        
        # 绑定事件处理函数
        self.bind()
        
    def bind(self):
        """绑定事件处理函数"""
        # 控制面板事件
        self.ui.control_panel.compressed_file_selected.connect(self.UpdateCompressedFilePath)
        self.ui.control_panel.plain_file_selected.connect(self.UpdatePlainFilePath)
        self.ui.control_panel.get_zip_info_clicked.connect(self.GetCompressedZipInfo)
        self.ui.control_panel.attack_clicked.connect(self.Attack)
        self.ui.control_panel.decrypt_clicked.connect(self.Decrypt)
        self.ui.control_panel.plain_name_changed.connect(self.onPlainNameChanged)
        
        # 输出面板事件
        self.ui.output_panel.clear_output_clicked.connect(self.clearOutput)
        self.ui.output_panel.save_output_clicked.connect(self.saveOutput)
        self.ui.output_panel.cancel_btn.clicked.connect(self.cancelOperation)
        
    def log(self, message):
        """输出调试信息"""
        if self.debug:
            print(f"[DEBUG] {message}")
            
    def UpdateCompressedFilePath(self, file_path):
        """更新压缩包路径"""
        self.compressedZipPath = file_path
        self.log(f"UpdateCompressedFilePath - 压缩包路径更新为: {file_path}")
        
    def UpdatePlainFilePath(self, file_path):
        """更新明文文件路径"""
        self.plainFilePath = file_path
        self.log(f"UpdatePlainFilePath - 明文路径更新为: {file_path}")
        self.ui.control_panel.set_plain_path(file_path)
        
    def loadPlainFiles(self):
        """加载plains目录下的所有文件"""
        # 获取plains目录路径
        plains_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plains")
        
        # 清空明文文件路径映射
        self.plain_file_paths = {}
        
        # 检查plains目录是否存在
        if not os.path.exists(plains_dir):
            self.log(f"loadPlainFiles - plains目录不存在，创建目录")
            os.makedirs(plains_dir)
            
        # 遍历plains目录下的所有文件
        if os.path.exists(plains_dir):
            for filename in os.listdir(plains_dir):
                file_path = os.path.join(plains_dir, filename)
                if os.path.isfile(file_path):
                    self.log(f"loadPlainFiles - 添加文件: {filename}, 路径: {file_path}")
                    # 存储文件名和路径的映射
                    self.plain_file_paths[filename] = file_path
                    
    def onPlainNameChanged(self, index):
        """当明文文件名称下拉框选择改变时触发"""
        if index >= 0:
            # 获取选中的文件名
            selected_filename = self.ui.control_panel.get_selected_plain_name()
            self.log(f"onPlainNameChanged - 选中的文件名: {selected_filename}")
            
            # 尝试自动匹配明文文件
            self.autoMatchPlainFile(selected_filename)
            
            # 如果有明文文件路径，则更新控制面板显示
            if self.plainFilePath:
                self.log(f"onPlainNameChanged - 使用已有的明文文件路径: {self.plainFilePath}")
            else:
                # 如果没有明文文件路径，提示用户选择
                self.ui.output_panel.set_output(f"已选择压缩包中的文件: {selected_filename}\n请选择对应的明文文件")
                
    def autoMatchPlainFile(self, filename):
        """根据压缩包中的文件名自动匹配明文文件"""
        if not filename:
            return
            
        # 获取文件扩展名
        file_ext = os.path.splitext(filename)[1].lower()
        if not file_ext:
            return
            
        # 去掉点号
        file_ext = file_ext[1:]
        
        self.log(f"autoMatchPlainFile - 文件扩展名: {file_ext}")
        
        # 在plains目录中查找匹配的明文文件
        for plain_filename, plain_path in self.plain_file_paths.items():
            self.log(f"autoMatchPlainFile - 检查文件: {plain_filename}")
            if f"plain_{file_ext}" in plain_filename.lower() or file_ext in plain_filename.lower():
                # 找到匹配的明文文件
                self.log(f"autoMatchPlainFile - 匹配到文件: {plain_filename}, 路径: {plain_path}")
                self.UpdatePlainFilePath(plain_path)
                return
                
    def GetCompressedZipInfo(self):
        """获取压缩包信息"""
        if not self.compressedZipPath:
            self.ui.output_panel.set_output("请先选择加密的ZIP压缩包")
            return
            
        # 禁用按钮，防止重复点击
        self.ui.control_panel.get_zip_info_btn.setEnabled(False)
        
        # 构建命令
        command = ["bkcrack.exe", "-L", self.compressedZipPath]
        print(command)
        
        # 显示取消按钮
        self.ui.output_panel.show_cancel_button()
        
        # 清空输出区域
        self.ui.output_panel.clear_output()
        self.ui.output_panel.append_output(f"正在获取压缩包信息...\n压缩包: {self.compressedZipPath}\n\n")
        
        # 创建并启动工作线程
        self.worker_thread = WorkerThread(command)
        self.worker_thread.resultReady.connect(self.handleZipInfoResult)
        self.worker_thread.progressUpdate.connect(self.updateProgress)
        self.worker_thread.start()
        
    def handleZipInfoResult(self, output):
        """处理压缩包信息结果"""
        # 重新启用按钮
        self.ui.control_panel.get_zip_info_btn.setEnabled(True)
        
        # 隐藏取消按钮
        self.ui.output_panel.hide_cancel_button()
        
        # 清空明文文件名称下拉框和文件名列表
        self.ui.control_panel.update_plain_names([])
        self.compressedFileNames = []
        
        # 解析输出，提取文件名
        if output:
            lines = output.split('\n')
            filenames = []
            
            # 使用与老版本相同的解析逻辑
            for line in lines:
                # 跳过标题行和空行
                if not line.strip() or "Index Encryption" in line or "-----" in line:
                    continue
                # 检查是否是文件信息行
                parts = line.strip().split()
                if len(parts) >= 7:  # 确保行有足够的部分
                    # 最后一个部分是文件名
                    filename = parts[-1]
                    filenames.append(filename)
                    self.log(f"handleZipInfoResult - 提取到文件名: {filename}")
            
            # 如果找到了文件名，添加到下拉框中
            if filenames:
                self.ui.control_panel.update_plain_names(filenames)
                self.compressedFileNames = filenames
                
                # 如果有文件，默认选择第一个
                if len(filenames) > 0:
                    self.log(f"handleZipInfoResult - 默认选择第一个文件: {filenames[0]}")
                    
                    # 自动匹配明文文件
                    self.autoMatchPlainFile(filenames[0])
                    
                    # 更新输出区域，提示用户选择明文文件
                    self.ui.output_panel.append_output(f"已从压缩包中提取到 {len(filenames)} 个文件\n请选择对应的明文文件")
            else:
                # 尝试使用另一种方式解析（查找"file name:"）
                for line in lines:
                    if "file name:" in line:
                        filename = line.split("file name:")[1].strip()
                        self.log(f"handleZipInfoResult - 提取到文件名: {filename}")
                        # 添加到明文文件名称下拉框和文件名列表
                        filenames.append(filename)
                
                if filenames:
                    self.ui.control_panel.update_plain_names(filenames)
                    self.compressedFileNames = filenames
                    
                    # 如果有文件，默认选择第一个
                    if len(filenames) > 0:
                        self.log(f"handleZipInfoResult - 默认选择第一个文件: {filenames[0]}")
                        
                        # 自动匹配明文文件
                        self.autoMatchPlainFile(filenames[0])
                        
                        # 更新输出区域，提示用户选择明文文件
                        self.ui.output_panel.append_output(f"已从压缩包中提取到 {len(filenames)} 个文件\n请选择对应的明文文件")
                else:
                    self.ui.output_panel.append_output("未能从压缩包中提取到文件名，请确认压缩包格式正确")
                    # 显示原始输出，帮助调试
                    self.ui.output_panel.append_output("\n\n原始输出：\n" + output)
        else:
            self.ui.output_panel.append_output("未能获取压缩包信息，请确认压缩包路径正确")
            
    def Attack(self):
        """执行攻击"""
        if not self.compressedZipPath:
            self.ui.output_panel.set_output("请先选择加密的ZIP压缩包")
            return
            
        if not self.plainFilePath:
            self.ui.output_panel.set_output("请先选择明文文件")
            return
            
        # 获取选中的压缩包内文件名
        plainname = self.ui.control_panel.get_selected_plain_name()
        if not plainname:
            self.ui.output_panel.set_output("请先选择压缩包内的文件")
            return
            
        self.log(f"Attack - 选择的压缩包内文件名: {plainname}")
        self.log(f"Attack - plainFilePath: {self.plainFilePath}")
        
        # 构建基本命令
        command = ["bkcrack.exe", "-C", self.compressedZipPath, "-c", plainname, "-p", self.plainFilePath]
        
        # 获取高级选项
        advanced_options = self.ui.control_panel.get_advanced_options()
        
        # 添加偏移量选项
        if advanced_options["offset"] is not None:
            command.extend(["-o", str(advanced_options["offset"])])
            
        # 添加截断大小选项
        if advanced_options["truncate"] is not None:
            command.extend(["-t", str(advanced_options["truncate"])])
            
        # 添加多线程选项
        if advanced_options["jobs"] is not None:
            command.extend(["-j", str(advanced_options["jobs"])])
            
        # 添加穷举所有解选项
        if advanced_options["exhaustive"]:
            command.append("-e")
            
        # 检查是否是暴力破解或恢复密码模式
        if advanced_options["bruteforce"]["enabled"] and self.ui.control_panel.get_key():
            # 暴力破解模式
            keys = self.ui.control_panel.get_key().split()
            if len(keys) >= 3:
                command = ["bkcrack.exe", "-C", self.compressedZipPath, "-k"]
                command.extend(keys[:3])
                command.extend(["-b", advanced_options["bruteforce"]["charset"]])
                command.extend(["-l", str(advanced_options["bruteforce"]["min_length"]), str(advanced_options["bruteforce"]["max_length"])])
        elif advanced_options["recover"]["enabled"] and self.ui.control_panel.get_key():
            # 恢复密码模式
            keys = self.ui.control_panel.get_key().split()
            if len(keys) >= 3:
                command = ["bkcrack.exe", "-C", self.compressedZipPath, "-k"]
                command.extend(keys[:3])
                command.extend(["-r", advanced_options["recover"]["charset"], str(advanced_options["recover"]["max_length"])])
                
        # 禁用按钮，防止重复点击
        self.ui.control_panel.attack_btn.setEnabled(False)
        
        # 显示命令
        self.log(f"执行命令: {command}")
        self.ui.output_panel.set_output(f"执行命令: {command} \n")
        
        # 显示取消按钮
        self.ui.output_panel.show_cancel_button()
        
        # 清空输出区域
        self.ui.output_panel.clear_output()
        self.ui.output_panel.append_output(f"开始攻击...\n压缩包: {self.compressedZipPath}\n明文文件: {self.plainFilePath}\n压缩包内文件: {plainname}\n\n")
        
        # 创建并启动工作线程
        self.worker_thread = WorkerThread(command)
        self.worker_thread.resultReady.connect(self.handleAttackResult)
        self.worker_thread.progressUpdate.connect(self.updateProgress)
        self.worker_thread.start()
        
    def handleAttackResult(self, output):
        """处理攻击结果"""
        # 重新启用按钮
        self.ui.control_panel.attack_btn.setEnabled(True)
        
        # 隐藏取消按钮
        self.ui.output_panel.hide_cancel_button()
        
        # 显示输出
        self.ui.output_panel.append_output(output)
        
        # 提取密钥
        keys = []
        lines = output.split('\n')
        
        # 首先尝试查找"Keys:"格式
        for line in lines:
            if "Keys:" in line:
                # 提取"Keys:"后面的内容
                keys_part = line.split("Keys:")[1].strip()
                potential_keys = keys_part.split()
                
                # 验证是否有3个可能的十六进制数
                if len(potential_keys) >= 3:
                    try:
                        # 验证是否为十六进制数
                        for i in range(3):
                            int(potential_keys[i], 16)
                        keys = potential_keys[:3]
                        self.log(f"handleAttackResult - 从'Keys:'格式提取到密钥: {keys}")
                        break
                    except ValueError:
                        # 不是有效的十六进制数，继续查找
                        pass
        
        # 如果没有找到"Keys:"格式，尝试查找"Keys"格式
        if not keys:
            for line in lines:
                if line.strip().startswith("Keys "):
                    potential_keys = line.strip().split()
                    
                    # 去掉"Keys"这个词
                    if potential_keys[0].lower() == "keys":
                        potential_keys = potential_keys[1:]
                    
                    # 验证是否有3个可能的十六进制数
                    if len(potential_keys) >= 3:
                        try:
                            # 验证是否为十六进制数
                            for i in range(3):
                                int(potential_keys[i], 16)
                            keys = potential_keys[:3]
                            self.log(f"handleAttackResult - 从'Keys '格式提取到密钥: {keys}")
                            break
                        except ValueError:
                            # 不是有效的十六进制数，继续查找
                            pass
        
        # 如果仍然没有找到，尝试直接查找3个连续的十六进制数
        if not keys:
            for line in lines:
                words = line.strip().split()
                if len(words) >= 3:
                    potential_keys = []
                    for word in words:
                        try:
                            # 尝试将单词解析为十六进制数
                            int(word, 16)
                            # 检查长度是否为8位十六进制数（32位整数）
                            if len(word) == 8:
                                potential_keys.append(word)
                                # 如果找到3个连续的十六进制数，就停止
                                if len(potential_keys) == 3:
                                    keys = potential_keys
                                    self.log(f"handleAttackResult - 从连续十六进制数格式提取到密钥: {keys}")
                                    break
                        except ValueError:
                            # 不是十六进制数，重置计数
                            potential_keys = []
                    
                    if len(potential_keys) == 3:
                        break
        
        # 如果找到了有效的密钥
        if len(keys) == 3:
            # 更新密钥输入框
            key_str = f"{keys[0]} {keys[1]} {keys[2]}"
            self.ui.control_panel.set_key(key_str)
            self.log(f"handleAttackResult - 提取到密钥: {key_str}")
            
            # 提示用户可以解密文件
            self.ui.output_panel.append_output("\n\n攻击成功！已获取密钥，可以使用\"解密文件\"按钮解密压缩包")
        else:
            self.ui.output_panel.append_output("\n\n未能提取到有效的密钥，请检查明文文件是否正确")
            # 打印调试信息
            self.log(f"handleAttackResult - 未能提取到有效的密钥，原始输出: {output}")
            
    def Decrypt(self):
        """解密文件"""
        if not self.compressedZipPath:
            self.ui.output_panel.set_output("请先选择加密的ZIP压缩包")
            return
            
        # 获取密钥
        key = self.ui.control_panel.get_key()
        if not key:
            self.ui.output_panel.set_output("请先获取密钥")
            return
            
        # 获取解密后的文件保存路径
        save_path, _ = QFileDialog.getSaveFileName(
            self.ui, "保存解密后的ZIP文件", "", "ZIP文件 (*.zip)"
        )
        if not save_path:
            return
            
        # 构建命令
        keys = key.split()
        if len(keys) < 3:
            self.ui.output_panel.set_output("密钥格式不正确，应为三个十六进制数")
            return
            
        command = ["bkcrack.exe", "-C", self.compressedZipPath, "-k"]
        command.extend(keys[:3])
        command.extend(["-U", save_path, "rockyou"])
        
        # 禁用按钮，防止重复点击
        self.ui.control_panel.decrypt_btn.setEnabled(False)
        
        # 显示命令
        self.log(f"执行命令: {command}")
        self.ui.output_panel.set_output(f"执行命令: {command} \n")
        
        # 显示取消按钮
        self.ui.output_panel.show_cancel_button()
        
        # 清空输出区域
        self.ui.output_panel.clear_output()
        self.ui.output_panel.append_output(f"开始解密...\n压缩包: {self.compressedZipPath}\n密钥: {key}\n输出: {save_path}\n\n")
        
        # 创建并启动工作线程
        self.worker_thread = WorkerThread(command)
        self.worker_thread.resultReady.connect(self.handleDecryptResult)
        self.worker_thread.progressUpdate.connect(self.updateProgress)
        self.worker_thread.start()
        
    def handleDecryptResult(self, output):
        """处理解密结果"""
        # 重新启用按钮
        self.ui.control_panel.decrypt_btn.setEnabled(True)
        
        # 隐藏取消按钮
        self.ui.output_panel.hide_cancel_button()
        
        # 显示输出
        self.ui.output_panel.append_output(output)
        
        # 检查是否成功
        if "Wrote unlocked archive" in output:
            self.ui.output_panel.append_output("\n\n解密成功！")
        else:
            self.ui.output_panel.append_output("\n\n解密失败，请检查密钥是否正确")
            
    def updateProgress(self, line):
        """更新进度信息"""
        # 将新行添加到输出区域
        self.ui.output_panel.append_output(line)
        
    def clearOutput(self):
        """清空输出区域"""
        self.ui.output_panel.clear_output()
        
    def saveOutput(self):
        """保存输出内容到文件"""
        # 获取输出内容
        output_text = self.ui.output_panel.get_output_text()
        if not output_text:
            return
            
        # 获取保存路径
        save_path, _ = QFileDialog.getSaveFileName(
            self.ui, "保存输出内容", "", "文本文件 (*.txt)"
        )
        if not save_path:
            return
            
        # 保存内容到文件
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(output_text)
            self.ui.output_panel.append_output(f"\n\n输出内容已保存到: {save_path}")
        except Exception as e:
            self.ui.output_panel.append_output(f"\n\n保存输出内容失败: {str(e)}")
            
    def cancelOperation(self):
        """取消当前操作"""
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.terminate()
            self.ui.output_panel.append_output("\n\n操作已取消")
            self.ui.output_panel.hide_cancel_button()
            
            # 重新启用按钮
            self.ui.control_panel.get_zip_info_btn.setEnabled(True)
            self.ui.control_panel.attack_btn.setEnabled(True)
            self.ui.control_panel.decrypt_btn.setEnabled(True)
            
    def show(self):
        """显示主窗口"""
        self.ui.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BKCrackGUI()
    window.show()
    sys.exit(app.exec())
