"""
Dashboard Mobile View - Module Separado
Interface para gerenciar servidores Local e Cloudflare Tunnel
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
from pathlib import Path
from tkinter import messagebox
from src.utils.logger import get_logger

logger = get_logger()


class DashboardMobileView:
    """
    View separada para Dashboard Mobile
    Gerencia 2 servidores independentes:
    - Servidor Local (Flask)
    - Cloudflare Tunnel
    """
    
    def __init__(self, parent, usuario):
        """
        Inicializa a janela de Dashboard Mobile
        
        Args:
            parent: Janela pai (root)
            usuario: Usuário autenticado
        """
        self.parent = parent
        self.usuario = usuario
        self.dashboard_process = None
        self.cloudflare_process = None
        self.cloudflare_url = None
        
        self._criar_dialog()
        self._mostrar_tela_principal()
    
    # ==================== HELPER FUNCTIONS ====================
    
    def verificar_cloudflared(self):
        """
        Verifica status do Cloudflare Tunnel
        Returns: dict com 'instalado', 'rodando', 'url'
        """
        status = {
            'instalado': False,
            'rodando': False,
            'url': None,
            'path': 'cloudflared' # Default to PATH
        }
        
        try:
            # 1. Verifica pasta bin local (prioridade)
            local_bin = Path(__file__).parent.parent.parent / "bin" / "cloudflared.exe"
            if local_bin.exists():
                status['path'] = str(local_bin)
            
            # 2. Tenta encontrar o executável se não estiver no PATH ou bin local
            elif not shutil.which("cloudflared"):
                common_paths = [
                    r"C:\Program Files\cloudflared\cloudflared.exe",
                    r"C:\Program Files (x86)\cloudflared\cloudflared.exe",
                    os.path.expanduser(r"~\cloudflared.exe"),
                    os.path.expanduser(r"~\AppData\Local\Microsoft\WinGet\Packages\Cloudflare.cloudflared_Microsoft.Winget.Source_8wekyb3d8bbwe\cloudflared.exe")
                ]
                for path in common_paths:
                    if os.path.exists(path):
                        status['path'] = path
                        break

            # Verifica instalação
            result = subprocess.run(
                [status['path'], "--version"],
                capture_output=True,
                timeout=5,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            )
            status['instalado'] = (result.returncode == 0)
            
            if not status['instalado']:
                return status
            
            # Verifica se está rodando (apenas o processo gerenciado por nós)
            if self.cloudflare_process and self.cloudflare_process.poll() is None:
                status['rodando'] = True
                status['url'] = self.cloudflare_url
            else:
                status['rodando'] = False
                status['url'] = None
                    
        except FileNotFoundError:
            # Erro específico quando o executável não é encontrado
            status['instalado'] = False
        except Exception as e:
            logger.error(f"Erro ao verificar cloudflared: {e}")
        
        return status

    def baixar_cloudflared(self):
        """Baixa o executável do cloudflared automaticamente"""
        try:
            bin_dir = Path(__file__).parent.parent.parent / "bin"
            bin_dir.mkdir(exist_ok=True)
            target_path = bin_dir / "cloudflared.exe"
            
            logger.info("Iniciando download do cloudflared...")
            
            # URL oficial do Cloudflare (Windows amd64)
            url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
            
            import urllib.request
            
            # Mostra progresso (simplificado)
            def report(block_num, block_size, total_size):
                if block_num % 100 == 0:
                    logger.info(f"Baixando: {block_num * block_size / 1024 / 1024:.1f} MB")
            
            urllib.request.urlretrieve(url, str(target_path), reporthook=report)
            
            if target_path.exists():
                logger.info("Download concluído com sucesso!")
                return str(target_path)
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao baixar cloudflared: {e}")
            return None
    
    def get_local_ip(self):
        """
        Retorna o melhor IP local (RFC 1918), ignorando VPNs/Hamachi.
        Prioridade: 192.168.x.x > 172.16-31.x.x > 10.x.x.x
        """
        try:
            candidates = []
            hostname = socket.gethostname()
            # Obtém todos os IPs associados ao hostname
            for ip in socket.gethostbyname_ex(hostname)[2]:
                # Filtra loopback e IPs de VPN conhecidos (Hamachi usa 26.x.x.x)
                if ip.startswith("127.") or ip.startswith("26."): 
                    continue
                
                # Check RFC 1918 (redes privadas reais)
                is_private = False
                if ip.startswith("192.168."): is_private = True
                elif ip.startswith("10."): is_private = True
                elif ip.startswith("172."):
                    try:
                        second_octet = int(ip.split('.')[1])
                        if 16 <= second_octet <= 31: is_private = True
                    except: pass
                
                # Adiciona apenas IPs privados válidos
                if is_private:
                    candidates.append(ip)
            
            # Ordena por prioridade (192.168.x.x primeiro)
            candidates.sort(key=lambda x: (
                not x.startswith("192.168."), # False (0) vem antes
                not x.startswith("172."),
                not x.startswith("10.")
            ))
            
            if candidates:
                logger.info(f"IP local selecionado: {candidates[0]} (de {len(candidates)} candidatos)")
                return candidates[0]
                
            # Fallback: Tenta conectar ao Google DNS para descobrir a rota padrão
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            
            # Verifica se o fallback também é privado e não é VPN
            if (ip.startswith("192.168.") or ip.startswith("10.")) and not ip.startswith("26."):
                logger.info(f"IP local (fallback): {ip}")
                return ip
                
            logger.warning("Nenhum IP local válido encontrado, usando localhost")
            return "127.0.0.1" # Último recurso
            
        except Exception as e:
            logger.error(f"Erro ao obter IP local: {e}")
            return "127.0.0.1"
    
    def check_server_running(self):
        """Verifica se servidor Flask está rodando na porta 8080"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex(('127.0.0.1', 8080))
            sock.close()
            return result == 0
        except:
            return False

    def wait_for_server_start(self, timeout=30):
        """Aguardar o servidor iniciar na porta 8080"""
        import time
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.check_server_running():
                return True
            time.sleep(0.5)
        return False
    
    def gerar_qr_code(self, url):
        """Gera QR code otimizado para CustomTkinter"""
        try:
            qr = qrcode.QRCode(version=1, box_size=8, border=2)
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img = img.resize((140, 140))
            return ctk.CTkImage(light_image=img, dark_image=img, size=(140, 140))
        except Exception as e:
            logger.error(f"Erro ao gerar QR code: {e}")
            return None
    
    def copiar_url(self, url):
        """Copia URL para clipboard"""
        self.parent.clipboard_clear()
        self.parent.clipboard_append(url)
        messagebox.showinfo(
            "✅ Copiado!", 
            "Link copiado para a área de transferência!", 
            parent=self.dialog
        )
    
    # ==================== SERVIDOR LOCAL ====================
    
    def iniciar_servidor_local(self):
        """Inicia servidor Flask local"""
        try:
            python_exe = sys.executable
            script_path = Path(__file__).parent.parent / "web" / "dashboard.py"
            
            if not script_path.exists():
                messagebox.showerror(
                    "Erro", 
                    f"Dashboard não encontrado:\n{script_path}", 
                    parent=self.dialog
                )
                return
            
            # Inicia o processo
            self.dashboard_process = subprocess.Popen(
                [python_exe, str(script_path)],
                cwd=str(Path(__file__).parent.parent.parent),
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
            )
            
            logger.info("Servidor local iniciado (processo criado)")
            
            # Feedback visual imediato
            messagebox.showinfo(
                "Iniciando", 
                "O servidor está iniciando...\nAguarde alguns segundos até que o status mude para 'Ativo'.",
                parent=self.dialog
            )

            # Thread para aguardar inicialização e atualizar UI
            def aguardar_inicio():
                if self.wait_for_server_start():
                    logger.info("Servidor detectado na porta 8080")
                    self.dialog.after(0, self._atualizar_tela_principal)
                else:
                    logger.warning("Timeout aguardando servidor iniciar")
                    # Verifica se o processo ainda está rodando
                    if self.dashboard_process and self.dashboard_process.poll() is None:
                        # Processo rodando mas não respondendo na porta
                        self.dialog.after(0, lambda: messagebox.showerror(
                            "Erro", 
                            "O servidor foi iniciado mas não está respondendo na porta 8080.\n\n"
                            "Possíveis causas:\n"
                            "• Porta 8080 já está em uso\n"
                            "• Erro ao importar dependências (verifique se SQLAlchemy está instalado)\n"
                            "• Verifique a janela do console para mais detalhes",
                            parent=self.dialog
                        ))
                    else:
                        # Processo morreu
                        self.dialog.after(0, lambda: messagebox.showerror(
                            "Erro", 
                            "O servidor falhou ao iniciar.\n\n"
                            "Verifique a janela do console para detalhes do erro.",
                            parent=self.dialog
                        ))
                    self.dialog.after(0, self._atualizar_tela_principal)

            threading.Thread(target=aguardar_inicio, daemon=True).start()
            
        except Exception as e:
            logger.error(f"Erro ao iniciar servidor: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Erro ao iniciar servidor:\n{e}", parent=self.dialog)
    
    def monitorar_tunnel_output(self, process):
        """Monitora stdout/stderr do cloudflared para capturar a URL"""
        try:
            while True:
                if process.poll() is not None:
                    break
                    
                # Lê linha por linha
                line = process.stderr.readline()
                if not line:
                    break
                    
                line = line.strip()
                if "trycloudflare.com" in line:
                    # Extrai URL
                    parts = line.split()
                    for part in parts:
                        if "trycloudflare.com" in part and part.startswith("https://"):
                            self.cloudflare_url = part
                            logger.info(f"URL do Tunnel capturada: {self.cloudflare_url}")
                            # Atualiza UI na thread principal
                            self.dialog.after(0, self._atualizar_tela_principal)
                            return
        except Exception as e:
            logger.error(f"Erro ao monitorar tunnel: {e}")

    def iniciar_tunnel_cloudflare(self, tunnel_name="padaria"):
        """Inicia o tunnel do Cloudflare usando subprocess"""
        # 1. Pré-verificação: Servidor Local deve estar rodando
        if not self.check_server_running():
            messagebox.showwarning(
                "Servidor Parado", 
                "O Servidor Local precisa estar rodando antes de iniciar o Tunnel.\n\n"
                "Por favor, inicie o Dashboard Local primeiro.", 
                parent=self.dialog
            )
            return

        try:
            # Verifica path correto
            status = self.verificar_cloudflared()
            if not status['instalado']:
                # Tenta baixar automaticamente
                if messagebox.askyesno("Cloudflared Ausente", "O componente 'cloudflared' não foi encontrado.\nDeseja baixá-lo automaticamente agora?", parent=self.dialog):
                    path = self.baixar_cloudflared()
                    if path:
                        status['path'] = path
                        status['instalado'] = True
                        messagebox.showinfo("Sucesso", "Componente baixado com sucesso!", parent=self.dialog)
                    else:
                        messagebox.showerror("Erro", "Falha ao baixar componente. Verifique sua internet.", parent=self.dialog)
                        return
                else:
                    return
                
            cmd = [status.get('path', 'cloudflared'), "tunnel"]
            if tunnel_name:
                # Named Tunnel
                cmd.extend(["run", tunnel_name])
            else:
                # Quick Tunnel
                cmd.extend(["--url", "http://localhost:8080"])
                
            self.cloudflare_process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True,
                bufsize=1,
                universal_newlines=True,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            )
            
            # Inicia thread de monitoramento
            monitor_thread = threading.Thread(
                target=self.monitorar_tunnel_output, 
                args=(self.cloudflare_process,),
                daemon=True
            )
            monitor_thread.start()
            
            type_msg = f"'{tunnel_name}'" if tunnel_name else "Rápido (TryCloudflare)"
            messagebox.showinfo("Tunnel Iniciado", f"Cloudflare Tunnel {type_msg} iniciado.\nAguarde a geração do link público...", parent=self.dialog)
            self._atualizar_tela_principal()
        except Exception as e:
            logger.error(f"Erro ao iniciar tunnel: {e}")
            messagebox.showerror("Erro", f"Falha ao iniciar tunnel: {e}", parent=self.dialog)

    def parar_tunnel_cloudflare(self):
        """Para o tunnel do Cloudflare em execução."""
        if self.cloudflare_process and self.cloudflare_process.poll() is None:
            self.cloudflare_process.terminate()
            try:
                self.cloudflare_process.wait(timeout=5)
            except Exception:
                self.cloudflare_process.kill()
            self.cloudflare_process = None
            messagebox.showinfo("Tunnel Parado", "Cloudflare Tunnel foi interrompido.", parent=self.dialog)
            self._atualizar_tela_principal()
        else:
            # Tenta matar qualquer processo cloudflared
            killed = False
            for proc in psutil.process_iter(['name']):
                if 'cloudflared' in proc.info['name'].lower():
                    try:
                        proc.terminate()
                        killed = True
                    except:
                        pass
            
            if killed:
                messagebox.showinfo("Tunnel Parado", "Processos Cloudflare encerrados.", parent=self.dialog)
                self._atualizar_tela_principal()
            else:
                messagebox.showinfo("Nenhum Tunnel", "Nenhum processo de tunnel ativo encontrado.", parent=self.dialog)
    
    def parar_servidor_local(self):
        """Para servidor Flask local"""
        try:
            # Para o tunnel primeiro se estiver rodando
            self.parar_tunnel_cloudflare()

            if self.dashboard_process and self.dashboard_process.poll() is None:
                self.dashboard_process.terminate()
                self.dashboard_process.wait(timeout=5)
                if self.dashboard_process.poll() is None:
                    self.dashboard_process.kill()
                self.dashboard_process = None
            
            # Limpa processos na porta 8080
            for proc in psutil.process_iter(['pid', 'name', 'connections']):
                try:
                    for conn in proc.connections(kind='inet'):
                        if conn.laddr.port == 8080:
                            proc.terminate()
                            try:
                                proc.wait(timeout=2)
                            except psutil.TimeoutExpired:
                                proc.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            
            logger.info("Servidor local parado")
            self._atualizar_tela_principal()
            
        except Exception as e:
            logger.error(f"Erro ao parar servidor: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Erro ao parar servidor:\n{e}", parent=self.dialog)
    
    # ==================== CLOUDFLARE TUNNEL ====================
    
    def instalar_cloudflared(self):
        """Instala cloudflared via winget automaticamente"""
        try:
            # Mostra confirmação
            if not messagebox.askyesno(
                "Instalar Cloudflare Tunnel",
                "Deseja instalar o Cloudflare Tunnel (cloudflared)?\n\n"
                "Isso pode levar alguns minutos.",
                parent=self.dialog
            ):
                return
            
            # Executa instalação
            logger.info("Instalando cloudflared via winget...")
            
            process = subprocess.run(
                ["winget", "install", "--id", "Cloudflare.cloudflared", "-e", "--accept-source-agreements", "--accept-package-agreements"],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutos
            )
            
            if process.returncode == 0:
                messagebox.showinfo(
                    "✅ Instalado!", 
                    "Cloudflared instalado com sucesso!\n\n"
                    "Você pode agora configurar o tunnel.",
                    parent=self.dialog
                )
                logger.info("Cloudflared instalado com sucesso")
                self._atualizar_tela_principal()
            else:
                error_msg = process.stderr or process.stdout
                logger.error(f"Falha na instalação do cloudflared: {error_msg}")
                messagebox.showerror(
                    "Erro na Instalação", 
                    f"Falha ao instalar cloudflared:\n\n{error_msg[:200]}",
                    parent=self.dialog
                )
                
        except subprocess.TimeoutExpired:
            messagebox.showerror(
                "Timeout", 
                "Instalação demorou muito tempo. Tente novamente.",
                parent=self.dialog
            )
        except Exception as e:
            logger.error(f"Erro ao instalar cloudflared: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Erro ao instalar:\n{e}", parent=self.dialog)
    
    def configurar_cloudflare(self):
        """Abre wizard de configuração do Cloudflare Tunnel"""
        # Cria janela do Wizard
        wizard = ctk.CTkToplevel(self.dialog)
        wizard.title("🧙‍♂️ Configuração Cloudflare Tunnel")
        wizard.geometry("500x600")
        wizard.resizable(False, False)
        wizard.transient(self.dialog)
        wizard.grab_set()
        
        # Centraliza
        wizard.update_idletasks()
        x = (wizard.winfo_screenwidth() // 2) - 250
        y = (wizard.winfo_screenheight() // 2) - 300
        wizard.geometry(f"+{x}+{y}")
        
        # Container
        container = ctk.CTkFrame(wizard, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            container,
            text="Configuração Automática",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=(0, 20))
        
        # Passo 1: Login
        step1 = ctk.CTkFrame(container, fg_color="#2C2C2C")
        step1.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            step1,
            text="1. Autenticação",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        ctk.CTkLabel(
            step1,
            text="Faça login na sua conta Cloudflare.",
            font=("Segoe UI", 12),
            text_color="gray"
        ).pack(anchor="w", padx=15, pady=(0, 10))
        
        def run_login():
            # Verifica path
            status = self.verificar_cloudflared()
            cmd_path = status.get('path', 'cloudflared')
            
            # Abre terminal com o comando
            # Aspas no título e no comando para evitar problemas com espaços
            cmd = f'start "Cloudflare Login" "{cmd_path}" tunnel login'
            subprocess.run(cmd, shell=True)
            messagebox.showinfo("Instrução", "Siga as instruções no terminal e navegador para autenticar.", parent=wizard)

        ctk.CTkButton(
            step1,
            text="💻 Abrir Terminal para Login",
            command=run_login,
            fg_color="#2196F3",
            hover_color="#1976D2"
        ).pack(fill="x", padx=15, pady=(0, 15))
        
        # Passo 2: Criar Tunnel
        step2 = ctk.CTkFrame(container, fg_color="#2C2C2C")
        step2.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            step2,
            text="2. Criar e Configurar (Manual)",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        ctk.CTkLabel(
            step2,
            text="Execute no terminal:",
            font=("Segoe UI", 12),
            text_color="gray"
        ).pack(anchor="w", padx=15)
        
        cmd_box = ctk.CTkTextbox(step2, height=80, font=("Consolas", 12))
        cmd_box.pack(fill="x", padx=15, pady=5)
        
        # Pega o path correto para exibir
        status = self.verificar_cloudflared()
        display_cmd = status.get('path', 'cloudflared')
        if " " in display_cmd: display_cmd = f'"{display_cmd}"'
        
        cmd_text = f"{display_cmd} tunnel create padaria\n{display_cmd} tunnel route dns padaria dashboard.seusite.com"
        cmd_box.insert("1.0", cmd_text)
        cmd_box.configure(state="disabled")
        
        ctk.CTkButton(
            step2,
            text="📋 Copiar Comandos",
            command=lambda: self.copiar_url(cmd_text),
            fg_color="#4CAF50",
            hover_color="#388E3C"
        ).pack(fill="x", padx=15, pady=(0, 15))
        
        # Passo 3: Iniciar
        step3 = ctk.CTkFrame(container, fg_color="#2C2C2C")
        step3.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            step3,
            text="3. Iniciar Tunnel",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))
        
        def run_start_named():
            # Tenta iniciar o tunnel nomeado 'padaria'
            self.iniciar_tunnel_cloudflare("padaria")
            wizard.destroy()

        ctk.CTkButton(
            step3,
            text="🚀 Iniciar Tunnel 'padaria'",
            command=run_start_named,
            fg_color="#FF9800",
            hover_color="#F57C00"
        ).pack(fill="x", padx=15, pady=(0, 15))
        
        # Opção Quick Tunnel (Sem Login)
        ctk.CTkLabel(
            container,
            text="Ou use o modo rápido (sem login):",
            font=("Segoe UI", 12),
            text_color="gray"
        ).pack(pady=(10, 5))
        
        ctk.CTkButton(
            container,
            text="⚡ Iniciar Quick Tunnel (TryCloudflare)",
            command=lambda: [self.iniciar_tunnel_cloudflare(None), wizard.destroy()],
            fg_color="transparent",
            border_width=1,
            text_color="#2196F3"
        ).pack(fill="x")
    
    # ==================== UI CONSTRUCTION ====================
    
    def _criar_dialog(self):
        """Cria janela principal"""
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title("📱 Dashboard Mobile")
        self.dialog.geometry("650x750")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Centraliza
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - 325
        y = (self.dialog.winfo_screenheight() // 2) - 375
        self.dialog.geometry(f"+{x}+{y}")
        
        # Container principal
        self.main_container = ctk.CTkFrame(self.dialog, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)
    
    def _atualizar_tela_principal(self):
        """Atualiza/refaz a tela principal"""
        for widget in self.main_container.winfo_children():
            widget.destroy()
        self._mostrar_tela_principal()
    
    def _mostrar_tela_principal(self):
        """
        Tela principal com 2 cards verticais:
        1. Servidor Local
        2. Cloudflare Tunnel
        """
        # Limpa container
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        # Header
        header = ctk.CTkFrame(self.main_container, height=80, fg_color="#2196F3", corner_radius=0)
        header.pack(fill="x")
        ctk.CTkLabel(
            header,
            text="📱 Dashboard Mobile",
            font=("Segoe UI", 26, "bold"),
            text_color="white"
        ).pack(pady=25)
        
        # Scroll container
        scroll = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        # ==================== CARD 1: SERVIDOR LOCAL ====================
        
        self._criar_card_servidor_local(scroll)
        
        # Espaçamento
        ctk.CTkFrame(scroll, height=20, fg_color="transparent").pack()
        
        # ==================== CARD 2: CLOUDFLARE TUNNEL ====================
        
        self._criar_card_cloudflare(scroll)
        
        # Footer com ajuda
        footer = ctk.CTkFrame(scroll, fg_color="transparent")
        footer.pack(fill="x", pady=(20, 0))
        
        ctk.CTkButton(
            footer,
            text="ℹ️  Preciso de Ajuda",
            font=("Segoe UI", 12),
            fg_color="transparent",
            text_color="#2196F3",
            hover_color="#1E1E1E",
            command=lambda: subprocess.Popen(["notepad", "docs/VPN_SETUP.md"], shell=True)
        ).pack()
    
    def _criar_card_servidor_local(self, parent):
        """Cria card do servidor local com estados progressivos"""
        card = ctk.CTkFrame(parent, fg_color="#1E1E1E", corner_radius=10)
        card.pack(fill="x", pady=10)
        
        # Header do card
        ctk.CTkLabel(
            card,
            text="🏠 Servidor Local (Rede Wi-Fi)",
            font=("Segoe UI", 18, "bold"),
            anchor="w"
        ).pack(fill="x", padx=20, pady=(15, 5))
        
        # Verifica status
        server_running = self.check_server_running()
        
        script_path = Path(__file__).parent.parent / "web" / "dashboard.py"
        is_configured = script_path.exists() 
        
        if not is_configured:
             # ESTADO 1: Não Configurado
            ctk.CTkLabel(
                card,
                text="⚪ Servidor Não Configurado",
                font=("Segoe UI", 14),
                text_color="gray",
                anchor="w"
            ).pack(fill="x", padx=20, pady=10)
            
            ctk.CTkButton(
                card,
                text="⚙️ Configurar Rede Local",
                font=("Segoe UI", 14, "bold"),
                fg_color="#FF9800",
                hover_color="#F57C00",
                height=45,
                command=lambda: messagebox.showinfo("Configuração", "Verificando arquivos e firewall...", parent=self.dialog)
            ).pack(fill="x", padx=20, pady=(15, 20))
            
        elif not server_running:
            # ESTADO 2: Configurado (Pronto para Iniciar)
            ctk.CTkLabel(
                card,
                text="⚪ Servidor Parado",
                font=("Segoe UI", 14),
                text_color="gray",
                anchor="w"
            ).pack(fill="x", padx=20, pady=10)
            
            ctk.CTkLabel(
                card,
                text="O servidor está pronto para ser iniciado.",
                font=("Segoe UI", 11),
                text_color="gray",
                anchor="w"
            ).pack(fill="x", padx=20)
            
            ctk.CTkButton(
                card,
                text="▶️ Iniciar Servidor",
                font=("Segoe UI", 14, "bold"),
                fg_color="#4CAF50",
                hover_color="#388E3C",
                height=45,
                command=self.iniciar_servidor_local
            ).pack(fill="x", padx=20, pady=(15, 20))
            
        else:
            # ESTADO 3: Rodando
            ctk.CTkLabel(
                card,
                text="🟢 Servidor Ativo",
                font=("Segoe UI", 14, "bold"),
                text_color="#4CAF50",
                anchor="w"
            ).pack(fill="x", padx=20, pady=10)
            
            # IP e URL
            local_ip = self.get_local_ip()
            url = f"http://{local_ip}:8080"
            
            info_frame = ctk.CTkFrame(card, fg_color="#2C2C2C", corner_radius=8)
            info_frame.pack(fill="x", padx=20, pady=10)
            
            ctk.CTkLabel(
                info_frame,
                text="🔗 Link de Acesso:",
                font=("Segoe UI", 12),
                text_color="gray",
                anchor="w"
            ).pack(fill="x", padx=15, pady=(12, 5))
            
            ctk.CTkLabel(
                info_frame,
                text=url,
                font=("Consolas", 14, "bold"),
                text_color="#F57C00"
            ).pack(fill="x", padx=15, pady=(0, 10))
            
            # QR Code
            qr_img = self.gerar_qr_code(url)
            if qr_img:
                qr_label = ctk.CTkLabel(info_frame, text="", image=qr_img)
                qr_label.image = qr_img
                qr_label.pack(pady=15)
            
            ctk.CTkButton(
                info_frame,
                text="📋 Copiar Link",
                font=("Segoe UI", 12),
                height=35,
                fg_color="#F57C00",
                hover_color="#EF6C00",
                command=lambda: self.copiar_url(url)
            ).pack(fill="x", padx=15, pady=(5, 15))
            
            # Botão Parar
            ctk.CTkButton(
                card,
                text="⏸️ Pausar/Parar",
                font=("Segoe UI", 14, "bold"),
                fg_color="#F44336",
                hover_color="#D32F2F",
                height=45,
                command=self.parar_servidor_local
            ).pack(fill="x", padx=20, pady=(10, 20))
    
    def _criar_card_cloudflare(self, parent):
        """Cria card do Cloudflare Tunnel com estados progressivos"""
        card = ctk.CTkFrame(parent, fg_color="#1E1E1E", corner_radius=10)
        card.pack(fill="x", pady=10)
        
        # Header do card
        ctk.CTkLabel(
            card,
            text="☁️ Cloudflare Tunnel (Acesso Remoto)",
            font=("Segoe UI", 18, "bold"),
            anchor="w"
        ).pack(fill="x", padx=20, pady=(15, 5))
        
        # Verifica status
        cloud_status = self.verificar_cloudflared()
        
        if not cloud_status['instalado']:
            # ESTADO 1: Não Instalado
            ctk.CTkLabel(
                card,
                text="❌ Cloudflared não instalado",
                font=("Segoe UI", 14),
                text_color="#F44336",
                anchor="w"
            ).pack(fill="x", padx=20, pady=10)

            ctk.CTkButton(
                card,
                text="⚙️ Instalar Cloudflared",
                font=("Segoe UI", 14, "bold"),
                fg_color="#FF5722",
                hover_color="#E64A19",
                height=45,
                command=self.instalar_cloudflared
            ).pack(fill="x", padx=20, pady=(15, 20))
            
        elif not cloud_status['rodando']:
            # ESTADO 2: Instalado mas Parado
            ctk.CTkLabel(
                card,
                text="⚪ Tunnel Parado",
                font=("Segoe UI", 14),
                text_color="gray",
                anchor="w"
            ).pack(fill="x", padx=20, pady=10)
            
            ctk.CTkButton(
                card,
                text="🧙‍♂️ Configurar Tunnel",
                font=("Segoe UI", 14, "bold"),
                fg_color="#2196F3",
                hover_color="#1976D2",
                height=45,
                command=self.configurar_cloudflare
            ).pack(fill="x", padx=20, pady=(15, 20))
            
        else:
            # ESTADO 3: Rodando
            ctk.CTkLabel(
                card,
                text="🟢 Tunnel Ativo",
                font=("Segoe UI", 14, "bold"),
                text_color="#4CAF50",
                anchor="w"
            ).pack(fill="x", padx=20, pady=10)
            
            url = cloud_status.get('url')
            
            if url:
                # URL Disponível
                info_frame = ctk.CTkFrame(card, fg_color="#2C2C2C", corner_radius=8)
                info_frame.pack(fill="x", padx=20, pady=10)
                
                ctk.CTkLabel(
                    info_frame,
                    text="🔗 Link Público:",
                    font=("Segoe UI", 12),
                    text_color="gray",
                    anchor="w"
                ).pack(fill="x", padx=15, pady=(12, 5))
                
                ctk.CTkLabel(
                    info_frame,
                    text=url,
                    font=("Consolas", 14, "bold"),
                    text_color="#F57C00"
                ).pack(fill="x", padx=15, pady=(0, 10))
                
                # QR Code
                qr_img = self.gerar_qr_code(url)
                if qr_img:
                    qr_label = ctk.CTkLabel(info_frame, text="", image=qr_img)
                    qr_label.image = qr_img
                    qr_label.pack(pady=15)
                
                ctk.CTkButton(
                    info_frame,
                    text="📋 Copiar Link",
                    font=("Segoe UI", 12),
                    height=35,
                    fg_color="#F57C00",
                    hover_color="#EF6C00",
                    command=lambda: self.copiar_url(url)
                ).pack(fill="x", padx=15, pady=(5, 15))
            else:
                # Carregando URL
                ctk.CTkLabel(
                    card,
                    text="⏳ Obtendo URL pública...",
                    font=("Segoe UI", 12, "italic"),
                    text_color="#FF9800",
                    anchor="w"
                ).pack(fill="x", padx=20, pady=10)
                
                # Botão para forçar atualização (opcional)
                ctk.CTkButton(
                    card,
                    text="🔄 Atualizar Status",
                    font=("Segoe UI", 12),
                    fg_color="transparent",
                    border_width=1,
                    text_color="gray",
                    command=self._atualizar_tela_principal
                ).pack(fill="x", padx=20, pady=5)
            
            # Botão Parar
            ctk.CTkButton(
                card,
                text="🛑 Parar Tunnel",
                font=("Segoe UI", 14, "bold"),
                fg_color="#F44336",
                hover_color="#D32F2F",
                height=45,
                command=self.parar_tunnel_cloudflare
            ).pack(fill="x", padx=20, pady=(10, 20))
