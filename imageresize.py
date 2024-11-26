import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


def resize_images(input_dir, output_dir, width, height, keep_aspect, format_choice, rename_option):
    """Resize images in a directory and save them to another directory."""
    try:
        os.makedirs(output_dir, exist_ok=True)
        supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
        image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(supported_formats)]

        if not image_files:
            messagebox.showerror("No Images Found", "No supported images found in the selected directory.")
            return

        for idx, img_file in enumerate(image_files, start=1):
            input_path = os.path.join(input_dir, img_file)
            file_name, _ = os.path.splitext(img_file)

            # Output file naming
            if rename_option:
                output_file_name = f"image_{idx}.{format_choice.lower()}"
            else:
                output_file_name = f"{file_name}.{format_choice.lower()}"

            output_path = os.path.join(output_dir, output_file_name)

            with Image.open(input_path) as img:
                if keep_aspect:
                    aspect_ratio = img.width / img.height
                    if img.width > img.height:
                        width = int(height * aspect_ratio)
                    else:
                        height = int(width / aspect_ratio)

                resized_img = img.resize((width, height))
                resized_img.save(output_path, format=format_choice.upper())

        messagebox.showinfo("Success", f"Resized {len(image_files)} images and saved to {output_dir}.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def select_input_directory():
    """Open a dialog to select the input directory."""
    folder_selected = filedialog.askdirectory(title="Select Input Directory")
    input_dir_var.set(folder_selected)


def select_output_directory():
    """Open a dialog to select the output directory."""
    folder_selected = filedialog.askdirectory(title="Select Output Directory")
    output_dir_var.set(folder_selected)


def start_resizing():
    """Handle the resizing operation."""
    input_dir = input_dir_var.get()
    output_dir = output_dir_var.get()

    if not input_dir or not os.path.isdir(input_dir):
        messagebox.showerror("Error", "Please select a valid input directory.")
        return

    if not output_dir:
        messagebox.showerror("Error", "Please select an output directory.")
        return

    try:
        width = int(width_var.get())
        height = int(height_var.get())
        keep_aspect = aspect_var.get()
        format_choice = format_var.get()
        rename_option = rename_var.get()
    except ValueError:
        messagebox.showerror("Error", "Please enter valid width and height values.")
        return

    resize_images(input_dir, output_dir, width, height, keep_aspect, format_choice, rename_option)


# Create GUI
root = tk.Tk()
root.title("Image Resizer Pro")
root.geometry("750x500")
root.configure(bg="#e6e6e6")

# Apply styles
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", font=("Arial", 11, "bold"), background="#e6e6e6")
style.configure("TButton", font=("Arial", 11, "bold"), background="#0078D7", foreground="white")
style.map("TButton", background=[("active", "#005a9e")])

# Variables
input_dir_var = tk.StringVar()
output_dir_var = tk.StringVar()
width_var = tk.StringVar(value="800")
height_var = tk.StringVar(value="600")
aspect_var = tk.BooleanVar(value=False)
format_var = tk.StringVar(value="JPEG")
rename_var = tk.BooleanVar(value=False)

# Header
header_frame = ttk.Frame(root, style="Header.TFrame")
header_frame.place(x=0, y=10, relwidth=1, height=50)
header_label = ttk.Label(
    header_frame,
    text="Professional Image Resizer",
    font=("Arial", 18, "bold"),
    background="#0078D7",
    foreground="white",
    anchor="center"
)
header_label.place(relx=0.5, rely=0.5, anchor="center")

# Main frame
frame = ttk.Frame(root, padding=20)
frame.place(x=30, y=80, relwidth=0.9, relheight=0.75)

# Input Directory
ttk.Label(frame, text="Input Directory:").place(x=10, y=10)
input_dir_entry = ttk.Entry(frame, textvariable=input_dir_var, width=50)
input_dir_entry.place(x=150, y=10)
ttk.Button(frame, text="Browse", command=select_input_directory).place(x=500, y=10)

# Output Directory
ttk.Label(frame, text="Output Directory:").place(x=10, y=50)
output_dir_entry = ttk.Entry(frame, textvariable=output_dir_var, width=50)
output_dir_entry.place(x=150, y=50)
ttk.Button(frame, text="Browse", command=select_output_directory).place(x=500, y=50)

# Width and Height
ttk.Label(frame, text="Width (px):").place(x=60, y=90)
width_entry = ttk.Entry(frame, textvariable=width_var, width=10)
width_entry.place(x=150, y=90)

#
ttk.Label(frame, text="Height (px):").place(x=300, y=90)
height_entry = ttk.Entry(frame, textvariable=height_var, width=10)
height_entry.place(x=400, y=90)

# Aspect Ratio Checkbox
aspect_checkbox = ttk.Checkbutton(frame, text="Maintain Aspect Ratio", variable=aspect_var)
aspect_checkbox.place(x=10, y=130)

# Format Dropdown
ttk.Label(frame, text="Output Format:").place(x=10, y=170)
format_dropdown = ttk.Combobox(frame, textvariable=format_var, values=["JPEG", "PNG", "BMP", "GIF"], state="readonly")
format_dropdown.place(x=150, y=170)

# Batch Rename Checkbox
rename_checkbox = ttk.Checkbutton(frame, text="Rename Files Sequentially", variable=rename_var)
rename_checkbox.place(x=10, y=210)

# Resize Button
resize_button = ttk.Button(frame, text="Resize Images", command=start_resizing)
resize_button.place(x=150, y=250, width=400, height=40)

# Mainloop
root.mainloop()
