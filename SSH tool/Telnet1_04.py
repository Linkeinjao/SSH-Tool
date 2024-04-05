import tkinter as tk
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
    except Exception as e:
        output_text.insert(tk.END, "Error connecting to {}: {}\n".format(address, e))
        return

def send_command():
    command = command_entry.get()
    try:
        stdin, stdout, stderr = ssh_client.exec_command(command)
        output_text.insert(tk.END, stdout.read().decode('utf-8'))
    except Exception as e:
        output_text.insert(tk.END, "Error sending command: {}\n".format(e))

# Create the main window
root = tk.Tk()
root.title("Simple SSH Client")

# Address entry
address_label = tk.Label(root, text="Enter Address:")
address_label.pack()
address_entry = tk.Entry(root)
address_entry.pack()

# Port entry
port_label = tk.Label(root, text="Enter Port (default 22):")
port_label.pack()
port_entry = tk.Entry(root)
port_entry.pack()

# Username entry
username_label = tk.Label(root, text="Enter Username:")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

# Password entry
password_label = tk.Label(root, text="Enter Password:")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

# Connect button
connect_button = tk.Button(root, text="Connect", command=connect_ssh)
connect_button.pack()

# Command entry
command_label = tk.Label(root, text="Enter Command:")
command_label.pack()
command_entry = tk.Entry(root)
command_entry.pack()

# Send button
send_button = tk.Button(root, text="Send", command=send_command)
send_button.pack()

# Output text box
output_text = tk.Text(root, height=10, width=50)
output_text.pack()

root.mainloop()
