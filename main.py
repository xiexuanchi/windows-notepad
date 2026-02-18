import tkinter as tk
from tkinter import filedialog, messagebox
import sys

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("NotePad")
        
        # 创建底部状态栏
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 状态栏 (靠右对齐)
        self.status_bar = tk.Label(self.bottom_frame, text="Line: 1, Col: 0", anchor='e')
        self.status_bar.pack(side=tk.RIGHT, padx=5, pady=2)
        
        # 增强文本框：字号调整为 16，增加内边距、开启撤销功能
        self.text_area = tk.Text(
            self.root, 
            font=("Consolas", 16), 
            padx=15, 
            pady=15, 
            undo=True, 
            autoseparators=True
        )
        self.text_area.pack(fill=tk.BOTH, expand=1)
        
        # 绑定事件更新状态栏
        self.text_area.bind('<KeyRelease>', self.update_status)
        self.text_area.bind('<ButtonRelease>', self.update_status)
        self.update_status()  # 初始化
        
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        
        # 检测平台
        mod = 'Command' if sys.platform == 'darwin' else 'Control'
        accel_mod = 'Cmd' if sys.platform == 'darwin' else 'Ctrl'
        
        self.file_menu.add_command(label="New", command=self.new_file, accelerator=f"{accel_mod}+N")
        self.file_menu.add_command(label="Open", command=self.open_file, accelerator=f"{accel_mod}+O")
        self.file_menu.add_command(label="Save", command=self.save_file, accelerator=f"{accel_mod}+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_app, accelerator=f"{accel_mod}+Q")
        
        # 绑定快捷键
        self.root.bind(f'<{mod}-n>', lambda e: self.new_file())
        self.root.bind(f'<{mod}-o>', lambda e: self.open_file())
        self.root.bind(f'<{mod}-s>', lambda e: self.save_file())
        self.root.bind(f'<{mod}-q>', lambda e: self.exit_app())

    def new_file(self):
        # 检查是否有内容，提示清空
        if self.text_area.get(1.0, "end-1c"):
            if not messagebox.askyesno("NotePad", "Clear current text?"):
                return
        self.text_area.delete(1.0, tk.END)
        self.text_area.edit_reset() 
        self.update_status()

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, content)
                    self.text_area.edit_reset()
                    self.update_status()
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            try:
                # 使用 end-1c 避免保存时末尾多出一个空行
                content = self.text_area.get(1.0, "end-1c")
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")

    def exit_app(self):
        self.root.destroy()

    def update_status(self, event=None):
        try:
            line, col = self.text_area.index(tk.INSERT).split('.')
            self.status_bar.config(text=f"Line: {line}, Col: {col}")
        except:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x700") # 稍微调大了初始窗口大小以匹配大字体
    editor = TextEditor(root)
    root.mainloop()