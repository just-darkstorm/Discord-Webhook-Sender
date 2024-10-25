import tkinter as tk
from tkinter import messagebox
import requests
import json

def send_message():
    webhook_url = webhook_entry.get()
    username = username_entry.get().strip()
    message = message_entry.get("1.0", tk.END).strip()
    message_type = message_type_var.get()
    mention_id = mention_entry.get().strip()
    thread_id = thread_entry.get().strip()
    color_choice = color_var.get()

    if not webhook_url or not username or not message:
        messagebox.showwarning("Warning", "Please provide webhook URL, username, and message.")
        return

    headers = {
        'Content-Type': 'application/json'
    }

    payload = {}

    if message_type == 'Normal':
        if mention_id:
            formatted_message = f"<@{mention_id}> {message}"
        else:
            formatted_message = f"{message}"
        payload = {
            'content': formatted_message,
            'username': username
        }
    elif message_type == 'Embed':
        embed = {
            'title': f'Message from {username}',
            'description': message,
            'color': int(color_choice, 16)  # Convert hex color to int
        }
        if mention_id:
            embed['description'] = f"<@{mention_id}> {message}"
        payload = {
            'embeds': [embed],
            'username': username
        }

    if thread_id:
        webhook_url = f"{webhook_url}?thread_id={thread_id}"

    try:
        response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
        if response.status_code != 204:
            messagebox.showerror("Error", f"Failed to send message. Status code: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def copy_to_clipboard(entry):
    entry.clipboard_clear()
    entry.clipboard_append(entry.get())
    entry.update()

def paste_from_clipboard(entry):
    try:
        entry.delete(0, tk.END)
        entry.insert(0, root.clipboard_get())
    except tk.TclError:
        messagebox.showwarning("Warning", "Clipboard is empty or contains invalid data.")

root = tk.Tk()
root.title("Discord Webhook Sender")
root.configure(bg='#2F2F2F')

frame_webhook = tk.Frame(root, bg='#2F2F2F')
frame_webhook.pack(pady=5)

tk.Label(frame_webhook, text="Webhook URL:", bg='#2F2F2F', fg='#00A4E4').pack(side=tk.LEFT, padx=5)
webhook_entry = tk.Entry(frame_webhook, width=50, bg='#3C3C3C', fg='white', insertbackground='white')
webhook_entry.pack(side=tk.LEFT, padx=5)

tk.Button(frame_webhook, text="Copy", command=lambda: copy_to_clipboard(webhook_entry), bg='#00A4E4', fg='white').pack(side=tk.LEFT, padx=5)
tk.Button(frame_webhook, text="Paste", command=lambda: paste_from_clipboard(webhook_entry), bg='#00A4E4', fg='white').pack(side=tk.LEFT, padx=5)

frame_username = tk.Frame(root, bg='#2F2F2F')
frame_username.pack(pady=5)

tk.Label(frame_username, text="Username:", bg='#2F2F2F', fg='#00A4E4').pack(side=tk.LEFT, padx=5)
username_entry = tk.Entry(frame_username, width=50, bg='#3C3C3C', fg='white', insertbackground='white')
username_entry.pack(side=tk.LEFT, padx=5)

tk.Button(frame_username, text="Copy", command=lambda: copy_to_clipboard(username_entry), bg='#00A4E4', fg='white').pack(side=tk.LEFT, padx=5)
tk.Button(frame_username, text="Paste", command=lambda: paste_from_clipboard(username_entry), bg='#00A4E4', fg='white').pack(side=tk.LEFT, padx=5)

frame_message = tk.Frame(root, bg='#2F2F2F')
frame_message.pack(pady=5)

tk.Label(frame_message, text="Message:", bg='#2F2F2F', fg='#00A4E4').pack(side=tk.LEFT, padx=5)
message_entry = tk.Text(frame_message, height=10, width=50, bg='#3C3C3C', fg='white', insertbackground='white')
message_entry.pack(side=tk.LEFT, padx=5)

tk.Button(frame_message, text="Copy", command=lambda: copy_to_clipboard(message_entry), bg='#00A4E4', fg='white').pack(side=tk.LEFT, padx=5)
tk.Button(frame_message, text="Paste", command=lambda: paste_from_clipboard(message_entry), bg='#00A4E4', fg='white').pack(side=tk.LEFT, padx=5)

frame_mention = tk.Frame(root, bg='#2F2F2F')
frame_mention.pack(pady=5)

tk.Label(frame_mention, text="Mention User ID:", bg='#2F2F2F', fg='#00A4E4').pack(side=tk.LEFT, padx=5)
mention_entry = tk.Entry(frame_mention, width=50, bg='#3C3C3C', fg='white', insertbackground='white')
mention_entry.pack(side=tk.LEFT, padx=5)

frame_thread = tk.Frame(root, bg='#2F2F2F')
frame_thread.pack(pady=5)

tk.Label(frame_thread, text="Thread ID:", bg='#2F2F2F', fg='#00A4E4').pack(side=tk.LEFT, padx=5)
thread_entry = tk.Entry(frame_thread, width=50, bg='#3C3C3C', fg='white', insertbackground='white')
thread_entry.pack(side=tk.LEFT, padx=5)

frame_type = tk.Frame(root, bg='#2F2F2F')
frame_type.pack(pady=5)

tk.Label(frame_type, text="Message Type:", bg='#2F2F2F', fg='#00A4E4').pack(side=tk.LEFT, padx=5)
message_type_var = tk.StringVar(value='Normal')
message_type_menu = tk.OptionMenu(frame_type, message_type_var, 'Normal', 'Embed')
message_type_menu.config(bg='#3C3C3C', fg='white', highlightbackground='#00A4E4')
message_type_menu.pack(side=tk.LEFT, padx=5)

frame_color = tk.Frame(root, bg='#2F2F2F')
frame_color.pack(pady=5)

tk.Label(frame_color, text="Embed Color (Hex):", bg='#2F2F2F', fg='#00A4E4').pack(side=tk.LEFT, padx=5)
color_var = tk.StringVar(value='3066993')  # Default color
color_entry = tk.Entry(frame_color, width=10, bg='#3C3C3C', fg='white', insertbackground='white', textvariable=color_var)
color_entry.pack(side=tk.LEFT, padx=5)

send_button = tk.Button(root, text="Send Message", command=send_message, bg='#00A4E4', fg='white')
send_button.pack(pady=10)

root.mainloop()
