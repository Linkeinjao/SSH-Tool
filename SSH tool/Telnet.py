import telnetlib
import tkinter as tk

def connect_telnet():
    global tn
    address = address_entry.get()
    try:
        tn = telnetlib.Telnet(address)
        output_text.insert(tk.END, "Connected to {}\n".format(address))
        output_text.insert(tk.END, tn.read_until(b"\n").decode('utf-8'))
    except Exception as e:
        output_text.insert(tk.END, "Error connecting to {}: {}\n".format(address, e))

def send_command():
    command = command_entry.get()
    try:
        tn.write(command.encode('ascii') + b"\n")
        output_text.insert(tk.END, tn.read_until(b"\n").decode('utf-8'))
    except Exception as e:
        output_text.insert(tk.END, "Error sending command: {}\n".format(e))

# Create the main window
root = tk.Tk()
root.title("Simple Telnet Client")

# Address entry
address_label = tk.Label(root, text="Enter Address:")
address_label.pack()
address_entry = tk.Entry(root)
address_entry.pack()

# Connect button
connect_button = tk.Button(root, text="Connect", command=connect_telnet)
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
