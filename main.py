import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry

# ==============================
# SETTINGS
# ==============================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ==============================
# DATA
# ==============================

current_plan = {
    "topic": "",
    "modules": [],
    "checkboxes": []
}

# ==============================
# APP
# ==============================

app = ctk.CTk()
app.title("Smart Study Planner")
app.geometry("1100x700")

# ==============================
# LAYOUT
# ==============================

sidebar = ctk.CTkFrame(
    app,
    width=220,
    corner_radius=0
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)

main_area = ctk.CTkFrame(
    app,
    corner_radius=0
)

main_area.pack(
    side="right",
    fill="both",
    expand=True
)

# ==============================
# HELPERS
# ==============================

def clear_page():
    for widget in main_area.winfo_children():
        widget.destroy()


def get_progress():

    if current_plan is None:
        return 0, 0, 0

    total = len(current_plan["checkboxes"])

    if total == 0:
        return 0, 0, 0

    completed = 0

    for var in current_plan["checkboxes"]:
        if var.get():
            completed += 1

    percent = int(
        (completed / total) * 100
    )

    return completed, total, percent


# ==============================
# DELETE PLAN
# ==============================

def delete_plan():

    global current_plan

    answer = messagebox.askyesno(
        "Delete Study Plan",
        "Delete the current study plan?"
    )

    if not answer:
        return

    current_plan = {
        "topic": "",
        "modules": [],
        "checkboxes": []
    }

    show_study_plan()


# ==============================
# DASHBOARD
# ==============================

def show_dashboard():

    clear_page()

    heading = ctk.CTkLabel(
        main_area,
        text="Dashboard",
        font=("Arial", 30, "bold")
    )

    heading.pack(
        anchor="w",
        padx=35,
        pady=(35, 20)
    )

    completed, total, percent = get_progress()

    if current_plan is None:

        topic = "No Study Plan"

    else:

        topic = (
        current_plan["topic"]
        if current_plan["topic"]
        else "No Study Plan"
    )

    stats = [
        ("Study Topic", topic),
        ("Total Modules", str(total)),
        ("Completed", str(completed)),
        ("Progress", f"{percent}%")
    ]

    stats_frame = ctk.CTkFrame(
        main_area,
        fg_color="transparent"
    )

    stats_frame.pack(
        fill="x",
        padx=20
    )

    for index, (title, value) in enumerate(stats):

        card = ctk.CTkFrame(
            stats_frame,
            height=120
        )

        card.grid(
            row=0,
            column=index,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        stats_frame.grid_columnconfigure(
            index,
            weight=1
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 14)
        ).pack(
            pady=(20, 5)
        )

        ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 22, "bold")
        ).pack()


# ==============================
# STUDY PLAN
# ==============================

def show_study_plan():

    clear_page()

    heading = ctk.CTkLabel(
        main_area,
        text="Study Plan",
        font=("Arial", 30, "bold")
    )

    heading.pack(
        anchor="w",
        padx=35,
        pady=(35, 10)
    )

    topic = current_plan["topic"]

    if topic:

        topic_label = ctk.CTkLabel(
            main_area,
            text=topic,
            font=("Arial", 18)
        )

        topic_label.pack(
            anchor="w",
            padx=35,
            pady=(0, 10)
        )

    if not current_plan["modules"]:

        ctk.CTkLabel(
            main_area,
            text="No study plan created."
        ).pack(
            pady=25
        )

        return
    
    delete_btn = ctk.CTkButton(
            main_area,
            text="Delete Study Plan",
            fg_color="red",
            hover_color="#8B0000",
            command=delete_plan
        )
    
    delete_btn.pack(
            anchor="w",
            padx=35,
            pady=(0, 15)
        )

    scroll_frame = ctk.CTkScrollableFrame(
        main_area
    )

    scroll_frame.pack(
        fill="both",
        expand=True,
        padx=35,
        pady=10
    )
    
    for module, var in zip(
        current_plan["modules"],
        current_plan["checkboxes"]
    ):

        row = ctk.CTkFrame(
            scroll_frame
        )

        row.pack(
            fill="x",
            pady=5
        )

        checkbox = ctk.CTkCheckBox(
            row,
            text=module,
            variable=var,
            command=show_dashboard
        )

        checkbox.pack(
            anchor="w",
            padx=15,
            pady=12
        )


# ==============================
# CREATE STUDY PLAN
# ==============================

def show_create_plan():

    clear_page()

    heading = ctk.CTkLabel(
        main_area,
        text="Create Study Plan",
        font=("Arial", 30, "bold")
    )

    heading.pack(
        anchor="w",
        padx=35,
        pady=(35, 20)
    )

    form_frame = ctk.CTkFrame(
        main_area
    )

    form_frame.pack(
        fill="x",
        padx=35,
        pady=10
    )

    ctk.CTkLabel(
        form_frame,
        text="Study Topic"
    ).pack(
        anchor="w",
        padx=20,
        pady=(20, 5)
    )

    topic_entry = ctk.CTkEntry(
        form_frame,
        width=500
    )

    topic_entry.pack(
        anchor="w",
        padx=20
    )

    ctk.CTkLabel(
        form_frame,
        text="Modules / Chapters (one per line)"
    ).pack(
        anchor="w",
        padx=20,
        pady=(20, 5)
    )

    modules_box = ctk.CTkTextbox(
        form_frame,
        width=600,
        height=250
    )

    modules_box.pack(
        anchor="w",
        padx=20,
        pady=(0, 20)
    )

    def create_plan():

        topic = topic_entry.get().strip()

        modules = [
            item.strip()
            for item in modules_box.get(
                "1.0",
                "end"
            ).splitlines()
            if item.strip()
        ]

        if not topic:

            messagebox.showerror(
                "Error",
                "Enter a study topic."
            )

            return

        if not modules:

            messagebox.showerror(
                "Error",
                "Enter at least one module."
            )

            return

        current_plan["topic"] = topic
        current_plan["modules"] = modules

        current_plan["checkboxes"] = [
            ctk.BooleanVar(value=False)
            for _ in modules
        ]

        show_study_plan()

    create_btn = ctk.CTkButton(
        form_frame,
        text="Create Study Plan",
        command=create_plan
    )

    create_btn.pack(
        anchor="w",
        padx=20,
        pady=(0, 20)
    )


# ==============================
# SIDEBAR
# ==============================

title = ctk.CTkLabel(
    sidebar,
    text="STUDY PLANNER",
    font=("Arial", 22, "bold")
)

title.pack(
    pady=(35, 30)
)

dashboard_btn = ctk.CTkButton(
    sidebar,
    text="Dashboard",
    command=show_dashboard
)

dashboard_btn.pack(
    fill="x",
    padx=20,
    pady=10
)

study_btn = ctk.CTkButton(
    sidebar,
    text="Study Plan",
    command=show_study_plan
)

study_btn.pack(
    fill="x",
    padx=20,
    pady=10
)

create_btn = ctk.CTkButton(
    sidebar,
    text="Create Study Plan",
    command=show_create_plan
)

create_btn.pack(
    fill="x",
    padx=20,
    pady=10
)

# ==============================
# START
# ==============================

show_dashboard()

app.mainloop()