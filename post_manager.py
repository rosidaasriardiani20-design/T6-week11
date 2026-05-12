# Nama    : Rosida Asri Ardiani
# NIM     : F1D02410142
# Kelas   : Pemrograman Visual C

import tkinter as tk
from tkinter import messagebox, ttk
import requests
import threading

# --- 1. API SERVICE (Logika Network) ---
# Bagian ini hanya fokus pada urusan HTTP Request
class PostService:
    def __init__(self):
        self.base_url = "https://api.pahrul.my.id/api/posts"

    def get_all(self):
        return requests.get(self.base_url, timeout=10)

    def get_detail(self, post_id):
        return requests.get(f"{self.base_url}/{post_id}", timeout=10)

    def create(self, data):
        return requests.post(self.base_url, json=data, timeout=10)

    def update(self, post_id, data):
        return requests.put(f"{self.base_url}/{post_id}", json=data, timeout=10)

    def delete(self, post_id):
        return requests.delete(f"{self.base_url}/{post_id}", timeout=10)

# --- 2. API WORKER (Logika Threading) ---
# Bagian ini bertugas menjalankan fungsi Service di thread terpisah
class ApiWorker(threading.Thread):
    def __init__(self, target_func, on_success, on_error):
        super().__init__()
        self.target_func = target_func
        self.on_success = on_success
        self.on_error = on_error
        self.daemon = True

    def run(self):
        try:
            response = self.target_func()
            if response.status_code in [200, 201]:
                self.on_success(response.json())
            else:
                self.on_error(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            self.on_error(str(e))

# --- 3. MAIN UI (Logika Tampilan) ---
class PostManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Post Manager - Week 11")
        self.service = PostService()
        self.selected_id = None
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # Frame Tabel
        frame_table = tk.Frame(self.root)
        frame_table.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(frame_table, columns=("ID", "Title", "Author", "Status"), show='headings')
        for col in ("ID", "Title", "Author", "Status"):
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Frame Form
        self.form_frame = tk.LabelFrame(self.root, text="Post Form")
        self.form_frame.pack(fill="x", padx=10, pady=5)

        # Input Fields
        labels = ["Title", "Author", "Slug", "Status"]
        self.entries = {}
        for i, label in enumerate(labels):
            tk.Label(self.form_frame, text=label).grid(row=0, column=i*2, padx=5, pady=5)
            ent = tk.Entry(self.form_frame)
            ent.grid(row=0, column=i*2+1, padx=5, pady=5)
            self.entries[label.lower()] = ent

        tk.Label(self.form_frame, text="Body").grid(row=1, column=0)
        self.txt_body = tk.Text(self.form_frame, height=3)
        self.txt_body.grid(row=1, column=1, columnspan=7, sticky="we", padx=5, pady=5)

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=5)

        self.btn_post = tk.Button(btn_frame, text="POST", command=self.add_post)
        self.btn_post.pack(side="left", padx=5)

        self.btn_put = tk.Button(btn_frame, text="PUT", state="disabled", command=self.edit_post)
        self.btn_put.pack(side="left", padx=5)

        self.btn_del = tk.Button(btn_frame, text="DELETE", state="disabled", fg="white", bg="red", command=self.delete_post)
        self.btn_del.pack(side="left", padx=5)

        # Status Bar
        self.status_var = tk.StringVar(value="Ready")
        tk.Label(self.root, textvariable=self.status_var, bd=1, relief="sunken", anchor="w").pack(side="bottom", fill="x")

    # --- Event Handlers ---
    def load_data(self):
        self.status_var.set("Loading data...")
        ApiWorker(
            target_func=self.service.get_all,
            on_success=self.fill_table,
            on_error=self.handle_error
        ).start()

    def fill_table(self, data):
        self.root.after(0, self._update_table_ui, data)

    def _update_table_ui(self, data):
        self.tree.delete(*self.tree.get_children())
        # Pastikan data adalah list (sesuai API)
        posts = data if isinstance(data, list) else data.get('data', [])
        for p in posts:
            self.tree.insert("", "end", values=(p['id'], p['title'], p['author'], p['status']))
        self.status_var.set("Data loaded.")

    def on_select(self, event):
        sel = self.tree.selection()
        if sel:
            item = self.tree.item(sel[0])['values']
            self.selected_id = item[0]
            self.btn_put.config(state="normal")
            self.btn_del.config(state="normal")
            self.status_var.set(f"Selected ID: {self.selected_id}")

    def add_post(self):
        data = self.get_form_inputs()
        self.status_var.set("Sending POST...")
        ApiWorker(lambda: self.service.create(data), lambda res: self.load_data(), self.handle_error).start()

    def edit_post(self):
        if not self.selected_id: return
        data = self.get_form_inputs()
        self.status_var.set("Sending PUT...")
        ApiWorker(lambda: self.service.update(self.selected_id, data), lambda res: self.load_data(), self.handle_error).start()

    def delete_post(self):
        if messagebox.askyesno("Confirm", "Hapus data ini?"):
            self.status_var.set("Sending DELETE...")
            ApiWorker(lambda: self.service.delete(self.selected_id), lambda res: self.load_data(), self.handle_error).start()

    def get_form_inputs(self):
        return {
            "title": self.entries['title'].get(),
            "author": self.entries['author'].get(),
            "slug": self.entries['slug'].get(),
            "status": self.entries['status'].get(),
            "body": self.txt_body.get("1.0", "end-1c")
        }

    def handle_error(self, msg):
        self.root.after(0, lambda: messagebox.showerror("API Error", msg))
        self.root.after(0, lambda: self.status_var.set("Error occurred."))

if __name__ == "__main__":
    app_root = tk.Tk()
    PostManagerApp(app_root)
    app_root.mainloop()