import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import pytesseract

# Tesseract location
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.title("Study Planner")
app.geometry("900x700")


def display_schedule(text):

    # Clear old tasks
    for widget in tasks_frame.winfo_children():
        widget.destroy()

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        checkbox = ctk.CTkCheckBox(
            tasks_frame,
            text=line
        )

        checkbox.pack(
            anchor="w",
            padx=10,
            pady=5
        )


def upload_schedule():

    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Images", "*.png *.jpg *.jpeg *.bmp")
        ]
    )

    if not file_path:
        return

    image = Image.open(file_path)

    text = pytesseract.image_to_string(image)

    display_schedule(text)


title = ctk.CTkLabel(
    app,
    text="Study Planner",
    font=("Segoe UI", 28, "bold")
)

title.pack(pady=20)

upload_button = ctk.CTkButton(
    app,
    text="Upload Schedule Screenshot",
    command=upload_schedule
)

upload_button.pack(pady=20)

today_label = ctk.CTkLabel(
    app,
    text="Today's Tasks",
    font=("Segoe UI", 22, "bold")
)

today_label.pack(pady=10)

tasks_frame = ctk.CTkScrollableFrame(
    app,
    width=800,
    height=500
)

tasks_frame.pack(
    padx=20,
    pady=10,
    fill="both",
    expand=True
)

app.mainloop()