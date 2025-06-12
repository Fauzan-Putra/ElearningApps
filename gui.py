import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from PIL import Image, ImageTk
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import data
import managers
import models

class ElearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aksanta - E-Learning Platform")
        self.root.geometry("900x700")
        self.root.configure(bg="#e6ecf0")
        self.store = data.CSVDataStore()
        self.um = managers.UserManager(self.store)
        self.am = managers.ArticleManager(self.store)
        self.qpm = managers.QuizPackageManager(self.store)
        self.qm = managers.QuestionManager(self.store)
        self.pm = managers.ProgressManager(self.store)
        self.current_user = None
        self.current_class_code = None
        self.setup_styles()
        self.show_login()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("Round.TButton", font=("Helvetica", 12), padding=10, background="#1E90FF", foreground="white")
        self.style.map("Round.TButton", background=[('active', '#1565C0'), ('!active', '#1E90FF')], foreground=[('active', 'white'), ('!active', 'white')])
        self.style.configure("TLabel", font=("Helvetica", 14), background="#e6ecf0", foreground="#2c3e50")
        self.style.configure("TEntry", font=("Helvetica", 14), padding=10, relief="flat", background="#ffffff", foreground="#2c3e50")
        self.style.configure("TScrolledText", font=("Helvetica", 14), padding=10, relief="flat", background="#ffffff", foreground="#2c3e50")
        self.style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"), background="#3498db", foreground="white")
        self.style.configure("Treeview", font=("Helvetica", 12), rowheight=30, background="#ffffff", foreground="#2c3e50")
        self.style.configure("TFrame", background="#e6ecf0")
        self.style.map("Treeview", background=[('selected', '#3498db')], foreground=[('selected', 'white')])

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_scrollable_frame(self):
        canvas = tk.Canvas(self.root, bg="#e6ecf0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        frame = ttk.Frame(canvas, padding=30, style="TFrame")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas_frame = canvas.create_window((0, 0), window=frame, anchor="nw")
        def configure_canvas(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas_width = event.width
            canvas.itemconfig(canvas_frame, width=canvas_width)
        def configure_frame(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.bind("<Configure>", configure_canvas)
        frame.bind("<Configure>", configure_frame)
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        return frame

    def show_login(self):
        self.clear_frame()
        
        primary_blue = "#1E90FF"
        light_blue = "#87CEFA"
        white = "#FFFFFF"

        self.canvas = tk.Canvas(self.root, bg=primary_blue, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_arc(0, 0, 900, 600, start=0, extent=180, fill=primary_blue, outline="")

        self.canvas.create_oval(100, 50, 150, 100, fill=light_blue, outline="")
        self.canvas.create_oval(400, 70, 470, 140, fill=light_blue, outline="")
        self.canvas.create_oval(700, 40, 740, 80, fill=light_blue, outline="")

        self.canvas.create_text(450, 150, text="Selamat datang di E-Learning Platform", font=("Helvetica", 20), fill=white)
        self.canvas.create_text(450, 220, text="AKSANTA", font=("Helvetica", 56, "bold"), fill=white)

        try:
            self.icon_image = ImageTk.PhotoImage(Image.open("laptop-book-icon.png").resize((100, 100)))
            self.icon_label = tk.Label(self.root, image=self.icon_image, bg=white)
            self.icon_label.place(relx=0.5, rely=0.5, anchor="center")
        except FileNotFoundError:
            self.icon_label = tk.Label(self.root, text="[Ikon Tidak Ditemukan]", font=("Helvetica", 14), bg=white, fg="#2c3e50")
            self.icon_label.place(relx=0.5, rely=0.5, anchor="center")

        self.button_frame = tk.Frame(self.root, bg=white)
        self.button_frame.pack(side="bottom", fill="x", pady=20)

        self.login_button = tk.Button(self.button_frame, text="Login", font=("Helvetica", 12), bg=primary_blue, fg=white, relief="flat", padx=20, pady=10, command=self.show_login_form)
        self.login_button.pack(side="left", expand=True)

        self.register_button = tk.Button(self.button_frame, text="Register", font=("Helvetica", 12), bg=primary_blue, fg=white, relief="flat", padx=20, pady=10, command=self.show_register)
        self.register_button.pack(side="left", expand=True)

        self.leave_button = tk.Button(self.button_frame, text="Leave", font=("Helvetica", 12), bg=primary_blue, fg=white, relief="flat", padx=20, pady=10, command=self.root.quit)
        self.leave_button.pack(side="left", expand=True)

    def show_login_form(self):
        self.clear_frame()
        frame = self.create_scrollable_frame()
        ttk.Label(frame, text="Selamat datang di Aksanta", font=("Helvetica", 24, "bold")).pack(pady=30)
        ttk.Label(frame, text="Username").pack()
        username_entry = ttk.Entry(frame, style="TEntry")
        username_entry.pack(pady=10, padx=20, fill="x")
        ttk.Label(frame, text="Password").pack()
        password_entry = ttk.Entry(frame, show="*", style="TEntry")
        password_entry.pack(pady=10, padx=20, fill="x")
        button_frame = ttk.Frame(frame, style="TFrame")
        button_frame.pack(pady=20)
        ttk.Button(button_frame, text="Login", command=lambda: self.handle_login(username_entry.get(), password_entry.get()), style="Round.TButton").pack(side="left", padx=10)
        ttk.Button(button_frame, text="Kembali", command=self.show_login, style="Round.TButton").pack(side="left", padx=10)

    def handle_login(self, username, password):
        if not username.strip() or not password.strip():
            messagebox.showerror("Error", "Username dan password tidak boleh kosong.")
            return
        user = self.um.login(username, password)
        if user:
            self.current_user = user
            if user.role == 'guru':
                self.show_teacher_menu()
            else:
                self.show_student_menu()
        else:
            messagebox.showerror("Error", "Username atau password salah.")

    def show_register(self):
        self.clear_frame()
        frame = self.create_scrollable_frame()
        ttk.Label(frame, text="Registrasi", font=("Helvetica", 20, "bold")).pack(pady=30)
        ttk.Label(frame, text="Username").pack()
        username_entry = ttk.Entry(frame, style="TEntry")
        username_entry.pack(pady=10, padx=20, fill="x")
        ttk.Label(frame, text="Password").pack()
        password_entry = ttk.Entry(frame, show="*", style="TEntry")
        password_entry.pack(pady=10, padx=20, fill="x")
        ttk.Label(frame, text="Pilih Role").pack(pady=10)
        role_var = tk.StringVar(value="murid")
        role_frame = ttk.Frame(frame, style="TFrame")
        role_frame.pack(pady=10)
        ttk.Radiobutton(role_frame, text="Guru", value="guru", variable=role_var).pack(side="left", padx=10)
        ttk.Radiobutton(role_frame, text="Murid", value="murid", variable=role_var).pack(side="left", padx=10)
        class_name_frame = ttk.Frame(frame, style="TFrame")
        class_name_label = ttk.Label(class_name_frame, text="Nama Kelas")
        class_name_entry_var = tk.StringVar()
        class_name_entry_widget = ttk.Entry(class_name_frame, style="TEntry", textvariable=class_name_entry_var)

        def update_class_field(*args):
            if role_var.get() == 'guru':
                class_name_frame.pack(pady=10)
                class_name_label.pack()
                class_name_entry_widget.pack(pady=5, padx=20, fill="x")
            else:
                class_name_entry_widget.pack_forget()
                class_name_label.pack_forget()
                class_name_frame.pack_forget()
                class_name_entry_var.set("")

        role_var.trace("w", update_class_field)
        update_class_field()

        button_frame = ttk.Frame(frame, style="TFrame")
        button_frame.pack(pady=15)
        ttk.Button(button_frame, text="Register", command=lambda: self.handle_register(
            username_entry.get(), password_entry.get(), role_var.get(), class_name_entry_var.get()), style="Round.TButton").pack(side="left", padx=10)
        ttk.Button(button_frame, text="Kembali", command=self.show_login, style="Round.TButton").pack(side="left", padx=10)

    def handle_register(self, username, password, role, class_name):
        if not username.strip():
            messagebox.showerror("Error", "Username tidak boleh kosong.")
            return
        if not password.strip():
            messagebox.showerror("Error", "Password tidak boleh kosong.")
            return
        if role not in ['guru', 'murid']:
            messagebox.showerror("Error", "Role tidak valid.")
            return
        if role == 'guru' and (not class_name or not class_name.strip()):
            messagebox.showerror("Error", "Nama kelas tidak boleh kosong untuk guru.")
            return
        success, message_or_code = self.um.register(username, password, role, class_name if role == 'guru' else None)
        if success:
            info_message = "Registrasi berhasil!"
            if role == 'guru' and message_or_code:
                info_message += f" Kode kelas: {message_or_code}"
            messagebox.showinfo("Sukses", info_message)
            self.show_login()
        else:
            messagebox.showerror("Error", message_or_code)

    def show_teacher_menu(self):
        self.clear_frame()
        frame = self.create_scrollable_frame()
        ttk.Label(frame, text=f"Selamat datang, Guru {self.current_user.username}", font=("Helvetica", 20, "bold")).pack(pady=20)
        if self.current_user.class_codes:
             ttk.Label(frame, text=f"Kode Kelas: {self.current_user.class_codes[0]}").pack(pady=10)
        else:
             ttk.Label(frame, text="Anda belum membuat kelas. Silakan hubungi admin jika ini adalah kesalahan.").pack(pady=10)

        button_frame = ttk.Frame(frame, style="TFrame")
        button_frame.pack(pady=20, padx=50, fill="x", anchor="center") 
        
        ttk.Button(button_frame, text="Kelola Artikel", command=self.show_manage_articles, style="Round.TButton").pack(fill="x", pady=5)
        ttk.Button(button_frame, text="Kelola Paket Soal", command=self.show_manage_quizzes, style="Round.TButton").pack(fill="x", pady=5)
        ttk.Button(button_frame, text="Lihat Statistik", command=self.show_statistics, style="Round.TButton").pack(fill="x", pady=5)
        ttk.Button(button_frame, text="Logout", command=self.show_login, style="Round.TButton").pack(fill="x", pady=5)

    def show_manage_articles(self):
        self.clear_frame()
        frame = self.create_scrollable_frame()
        ttk.Label(frame, text="Kelola Artikel", font=("Helvetica", 20, "bold")).pack(pady=20)
        tree = ttk.Treeview(frame, columns=("Title",), show="headings")
        tree.heading("Title", text="Judul Artikel")
        tree.pack(fill="both", expand=True, pady=10, padx=20)
        if self.current_user.class_codes:
            articles = self.am.list(self.current_user.class_codes[0])
            for art in articles:
                tree.insert("", "end", values=(art.title,))
        else:
            ttk.Label(frame, text="Tidak ada kelas terdaftar untuk guru ini.").pack(pady=10)

        button_frame = ttk.Frame(frame, style="TFrame")
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Tambah Artikel", command=self.show_add_article, style="Round.TButton").pack(side="left", padx=10)
        ttk.Button(button_frame, text="Edit Artikel", command=lambda: self.show_edit_article(tree), style="Round.TButton").pack(side="left", padx=10)
        ttk.Button(button_frame, text="Hapus Artikel", command=lambda: self.delete_article(tree), style="Round.TButton").pack(side="left", padx=10)
        ttk.Button(frame, text="Kembali", command=self.show_teacher_menu, style="Round.TButton").pack(pady=10)

    def show_add_article(self):
        self.clear_frame()
        frame = self.create_scrollable_frame()
        ttk.Label(frame, text="Tambah Artikel", font=("Helvetica", 20, "bold")).pack(pady=20)
        ttk.Label(frame, text="Judul").pack()
        title_entry = ttk.Entry(frame, style="TEntry")
        title_entry.pack(pady=10, padx=20, fill="x")
        ttk.Label(frame, text="Isi Artikel").pack()
        text_entry = scrolledtext.ScrolledText(frame, height=12, font=("Helvetica", 14), relief="flat", background="#ffffff", foreground="#2c3e50")
        text_entry.pack(pady=10, padx=20, fill="both", expand=True)

        def browse_image():
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])
            if file_path:
                cursor_pos = text_entry.index(tk.INSERT)
                text_entry.insert(cursor_pos, f"[Image: {file_path}]")

        ttk.Button(frame, text="Sisipkan Gambar", command=browse_image, style="Round.TButton").pack(pady=10)
        
        button_frame_bottom = ttk.Frame(frame, style="TFrame")
        button_frame_bottom.pack(pady=10)
        ttk.Button(button_frame_bottom, text="Simpan", command=lambda: self.confirm_article(title_entry.get(), text_entry.get("1.0", tk.END+"-1c")), style="Round.TButton").pack(side="left", padx=10)
        ttk.Button(frame, text="Kembali", command=self.show_manage_articles, style="Round.TButton").pack(pady=10)

    def confirm_article(self, title, text):
        if not title.strip() or not text.strip():
            messagebox.showerror("Error", "Judul dan isi artikel tidak boleh kosong.")
            return
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menyimpan artikel ini?"):
            self.save_article(title, text)

    def save_article(self, title, text):
        if not self.current_user.class_codes:
            messagebox.showerror("Error", "Guru tidak memiliki kelas terdaftar.")
            return
        self.am.create(self.current_user.class_codes[0], title, text, image_path=None)
        messagebox.showinfo("Sukses", "Artikel dibuat!")
        self.show_manage_articles()

    def show_edit_article(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Pilih artikel terlebih dahulu.")
            return
        
        title_from_tree = tree.item(selected[0])["values"][0]
        if not self.current_user.class_codes:
            messagebox.showerror("Error", "Guru tidak memiliki kelas terdaftar.")
            return

        articles = self.am.list(self.current_user.class_codes[0])
        article = next((a for a in articles if a.title == title_from_tree), None)
        
        if not article:
            messagebox.showerror("Error", "Artikel tidak ditemukan.")
            return

        self.clear_frame()
        frame = self.create_scrollable_frame()
        ttk.Label(frame, text="Edit Artikel", font=("Helvetica", 20, "bold")).pack(pady=20)
        
        ttk.Label(frame, text="Judul").pack()
        title_entry = ttk.Entry(frame, style="TEntry")
        title_entry.insert(0, article.title)
        title_entry.pack(pady=10, padx=20, fill="x")
        
        ttk.Label(frame, text="Isi Artikel").pack()
        text_entry = scrolledtext.ScrolledText(frame, height=12, font=("Helvetica", 14), relief="flat", background="#ffffff", foreground="#2c3e50")
        text_entry.insert("1.0", article.text)
        text_entry.pack(pady=10, padx=20, fill="both", expand=True)

        def browse_image():
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])
            if file_path:
                cursor_pos = text_entry.index(tk.INSERT)
                text_entry.insert(cursor_pos, f"[Image: {file_path}]")
        
        ttk.Button(frame, text="Sisipkan Gambar", command=browse_image, style="Round.TButton").pack(pady=10)
        
        button_frame_bottom = ttk.Frame(frame, style="TFrame")
        button_frame_bottom.pack(pady=10)
        
        ttk.Button(button_frame_bottom, text="Simpan", command=lambda: self.confirm_edit_article(article.id, title_entry.get(), text_entry.get("1.0", tk.END+"-1c")), style="Round.TButton").pack(side="left", padx=10)
        ttk.Button(frame, text="Kembali", command=self.show_manage_articles, style="Round.TButton").pack(pady=10)

    def confirm_edit_article(self, art_id, title, text):
        if not title.strip() or not text.strip():
            messagebox.showerror("Error", "Judul dan isi artikel tidak boleh kosong.")
            return
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin memperbarui artikel ini?"):
            self.update_article(art_id, title, text)

    def update_article(self, art_id, title, text):
        self.am.update(art_id, title=title, text=text, image_path=None)
        messagebox.showinfo("Sukses", "Artikel diperbarui!")
        self.show_manage_articles()

    def delete_article(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Pilih artikel terlebih dahulu.")
            return
        
        title = tree.item(selected[0])["values"][0]
        if not self.current_user.class_codes:
            messagebox.showerror("Error", "Guru tidak memiliki kelas terdaftar.")
            return

        articles = self.am.list(self.current_user.class_codes[0])
        article = next((a for a in articles if a.title == title), None)
        
        if article and messagebox.askyesno("Konfirmasi", f"Apakah Anda yakin ingin menghapus artikel '{article.title}'?"):
            self.am.delete(article.id)
            messagebox.showinfo("Sukses", "Artikel dihapus!")
            self.show_manage_articles()
        elif not article:
            messagebox.showerror("Error", "Artikel tidak ditemukan untuk dihapus.")

    def show_manage_quizzes(self):
        self.clear_frame()
        frame = self.create_scrollable_frame()
        ttk.Label(frame, text="Kelola Paket Soal", font=("Helvetica", 20, "bold")).pack(pady=20)
        tree = ttk.Treeview(frame, columns=("Name", "Timer"), show="headings")
        tree.heading("Name", text="Nama Paket")
        tree.heading("Timer", text="Timer (detik)")
        tree.pack(fill="both", expand=True, pady=10, padx=20)
        
        if self.current_user.class_codes:
            packages = self.qpm.list(self.current_user.class_codes[0])
            for pkg in packages:
                tree.insert("", "end", values=(pkg.package_name, pkg.total_timer))
        else:
            ttk.Label(frame, text="Tidak ada kelas terdaftar untuk guru ini.").pack(pady=10)

        button_frame = ttk.Frame(frame, style="TFrame")
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Tambah Paket Soal", command=self.show_add_quiz_package, style="Round.TButton").pack(side="left", padx=10)
        ttk.Button(button_frame, text="Edit Paket Soal", command=lambda: self.show_edit_quiz_package_contents(tree), style="Round.TButton").pack(side="left", padx=10)
        ttk.Button(button_frame, text="Hapus Paket Soal", command=lambda: self.delete_quiz_package(tree), style="Round.TButton").pack(side="left", padx=10)
        ttk.Button(frame, text="Kembali", command=self.show_teacher_menu, style="Round.TButton").pack(pady=10)

    def show_add_quiz_package(self):
        self.clear_frame()
        frame = self.create_scrollable_frame()
        ttk.Label(frame, text="Tambah Paket Soal Baru", font=("Helvetica", 20, "bold")).pack(pady=20)
        
        ttk.Label(frame, text="Nama Paket").pack()
        name_entry = ttk.Entry(frame, style="TEntry")
        name_entry.pack(pady=10, padx=20, fill="x")
        
        ttk.Label(frame, text="Total Waktu (detik)").pack()
        timer_entry = ttk.Entry(frame, style="TEntry")
        timer_entry.pack(pady=10, padx=20, fill="x")
        
        self.current_quiz_questions_data = []
        self.questions_gui_frame = ttk.Frame(frame, style="TFrame")
        self.questions_gui_frame.pack(pady=10, fill="x")

        ttk.Button(frame, text="Tambah Soal ke Paket Ini", command=lambda: self.add_question_gui_entry(self.questions_gui_frame), style="Round.TButton").pack(pady=10)
        ttk.Button(frame, text="Simpan Paket Soal", command=lambda: self.save_quiz_package_with_questions(name_entry.get(), timer_entry.get()), style="Round.TButton").pack(pady=10)
        ttk.Button(frame, text="Kembali", command=self.show_manage_quizzes, style="Round.TButton").pack(pady=10)

    def add_question_gui_entry(self, parent_gui_frame, question_data=None):
        q_frame = ttk.Frame(parent_gui_frame, style="TFrame", relief="groove", borderwidth=2)
        q_frame.pack(pady=10, padx=20, fill="x")

        ttk.Label(q_frame, text="Pertanyaan:").pack(anchor="w")
        q_entry = scrolledtext.ScrolledText(q_frame, height=3, font=("Helvetica", 12), relief="flat", background="#ffffff", foreground="#2c3e50")
        q_entry.pack(pady=5, fill="x")
        if question_data: q_entry.insert("1.0", question_data[0])

        options_entries = []
        for i in range(4):
            ttk.Label(q_frame, text=f"Opsi {i+1}:").pack(anchor="w")
            opt_entry = ttk.Entry(q_frame, style="TEntry", font=("Helvetica", 12))
            opt_entry.pack(pady=2, fill="x")
            if question_data and i < len(question_data[1]): opt_entry.insert(0, question_data[1][i])
            options_entries.append(opt_entry)

        ttk.Label(q_frame, text="Nomor Jawaban Benar (1-4):").pack(anchor="w")
        ans_entry = ttk.Entry(q_frame, style="TEntry", font=("Helvetica", 12))
        ans_entry.pack(pady=5, fill="x")
        if question_data: ans_entry.insert(0, question_data[2])

        ttk.Label(q_frame, text="Penjelasan Jawaban:").pack(anchor="w")
        exp_entry = scrolledtext.ScrolledText(q_frame, height=3, font=("Helvetica", 12), relief="flat", background="#ffffff", foreground="#2c3e50")
        exp_entry.pack(pady=5, fill="x")
        if question_data: exp_entry.insert("1.0", question_data[3])
        
        self.current_quiz_questions_data.append({
            "gui_frame": q_frame,
            "q_entry": q_entry,
            "options_entries": options_entries,
            "ans_entry": ans_entry,
            "exp_entry": exp_entry,
            "original_id": question_data[4] if question_data and len(question_data) > 4 else None
        })

    def save_quiz_package_with_questions(self, name, timer_str):
        if not name.strip():
            messagebox.showerror("Error", "Nama paket tidak boleh kosong.")
            return
        if not timer_str.strip():
            messagebox.showerror("Error", "Waktu timer tidak boleh kosong.")
            return
        try:
            timer_val = int(timer_str)
            if timer_val <= 0:
                messagebox.showerror("Error", "Waktu harus minimal 1 detik.")
                return
        except ValueError:
            messagebox.showerror("Error", "Waktu timer harus berupa angka.")
            return

        if not self.current_quiz_questions_data:
            messagebox.showerror("Error", "Paket soal harus memiliki setidaknya satu pertanyaan.")
            return
        
        if not self.current_user.class_codes:
            messagebox.showerror("Error", "Guru tidak memiliki kelas terdaftar.")
            return

        package_id = self.qpm.create(self.current_user.class_codes[0], name, timer_val)
        if not package_id:
            messagebox.showerror("Error", "Gagal membuat paket soal.")
            return

        all_questions_valid = True
        for q_gui_data in self.current_quiz_questions_data:
            question = q_gui_data["q_entry"].get("1.0", tk.END+"-1c").strip()
            options = [opt_e.get().strip() for opt_e in q_gui_data["options_entries"]]
            answer = q_gui_data["ans_entry"].get().strip()
            explanation = q_gui_data["exp_entry"].get("1.0", tk.END+"-1c").strip()

            if not (question and all(options) and answer and explanation):
                all_questions_valid = False
                messagebox.showerror("Error", f"Semua field untuk pertanyaan '{question[:20]}...' harus diisi.")
                break 
            
            try:
                ans_num = int(answer)
                if not (1 <= ans_num <= 4):
                    raise ValueError
            except ValueError:
                all_questions_valid = False
                messagebox.showerror("Error", f"Nomor jawaban benar untuk '{question[:20]}...' harus antara 1 dan 4.")
                break
            
            self.qm.create(package_id, question, options, answer, explanation)
        
        if all_questions_valid:
            messagebox.showinfo("Sukses", "Paket soal dan semua pertanyaannya berhasil dibuat!")
            self.show_manage_quizzes()
        else:
            messagebox.showwarning("Peringatan", "Paket soal dibuat, tetapi beberapa pertanyaan mungkin gagal disimpan karena data tidak valid.")
            self.qpm.delete(package_id)
            messagebox.showinfo("Info Tambahan", "Paket soal yang baru dibuat telah dihapus karena kesalahan pada pertanyaan.")
            self.show_add_quiz_package()

    def show_edit_quiz_package_contents(self, tiny_tree):
        selected = tiny_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Pilih paket soal terlebih dahulu.")
            return
        
        package_name_from_tree = tiny_tree.item(selected[0])["values"][0]
        if not self.current_user.class_codes:
            messagebox.showerror("Error", "Guru tidak memiliki kelas terdaftar.")
            return
        
        packages = self.qpm.list(self.current_user.class_codes[0])
        package = next((p for p in packages if p.package_name == package_name_from_tree), None)
        
        if not package:
            messagebox.showerror("Error", "Paket soal tidak ditemukan.")
            return

        self.clear_frame()
        frame = self.create_scrollable_frame()
        ttk.Label(frame, text=f"Edit Paket Soal: {package.package_name}", font=("Helvetica", 20, "bold")).pack(pady=10)
        ttk.Label(frame, text=f"ID Paket: {package.package_id}").pack(pady=5)

        self.current_quiz_questions_data = []
        self.questions_gui_frame = ttk.Frame(frame, style="TFrame")
        self.questions_gui_frame.pack(pady=10, fill="x")

        existing_questions = self.qm.list(package.package_id)
        for q_obj in existing_questions:
            self.add_question_gui_entry(self.questions_gui_frame, 
                                        (q_obj.question, q_obj.options, q_obj.answer, q_obj.explanation, q_obj.question_id))

        ttk.Button(frame, text="Tambah Soal Baru ke Paket Ini", command=lambda: self.add_question_gui_entry(self.questions_gui_frame), style="Round.TButton").pack(pady=10)
        ttk.Button(frame, text="Simpan Perubahan Paket Soal", command=lambda: self.update_quiz_package_with_questions(package.package_id), style="Round.TButton").pack(pady=10)
        ttk.Button(frame, text="Kembali", command=self.show_manage_quizzes, style="Round.TButton").pack(pady=10)

    def update_quiz_package_with_questions(self, package_id):
        if not self.current_quiz_questions_data:
            messagebox.showerror("Error", "Tidak ada pertanyaan untuk disimpan. Paket harus memiliki setidaknya satu pertanyaan.")
            return

        all_questions_valid = True
        existing_question_ids = [q.question_id for q in self.qm.list(package_id)]
        for q_id in existing_question_ids:
            self.qm.delete(q_id)

        for q_gui_data in self.current_quiz_questions_data:
            question = q_gui_data["q_entry"].get("1.0", tk.END+"-1c").strip()
            options = [opt_e.get().strip() for opt_e in q_gui_data["options_entries"]]
            answer = q_gui_data["ans_entry"].get().strip()
            explanation = q_gui_data["exp_entry"].get("1.0", tk.END+"-1c").strip()

            if not (question and all(options) and answer and explanation):
                all_questions_valid = False
                messagebox.showerror("Error", f"Semua field untuk pertanyaan '{question[:20]}...' harus diisi.")
                break
            
            try:
                ans_num = int(answer)
                if not (1 <= ans_num <= 4): raise ValueError
            except ValueError:
                all_questions_valid = False
                messagebox.showerror("Error", f"Nomor jawaban benar untuk '{question[:20]}...' harus antara 1 dan 4.")
                break
            
            self.qm.create(package_id, question, options, answer, explanation)
        
        if all_questions_valid:
            messagebox.showinfo("Sukses", "Paket soal dan semua pertanyaannya berhasil diperbarui!")
            self.show_manage_quizzes()
        else:
            messagebox.showwarning("Peringatan", "Paket soal mungkin tidak sepenuhnya diperbarui karena ada data pertanyaan yang tidak valid.")
            self.show_manage_quizzes()

    def delete_quiz_package(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Pilih paket soal terlebih dahulu.")
            return
        
        name = tree.item(selected[0])["values"][0]
        if not self.current_user.class_codes:
            messagebox.showerror("Error", "Guru tidak memiliki kelas terdaftar.")
            return

        packages = self.qpm.list(self.current_user.class_codes[0])
        package = next((p for p in packages if p.package_name == name), None)
        
        if package and messagebox.askyesno("Konfirmasi", f"Hapus paket soal '{package.package_name}' dan semua soal di dalamnya?"):
            self.qpm.delete(package.package_id)
            messagebox.showinfo("Sukses", "Paket soal dihapus!")
            self.show_manage_quizzes()
        elif not package:
             messagebox.showerror("Error", "Paket soal tidak ditemukan untuk dihapus.")

    def show_statistics(self):
        self.clear_frame()
        frame = self.create_scrollable_frame()
        ttk.Label(frame, text="Statistik Murid", font=("Helvetica", 20, "bold")).pack(pady=20)
        
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill="both", expand=True, pady=10, padx=20)

        tree = ttk.Treeview(tree_frame, columns=("Student", "QuizzesTaken", "AvgScore"), show="headings")
        tree.heading("Student", text="Nama Murid")
        tree.heading("QuizzesTaken", text="Jumlah Paket Dikerjakan")
        tree.heading("AvgScore", text="Rata-rata Skor (%)")
        tree.column("Student", width=200, anchor="w")
        tree.column("QuizzesTaken", width=150, anchor="center")
        tree.column("AvgScore", width=150, anchor="center")
        tree.pack(side="left", fill="both", expand=True)

        scrollbar_tree = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_tree.set)
        scrollbar_tree.pack(side="right", fill="y")
        
        if not self.current_user.class_codes:
            ttk.Label(frame, text="Guru tidak memiliki kelas terdaftar.").pack(pady=10)
            ttk.Button(frame, text="Kembali", command=self.show_teacher_menu, style="Round.TButton").pack(pady=20)
            return

        progress_data_for_chart = []
        all_users = self.um.list_users()
        students_in_class = [u for u in all_users if u.role == 'murid' and self.current_user.class_codes[0] in u.class_codes]

        if not students_in_class:
            ttk.Label(frame, text="Belum ada murid yang bergabung di kelas ini.").pack(pady=10)
        else:
            for student_user in students_in_class:
                progresses = self.pm.list_by_user_and_class(student_user.username, self.current_user.class_codes[0])
                if progresses:
                    scores = [float(p['score']) for p in progresses]
                    avg_score = sum(scores) / len(scores) if scores else 0.0
                    num_quizzes = len(scores)
                    tree.insert("", "end", values=(student_user.username, num_quizzes, f"{avg_score:.2f}"))
                    if num_quizzes > 0:
                        progress_data_for_chart.append((student_user.username, avg_score))
                else:
                    tree.insert("", "end", values=(student_user.username, 0, "0.00"))

        if progress_data_for_chart:
            chart_frame = ttk.Frame(frame)
            chart_frame.pack(pady=20, fill="x", expand=True)
            try:
                fig, ax = plt.subplots(figsize=(8, 5))
                students_names, avg_scores_values = zip(*progress_data_for_chart)
                ax.bar(students_names, avg_scores_values, color="#3498db", width=0.6)
                ax.set_xlabel("Murid", fontsize=12)
                ax.set_ylabel("Rata-rata Nilai (%)", fontsize=12)
                ax.set_title("Rata-rata Nilai Kuis Murid", fontsize=14)
                ax.tick_params(axis='x', rotation=45, labelsize=10)
                ax.tick_params(axis='y', labelsize=10)
                ax.set_ylim(0, 100)
                plt.tight_layout()

                canvas = FigureCanvasTkAgg(fig, master=chart_frame)
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(fill="both", expand=True)
                canvas.draw()
            except Exception as e:
                ttk.Label(chart_frame, text=f"Gagal membuat grafik: {e}").pack()
        elif students_in_class:
             ttk.Label(frame, text="Belum ada murid yang mengerjakan kuis di kelas ini.").pack(pady=10)

        ttk.Button(frame, text="Kembali", command=self.show_teacher_menu, style="Round.TButton").pack(pady=20)

    def show_student_menu(self):
        self.clear_frame()
        frame = self.create_scrollable_frame()
        ttk.Label(frame, text=f"Selamat datang, Murid {self.current_user.username}", font=("Helvetica", 20, "bold")).pack(pady=20)
        
        ttk.Label(frame, text="Pilih Kelas yang Sudah Diikuti:").pack(pady=(10,0))
        class_tree_frame = ttk.Frame(frame)
        class_tree_frame.pack(fill="x", expand=True, pady=10, padx=20)

        tree = ttk.Treeview(class_tree_frame, columns=("ClassName", "ClassCode"), show="headings", height=5)
        tree.heading("ClassName", text="Nama Kelas")
        tree.heading("ClassCode", text="Kode Kelas")
        tree.column("ClassName", width=300)
        tree.column("ClassCode", width=150, anchor="center")
        tree.pack(side="left", fill="x", expand=True)

        scrollbar_class_tree = ttk.Scrollbar(class_tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_class_tree.set)
        scrollbar_class_tree.pack(side="right", fill="y")

        if self.current_user.class_codes:
            for code in self.current_user.class_codes:
                class_name = self.store.get_class_name(code)
                if not class_name: class_name = f"Kelas (Kode: {code})"
                tree.insert("", "end", values=(class_name, code))
        else:
            ttk.Label(frame, text="Anda belum bergabung dengan kelas manapun.").pack(pady=10)

        button_frame = ttk.Frame(frame, style="TFrame")
        button_frame.pack(pady=20)
        ttk.Button(button_frame, text="Masuk Kelas Terpilih", command=lambda: self.enter_class(tree), style="Round.TButton").pack(side="left", padx=10)
        ttk.Button(button_frame, text="Bergabung Kelas Baru", command=self.show_join_class, style="Round.TButton").pack(side="left", padx=10)
        ttk.Button(frame, text="Logout", command=self.show_login, style="Round.TButton").pack(pady=10)

    def show_join_class(self):
        self.clear_frame()
        frame = self.create_scrollable_frame()
        ttk.Label(frame, text="Bergabung ke Kelas Baru", font=("Helvetica", 20, "bold")).pack(pady=20)
        
        ttk.Label(frame, text="Masukkan Kode Kelas:").pack(pady=(10,0))
        class_code_entry = ttk.Entry(frame, style="TEntry", width=30, justify='center')
        class_code_entry.pack(pady=10, padx=20)
        
        button_frame = ttk.Frame(frame, style="TFrame")
        button_frame.pack(pady=15)
        ttk.Button(button_frame, text="Bergabung", command=lambda: self.handle_join_class(class_code_entry.get()), style="Round.TButton").pack(side="left", padx=10)
        ttk.Button(button_frame, text="Kembali", command=self.show_student_menu, style="Round.TButton").pack(side="left", padx=10)

    def handle_join_class(self, class_code):
        if not class_code.strip():
            messagebox.showerror("Error", "Kode kelas tidak boleh kosong.")
            return
        
        success, message = self.um.join_class(self.current_user.username, class_code)
        if success:
            self.current_user.class_codes.append(class_code)
            messagebox.showinfo("Sukses", message)
            self.show_student_menu()
        else:
            messagebox.showerror("Error", message)

    def enter_class(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Pilih kelas terlebih dahulu dari daftar.")
            return
        
        selected_values = tree.item(selected_item[0])["values"]
        if not selected_values or len(selected_values) < 2:
            messagebox.showerror("Error", "Data kelas tidak valid pada item terpilih.")
            return

        self.current_class_code = selected_values[1]
        self.show_class_menu()

    def show_class_menu(self):
        self.clear_frame()
        frame = self.create_scrollable_frame()
        class_name = self.store.get_class_name(self.current_class_code) or f"Kode: {self.current_class_code}"
        ttk.Label(frame, text=f"Menu Kelas: {class_name}", font=("Helvetica", 20, "bold")).pack(pady=20)
        
        button_container = ttk.Frame(frame, style="TFrame")
        button_container.pack(pady=20, fill="x")
        ttk.Button(button_container, text="Baca Artikel", command=self.show_read_articles, style="Round.TButton").pack(pady=10, padx=20, fill="x", expand=True)
        ttk.Button(button_container, text="Kerjakan Paket Soal", command=self.show_take_quiz, style="Round.TButton").pack(pady=10, padx=20, fill="x", expand=True)
        ttk.Button(button_container, text="Review Riwayat Soal", command=self.show_review_quizzes, style="Round.TButton").pack(pady=10, padx=20, fill="x", expand=True)
        ttk.Button(frame, text="Kembali ke Daftar Kelas", command=self.show_student_menu, style="Round.TButton").pack(pady=20)

    def show_read_articles(self):
        self.clear_frame()
        frame = self.create_scrollable_frame()
        class_name = self.store.get_class_name(self.current_class_code) or self.current_class_code
        ttk.Label(frame, text=f"Daftar Artikel - Kelas: {class_name}", font=("Helvetica", 20, "bold")).pack(pady=20)
        
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill="both", expand=True, pady=10, padx=20)

        tree = ttk.Treeview(tree_frame, columns=("Title",), show="headings")
        tree.heading("Title", text="Judul Artikel")
        tree.pack(side="left", fill="both", expand=True)

        scrollbar_article_tree = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_article_tree.set)
        scrollbar_article_tree.pack(side="right", fill="y")
        
        articles = self.am.list(self.current_class_code)
        if articles:
            for art in articles:
                tree.insert("", "end", values=(art.title,))
        else:
            ttk.Label(frame, text="Belum ada artikel di kelas ini.").pack(pady=10)

        button_frame_bottom = ttk.Frame(frame, style="TFrame")
        button_frame_bottom.pack(pady=10)
        ttk.Button(button_frame_bottom, text="Baca Artikel Terpilih", command=lambda: self.display_article(tree), style="Round.TButton").pack(side="left", padx=10)
        ttk.Button(button_frame_bottom, text="Kembali ke Menu Kelas", command=self.show_class_menu, style="Round.TButton").pack(side="left", padx=10)

    def display_article(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Pilih artikel terlebih dahulu.")
            return
        
        title = tree.item(selected[0])["values"][0]
        articles = self.am.list(self.current_class_code)
        article = next((a for a in articles if a.title == title), None)
        
        if not article:
            messagebox.showerror("Error", "Artikel tidak ditemukan.")
            return

        self.clear_frame()
        display_frame_container = self.create_scrollable_frame()
        ttk.Label(display_frame_container, text=article.title, font=("Helvetica", 22, "bold"), wraplength=800).pack(pady=(10,15), anchor="w")
        
        text_area = tk.Text(display_frame_container, font=("Helvetica", 14), wrap="word", bg="#ffffff", fg="#2c3e50", relief="flat", padx=10, pady=10)
        text_area.pack(pady=10, padx=5, fill="both", expand=True)

        if not hasattr(text_area, 'images_references'):
            text_area.images_references = []
        else:
            text_area.images_references.clear()

        content = article.text
        last_pos = 0
        while True:
            img_tag_start = content.find("[Image:", last_pos)
            text_to_insert = content[last_pos : img_tag_start if img_tag_start != -1 else len(content)]
            if text_to_insert:
                text_area.insert(tk.END, text_to_insert)

            if img_tag_start == -1:
                break
            
            img_tag_end = content.find("]", img_tag_start)
            if img_tag_end == -1:
                text_area.insert(tk.END, content[img_tag_start:])
                break
            
            img_path = content[img_tag_start + len("[Image:") : img_tag_end].strip()
            
            try:
                img = Image.open(img_path)
                max_img_width = 500
                original_width, original_height = img.size
                if original_width > max_img_width:
                    w_percent = (max_img_width / float(original_width))
                    new_height = int((float(original_height) * float(w_percent)))
                    img = img.resize((max_img_width, new_height), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                text_area.images_references.append(photo)
                text_area.insert(tk.END, '\n')
                text_area.image_create(tk.END, image=photo)
                text_area.insert(tk.END, '\n\n')
            except FileNotFoundError:
                text_area.insert(tk.END, f"\n[Gambar tidak ditemukan: {img_path}]\n")
            except Exception as e:
                text_area.insert(tk.END, f"\n[Gagal memuat gambar: {img_path} ({e})]\n")
            
            last_pos = img_tag_end + 1

        text_area.config(state="disabled")
        ttk.Button(display_frame_container, text="Kembali ke Daftar Artikel", command=self.show_read_articles, style="Round.TButton").pack(pady=20)

    def show_take_quiz(self):
        self.clear_frame()
        frame = self.create_scrollable_frame()
        class_name = self.store.get_class_name(self.current_class_code) or self.current_class_code
        ttk.Label(frame, text=f"Pilih Paket Soal - Kelas: {class_name}", font=("Helvetica", 20, "bold")).pack(pady=20)
        
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill="both", expand=True, pady=10, padx=20)

        tree = ttk.Treeview(tree_frame, columns=("Name", "Timer", "Status"), show="headings")
        tree.heading("Name", text="Nama Paket")
        tree.heading("Timer", text="Timer (detik)")
        tree.heading("Status", text="Status")
        tree.column("Name", width=300)
        tree.column("Timer", width=100, anchor="center")
        tree.column("Status", width=150, anchor="center")
        tree.pack(side="left", fill="both", expand=True)

        scrollbar_quiz_tree = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_quiz_tree.set)
        scrollbar_quiz_tree.pack(side="right", fill="y")
        
        packages = self.qpm.list(self.current_class_code)
        if packages:
            for pkg in packages:
                if self.pm.has_taken_package(self.current_user.username, pkg.package_id):
                    status = "Sudah Dikerjakan"
                else:
                    status = "Belum Dikerjakan"
                tree.insert("", "end", values=(pkg.package_name, pkg.total_timer, status))
        else:
            ttk.Label(frame, text="Belum ada paket soal di kelas ini.").pack(pady=10)

        button_frame_bottom = ttk.Frame(frame, style="TFrame")
        button_frame_bottom.pack(pady=10)
        ttk.Button(button_frame_bottom, text="Kerjakan Paket Terpilih", command=lambda: self.start_quiz(tree), style="Round.TButton").pack(side="left", padx=10)
        ttk.Button(button_frame_bottom, text="Kembali ke Menu Kelas", command=self.show_class_menu, style="Round.TButton").pack(side="left", padx=10)

    def start_quiz(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Pilih paket soal terlebih dahulu.")
            return
        
        selected_values = tree.item(selected[0])["values"]
        package_name_from_tree = selected_values[0]
        status = selected_values[2]

        if status == "Sudah Dikerjakan":
            messagebox.showinfo("Info", f"Anda sudah mengerjakan paket soal '{package_name_from_tree}'. Anda dapat mereviewnya.")
            return
            
        packages = self.qpm.list(self.current_class_code)
        package = next((p for p in packages if p.package_name == package_name_from_tree), None)
        
        if not package:
            messagebox.showerror("Error", "Paket soal tidak ditemukan.")
            return
            
        questions = self.qm.list(package.package_id)
        if not questions:
            messagebox.showerror("Error", "Paket soal ini tidak memiliki pertanyaan.")
            return
            
        self.current_questions = questions
        self.current_package = package
        self.current_answers = [""] * len(questions)
        self.current_question_index = 0
        self.quiz_start_time = time.time()
        
        if hasattr(self, '_timer_job_id') and self._timer_job_id:
            self.root.after_cancel(self._timer_job_id)
            self._timer_job_id = None

        self.show_quiz_question()

    def show_quiz_question(self):
        if self.current_question_index >= len(self.current_questions):
            self.submit_quiz()
            return

        elapsed_time = time.time() - self.quiz_start_time
        remaining_time = self.current_package.total_timer - elapsed_time
        if remaining_time <= 0:
            self.submit_quiz()
            return

        self.clear_frame()
        frame = self.create_scrollable_frame()
        
        question = self.current_questions[self.current_question_index]
        
        ttk.Label(frame, text=f"Pertanyaan {self.current_question_index + 1} dari {len(self.current_questions)}", 
                  font=("Helvetica", 18, "bold")).pack(pady=(15, 10))
        
        q_text_area = scrolledtext.ScrolledText(frame, height=6, font=("Helvetica", 14), relief="flat", 
                                                background="#ffffff", foreground="#2c3e50", wrap=tk.WORD)
        q_text_area.insert("1.0", question.question)
        q_text_area.config(state="disabled")
        q_text_area.pack(pady=10, padx=20, fill="x")
        
        options_frame = ttk.Frame(frame, style="TFrame")
        options_frame.pack(pady=10, padx=20, fill="x")
        
        self.selected_option_var = tk.StringVar(value=self.current_answers[self.current_question_index] or "")
        
        for i, opt_text in enumerate(question.options, 1):
            rb = ttk.Radiobutton(options_frame, text=opt_text, value=str(i), variable=self.selected_option_var, style="TRadiobutton")
            rb.pack(anchor="w", pady=3, padx=5)
            
        self.timer_label = ttk.Label(frame, text="", font=("Helvetica", 16, "bold"))
        self.timer_label.pack(pady=(15,5))
        self.update_timer_display()

        nav_buttons_frame = ttk.Frame(frame, style="TFrame")
        nav_buttons_frame.pack(pady=20)

        if self.current_question_index > 0:
            ttk.Button(nav_buttons_frame, text="<< Sebelumnya", command=self.prev_question, style="Round.TButton").pack(side="left", padx=10)

        if self.current_question_index < len(self.current_questions) - 1:
            ttk.Button(nav_buttons_frame, text="Berikutnya >>", command=self.next_question, style="Round.TButton").pack(side="left", padx=10)
        else:
            ttk.Button(nav_buttons_frame, text="Kumpulkan Jawaban", command=self.confirm_submit_quiz, style="Round.TButton").pack(side="left", padx=10)

    def update_timer_display(self):
        if not hasattr(self, 'current_package') or self.current_question_index >= len(self.current_questions):
            if hasattr(self, '_timer_job_id') and self._timer_job_id:
                self.root.after_cancel(self._timer_job_id)
                self._timer_job_id = None
            return

        elapsed_time = time.time() - self.quiz_start_time
        remaining_time = self.current_package.total_timer - elapsed_time

        if remaining_time < 0: remaining_time = 0
        
        minutes, seconds = divmod(int(remaining_time), 60)
        self.timer_label.config(text=f"Sisa Waktu: {minutes:02d}:{seconds:02d}")
        
        if remaining_time <= 0:
            self.timer_label.config(foreground="red")
            self.submit_quiz()
        elif remaining_time < 30:
            self.timer_label.config(foreground="orange")
        else:
            self.timer_label.config(foreground="black")
        
        self._timer_job_id = self.root.after(1000, self.update_timer_display)

    def record_current_answer(self):
        if hasattr(self, 'selected_option_var'):
            selected_value = self.selected_option_var.get()
            if selected_value:
                self.current_answers[self.current_question_index] = selected_value

    def next_question(self):
        self.record_current_answer()
        if self.current_question_index < len(self.current_questions) - 1:
            self.current_question_index += 1
            self.show_quiz_question()

    def prev_question(self):
        self.record_current_answer()
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.show_quiz_question()
            
    def confirm_submit_quiz(self):
        self.record_current_answer()
        unanswered_count = self.current_answers.count("")
        confirmation_message = "Apakah Anda yakin ingin mengumpulkan jawaban?"
        if unanswered_count > 0:
            confirmation_message = f"Ada {unanswered_count} pertanyaan yang belum dijawab. Tetap kumpulkan?"

        if messagebox.askyesno("Konfirmasi Submit", confirmation_message):
            self.submit_quiz()

    def submit_quiz(self):
        if hasattr(self, '_timer_job_id') and self._timer_job_id:
            self.root.after_cancel(self._timer_job_id)
            self._timer_job_id = None
            
        correct_count = 0
        for i, q_obj in enumerate(self.current_questions):
            if i < len(self.current_answers) and self.current_answers[i] == q_obj.answer:
                correct_count += 1
        
        score = (correct_count / len(self.current_questions)) * 100 if self.current_questions else 0.0
        answers_str = "|".join(str(ans if ans else "") for ans in self.current_answers)
        self.pm.record(self.current_user.username, self.current_package.package_id, f"{score:.2f}", answers_str)
        
        messagebox.showinfo("Kuis Selesai", f"Kuis telah dikumpulkan.\nSkor Anda: {score:.2f}%")
        
        for attr in ['current_questions', 'current_package', 'current_answers', 
                     'current_question_index', 'quiz_start_time', 'selected_option_var', 'timer_label']:
            if hasattr(self, attr):
                delattr(self, attr)

        self.show_class_menu()

    def show_review_quizzes(self):
        self.clear_frame()
        frame = self.create_scrollable_frame()
        class_name = self.store.get_class_name(self.current_class_code) or self.current_class_code
        ttk.Label(frame, text=f"Riwayat & Review Paket Soal - Kelas: {class_name}", font=("Helvetica", 20, "bold")).pack(pady=20)
        
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill="both", expand=True, pady=10, padx=20)

        tree = ttk.Treeview(tree_frame, columns=("Name", "Score", "DateTaken"), show="headings")
        tree.heading("Name", text="Nama Paket")
        tree.heading("Score", text="Skor (%)")
        tree.heading("DateTaken", text="Tanggal Pengerjaan")
        tree.column("Name", width=300)
        tree.column("Score", width=100, anchor="center")
        tree.column("DateTaken", width=150, anchor="center")
        tree.pack(side="left", fill="both", expand=True)

        scrollbar_review_tree = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_review_tree.set)
        scrollbar_review_tree.pack(side="right", fill="y")
        
        progresses = self.pm.list_by_user_and_class(self.current_user.username, self.current_class_code)
        
        if progresses:
            all_packages_in_class = self.qpm.list(self.current_class_code)
            package_dict = {pkg.package_id: pkg for pkg in all_packages_in_class}

            for prog_entry in progresses:
                package_obj = package_dict.get(prog_entry['package_id'])
                if package_obj:
                    date_taken = prog_entry.get('timestamp', 'N/A')
                    tree.insert("", "end", values=(package_obj.package_name, prog_entry['score'], date_taken))
        else:
            ttk.Label(frame, text="Anda belum mengerjakan paket soal apapun di kelas ini.").pack(pady=10)

        button_frame_bottom = ttk.Frame(frame, style="TFrame")
        button_frame_bottom.pack(pady=10)
        ttk.Button(button_frame_bottom, text="Lihat Review Terpilih", command=lambda: self.display_review(tree), style="Round.TButton").pack(side="left", padx=10)
        ttk.Button(button_frame_bottom, text="Kembali ke Menu Kelas", command=self.show_class_menu, style="Round.TButton").pack(side="left", padx=10)

    def display_review(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Pilih paket soal dari riwayat terlebih dahulu.")
            return
        
        package_name_from_tree = tree.item(selected[0])["values"][0]
        
        all_packages_in_class = self.qpm.list(self.current_class_code)
        package_to_review = next((p for p in all_packages_in_class if p.package_name == package_name_from_tree), None)
        
        if not package_to_review:
            messagebox.showerror("Error", "Paket soal tidak ditemukan atau tidak lagi valid.")
            return
            
        user_progresses = self.pm.list_by_user_and_class(self.current_user.username, self.current_class_code)
        progress_entry = next((p for p in user_progresses if p['package_id'] == package_to_review.package_id), None)
        
        if not progress_entry:
            messagebox.showerror("Error", "Data pengerjaan untuk paket soal ini tidak ditemukan.")
            return
            
        questions_in_package = self.qm.list(package_to_review.package_id)
        user_answers_list = progress_entry.get('answers', "").split('|')
        user_answers_list_padded = user_answers_list + [''] * (len(questions_in_package) - len(user_answers_list))

        self.clear_frame()
        review_scroll_frame = self.create_scrollable_frame()
        
        ttk.Label(review_scroll_frame, text=f"Review Kuis: {package_to_review.package_name}", font=("Helvetica", 20, "bold")).pack(pady=15)
        ttk.Label(review_scroll_frame, text=f"Skor Anda: {progress_entry['score']}%", font=("Helvetica", 16)).pack(pady=(0,15))

        for i, q_obj in enumerate(questions_in_package):
            q_container = ttk.Frame(review_scroll_frame, style="TFrame", relief="solid", borderwidth=1)
            q_container.pack(pady=10, padx=20, fill="x")

            ttk.Label(q_container, text=f"Pertanyaan {i+1}:", font=("Helvetica", 14, "bold")).pack(anchor="w", padx=10, pady=(10,5))
            
            q_text_widget = tk.Text(q_container, font=("Helvetica", 12), wrap="word", height=3, relief="flat", bg="#ffffff", fg="#2c3e50")
            q_text_widget.insert("1.0", q_obj.question)
            q_text_widget.config(state="disabled")
            q_text_widget.pack(fill="x", padx=10, pady=5)

            ttk.Label(q_container, text="Opsi Jawaban:", font=("Helvetica", 12, "italic")).pack(anchor="w", padx=10, pady=(5,0))
            for j, opt_text in enumerate(q_obj.options, 1):
                opt_label_text = f"  {j}. {opt_text}"
                ttk.Label(q_container, text=opt_label_text, font=("Helvetica", 12), wraplength=700).pack(anchor="w", padx=15)
            
            user_ans_idx_str = user_answers_list_padded[i]
            user_ans_text = "Tidak Dijawab"
            if user_ans_idx_str.isdigit():
                user_ans_idx = int(user_ans_idx_str)
                if 1 <= user_ans_idx <= len(q_obj.options):
                    user_ans_text = f"{user_ans_idx_str}. {q_obj.options[user_ans_idx-1]}"
            
            correct_ans_idx_str = q_obj.answer
            correct_ans_text = "N/A"
            if correct_ans_idx_str.isdigit():
                correct_ans_idx = int(correct_ans_idx_str)
                if 1 <= correct_ans_idx <= len(q_obj.options):
                    correct_ans_text = f"{correct_ans_idx_str}. {q_obj.options[correct_ans_idx-1]}"

            ttk.Label(q_container, text=f"Jawaban Anda: {user_ans_text}", font=("Helvetica", 12), wraplength=700).pack(anchor="w", padx=10, pady=5)
            
            color = "green" if user_ans_idx_str == correct_ans_idx_str else "red"
            if user_ans_text == "Tidak Dijawab": color = "orange"

            correct_ans_label = ttk.Label(q_container, text=f"Jawaban Benar: {correct_ans_text}", font=("Helvetica", 12, "bold"), foreground=color, wraplength=700)
            correct_ans_label.pack(anchor="w", padx=10, pady=5)
            
            ttk.Label(q_container, text="Penjelasan:", font=("Helvetica", 12, "italic")).pack(anchor="w", padx=10, pady=(5,0))
            exp_text_widget = tk.Text(q_container, font=("Helvetica", 12), wrap="word", height=3, relief="flat", bg="#ffffff", fg="#2c3e50")
            exp_text_widget.insert("1.0", q_obj.explanation)
            exp_text_widget.config(state="disabled")
            exp_text_widget.pack(fill="x", padx=10, pady=(0,10))

        ttk.Button(review_scroll_frame, text="Kembali ke Riwayat Soal", command=self.show_review_quizzes, style="Round.TButton").pack(pady=20, padx=20, fill="x")

if __name__ == '__main__':
    root = tk.Tk()
    app = ElearningApp(root)
    root.mainloop()