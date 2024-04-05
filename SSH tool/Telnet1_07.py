import tkinter as tk
from tkinter import simpledialog
import paramiko

def connect_ssh():
    global ssh_client
    address = address_entry.get()
    port = int(port_entry.get()) if port_entry.get() else 22
    username = username_entry.get()
    password = password_entry.get()
    
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=address, port=port, username=username, password=password)
        output_text.insert(tk.END, "Connected to {}:{} as {}\n".format(address, port, username))
        prompt.set(username + "@" + address + ":~$ ")
    except Exception as e:
        output_text.insert(tk.END, "Error connecting to {}: {}\n".format(address, e))

def send_command():
    command = command_entry.get()
    try:
        stdin, stdout, stderr = ssh_client.exec_command(command)
        output_text.insert(tk.END, stdout.read().decode('utf-8'))
        output_text.insert(tk.END, stderr.read().decode('utf-8'))
        output_text.insert(tk.END, prompt.get())
    except Exception as e:
        output_text.insert(tk.END, "Error sending command: {}\n".format(e))

# Create the main window
root = tk.Tk()
root.title("Simple SSH Client")

# Address entry
address_label = tk.Label(root, text="Enter Address:")
address_label.grid(row=0, column=0, sticky="w")
address_entry = tk.Entry(root)
address_entry.grid(row=0, column=1)

# Port entry
port_label = tk.Label(root, text="Enter Port (default 22):")
port_label.grid(row=1, column=0, sticky="w")
port_entry = tk.Entry(root)
port_entry.grid(row=1, column=1)

# Username entry
username_label = tk.Label(root, text="Enter Username:")
username_label.grid(row=2, column=0, sticky="w")
username_entry = tk.Entry(root)
username_entry.grid(row=2, column=1)

# Password entry
password_label = tk.Label(root, text="Enter Password:")
password_label.grid(row=3, column=0, sticky="w")
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=3, column=1)

# Connect button
connect_button = tk.Button(root, text="Connect", command=connect_ssh)
connect_button.grid(row=4, column=0, columnspan=2)

# Command entry
command_label = tk.Label(root, text="Enter Command:")
command_label.grid(row=5, column=0, sticky="w")
command_entry = tk.Entry(root)
command_entry.grid(row=5, column=1)

# Send button
send_button = tk.Button(root, text="Send", command=send_command)
send_button.grid(row=6, column=0, columnspan=2)

# Output text box
output_text = tk.Text(root, height=20, width=80)
output_text.grid(row=7, column=0, columnspan=2, sticky="nsew")

# Prompt
prompt = tk.StringVar()
prompt_label = tk.Label(root, textvariable=prompt, anchor="w", justify="left")
prompt_label.grid(row=8, column=0, columnspan=2, sticky="we")

# Configure resizing behavior
root.grid_rowconfigure(7, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()
