"""
Guia de Alter - Painel de Controle (Control Panel)
Interface gráfica para gerenciar o servidor local e o túnel Cloudflare.
Baseado no DashboardMobileView.py
"""
import customtkinter as ctk
import threading
import subprocess
import socket
import sys
import qrcode
import os
import shutil
import psutil
import urllib.request
import re
from pathlib import Path
from tkinter import messagebox
from PIL import Image

# Configuração do CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ControlPanel(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("🌴 Guia de Alter - Central de Comando")
        self.geometry("600x750")
        self.resizable(False, False)
        
        # Centraliza na tela
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 300
        y = (self.winfo_screenheight() // 2) - 375
        self.geometry(f"+{x}+{y}")
        
        self.dashboard_process = None
        self.cloudflare_process = None
        self.cloudflare_url = None
        
        self._criar_interface()
        
    def _criar_interface(self):
        # Container principal
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)
        
        self._mostrar_tela_principal()
        
    def _mostrar_tela_principal(self):
        # Limpa container
        for widget in self.main_container.winfo_children():
            widget.destroy()
            
        # Header
        header = ctk.CTkFrame(self.main_container, height=80, fg_color="#2196F3", corner_radius=0)
        header.pack(fill="x")
        
        ctk.CTkLabel(
            header,
            text="🌴 Guia de Alter",
            font=("Segoe UI", 26, "bold"),
            text_color="white"
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            header,
            text="Central de Comando",
            font=("Segoe UI", 14),
            text_color="#E3F2FD"
        ).pack(pady=(0, 15))
        
        # Scroll container
        scroll = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Card Servidor Local
        self._criar_card_servidor_local(scroll)
        
        # Espaçamento
        ctk.CTkFrame(scroll, height=20, fg_color="transparent").pack()
        
        # Card Cloudflare
        self._criar_card_cloudflare(scroll)
        
        # Footer
        footer = ctk.CTkFrame(self.main_container, height=40, fg_color="#1a1a1a", corner_radius=0)
        footer.pack(fill="x", side="bottom")
        
        ctk.CTkLabel(
            footer,
            text="v1.0.0 - Desktop Edition",
            font=("Segoe UI", 10),
            text_color="gray"
        ).pack(pady=10)

    # ==================== HELPER FUNCTIONS ====================
    
    def get_local_ip(self):
        """Retorna o melhor IP local (RFC 1918)"""
        try:
            candidates = []
            hostname = socket.gethostname()
            for ip in socket.gethostbyname_ex(hostname)[2]:
                if ip.startswith("127.") or ip.startswith("26."): continue
                
                is_private = False
                if ip.startswith("192.168."): is_private = True
                elif ip.startswith("10."): is_private = True
                elif ip.startswith("172."):
                    try:
                        second_octet = int(ip.split('.')[1])
                        if 16 <= second_octet <= 31: is_private = True
                    except: pass
                
                if is_private: candidates.append(ip)
            
            candidates.sort(key=lambda x: (
                not x.startswith("192.168."),
                not x.startswith("172."),
                not x.startswith("10.")
            ))
            
            if candidates: return candidates[0]
            
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

    def check_server_running(self):
        """Verifica se servidor Flask está rodando na porta 5000"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex(('127.0.0.1', 5000))
            sock.close()
            return result == 0
        except:
            return False

    def wait_for_server_start(self, timeout=30):
        import time
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.check_server_running():
                return True
            time.sleep(0.5)
        return False

    def gerar_qr_code(self, url):
        try:
            qr = qrcode.QRCode(version=1, box_size=8, border=2)
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img = img.resize((140, 140))
            return ctk.CTkImage(light_image=img, dark_image=img, size=(140, 140))
        except Exception as e:
            print(f"Erro QR: {e}")
            return None

    def copiar_url(self, url):
        self.clipboard_clear()
        self.clipboard_append(url)
        messagebox.showinfo("Copiado", "Link copiado para a área de transferência!")

    # ==================== SERVIDOR LOCAL ====================

    def iniciar_servidor_local(self):
        try:
            python_exe = sys.executable
            script_path = Path("run.py").absolute()
            
            if not script_path.exists():
                messagebox.showerror("Erro", f"Arquivo run.py não encontrado:\n{script_path}")
                return
            
            # Define variável de ambiente para IP local
            env = os.environ.copy()
            env['LOCAL_IP'] = self.get_local_ip()
            
            self.dashboard_process = subprocess.Popen(
                [python_exe, str(script_path)],
                cwd=str(Path.cwd()),
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0,
                env=env
            )
            
            messagebox.showinfo("Iniciando", "O servidor está iniciando...\nAguarde o status mudar para 'Ativo'.")

            def aguardar():
                if self.wait_for_server_start():
                    self.after(0, self._mostrar_tela_principal)
                else:
                    messagebox.showerror("Erro", "Timeout aguardando servidor iniciar na porta 5000.")
                    self.after(0, self._mostrar_tela_principal)

            threading.Thread(target=aguardar, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao iniciar servidor: {e}")

    def parar_servidor_local(self):
        try:
            self.parar_tunnel_cloudflare()
            
            if self.dashboard_process:
                self.dashboard_process.terminate()
                self.dashboard_process = None
            
            # Mata processos na porta 5000
            for proc in psutil.process_iter(['pid', 'name', 'connections']):
                try:
                    for conn in proc.connections(kind='inet'):
                        if conn.laddr.port == 5000:
                            proc.terminate()
                except: pass
            
            self._mostrar_tela_principal()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao parar: {e}")

    def _criar_card_servidor_local(self, parent):
        card = ctk.CTkFrame(parent, fg_color="#1E1E1E", corner_radius=10)
        card.pack(fill="x", pady=10)
        
        ctk.CTkLabel(card, text="🏠 Servidor Local (Wi-Fi)", font=("Segoe UI", 18, "bold"), anchor="w").pack(fill="x", padx=20, pady=(15, 5))
        
        running = self.check_server_running()
        
        if not running:
            ctk.CTkLabel(card, text="⚪ Servidor Parado", font=("Segoe UI", 14), text_color="gray", anchor="w").pack(fill="x", padx=20, pady=10)
            ctk.CTkButton(card, text="▶️ Iniciar Servidor", font=("Segoe UI", 14, "bold"), fg_color="#4CAF50", hover_color="#388E3C", height=45, command=self.iniciar_servidor_local).pack(fill="x", padx=20, pady=(15, 20))
        else:
            ctk.CTkLabel(card, text="🟢 Servidor Ativo", font=("Segoe UI", 14, "bold"), text_color="#4CAF50", anchor="w").pack(fill="x", padx=20, pady=10)
            
            local_ip = self.get_local_ip()
            url = f"http://{local_ip}:5000"
            
            info_frame = ctk.CTkFrame(card, fg_color="#2C2C2C")
            info_frame.pack(fill="x", padx=20, pady=10)
            
            ctk.CTkLabel(info_frame, text=url, font=("Consolas", 14, "bold"), text_color="#F57C00").pack(pady=10)
            
            qr = self.gerar_qr_code(url)
            if qr: ctk.CTkLabel(info_frame, text="", image=qr).pack(pady=10)
            
            ctk.CTkButton(info_frame, text="📋 Copiar", command=lambda: self.copiar_url(url)).pack(pady=10)
            
            ctk.CTkButton(card, text="⏸️ Parar Servidor", font=("Segoe UI", 14, "bold"), fg_color="#F44336", hover_color="#D32F2F", height=45, command=self.parar_servidor_local).pack(fill="x", padx=20, pady=(10, 20))

    # ==================== CLOUDFLARE ====================

    def verificar_cloudflared(self):
        status = {'instalado': False, 'rodando': False, 'url': None, 'path': 'cloudflared'}
        
        # Verifica bin local
        bin_dir = Path("bin")
        local_bin = bin_dir / "cloudflared.exe"
        if local_bin.exists():
            status['path'] = str(local_bin)
            status['instalado'] = True
        elif shutil.which("cloudflared"):
            status['instalado'] = True
            
        if self.cloudflare_process and self.cloudflare_process.poll() is None:
            status['rodando'] = True
            status['url'] = self.cloudflare_url
            
        return status

    def baixar_cloudflared(self):
        try:
            bin_dir = Path("bin")
            bin_dir.mkdir(exist_ok=True)
            target = bin_dir / "cloudflared.exe"
            
            url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
            urllib.request.urlretrieve(url, str(target))
            return str(target)
        except Exception as e:
            print(f"Erro download: {e}")
            return None

    def monitorar_tunnel(self, process):
        while True:
            if process.poll() is not None: break
            line = process.stderr.readline()
            if not line: break
            
            if "trycloudflare.com" in line:
                match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
                if match:
                    self.cloudflare_url = match.group(0)
                    self.after(0, self._mostrar_tela_principal)
                    return

    def iniciar_tunnel(self):
        if not self.check_server_running():
            messagebox.showwarning("Aviso", "Inicie o servidor local primeiro!")
            return
            
        status = self.verificar_cloudflared()
        if not status['instalado']:
            if messagebox.askyesno("Baixar", "Cloudflared não encontrado. Baixar agora?"):
                path = self.baixar_cloudflared()
                if not path:
                    messagebox.showerror("Erro", "Falha no download.")
                    return
                status['path'] = path
            else:
                return
                
        cmd = [status['path'], "tunnel", "--url", "http://localhost:5000"]
        
        self.cloudflare_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            encoding='utf-8',
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        )
        
        threading.Thread(target=self.monitorar_tunnel, args=(self.cloudflare_process,), daemon=True).start()
        messagebox.showinfo("Iniciado", "Tunnel iniciado! Aguarde o link aparecer.")
        self._mostrar_tela_principal()

    def parar_tunnel_cloudflare(self):
        if self.cloudflare_process:
            self.cloudflare_process.terminate()
            self.cloudflare_process = None
        
        # Mata processos cloudflared
        for proc in psutil.process_iter(['name']):
            if 'cloudflared' in proc.info['name'].lower():
                try: proc.terminate() 
                except: pass
                
        self.cloudflare_url = None
        self._mostrar_tela_principal()

    def _criar_card_cloudflare(self, parent):
        card = ctk.CTkFrame(parent, fg_color="#1E1E1E", corner_radius=10)
        card.pack(fill="x", pady=10)
        
        ctk.CTkLabel(card, text="☁️ Cloudflare Tunnel (Internet)", font=("Segoe UI", 18, "bold"), anchor="w").pack(fill="x", padx=20, pady=(15, 5))
        
        status = self.verificar_cloudflared()
        
        if not status['rodando']:
            ctk.CTkLabel(card, text="⚪ Tunnel Parado", font=("Segoe UI", 14), text_color="gray", anchor="w").pack(fill="x", padx=20, pady=10)
            ctk.CTkButton(card, text="🚀 Iniciar Tunnel", font=("Segoe UI", 14, "bold"), fg_color="#2196F3", hover_color="#1976D2", height=45, command=self.iniciar_tunnel).pack(fill="x", padx=20, pady=(15, 20))
        else:
            ctk.CTkLabel(card, text="🟢 Tunnel Ativo", font=("Segoe UI", 14, "bold"), text_color="#4CAF50", anchor="w").pack(fill="x", padx=20, pady=10)
            
            url = status['url']
            if url:
                info_frame = ctk.CTkFrame(card, fg_color="#2C2C2C")
                info_frame.pack(fill="x", padx=20, pady=10)
                
                ctk.CTkLabel(info_frame, text=url, font=("Consolas", 14, "bold"), text_color="#F57C00").pack(pady=10)
                
                qr = self.gerar_qr_code(url)
                if qr: ctk.CTkLabel(info_frame, text="", image=qr).pack(pady=10)
                
                ctk.CTkButton(info_frame, text="📋 Copiar", command=lambda: self.copiar_url(url)).pack(pady=10)
            else:
                ctk.CTkLabel(card, text="⏳ Gerando link...", font=("Segoe UI", 12, "italic"), text_color="#FF9800").pack(pady=10)
                
            ctk.CTkButton(card, text="🛑 Parar Tunnel", font=("Segoe UI", 14, "bold"), fg_color="#F44336", hover_color="#D32F2F", height=45, command=self.parar_tunnel_cloudflare).pack(fill="x", padx=20, pady=(10, 20))

if __name__ == "__main__":
    app = ControlPanel()
    app.mainloop()
