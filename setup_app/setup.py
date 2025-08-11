import os
import yaml
import tkinter as tk
from tkinter import ttk, messagebox, font
import threading
import time

try:
    import keyboard  # pip install keyboard
except ImportError:
    keyboard = None

# ------------------- CONFIG GENERATION -------------------
def create_config_dir():
    os.makedirs("config", exist_ok=True)

def generate_binds_yaml():
    binds_data = {"buttons": {}}
    for i in range(1, 81):
        binds_data["buttons"][str(i)] = {
            "text": "",
            "img": "img/none.png",
            "action": "none"
        }
    with open("config/binds.yaml", "w", encoding="utf-8") as f:
        yaml.dump(binds_data, f, sort_keys=False, allow_unicode=True)

def generate_config_yaml(data):
    with open("config/config.yaml", "w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

# ------------------- ENHANCED WIZARD CLASS -------------------
class EnhancedInstallWizard:
    def __init__(self, root):
        self.root = root
        self.root.title("Configuration Installation Wizard")
        self.root.configure(bg='#f5f5f5')
        self.center_window(self.root, 800, 650)
        self.root.resizable(False, False)
        
        # Configure custom styles
        self.setup_styles()
        
        # Create fonts
        self.title_font = font.Font(family="Arial", size=18, weight="bold")
        self.subtitle_font = font.Font(family="Arial", size=10)
        self.header_font = font.Font(family="Arial", size=14, weight="bold")
        self.body_font = font.Font(family="Arial", size=9)
        
        # State variables
        self.var_home = tk.BooleanVar(value=False)
        self.var_discord = tk.BooleanVar(value=False)
        self.var_soundboard = tk.BooleanVar(value=False)
        self.var_obs = tk.BooleanVar(value=False)

        self.home_ip = tk.StringVar(value="http://homeassistant.local:8123")
        self.home_token = tk.StringVar(value="")
        self.obs_ip = tk.StringVar(value="localhost")
        self.obs_port = tk.IntVar(value=4455)

        self.current_step = 0
        self.steps = [
            {"title": "Welcome", "func": self.step_select_modules},
            {"title": "Home Assistant", "func": self.step_home_assistant},
            {"title": "Discord", "func": self.step_discord},
            {"title": "OBS Studio", "func": self.step_obs},
            {"title": "Complete", "func": self.step_finish}
        ]
        
        # Create main container
        self.create_main_container()
        self.show_step()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('Primary.TButton',
                        foreground='white',
                        padding=(20, 10))  # etwas mehr vertikales Padding

        style.map('Primary.TButton',
                background=[('!disabled', '#007acc'),
                            ('active', '#005a99'),
                            ('pressed', '#004477')],
                foreground=[('disabled', '#dddddd'),
                            ('!disabled', 'white')])

        style.configure('Secondary.TButton',
                        foreground='white',
                        padding=(15, 8))

        style.map('Secondary.TButton',
                background=[('!disabled', '#6c757d'),
                            ('active', '#5a6268'),
                            ('pressed', '#495057')],
                foreground=[('disabled', '#eeeeee'),
                            ('!disabled', 'white')])

        style.configure('Card.TFrame', background='white', borderwidth=1, relief='solid')
        style.configure('Custom.TCheckbutton', background='white', font=('Arial', 10))


    def center_window(self, win, width, height):
        screen_w = win.winfo_screenwidth()
        screen_h = win.winfo_screenheight()
        x = int((screen_w / 2) - (width / 2))
        y = int((screen_h / 2) - (height / 2))
        win.geometry(f"{width}x{height}+{x}+{y}")

    def create_main_container(self):
        # Header frame – entferne feste Höhe und propagate(False)
        self.header_frame = tk.Frame(self.root, bg='#2c3e50')
        self.header_frame.pack(fill='x')
        # self.header_frame.pack_propagate(False)  # raus

        # Progress bar frame (kann bleiben wie ist oder ebenfalls ohne feste Höhe)
        self.progress_frame = tk.Frame(self.root, bg='#ecf0f1')
        self.progress_frame.pack(fill='x')
        # self.progress_frame.pack_propagate(False)  # optional raus

        # Content frame
        self.content_frame = tk.Frame(self.root, bg='#f5f5f5')
        self.content_frame.pack(fill='both', expand=True, padx=40, pady=20)

        # Footer frame – entferne feste Höhe und propagate(False)
        self.footer_frame = tk.Frame(self.root, bg='#ecf0f1')
        self.footer_frame.pack(fill='x', side='bottom')
        # self.footer_frame.pack_propagate(False)  # raus

    def update_header(self, title, subtitle=""):
        for widget in self.header_frame.winfo_children():
            widget.destroy()

        # etwas geringeres padding, damit mehr Platz bleibt
        header_container = tk.Frame(self.header_frame, bg='#2c3e50')
        header_container.pack(expand=True, fill='both', padx=30, pady=10)

        title_label = tk.Label(header_container, text=title,
                            font=self.title_font, bg='#2c3e50', fg='white')
        title_label.pack(anchor='w')

        if subtitle:
            # feste wraplength passend zu 800px Breite abzüglich 2*30px Rand
            subtitle_label = tk.Label(header_container, text=subtitle,
                                    font=self.subtitle_font, bg='#2c3e50', fg='#bdc3c7',
                                    wraplength=740, justify='left')
            subtitle_label.pack(anchor='w', pady=(2, 0))


    def update_progress(self):
        """Update progress indicator"""
        for widget in self.progress_frame.winfo_children():
            widget.destroy()
            
        progress_container = tk.Frame(self.progress_frame, bg='#ecf0f1')
        progress_container.pack(expand=True, fill='both', padx=30, pady=8)
        
        # Progress indicator
        progress_text = f"Step {self.current_step + 1} of {len(self.steps)}"
        progress_label = tk.Label(progress_container, text=progress_text,
                                font=('Arial', 9), fg='#7f8c8d', bg='#ecf0f1')
        progress_label.pack(anchor='w')
        
        # Progress bar
        progress_bar_frame = tk.Frame(progress_container, bg='#ecf0f1')
        progress_bar_frame.pack(fill='x', pady=(3, 0))
        
        progress_width = 200
        filled_width = int((self.current_step / (len(self.steps) - 1)) * progress_width)
        
        # Background bar
        bg_bar = tk.Frame(progress_bar_frame, bg='#bdc3c7', height=4, width=progress_width)
        bg_bar.pack(anchor='w')
        bg_bar.pack_propagate(False)
        
        # Filled bar
        if filled_width > 0:
            filled_bar = tk.Frame(bg_bar, bg='#007acc', height=4, width=filled_width)
            filled_bar.pack(anchor='w')
            filled_bar.pack_propagate(False)

    def create_card_frame(self, parent, title=None):
        """Create a styled card frame"""
        card = ttk.Frame(parent, style='Card.TFrame')
        card.pack(fill='both', expand=True, pady=10)
        
        card_inner = tk.Frame(card, bg='white')
        card_inner.pack(fill='both', expand=True, padx=25, pady=25)
        
        if title:
            title_label = tk.Label(card_inner, text=title, font=self.header_font, 
                                 bg='white', fg='#2c3e50')
            title_label.pack(anchor='w', pady=(0, 15))
        
        return card_inner

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def clear_footer(self):
        for widget in self.footer_frame.winfo_children():
            widget.destroy()

    def create_navigation_buttons(self, show_back=True, show_next=True, next_text="Next"):
        self.clear_footer()

        # Button-Container darf sich ausdehnen, aber kein unnötiges Innen-Padding
        button_frame = tk.Frame(self.footer_frame, bg='#ecf0f1')
        button_frame.pack(fill='x', padx=15, pady=10)

        if show_back and self.current_step > 0:
            back_btn = ttk.Button(button_frame, text="Back",
                                command=self.prev_step, style='Secondary.TButton')
            back_btn.pack(side='left')

        if show_next:
            next_btn = ttk.Button(button_frame, text=next_text,
                                command=self.next_step if next_text == "Next" else self.root.quit,
                                style='Primary.TButton')
            next_btn.pack(side='right')

    def next_step(self):
        self.current_step += 1
        self.show_step()

    def prev_step(self):
        self.current_step -= 1
        self.show_step()

    def show_step(self):
        """Display current step"""
        self.clear_content()
        step = self.steps[self.current_step]
        self.update_progress()
        step['func']()

    # ------------------- STEP 1: MODULE SELECTION -------------------
    def step_select_modules(self):
        self.update_header("Welcome to Configuration Installer", 
                          "Set up your application with the modules you need")
        
        card = self.create_card_frame(self.content_frame, "Select Modules to Configure")
        
        description = tk.Label(card, 
                             text="Choose which integrations you would like to set up. You can modify these settings later if needed.",
                             font=self.body_font, bg='white', fg='#7f8c8d', wraplength=600)
        description.pack(anchor='w', pady=(0, 25))
        
        # Module options
        modules = [
            ("Home Assistant", self.var_home, "Control and monitor your smart home devices"),
            ("Discord", self.var_discord, "Voice chat integration with custom hotkeys"),
            ("Soundboard", self.var_soundboard, "Play custom audio files and sound effects"),
            ("OBS Studio", self.var_obs, "Streaming and recording software controls")
        ]
        
        for name, var, desc in modules:
            module_frame = tk.Frame(card, bg='white')
            module_frame.pack(fill='x', pady=10)
            
            cb = ttk.Checkbutton(module_frame, text=name, variable=var, 
                               style='Custom.TCheckbutton')
            cb.pack(anchor='w')
            
            desc_label = tk.Label(module_frame, text=desc, font=('Arial', 8), 
                                bg='white', fg='#95a5a6')
            desc_label.pack(anchor='w', padx=(25, 0), pady=(2, 0))
        
        self.create_navigation_buttons(show_back=False)

    # ------------------- STEP 2: HOME ASSISTANT -------------------
    def step_home_assistant(self):
        if not self.var_home.get():
            self.next_step()
            return
            
        self.update_header("Home Assistant Configuration", 
                          "Configure your Home Assistant server connection")
        
        card = self.create_card_frame(self.content_frame, "Home Assistant Settings")
        
        # Instructions
        info_frame = tk.Frame(card, bg='#e8f4fd', relief='solid', borderwidth=1)
        info_frame.pack(fill='x', pady=(0, 20))
        
        info_inner = tk.Frame(info_frame, bg='#e8f4fd')
        info_inner.pack(fill='x', padx=15, pady=12)
        
        tk.Label(info_inner, text="Setup Instructions:", font=('Arial', 9, 'bold'), 
                bg='#e8f4fd', fg='#2c3e50').pack(anchor='w')
        tk.Label(info_inner, text="1. Server IP is typically: http://homeassistant.local:8123", 
                font=('Arial', 8), bg='#e8f4fd', fg='#34495e').pack(anchor='w', pady=(2, 0))
        tk.Label(info_inner, text="2. Create Access Token in Home Assistant: Profile > Long-Lived Access Tokens", 
                font=('Arial', 8), bg='#e8f4fd', fg='#34495e').pack(anchor='w')
        
        # Input fields
        self.create_input_field(card, "Server IP:", self.home_ip, width=50)
        self.create_input_field(card, "Access Token:", self.home_token, width=50, show="*")
        
        self.create_navigation_buttons()

    # ------------------- STEP 3: DISCORD -------------------
    def step_discord(self):
        if not self.var_discord.get():
            self.next_step()
            return
            
        self.update_header("Discord Configuration", 
                          "Set up Discord voice chat hotkeys")
        
        card = self.create_card_frame(self.content_frame, "Discord Hotkey Setup")
        
        # Instructions
        instruction_text = ("Use the buttons below to test Discord hotkeys. Each button will send the "
                          "corresponding function key after a 5-second delay.\n\n"
                          "To configure these in Discord:\n"
                          "1. Open Discord Settings\n"
                          "2. Go to Voice & Video\n"
                          "3. Scroll down to Hotkeys\n"
                          "4. Set F13 for Mute and F14 for Deafen")
        
        tk.Label(card, text=instruction_text, font=self.body_font, bg='white', 
                wraplength=600, justify='left').pack(anchor='w', pady=(0, 20))
        
        # Hotkey buttons
        hotkey_frame = tk.Frame(card, bg='white')
        hotkey_frame.pack(fill='x', pady=15)
        
        btn_f13 = ttk.Button(hotkey_frame, text="Test Mute Hotkey (F13)", 
                           command=lambda: self.send_hotkey("f13"), style='Primary.TButton')
        btn_f13.pack(side='left', padx=(0, 15))
        
        btn_f14 = ttk.Button(hotkey_frame, text="Test Deafen Hotkey (F14)", 
                           command=lambda: self.send_hotkey("f14"), style='Primary.TButton')
        btn_f14.pack(side='left')
        
        self.create_navigation_buttons()

    def create_input_field(self, parent, label, textvariable, width=40, show=None):
        """Create a styled input field"""
        field_frame = tk.Frame(parent, bg='white')
        field_frame.pack(fill='x', pady=10)
        
        tk.Label(field_frame, text=label, font=('Arial', 9, 'bold'), 
                bg='white', fg='#2c3e50').pack(anchor='w')
        
        entry = ttk.Entry(field_frame, textvariable=textvariable, width=width, 
                         font=('Arial', 9), show=show)
        entry.pack(anchor='w', pady=(5, 0))
        
        return entry

    def send_hotkey(self, key):
        if keyboard is None:
            messagebox.showerror("Module Not Found", 
                               "The 'keyboard' module is not installed.\n\n"
                               "Please install it using: pip install keyboard")
            return

        def worker():
            time.sleep(5)
            keyboard.send(key)

        threading.Thread(target=worker, daemon=True).start()
        messagebox.showinfo("Hotkey Test", 
                          f"The {key.upper()} key will be sent in 5 seconds.\n"
                          "Please switch to Discord now to test the hotkey.")

    # ------------------- STEP 4: OBS -------------------
    def step_obs(self):
        if not self.var_obs.get():
            self.next_step()
            return
            
        self.update_header("OBS Studio Configuration", 
                          "Configure OBS WebSocket connection settings")
        
        card = self.create_card_frame(self.content_frame, "OBS Studio Settings")
        
        # Warning box
        warning_frame = tk.Frame(card, bg='#fdf2e9', relief='solid', borderwidth=1)
        warning_frame.pack(fill='x', pady=(0, 20))
        
        warning_inner = tk.Frame(warning_frame, bg='#fdf2e9')
        warning_inner.pack(fill='x', padx=15, pady=12)
        
        tk.Label(warning_inner, text="Important Notice:", font=('Arial', 9, 'bold'), 
                bg='#fdf2e9', fg='#d35400').pack(anchor='w')
        tk.Label(warning_inner, text="Do not set a password for the OBS WebSocket connection.", 
                font=('Arial', 8), bg='#fdf2e9', fg='#e67e22').pack(anchor='w', pady=(2, 0))
        tk.Label(warning_inner, text="Password protection will cause compatibility issues with this application.", 
                font=('Arial', 8), bg='#fdf2e9', fg='#e67e22').pack(anchor='w')
        
        # Input fields
        self.create_input_field(card, "Server IP Address:", self.obs_ip, width=40)
        
        port_frame = tk.Frame(card, bg='white')
        port_frame.pack(fill='x', pady=10)
        
        tk.Label(port_frame, text="Server Port:", font=('Arial', 9, 'bold'), 
                bg='white', fg='#2c3e50').pack(anchor='w')
        
        port_entry = ttk.Entry(port_frame, textvariable=self.obs_port, width=20, 
                              font=('Arial', 9))
        port_entry.pack(anchor='w', pady=(5, 0))
        
        self.create_navigation_buttons()

    # ------------------- STEP 5: FINISH -------------------
    def step_finish(self):
        self.update_header("Installation Complete", 
                          "Your configuration has been successfully created")
        
        # Generate config files
        create_config_dir()
        generate_binds_yaml()

        config_data = {
            "binds": {
                "file_path": "config/binds.yaml"
            },
            "home_assistant": {
                "enabled": self.var_home.get(),
                "server_ip": self.home_ip.get() if self.var_home.get() else "http://homeassistant.local:8123",
                "access_token": self.home_token.get() if self.var_home.get() else ""
            },
            "discord": {
                "enabled": self.var_discord.get()
            },
            "soundboard": {
                "enabled": self.var_soundboard.get()
            },
            "obs": {
                "enabled": self.var_obs.get(),
                "server_ip": self.obs_ip.get() if self.var_obs.get() else "localhost",
                "server_port": self.obs_port.get() if self.var_obs.get() else 4455
            }
        }

        generate_config_yaml(config_data)
        
        card = self.create_card_frame(self.content_frame, "Setup Complete")
        
        success_frame = tk.Frame(card, bg='#d5f4e6', relief='solid', borderwidth=1)
        success_frame.pack(fill='x', pady=(0, 20))
        
        success_inner = tk.Frame(success_frame, bg='#d5f4e6')
        success_inner.pack(fill='x', padx=15, pady=15)
        
        tk.Label(success_inner, text="Configuration files have been created successfully!", 
                font=('Arial', 10, 'bold'), bg='#d5f4e6', fg='#27ae60').pack()
        
        # Summary of enabled modules
        enabled_modules = []
        if self.var_home.get():
            enabled_modules.append("Home Assistant")
        if self.var_discord.get():
            enabled_modules.append("Discord")
        if self.var_soundboard.get():
            enabled_modules.append("Soundboard")
        if self.var_obs.get():
            enabled_modules.append("OBS Studio")
        
        if enabled_modules:
            tk.Label(card, text="Enabled modules:", font=('Arial', 10, 'bold'), 
                    bg='white', fg='#2c3e50').pack(anchor='w', pady=(15, 5))
            for module in enabled_modules:
                tk.Label(card, text=f"• {module}", font=('Arial', 9), 
                        bg='white', fg='#27ae60').pack(anchor='w', padx=(20, 0))
        
        tk.Label(card, text="All configuration files have been saved to the 'config' folder.", 
                font=self.body_font, bg='white', fg='#7f8c8d').pack(anchor='w', pady=(20, 5))
        
        tk.Label(card, text="You can now close this installer and run your application.", 
                font=self.body_font, bg='white', fg='#7f8c8d').pack(anchor='w')
        
        self.create_navigation_buttons(show_back=False, show_next=True, next_text="Finish")


if __name__ == "__main__":
    root = tk.Tk()
    wizard = EnhancedInstallWizard(root)
    root.mainloop()