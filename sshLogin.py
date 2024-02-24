import tkinter as tk
import paramiko

# ==== Colors ====
m1c = '#00ffff'
bgc = '#222222'
dbg = '#000000'
fgc = '#111111'

class SSHLoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SSH-Login")
        self.root.tk_setPalette(
            background=bgc,
            foreground=m1c,
            activeBackground=fgc,
            activeForeground=bgc,
            highlightColor=m1c,
            highlightBackground=m1c
        )

        self.frame = tk.Frame(self.root, bg=bgc)
        self.frame.pack(padx=20, pady=20)

        self.host_label = tk.Label(self.frame, text="Host to Target:", bg=bgc, fg=m1c)
        self.host_label.grid(row=0, column=0, pady=5)
        self.host_entry = tk.Entry(self.frame, width=32, bg='#4A4A4A', fg='#00f000')
        self.host_entry.grid(row=0, column=1)

        self.port_label = tk.Label(self.frame, text="Port:", bg=bgc, fg=m1c)
        self.port_label.grid(row=1, column=0, pady=5)
        self.port_entry = tk.Entry(self.frame, width=32, bg='#4A4A4A', fg='#00f000')
        self.port_entry.grid(row=1, column=1)

        self.user_label = tk.Label(self.frame, text="SSH Username:", bg=bgc, fg=m1c)
        self.user_label.grid(row=2, column=0, pady=5)
        self.user_entry = tk.Entry(self.frame, width=32, bg='#4A4A4A', fg='#00f000')
        self.user_entry.grid(row=2, column=1)

        self.pass_label = tk.Label(self.frame, text="SSH Password:", bg=bgc, fg=m1c)
        self.pass_label.grid(row=3, column=0, pady=5)
        self.pass_entry = tk.Entry(self.frame, width=32, bg='#4A4A4A', fg='#00f000', show="*")
        self.pass_entry.grid(row=3, column=1)

        self.login_button = tk.Button(self.frame, text="Connect", command=self.connect_ssh, bg='#4A4A4A', fg=m1c)
        self.login_button.grid(row=4, columnspan=2, pady=10)

        self.commands_label = tk.Label(self.frame, text="Command Output:", bg=bgc, fg=m1c)
        self.commands_label.grid(row=5, columnspan=2, pady=5)
        self.output_listbox = tk.Listbox(self.frame, bg='#A4A4A4', fg=m1c, width=60, height=10)
        self.output_listbox.grid(row=6, columnspan=2)

        # Adding status bar at the bottom
        self.status_bar = tk.Label(self.root, text="#################################################", fg='#A9A9A9', bd=2)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_message = tk.Label(self.root, text='Paramiko', fg='#A9A9A9', bd=2)
        self.status_message.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_desc = tk.Label(self.root, text="Pure-Python implementation of the SSHv2 protocol", fg='#A9A9A9', bd=2)
        self.status_desc.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_separator = tk.Label(self.root, text="#################################################", fg='#A9A9A9', bd=2)
        self.status_separator.pack(side=tk.BOTTOM, fill=tk.X)

    def connect_ssh(self):
        host = self.host_entry.get()
        user = self.user_entry.get()
        password = self.pass_entry.get()
        port = self.port_entry.get() if self.port_entry.get() else 22  # Default port is 22 if not specified

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh_client.connect(hostname=host, username=user, password=password)
            self.output_listbox.insert(tk.END, "Connected successfully!")

            # Example command: 'cat /etc/shadow | grep root;ps'
            command = 'cat /etc/shadow | grep root;ps'
            stdin, stdout, stderr = ssh_client.exec_command(command)

            output = stdout.read().decode()
            self.output_listbox.insert(tk.END, output)

        except paramiko.AuthenticationException:
            self.output_listbox.insert(tk.END, "Authentication failed. Please check credentials.")
        except paramiko.SSHException as e:
            self.output_listbox.insert(tk.END, f"SSH error: {e}")
        finally:
            ssh_client.close()

def main():
    root = tk.Tk()
    app = SSHLoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
