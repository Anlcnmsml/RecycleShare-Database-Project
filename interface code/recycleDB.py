import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

# =============================================================================
# AYARLAR (Veritabanı Bağlantısı)
# =============================================================================
DB_HOST = "localhost"
DB_NAME = "RecycleShareDB" # <-- OLUŞTURDUĞUNUZ DATABASE İSMİNİ BURAYA YAZINIZ
DB_USER = "postgres"   # <-- KULLANICI ADINIZI BURAYA YAZINIZ
DB_PASS = "147896325"  # <-- ŞİFRENİZİ BURAYA YAZINIZ

# =============================================================================
# GÖRSEL TEMA AYARLARI (Modern Renk Paleti)
# =============================================================================
COLOR_PRIMARY = "#2E7D32"    # Koyu Yeşil (Başlıklar)
COLOR_ACCENT = "#4CAF50"     # Açık Yeşil (Butonlar)
COLOR_BG = "#F5F7FA"         # Açık Gri (Arkaplan)
COLOR_WHITE = "#FFFFFF"      # Beyaz (Kartlar)
COLOR_TEXT = "#333333"       # Koyu Gri (Yazılar)

def apply_theme():
    """Tkinter stillerini modernleştirir."""
    style = ttk.Style()
    try:
        style.theme_use('clam') 
    except:
        pass

    # Genel Arkaplan ve Yazı Tipi
    style.configure(".", background=COLOR_BG, foreground=COLOR_TEXT, font=("Segoe UI", 10))
    style.configure("TLabel", background=COLOR_BG, foreground=COLOR_TEXT)
    style.configure("TFrame", background=COLOR_BG)
    style.configure("TEntry", fieldbackground=COLOR_WHITE, bordercolor="#CFD8DC")
    
    # Labelframe (Gruplar)
    style.configure("TLabelframe", background=COLOR_BG, bordercolor="#CFD8DC", borderwidth=1)
    style.configure("TLabelframe.Label", font=("Segoe UI", 10, "bold"), foreground=COLOR_PRIMARY, background=COLOR_BG)

    # Butonlar
    style.configure("TButton", 
                    font=("Segoe UI", 9, "bold"), 
                    background=COLOR_ACCENT, 
                    foreground="white", 
                    borderwidth=0, 
                    focuscolor="none",
                    padding=(10, 5))
    style.map("TButton", 
              background=[('active', COLOR_PRIMARY)], 
              foreground=[('active', 'white')])

    # Sekmeler (Notebook)
    style.configure("TNotebook", background=COLOR_BG, borderwidth=0)
    style.configure("TNotebook.Tab", 
                    font=("Segoe UI", 10, "bold"), 
                    padding=[15, 8], 
                    background="#E0E0E0", 
                    foreground="#555")
    style.map("TNotebook.Tab", 
              background=[("selected", COLOR_WHITE)], 
              foreground=[("selected", COLOR_PRIMARY)])

    # Listeler (Treeview)
    style.configure("Treeview", 
                    background=COLOR_WHITE,
                    fieldbackground=COLOR_WHITE,
                    foreground=COLOR_TEXT,
                    rowheight=28,
                    font=("Segoe UI", 9),
                    borderwidth=0)
    style.configure("Treeview.Heading", 
                    font=("Segoe UI", 9, "bold"), 
                    background="#ECEFF1", 
                    foreground=COLOR_TEXT,
                    relief="flat")
    style.map("Treeview", background=[('selected', '#C8E6C9')], foreground=[('selected', 'black')])

