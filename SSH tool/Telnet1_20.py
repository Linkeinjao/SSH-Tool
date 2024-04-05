import tkinter as tk
import paramiko
import json
from tkinter import simpledialog, messagebox

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

def disconnect_ssh():
    global ssh_client
    if ssh_client:
        ssh_client.close()
        output_text.insert(tk.END, "SSH session disconnected\n")
    else:
        output_text.insert(tk.END, "No active SSH session\n")

def send_command():
    command = command_entry.get()
    try:
        stdin, stdout, stderr = ssh_client.exec_command(command)
        output_text.insert(tk.END, stdout.read().decode('utf-8'))
        output_text.insert(tk.END, stderr.read().decode('utf-8'))
        output_text.see(tk.END)  # Scroll to the end of the text box
    except Exception as e:
        output_text.insert(tk.END, "Error sending command: {}\n".format(e))

def save_settings():
    address = address_entry.get()
    port = port_entry.get()
    username = username_entry.get()
    name = simpledialog.askstring("Save Address", "Enter a name for this address:")
    if not name:
        return
    settings = {}
    try:
        with open("address.json", "r") as file:
            settings = json.load(file)
            if name in settings:
                messagebox.showwarning("Warning", "Address with name '{}' already exists!".format(name))
                return
    except FileNotFoundError:
        pass
    
    settings[name] = {"address": address, "port": port, "username": username}
    with open("address.json", "w") as file:
        json.dump(settings, file)
    output_text.insert(tk.END, "Address saved as '{}' in address.json\n".format(name))

def load_settings():
    try:
        with open("address.json", "r") as file:
            settings = json.load(file)
            options = list(settings.keys())
            load_window = tk.Toplevel(root)
            load_window.title("Load Address")
            load_window.geometry("300x250")
            load_label = tk.Label(load_window, text="Select an address to load or remove:")
            load_label.pack()
            listbox = tk.Listbox(load_window)
            for option in options:
                listbox.insert(tk.END, option)
            listbox.pack()

            def select_address():
                selection = listbox.curselection()
                if selection:
                    selected_option = options[selection[0]]
                    address_entry.delete(0, tk.END)
                    address_entry.insert(0, settings[selected_option]["address"])
                    port_entry.delete(0, tk.END)
                    port_entry.insert(0, settings[selected_option]["port"])
                    username_entry.delete(0, tk.END)
                    username_entry.insert(0, settings[selected_option]["username"])
                    output_text.insert(tk.END, "Address '{}' loaded\n".format(selected_option))
                load_window.destroy()

            load_frame = tk.Frame(load_window)
            load_frame.pack()

            load_button = tk.Button(load_frame, text="Load", command=select_address)
            load_button.pack(side=tk.LEFT, padx=5, pady=5)

            def remove_address():
                selection = listbox.curselection()
                if selection:
                    selected_option = options[selection[0]]
                    del settings[selected_option]
                    listbox.delete(selection[0])
                    with open("address.json", "w") as file:
                        json.dump(settings, file)
                    output_text.insert(tk.END, "Address '{}' removed\n".format(selected_option))

            remove_button = tk.Button(load_frame, text="Remove", command=remove_address)
            remove_button.pack(side=tk.LEFT, padx=5, pady=5)

    except FileNotFoundError:
        output_text.insert(tk.END, "No saved addresses found\n")

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
connect_button.grid(row=4, column=0, padx=(10, 5), ipadx=100)  # Add ipadx parameter to set internal padding

# Disconnect button
disconnect_button = tk.Button(root, text="Disconnect", command=disconnect_ssh)
disconnect_button.grid(row=4, column=1, padx=(5, 10), ipadx=100)  # Add ipadx parameter to set internal padding

# Save settings button
save_button = tk.Button(root, text="Save Settings", command=save_settings)
save_button.grid(row=4, column=2)

# Load settings button
load_button = tk.Button(root, text="Load Settings", command=load_settings)
load_button.grid(row=4, column=3)

# Command entry
command_label = tk.Label(root, text="Enter Command:")
command_label.grid(row=9, column=0, sticky="w")
command_entry = tk.Entry(root)
command_entry.grid(row=9, column=1, sticky="ew")

# Send button
send_button = tk.Button(root, text="Send", command=send_command)
send_button.grid(row=9, column=2, sticky="e")

# Output text box
output_text = tk.Text(root, height=20, width=80)
output_text.grid(row=7, column=0, columnspan=4, sticky="nsew")

# Prompt
prompt = tk.StringVar()
prompt_label = tk.Label(root, textvariable=prompt, anchor="w", justify="left")
prompt_label.grid(row=8, column=0, columnspan=2, sticky="we")

# Configure resizing behavior
root.grid_rowconfigure(7, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()
