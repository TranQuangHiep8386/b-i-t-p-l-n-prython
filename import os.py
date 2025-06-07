import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import mimetypes

class FileManagerApp:
    def __init__(self, root):
        """Khởi tạo ứng dụng GUI với cửa sổ chính và các thành phần giao diện."""
        self.root = root
        self.root.title("Trình Quản Lý Thư Mục")
        self.root.geometry("700x500")  # Kích thước cửa sổ lớn hơn cho giao diện rõ ràng

        # Biến lưu đường dẫn thư mục hiện tại
        self.current_directory = ""
        # Danh sách các phần mở rộng được phép
        self.allowed_extensions = ('.txt', '.py', '.jpg')

        # Tạo frame chính để chứa các widget
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)  # Cho phép frame mở rộng theo chiều ngang
        self.root.rowconfigure(0, weight=1)     # Cho phép frame mở rộng theo chiều dọc

        # Label hiển thị đường dẫn thư mục hiện tại
        self.path_label = ttk.Label(self.main_frame, text="Chưa chọn thư mục")
        self.path_label.grid(row=0, column=0, columnspan=2, pady=5, sticky=tk.W)

        # Nút chọn thư mục
        self.select_button = ttk.Button(self.main_frame, text="Chọn Thư Mục", command=self.select_directory)
        self.select_button.grid(row=1, column=0, pady=10, sticky=tk.W)

        # Treeview để hiển thị danh sách file
        self.tree = ttk.Treeview(self.main_frame, columns=("File", "Type", "Path"), show="headings")
        self.tree.heading("File", text="Tên File")
        self.tree.heading("Type", text="Loại File")
        self.tree.heading("Path", text="Đường Dẫn")
        self.tree.column("File", width=250, anchor=tk.W)
        self.tree.column("Type", width=150, anchor=tk.CENTER)
        self.tree.column("Path", width=300, anchor=tk.W)
        self.tree.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Thêm scrollbar dọc cho Treeview
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=2, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Nút mở file
        self.open_button = ttk.Button(self.main_frame, text="Mở File", command=self.open_file)
        self.open_button.grid(row=3, column=0, pady=10, sticky=tk.W)

        # Bind sự kiện double-click để mở file
        self.tree.bind("<Double-1>", self.on_double_click)

        # Cấu hình trọng số cho hàng và cột trong main_frame
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(2, weight=1)

    def select_directory(self):
        """Mở hộp thoại chọn thư mục và cập nhật danh sách file."""
        try:
            directory = filedialog.askdirectory(title="Chọn Thư Mục")
            if directory:
                self.current_directory = directory
                self.path_label.config(text=f"Thư mục: {directory}")
                self.show_files()
            else:
                self.path_label.config(text="Chưa chọn thư mục")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở thư mục: {str(e)}")
            self.path_label.config(text="Chưa chọn thư mục")

    def show_files(self):
        """Quét thư mục và hiển thị các file .txt, .py, .jpg trong Treeview."""
        # Xóa toàn bộ nội dung hiện tại của Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not self.current_directory:
            return

        try:
            # Duyệt qua tất cả các file trong thư mục
            for filename in os.listdir(self.current_directory):
                file_path = os.path.join(self.current_directory, filename)
                # Kiểm tra xem có phải là file (không phải thư mục)
                if os.path.isfile(file_path):
                    # Lấy phần mở rộng của file
                    _, ext = os.path.splitext(filename)
                    # Chỉ hiển thị các file có phần mở rộng được phép
                    if ext.lower() in self.allowed_extensions:
                        # Lấy loại MIME của file
                        file_type, _ = mimetypes.guess_type(filename)
                        file_type = file_type if file_type else "Không xác định"
                        # Thêm file vào Treeview
                        self.tree.insert("", tk.END, values=(filename, file_type, file_path))
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "Thư mục không tồn tại!")
            self.path_label.config(text="Chưa chọn thư mục")
        except PermissionError:
            messagebox.showerror("Lỗi", "Không có quyền truy cập thư mục!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi liệt kê file: {str(e)}")

    def open_file(self):
        """Mở file được chọn bằng chương trình mặc định."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một file để mở!")
            return

        try:
            # Lấy đường dẫn file từ cột Path của Treeview
            file_path = self.tree.item(selected_item)["values"][2]
            os.startfile(file_path)  # Mở file bằng chương trình mặc định
        except FileNotFoundError:
            messagebox.showerror("Lỗi", "File không tồn tại!")
        except OSError as e:
            messagebox.showerror("Lỗi", f"Không thể mở file: {str(e)}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi không xác định: {str(e)}")

    def on_double_click(self, event):
        """Xử lý sự kiện double-click để mở file."""
        self.open_file()

if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()