# =============================================================================
# GİRİŞ EKRANI
# =============================================================================
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Giriş Yap - RecycleShare")
        self.root.geometry("400x550") # Yüksekliği biraz artırdım buton sığsın diye
        self.root.configure(bg=COLOR_BG) 
        
        apply_theme() # Temayı yükle

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width/2) - (400/2)
        y = (screen_height/2) - (550/2)
        self.root.geometry('%dx%d+%d+%d' % (400, 550, x, y))

        self.conn = None
        if self.connect_db():
            self.setup_ui()

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
            return True
        except Exception as e:
            messagebox.showerror("Bağlantı Hatası", f"Veritabanına bağlanılamadı:\n{e}")
            return False

    def setup_ui(self):
        # Beyaz bir kart (Card) oluşturarak modern görünüm veriyoruz
        card = tk.Frame(self.root, bg=COLOR_WHITE, padx=30, pady=30)
        card.pack(expand=True, fill="both", padx=20, pady=20)

        # Başlık ve Logo
        tk.Label(card, text="♻️", font=("Segoe UI", 50), bg=COLOR_WHITE, fg=COLOR_PRIMARY).pack()
        tk.Label(card, text="RecycleShare", font=("Segoe UI", 22, "bold"), bg=COLOR_WHITE, fg=COLOR_TEXT).pack(pady=(0, 5))
        tk.Label(card, text="Giriş Paneli", font=("Segoe UI", 10), bg=COLOR_WHITE, fg="gray").pack(pady=(0, 20))

        # Giriş Alanları
        tk.Label(card, text="Kullanıcı Adı:", bg=COLOR_WHITE, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.entry_user = ttk.Entry(card, font=("Segoe UI", 11))
        self.entry_user.pack(pady=(5, 15), fill="x", ipady=3)

        tk.Label(card, text="Şifre:", bg=COLOR_WHITE, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.entry_pass = ttk.Entry(card, show="*", font=("Segoe UI", 11))
        self.entry_pass.pack(pady=(5, 20), fill="x", ipady=3)

        # --- BURASI DÜZELTİLDİ ---
        # Giriş Butonu
        ttk.Button(card, text="GİRİŞ YAP", command=self.login).pack(fill="x", pady=5)
        
        # Ayırıcı Çizgi
        ttk.Separator(card, orient="horizontal").pack(fill="x", pady=15)
        
        # Kayıt Ol Butonu
        ttk.Button(card, text="Yeni Hesap Oluştur (Kayıt Ol)", command=self.open_register_window).pack(fill="x")
        # -------------------------
        
        tk.Label(card, text="Admin: admin / 1234\nUser: ahmet / 1234", bg=COLOR_WHITE, fg="gray", font=("Segoe UI", 8)).pack(side="bottom", pady=10)

    def login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()

        if self.conn is None or self.conn.closed != 0: self.connect_db()

        try:
            cur = self.conn.cursor()
            sql = "SELECT user_id, username, role FROM users WHERE username = %s AND password = %s"
            cur.execute(sql, (username, password))
            user = cur.fetchone()
            cur.close()

            if user:
                self.conn.close()
                self.open_main_app(user)
            else:
                messagebox.showerror("Hata", "Hatalı kullanıcı adı veya şifre!")
        except Exception as e:
            messagebox.showerror("Hata", str(e))
            if self.conn:
                try: self.conn.close()
                except: pass
            self.conn = None

    def open_register_window(self):
        reg_win = tk.Toplevel(self.root)
        reg_win.title("Yeni Kullanıcı Kaydı")
        reg_win.geometry("350x450")
        reg_win.configure(bg=COLOR_BG)
        
        x = (self.root.winfo_screenwidth()/2) - 175
        y = (self.root.winfo_screenheight()/2) - 225
        reg_win.geometry('%dx%d+%d+%d' % (350, 450, x, y))

        # Kayıt Ekranı Tasarımı
        card = tk.Frame(reg_win, bg=COLOR_WHITE, padx=20, pady=20)
        card.pack(expand=True, fill="both", padx=15, pady=15)

        tk.Label(card, text="Kayıt Ol", font=("Segoe UI", 18, "bold"), bg=COLOR_WHITE, fg=COLOR_PRIMARY).pack(pady=(0, 20))

        tk.Label(card, text="Kullanıcı Adı:", bg=COLOR_WHITE).pack(anchor="w")
        e_user = ttk.Entry(card); e_user.pack(pady=5, fill="x")

        tk.Label(card, text="Şifre:", bg=COLOR_WHITE).pack(anchor="w")
        e_pass = ttk.Entry(card, show="*"); e_pass.pack(pady=5, fill="x")

        tk.Label(card, text="Rol Seçiniz:", bg=COLOR_WHITE).pack(anchor="w")
        c_role = ttk.Combobox(card, values=["user", "collector"], state="readonly")
        c_role.pack(pady=5, fill="x")
        c_role.current(0) 

        def register_action():
            u = e_user.get()
            p = e_pass.get()
            r = c_role.get()

            if not u or not p:
                messagebox.showwarning("Uyarı", "Tüm alanları doldurunuz.")
                return

            if self.conn is None or self.conn.closed != 0: self.connect_db()

            try:
                cur = self.conn.cursor()
                cur.execute("SELECT 1 FROM users WHERE username = %s", (u,))
                if cur.fetchone():
                    messagebox.showerror("Hata", "Bu kullanıcı adı zaten alınmış.")
                    cur.close()
                    return

                cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (u, p, r))
                self.conn.commit()
                cur.close()
                
                messagebox.showinfo("Başarılı", "Kayıt oluşturuldu! Giriş yapabilirsiniz.")
                reg_win.destroy()
            except Exception as e:
                self.conn.rollback()
                messagebox.showerror("Hata", str(e))

        ttk.Button(card, text="KAYDET", command=register_action).pack(pady=20, fill="x")

    def open_main_app(self, user_info):
        self.root.destroy()
        new_root = tk.Tk()
        app = RecycleShareApp(new_root, user_info)
        new_root.mainloop()


# =============================================================================
# ANA UYGULAMA (MAIN APP)
# =============================================================================
class RecycleShareApp:
    def __init__(self, root, user_info):
        self.root = root
        self.user_id, self.username, self.role = user_info 
        
        self.root.title(f"RecycleShare - Hoşgeldin, {self.username} ({self.role})")
        self.root.geometry("1100x750")
        self.root.configure(bg=COLOR_BG) # Arkaplan
        
        apply_theme() # Temayı uygula

        self.conn = None
        self.connect_db()

        self.setup_header()

        # Ana İçerik Alanı
        main_frame = ttk.Frame(root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.tabs = ttk.Notebook(main_frame)
        
        self.tab_add = ttk.Frame(self.tabs)
        self.tab_search = ttk.Frame(self.tabs)
        self.tab_process = ttk.Frame(self.tabs)
        self.tab_review = ttk.Frame(self.tabs)
        self.tab_message = ttk.Frame(self.tabs)
        self.tab_analysis = ttk.Frame(self.tabs)
        self.tab_profile = ttk.Frame(self.tabs) 
        
        # --- SEKME EKLEME SIRASI ---

        if self.role in ['user', 'admin']:
            self.tabs.add(self.tab_add, text=" ➕ İlan Ver ")
            self.setup_add_tab()

        self.tabs.add(self.tab_search, text=" 🔍 Ara ")
        self.setup_search_tab()

        if self.role in ['collector', 'admin']:
            self.tabs.add(self.tab_process, text=" ⚙️ İşlem Yap ")
            self.setup_process_tab()

        self.tabs.add(self.tab_review, text=" ⭐ Değerlendir ")
        self.setup_review_tab()
        
        self.tabs.add(self.tab_message, text=" 💬 Mesajlar ")
        self.setup_message_tab()
        
        self.tabs.add(self.tab_analysis, text=" 📊 Analiz ")
        self.setup_analysis_tab()

        if self.role == 'admin':
            self.tab_admin = ttk.Frame(self.tabs)
            self.tab_report = ttk.Frame(self.tabs)
            self.tabs.add(self.tab_admin, text=" 🛡️ YÖNETİM ")
            self.tabs.add(self.tab_report, text=" 📈 RAPORLAR ")
            self.setup_admin_tab()
            self.setup_report_tab()

        if self.role != 'admin':
            self.tabs.add(self.tab_profile, text=" 👤 Profilim ")
            self.setup_profile_tab()
        
        self.tabs.pack(expand=1, fill="both")

        self.refresh_locations() 

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        except Exception as e: messagebox.showerror("Hata", f"Bağlantı Hatası:\n{e}")

    def setup_header(self):
        # Modern Başlık (Header)
        header_frame = tk.Frame(self.root, bg=COLOR_PRIMARY, height=60)
        header_frame.pack(side="top", fill="x")
        
        welcome_text = f"Hoşgeldin, {self.username.upper()} (Rol: {self.role})"
        
        # Logo Sol
        tk.Label(header_frame, text="♻️ RecycleShare", font=("Segoe UI", 16, "bold"), bg=COLOR_PRIMARY, fg="white").pack(side="left", padx=20, pady=10)
        
        # Buton Sağ
        tk.Button(header_frame, text="Çıkış Yap", command=self.logout, bg="#D32F2F", fg="white", font=("Segoe UI", 9, "bold"), padx=10, bd=0).pack(side="right", padx=20, pady=10)
        
        # İsim Sağ
        tk.Label(header_frame, text=welcome_text, font=("Segoe UI", 11), bg=COLOR_PRIMARY, fg="#E8F5E9").pack(side="right", padx=10)

    def logout(self):
        if messagebox.askyesno("Çıkış", "Oturumu kapatmak istediğinize emin misiniz?"):
            if self.conn: self.conn.close()
            self.root.destroy()
            new_root = tk.Tk()
            LoginWindow(new_root)
            new_root.mainloop()

    def refresh_locations(self):
        loc_list = []
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT DISTINCT location FROM waste_items ORDER BY location")
            for row in cur.fetchall(): loc_list.append(row[0])
            cur.close()
            if hasattr(self, 'combo_search'):
                self.combo_search['values'] = loc_list
                if loc_list and not self.combo_search.get(): self.combo_search.current(0)
            if hasattr(self, 'combo_analysis_loc'):
                self.combo_analysis_loc['values'] = loc_list
                if loc_list and not self.combo_analysis_loc.get(): self.combo_analysis_loc.current(0)
        except Exception as e: print("Yenileme hatası:", e)

    # --- PROFİL & RAPOR TAB ---
    def setup_profile_tab(self):
        # Profil Kartı Tasarımı
        container = ttk.Frame(self.tab_profile)
        container.pack(expand=True, fill="both", padx=50, pady=30)
        
        card = tk.Frame(container, bg=COLOR_WHITE, padx=30, pady=30)
        card.pack(expand=True, fill="both")

        tk.Label(card, text=f"Sayın {self.username.upper()}", font=("Segoe UI", 20, "bold"), bg=COLOR_WHITE, fg=COLOR_PRIMARY).pack(pady=10)
        tk.Label(card, text="Kişisel Çevresel Etki Raporu", font=("Segoe UI", 12), bg=COLOR_WHITE, fg="gray").pack(pady=(0, 20))

        # İstatistik Alanı
        stats_frame = tk.Frame(card, bg=COLOR_WHITE)
        stats_frame.pack(pady=10)

        self.lbl_stat1 = tk.Label(stats_frame, text="Yükleniyor...", font=("Segoe UI", 16, "bold"), bg=COLOR_WHITE, fg="#388E3C")
        self.lbl_stat1.pack(pady=10)
        
        self.lbl_stat2 = tk.Label(stats_frame, text="", font=("Segoe UI", 14), bg=COLOR_WHITE, fg=COLOR_TEXT)
        self.lbl_stat2.pack(pady=5)
        
        self.lbl_stat3 = tk.Label(stats_frame, text="", font=("Segoe UI", 14), bg=COLOR_WHITE, fg=COLOR_TEXT)
        self.lbl_stat3.pack(pady=5)

        def load_my_stats():
            try:
                cur = self.conn.cursor()
                if self.role == 'user':
                    sql = """
                    SELECT 
                        COUNT(item_id), 
                        SUM(CASE WHEN status = 'Recycled' THEN weight_kg ELSE 0 END)
                    FROM waste_items 
                    WHERE user_id = %s
                    """
                    cur.execute(sql, (self.user_id,))
                    res = cur.fetchone()
                    count = res[0] if res[0] else 0
                    weight = res[1] if res[1] else 0
                    
                    cur.execute("SELECT score FROM users WHERE user_id = %s", (self.user_id,))
                    score = cur.fetchone()[0]
                    
                    self.lbl_stat1.config(text=f"♻️ Onaylanmış Dönüşüm: {weight:.2f} KG")
                    self.lbl_stat2.config(text=f"📦 Toplam İlan Sayısı: {count}")
                    self.lbl_stat3.config(text=f"⭐ Mevcut Puanınız: {score}")

                elif self.role == 'collector':
                    sql = """
                    SELECT COUNT(b.booking_id), SUM(w.weight_kg)
                    FROM bookings b 
                    JOIN waste_items w ON b.item_id = w.item_id 
                    WHERE b.collector_id = %s
                    """
                    cur.execute(sql, (self.user_id,))
                    res = cur.fetchone()
                    count = res[0] if res[0] else 0
                    weight = res[1] if res[1] else 0
                    
                    self.lbl_stat1.config(text=f"🚛 Toplam Toplanan Atık: {weight:.2f} KG")
                    self.lbl_stat2.config(text=f"✅ Tamamlanan İşlem: {count}")
                    self.lbl_stat3.config(text="Teşekkürler, dünyayı temizliyorsunuz!")
                
                self.conn.commit()
                cur.close()
            except Exception as e:
                self.conn.rollback()
                self.lbl_stat1.config(text="Veri çekilemedi.")
                print(e)

        ttk.Button(card, text="Raporumu Güncelle", command=load_my_stats).pack(pady=30, ipadx=20)
        load_my_stats()

    # SEKME 1: İLAN VERME
    def setup_add_tab(self):
        frame = ttk.Labelframe(self.tab_add, text="Atık Bilgileri", padding=20) # Labelframe ile çerçeve
        frame.pack(padx=30, pady=30, fill="both", expand=True)
        
        self.cat_map = {} 
        cat_names = []
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT category_id, name FROM categories ORDER BY category_id")
            for row in cur.fetchall():
                self.cat_map[row[1]] = row[0]
                cat_names.append(row[1])
            cur.close()
        except: pass

        entries = {}
        # Grid düzeni ile daha hizalı form
        ttk.Label(frame, text=f"Kullanıcı: {self.username} (ID: {self.user_id})").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        ttk.Label(frame, text="Kategori Seç:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        entries["cat"] = ttk.Combobox(frame, values=cat_names, state="readonly", width=30)
        entries["cat"].grid(row=1, column=1, padx=10, pady=10, sticky="w")
        if cat_names: entries["cat"].current(0)

        labels = ["Açıklama:", "Ağırlık (KG):", "Konum (İlçe):"]
        keys = ["desc", "w", "loc"]
        for i, (lbl, key) in enumerate(zip(labels, keys)):
            ttk.Label(frame, text=lbl).grid(row=i+2, column=0, padx=10, pady=10, sticky="e")
            entries[key] = ttk.Entry(frame, width=32)
            entries[key].grid(row=i+2, column=1, padx=10, pady=10, sticky="w")
            
        def save():
            try:
                selected_name = entries["cat"].get()
                if not selected_name:
                    messagebox.showwarning("Uyarı", "Kategori seçiniz.")
                    return
                selected_id = self.cat_map[selected_name]
                cur = self.conn.cursor()
                cur.execute("INSERT INTO waste_items (user_id, category_id, description, weight_kg, location) VALUES (%s, %s, %s, %s, %s)",
                            (self.user_id, selected_id, entries["desc"].get(), entries["w"].get(), entries["loc"].get()))
                self.conn.commit()
                cur.close()
                messagebox.showinfo("Başarılı", "İlan eklendi!")
                self.refresh_locations() 
            except Exception as e:
                self.conn.rollback()
                messagebox.showerror("Hata", str(e))
        
        ttk.Button(frame, text="✅ İlanı Kaydet", command=save).grid(row=6, column=1, pady=20, sticky="ew")

    # SEKME 2: ARAMA
    def setup_search_tab(self):
        # Filtre Alanı
        frame = ttk.Frame(self.tab_search)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        sch_frame = ttk.Frame(frame)
        sch_frame.pack(fill="x", pady=10)
        
        ttk.Label(sch_frame, text="Konum Filtrele:", font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
        self.combo_search = ttk.Combobox(sch_frame, state="readonly", width=25)
        self.combo_search.pack(side="left", padx=5)
        
        ttk.Button(sch_frame, text="Ara", command=lambda: search()).pack(side="left", padx=10)
        ttk.Button(sch_frame, text="Listeyi Yenile", command=self.refresh_locations).pack(side="left")

        # Tablo
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill="both", expand=True)
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        tree = ttk.Treeview(list_frame, columns=("ID", "Açıklama", "KG", "Durum", "Konum", "Ekleyen"), show="headings", yscrollcommand=scrollbar.set)
        for c in tree["columns"]: tree.heading(c, text=c)
        
        tree.column("ID", width=40, anchor="center")
        tree.column("KG", width=60, anchor="center")
        tree.column("Durum", width=80, anchor="center")
        tree.column("Konum", width=100, anchor="center")
        tree.column("Ekleyen", width=100, anchor="center")
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=tree.yview)
        
        def search():
            for i in tree.get_children(): tree.delete(i)
            try:
                cur = self.conn.cursor()
                sql = """
                SELECT w.item_id, w.description, w.weight_kg, w.status, w.location, u.username
                FROM waste_items w
                JOIN users u ON w.user_id = u.user_id
                WHERE w.location = %s
                """
                cur.execute(sql, (self.combo_search.get(),))
                for row in cur.fetchall(): tree.insert("", "end", values=row)
                cur.close()
            except Exception as e: messagebox.showerror("Hata", str(e))

    # SEKME 3: İŞLEM YAP
    def setup_process_tab(self):
        container = ttk.Frame(self.tab_process)
        container.pack(fill="both", expand=True, padx=30, pady=20)

        # Kart 1: Rezervasyon
        frame_res = ttk.Labelframe(container, text="1. Rezervasyon Yap (Trigger)", padding=20)
        frame_res.pack(fill="x", pady=10)
        ttk.Label(frame_res, text="Ürün ID:").pack(side="left", padx=5)
        e_item = ttk.Entry(frame_res, width=10)
        e_item.pack(side="left", padx=5)
        
        def reserve():
            try:
                cur = self.conn.cursor()
                cur.execute("INSERT INTO bookings (item_id, collector_id) VALUES (%s, %s)", (e_item.get(), self.user_id))
                self.conn.commit()
                msg = "Rezervasyon Başarılı!"
                if self.conn.notices:
                    msg += "\nDB Mesajı: " + self.conn.notices[-1]
                    del self.conn.notices[:]
                cur.close()
                messagebox.showinfo("Başarılı", msg)
            except Exception as e:
                self.conn.rollback()
                messagebox.showerror("Hata", str(e))
        ttk.Button(frame_res, text="Rezerve Et", command=reserve).pack(side="left", padx=20)

        # Kart 2: Teslim Alma
        frame_col = ttk.Labelframe(container, text="2. Teslim Aldım (Statü + Puan)", padding=20)
        frame_col.pack(fill="x", pady=10)
        ttk.Label(frame_col, text="Teslim Alınan Ürün ID:").pack(side="left", padx=5)
        e_col_item = ttk.Entry(frame_col, width=10)
        e_col_item.pack(side="left", padx=5)

        def collect():
            try:
                cur = self.conn.cursor()
                sql_update = "UPDATE waste_items SET status = 'Recycled' WHERE item_id = %s AND status = 'Reserved'"
                cur.execute(sql_update, (e_col_item.get(),))
                if cur.rowcount == 0:
                    messagebox.showwarning("Uyarı", "Hata: Ürün bulunamadı veya rezerve değil.")
                    self.conn.rollback()
                    return
                cur.execute("SELECT user_id FROM waste_items WHERE item_id = %s", (e_col_item.get(),))
                target_user = cur.fetchone()[0]
                cur.execute("SELECT update_user_score(%s, %s)", (target_user, 10))
                self.conn.commit()
                cur.close()
                messagebox.showinfo("Başarılı", "Teslim alındı, 10 puan verildi!")
            except Exception as e:
                self.conn.rollback()
                messagebox.showerror("Hata", str(e))
        ttk.Button(frame_col, text="Teslim Al", command=collect).pack(side="left", padx=20)

    # SEKME 4: DEĞERLENDİRME
    def setup_review_tab(self):
        # Yorum Ekleme Paneli
        frame = ttk.Frame(self.tab_review)
        frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        top_frame = ttk.Frame(frame)
        top_frame.pack(fill="x", pady=5)

        self.user_map = {} 
        user_names = []
        try:
            cur = self.conn.cursor()
            sql = "SELECT user_id, username FROM users WHERE user_id != %s AND role != 'admin' ORDER BY username"
            cur.execute(sql, (self.user_id,))
            for row in cur.fetchall():
                self.user_map[row[1]] = row[0]
                user_names.append(row[1])
            cur.close()
        except: pass

        ttk.Label(top_frame, text="Hedef Kullanıcı:").pack(side="left", padx=5)
        self.combo_target_user = ttk.Combobox(top_frame, values=user_names, state="readonly", width=15)
        self.combo_target_user.pack(side="left", padx=5)
        if user_names: self.combo_target_user.current(0)

        ttk.Label(top_frame, text="Puan (1-5):").pack(side="left", padx=5)
        rating = ttk.Spinbox(top_frame, from_=1, to=5, width=5)
        rating.pack(side="left", padx=5)
        rating.set(5)

        ttk.Label(top_frame, text="Yorum:").pack(side="left", padx=5)
        comment = ttk.Entry(top_frame, width=30)
        comment.pack(side="left", padx=5)

        def add_review():
            try:
                selected_name = self.combo_target_user.get()
                if not selected_name:
                    messagebox.showwarning("Uyarı", "Kullanıcı seçiniz.")
                    return
                target_id = self.user_map[selected_name]
                cur = self.conn.cursor()
                sql = "INSERT INTO reviews (reviewer_id, target_user_id, rating, comment) VALUES (%s, %s, %s, %s)"
                cur.execute(sql, (self.user_id, target_id, rating.get(), comment.get()))
                self.conn.commit()
                msg = "Değerlendirme kaydedildi!"
                if self.conn.notices:
                    msg += "\n" + self.conn.notices[-1]
                    del self.conn.notices[:]
                cur.close()
                messagebox.showinfo("Başarılı", msg)
            except Exception as e:
                self.conn.rollback()
                messagebox.showerror("Hata", str(e))
        ttk.Button(top_frame, text="Gönder", command=add_review).pack(side="left", padx=10)
        
        # Liste
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill="both", expand=True, pady=10)
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        tree = ttk.Treeview(list_frame, columns=("Kimden", "Kime", "Puan", "Yorum"), show="headings", yscrollcommand=scrollbar.set)
        for c in tree["columns"]: tree.heading(c, text=c)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=tree.yview)

        def refresh():
            for i in tree.get_children(): tree.delete(i)
            try:
                cur = self.conn.cursor()
                sql = """SELECT u1.username, u2.username, r.rating, r.comment FROM reviews r JOIN users u1 ON r.reviewer_id = u1.user_id JOIN users u2 ON r.target_user_id = u2.user_id ORDER BY r.review_id DESC"""
                cur.execute(sql)
                for row in cur.fetchall(): tree.insert("", "end", values=row)
                cur.close()
            except Exception: pass
        ttk.Button(frame, text="Listeyi Yenile", command=refresh).pack(pady=5)
        refresh()

    # SEKME 5: MESAJLAR
    def setup_message_tab(self):
        # Gönderim Alanı
        frame = ttk.Frame(self.tab_message)
        frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        send_frame = ttk.Labelframe(frame, text="Mesaj Gönder", padding=10)
        send_frame.pack(fill="x", pady=5)
        
        self.msg_user_map = {}
        msg_users = []
        try:
            cur = self.conn.cursor()
            sql = "SELECT user_id, username FROM users WHERE user_id != %s AND role != 'admin' ORDER BY username"
            cur.execute(sql, (self.user_id,))
            for row in cur.fetchall():
                self.msg_user_map[row[1]] = row[0]
                msg_users.append(row[1])
            cur.close()
        except: pass

        ttk.Label(send_frame, text="Alıcı:").pack(side="left", padx=5)
        self.combo_recv = ttk.Combobox(send_frame, values=msg_users, state="readonly", width=20)
        self.combo_recv.pack(side="left", padx=5)
        
        ttk.Label(send_frame, text="Mesaj:").pack(side="left", padx=5)
        msg_content = ttk.Entry(send_frame, width=40)
        msg_content.pack(side="left", padx=5)

        def send_msg():
            try:
                selected_name = self.combo_recv.get()
                if not selected_name: return messagebox.showwarning("Uyarı", "Alıcı seçiniz.")
                receiver_id = self.msg_user_map[selected_name]
                cur = self.conn.cursor()
                sql = "INSERT INTO messages (sender_id, receiver_id, message_content) VALUES (%s, %s, %s)"
                cur.execute(sql, (self.user_id, receiver_id, msg_content.get()))
                self.conn.commit()
                cur.close()
                messagebox.showinfo("Başarılı", "Mesaj gönderildi!")
                msg_content.delete(0, tk.END)
                check_inbox()
            except Exception as e:
                self.conn.rollback()
                messagebox.showerror("Hata", str(e))
        ttk.Button(send_frame, text="Gönder", command=send_msg).pack(side="left", padx=10)

        # Gelen Kutusu
        lbl_inbox = ttk.Label(frame, text="Gelen Kutusu", font=("Segoe UI", 10, "bold"))
        lbl_inbox.pack(pady=(15,5), anchor="w")
        
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill="both", expand=True)
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        tree = ttk.Treeview(list_frame, columns=("ID", "Kimden", "Mesaj", "Tarih"), show="headings", height=5, yscrollcommand=scrollbar.set)
        tree.column("ID", width=0, stretch=tk.NO)
        tree.column("Kimden", width=100)
        tree.column("Mesaj", width=300)
        tree.column("Tarih", width=120)
        for c in ["Kimden", "Mesaj", "Tarih"]: tree.heading(c, text=c)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=tree.yview)

        def check_inbox():
            for i in tree.get_children(): tree.delete(i)
            try:
                cur = self.conn.cursor()
                sql = """
                SELECT m.message_id, u.username, m.message_content, 
                       TO_CHAR(m.sent_at, 'DD.MM.YYYY HH24:MI:SS') 
                FROM messages m 
                JOIN users u ON m.sender_id = u.user_id 
                WHERE m.receiver_id = %s 
                ORDER BY m.sent_at DESC
                """
                cur.execute(sql, (self.user_id,))
                for row in cur.fetchall(): tree.insert("", "end", values=row)
                cur.close()
            except Exception: pass
            
        def delete_msg():
            selected_item = tree.selection()
            if not selected_item: return
            item_data = tree.item(selected_item)['values']
            msg_id = item_data[0]
            if messagebox.askyesno("Onay", "Bu mesajı silmek istiyor musunuz?"):
                try:
                    cur = self.conn.cursor()
                    cur.execute("DELETE FROM messages WHERE message_id = %s", (msg_id,))
                    self.conn.commit()
                    cur.close()
                    check_inbox()
                except Exception as e:
                    self.conn.rollback()
                    messagebox.showerror("Hata", str(e))

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Yenile", command=check_inbox).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Sil", command=delete_msg).pack(side="left", padx=5)
        check_inbox()

    # SEKME 6: ANALİZ
    def setup_analysis_tab(self):
        container = ttk.Frame(self.tab_analysis)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # 1. Bölge
        frame1 = ttk.Frame(container); frame1.pack(fill="x", pady=10)
        ttk.Label(frame1, text="1. Bölge Analizi:").pack(side="left", padx=5)
        self.combo_analysis_loc = ttk.Combobox(frame1, state="readonly", width=15)
        self.combo_analysis_loc.pack(side="left", padx=5)
        ttk.Button(frame1, text="↻", width=3, command=self.refresh_locations).pack(side="left", padx=2)
        def call_func1():
            try:
                cur = self.conn.cursor()
                cur.execute("SELECT list_waste_status_by_location(%s)", (self.combo_analysis_loc.get(),))
                res = cur.fetchone()[0]
                messagebox.showinfo("Rapor", res if res else "Kayıt yok.")
                cur.close()
            except Exception as e: messagebox.showerror("Hata", str(e))
        ttk.Button(frame1, text="Analiz Et", command=call_func1).pack(side="left", padx=5)

        # 2. Kategori
        frame2 = ttk.Frame(container); frame2.pack(fill="x", pady=10)
        ttk.Label(frame2, text="2. Kategori Toplamı:").pack(side="left", padx=5)
        cat_names = list(self.cat_map.keys()) if hasattr(self, 'cat_map') else []
        entry_cat = ttk.Combobox(frame2, values=cat_names, state="readonly", width=15)
        entry_cat.pack(side="left", padx=5)
        lbl_res2 = ttk.Label(frame2, text="0 KG", foreground=COLOR_PRIMARY, font=("Segoe UI", 10, "bold"))
        def call_func2():
            try:
                cur = self.conn.cursor()
                cur.execute("SELECT get_total_waste_by_category(%s)", (entry_cat.get(),))
                res = cur.fetchone()[0]
                lbl_res2.config(text=f"{res if res else 0} KG")
                cur.close()
            except Exception as e: messagebox.showerror("Hata", str(e))
        ttk.Button(frame2, text="Hesapla", command=call_func2).pack(side="left", padx=5)
        lbl_res2.pack(side="left", padx=20)

        # 3. Puan
        frame3 = ttk.Frame(container); frame3.pack(fill="x", pady=10)
        ttk.Label(frame3, text="3. Puan Tahmini:").pack(side="left", padx=5)
        entry_w = ttk.Entry(frame3, width=5); entry_w.pack(side="left", padx=5)
        ttk.Label(frame3, text="KG").pack(side="left")
        entry_cid = ttk.Combobox(frame3, values=cat_names, state="readonly", width=15)
        entry_cid.pack(side="left", padx=5)
        lbl_res3 = ttk.Label(frame3, text="Puan: 0", foreground="blue", font=("Segoe UI", 10, "bold"))
        def call_func3():
            try:
                cur = self.conn.cursor()
                cat_id = self.cat_map[entry_cid.get()]
                try:
                    cur.execute("SELECT calculate_potential_points(%s, %s)", (entry_w.get(), cat_id))
                    res = cur.fetchone()[0]
                except:
                    self.conn.rollback()
                    cur.execute("SELECT points_per_kg FROM categories WHERE category_id=%s", (cat_id,))
                    res = float(entry_w.get()) * float(cur.fetchone()[0])
                lbl_res3.config(text=f"Puan: {res}")
                cur.close()
            except Exception as e: messagebox.showerror("Hata", str(e))
        ttk.Button(frame3, text="Hesapla", command=call_func3).pack(side="left", padx=5)
        lbl_res3.pack(side="left", padx=20)

    # SEKME 7: ADMIN YÖNETİM
    def setup_admin_tab(self):
        f = ttk.Labelframe(self.tab_admin, text="Ürün Düzenle", padding=15); f.pack(fill="x", padx=20, pady=20)
        ttk.Label(f, text="ID:").grid(row=0, column=0); e_id = ttk.Entry(f, width=10); e_id.grid(row=0, column=1, padx=5)
        ttk.Label(f, text="Yeni KG:").grid(row=0, column=2); e_w = ttk.Entry(f, width=10); e_w.grid(row=0, column=3, padx=5)
        
        def upd():
            try: 
                c=self.conn.cursor(); c.execute("UPDATE waste_items SET weight_kg=%s WHERE item_id=%s", (e_w.get(), e_id.get())); self.conn.commit(); c.close(); messagebox.showinfo("OK", "Güncellendi")
            except Exception as e: self.conn.rollback(); messagebox.showerror("Hata", str(e))
        ttk.Button(f, text="Güncelle", command=upd).grid(row=0, column=4, padx=10)
        
        def dele():
            try: 
                c=self.conn.cursor(); c.execute("DELETE FROM waste_items WHERE item_id=%s", (e_id.get(),)); self.conn.commit(); c.close(); messagebox.showinfo("OK", "Silindi")
            except Exception as e: self.conn.rollback(); messagebox.showerror("Hata", str(e))
        ttk.Button(f, text="Sil", command=dele).grid(row=0, column=5, padx=10)

    def setup_report_tab(self):
        f = ttk.Frame(self.tab_report, padding=10); f.pack(fill="x")
        
        # Admin tablosu
        frame = ttk.Frame(self.tab_report)
        frame.pack(fill="both", expand=True)
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        tree = ttk.Treeview(frame, columns=["Kullanıcı", "Veri 1", "Veri 2", "Veri 3"], show="headings", yscrollcommand=scrollbar.set)
        for c in ["Kullanıcı", "Veri 1", "Veri 2", "Veri 3"]: tree.heading(c, text=c); tree.column(c, anchor="center")
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=tree.yview)

        def run(sql, cols=None):
            for i in tree.get_children(): tree.delete(i)
            if cols:
                tree["columns"] = cols
                for c in cols: tree.heading(c, text=c)
            try: 
                c=self.conn.cursor(); c.execute(sql)
                for r in c.fetchall(): tree.insert("", "end", values=r)
                c.close()
            except Exception as e: messagebox.showerror("Hata", str(e))
            
        ttk.Button(f, text="Etki Raporu (View)", command=lambda: run("SELECT * FROM v_user_impact_report", ["Kullanıcı", "Adet", "KG", "Puan"])).pack(side="left", padx=5)
        ttk.Button(f, text="Aktivite (Union)", command=lambda: run("SELECT u.username, 'İlan Sahibi' FROM users u JOIN waste_items w ON u.user_id=w.user_id UNION SELECT u.username, 'Toplayıcı' FROM users u JOIN bookings b ON u.user_id=b.collector_id", ["Kullanıcı", "Rol"])).pack(side="left", padx=5)
        ttk.Button(f, text="Büyük Atıklar (Having)", command=lambda: run("SELECT c.name, AVG(w.weight_kg), COUNT(w.item_id) FROM waste_items w JOIN categories c ON w.category_id=c.category_id GROUP BY c.name HAVING AVG(w.weight_kg)>2.0", ["Kategori", "Ort KG", "Adet"])).pack(side="left", padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()