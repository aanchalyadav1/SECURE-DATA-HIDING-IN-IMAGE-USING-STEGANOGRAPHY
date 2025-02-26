import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import struct
from PIL import Image, ImageTk

# Global dictionaries for character-to-ASCII and ASCII-to-character mappings
d = {}
c = {}
for i in range(256):  # Include 255
    d[chr(i)] = i
    c[i] = chr(i)

# Function to display the selected image
def display_image(image_path, label):
    try:
        # Open and resize the image
        img = Image.open(image_path)
        img = img.resize((250, 250), Image.Resampling.LANCZOS)  # Resize for display
        img_tk = ImageTk.PhotoImage(img)

        # Update the label with the new image
        label.config(image=img_tk)
        label.image = img_tk  # Keep a reference to avoid garbage collection
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image: {e}")

# Function to encode the message into the image
def encode_image():
    # Get the image path
    image_path = encode_image_entry.get()
    if not image_path:
        messagebox.showerror("Error", "Please select an image for encoding.")
        return

    # Read the image
    img = cv2.imread(image_path)

    # Get the secret message and password
    msg = encode_message_entry.get("1.0", tk.END).strip()  # Get multi-line input
    password = encode_password_entry.get()

    if not msg or not password:
        messagebox.showerror("Error", "Please enter a message and password for encoding.")
        return

    # Store the length of the message in the first 4 pixels
    message_length = len(msg)
    length_bytes = struct.pack(">I", message_length)  # Pack length as 4-byte integer

    # Embed the length into the first 4 pixels
    for i in range(4):
        img[0, i, 0] = length_bytes[i]

    # Initialize variables for embedding the message
    m = 0
    n = 4  # Start embedding after the first 4 pixels
    z = 0

    # Embed the message into the image
    for i in range(len(msg)):
        img[n, m, z] = d[msg[i]]
        n = n + 1
        m = m + 1
        z = (z + 1) % 3

    # Create the "Encrypted_Images" folder if it doesn't exist
    if not os.path.exists("Encrypted_Images"):
        os.makedirs("Encrypted_Images")

    # Get the original image name and create the new name
    original_name = os.path.basename(image_path)
    encrypted_image_name = f"Encrypted_{original_name}"
    encrypted_image_path = os.path.join("Encrypted_Images", encrypted_image_name)

    # Save the encrypted image
    cv2.imwrite(encrypted_image_path, img)

    # Show success message
    messagebox.showinfo("Success", "Message encoded successfully!")

# Function to decode the message from the image
def decode_image():
    # Get the encrypted image path
    encrypted_image_path = decode_image_entry.get()
    if not encrypted_image_path:
        messagebox.showerror("Error", "Please select an encrypted image for decoding.")
        return

    # Read the encrypted image
    img = cv2.imread(encrypted_image_path)

    # Get the passcode for decryption
    pas = decode_password_entry.get()

    if not pas:
        messagebox.showerror("Error", "Please enter a passcode for decoding.")
        return

    # Retrieve the length of the message from the first 4 pixels
    length_bytes = bytes([img[0, i, 0] for i in range(4)])
    message_length = struct.unpack(">I", length_bytes)[0]  # Unpack length as 4-byte integer

    # Decrypt the message if the passcode is correct
    if decode_password_entry.get() == pas:
        message = ""
        n = 4  # Start reading after the first 4 pixels
        m = 0
        z = 0
        for i in range(message_length):
            message = message + c[img[n, m, z]]
            n = n + 1
            m = m + 1
            z = (z + 1) % 3

        # Display the decoded message in a pop-up uneditable text box
        popup = tk.Toplevel()
        popup.title("Decrypted Message")
        text_box = scrolledtext.ScrolledText(popup, wrap=tk.WORD, width=50, height=10, state="disabled")
        text_box.pack(padx=10, pady=10)
        text_box.config(state="normal")
        text_box.insert(tk.END, message)
        text_box.config(state="disabled")
    else:
        messagebox.showerror("Error", "YOU ARE NOT auth")

# Function to open a file dialog and select an image for encoding
def select_encode_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.webp")])
    encode_image_entry.delete(0, tk.END)
    encode_image_entry.insert(0, file_path)
    display_image(file_path, encode_image_label)

# Function to open a file dialog and select an encrypted image for decoding
def select_decode_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.webp")])
    decode_image_entry.delete(0, tk.END)
    decode_image_entry.insert(0, file_path)
    display_image(file_path, decode_image_label)

# Create the main window
root = tk.Tk()
root.title("Steganography App")

# Encoding Section
encode_frame = tk.LabelFrame(root, text="Encoding", padx=10, pady=10)
encode_frame.grid(row=0, column=0, padx=10, pady=10)

tk.Label(encode_frame, text="Image Path:").grid(row=0, column=0, padx=5, pady=5)
encode_image_entry = tk.Entry(encode_frame, width=50)
encode_image_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(encode_frame, text="Browse", command=select_encode_image).grid(row=0, column=2, padx=5, pady=5)

# Label to display the selected image for encoding
encode_image_label = tk.Label(encode_frame)
encode_image_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

tk.Label(encode_frame, text="Secret Message:").grid(row=2, column=0, padx=5, pady=5)
encode_message_entry = tk.Text(encode_frame, width=50, height=5)  # Bigger input box
encode_message_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(encode_frame, text="Password:").grid(row=3, column=0, padx=5, pady=5)
encode_password_entry = tk.Entry(encode_frame, width=50, show="*")
encode_password_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Button(encode_frame, text="Encode Message", command=encode_image).grid(row=4, column=1, padx=5, pady=5)

# Decoding Section
decode_frame = tk.LabelFrame(root, text="Decoding", padx=10, pady=10)
decode_frame.grid(row=0, column=1, padx=10, pady=10)

tk.Label(decode_frame, text="Encrypted Image Path:").grid(row=0, column=0, padx=5, pady=5)
decode_image_entry = tk.Entry(decode_frame, width=50)
decode_image_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(decode_frame, text="Browse", command=select_decode_image).grid(row=0, column=2, padx=5, pady=5)

# Label to display the selected image for decoding
decode_image_label = tk.Label(decode_frame)
decode_image_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

tk.Label(decode_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5)
decode_password_entry = tk.Entry(decode_frame, width=50, show="*")
decode_password_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Button(decode_frame, text="Decode Message", command=decode_image).grid(row=3, column=1, padx=5, pady=5)

# Start the main loop
root.mainloop()
