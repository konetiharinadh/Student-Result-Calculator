
"""Student Result Calculator - Tkinter mini project."""

import csv
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk, filedialog, font as tkfont

SUBJECTS = [
    "English",
    "Mathematics",
    "Physics",
    "Chemistry",
    "Computer Science"
]

PASS_MARK = 35
PROJECT_DIR = Path(__file__).resolve().parent
CSV_FILE = PROJECT_DIR / "results.csv"

current_result = None


# -------------------- Grade Calculation --------------------

def grade_for(percentage):
    if percentage >= 90:
        return "A+"
    if percentage >= 80:
        return "A"
    if percentage >= 70:
        return "B"
    if percentage >= 60:
        return "C"
    if percentage >= 50:
        return "D"
    if percentage >= 35:
        return "E"
    return "F"


# -------------------- Save Results --------------------

def save_to_csv(result):
    file_exists = CSV_FILE.exists()

    with CSV_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Name", "Roll Number", *SUBJECTS,
                "Total", "Percentage", "Grade", "Result"
            ])

        writer.writerow([
            result["name"],
            result["roll"],
            *result["marks"],
            result["total"],
            f"{result['percentage']:.2f}",
            result["grade"],
            result["status"]
        ])


# -------------------- Calculate Result --------------------

def calculate_result():
    global current_result

    name = name_entry.get().strip()
    roll = roll_entry.get().strip()

    if not name or not roll:
        messagebox.showwarning(
            "Missing Details",
            "Please enter student name and roll number."
        )
        return

    marks = []

    for subject, entry in zip(SUBJECTS, mark_entries):
        raw = entry.get().strip()

        try:
            mark = int(raw)
        except ValueError:
            messagebox.showerror(
                "Invalid Marks",
                f"Enter a whole number for {subject}."
            )
            entry.focus()
            return

        if not 0 <= mark <= 100:
            messagebox.showerror(
                "Invalid Marks",
                f"{subject} marks must be between 0 and 100."
            )
            entry.focus()
            return

        marks.append(mark)

    total = sum(marks)
    percentage = total / len(SUBJECTS)

    passed = all(mark >= PASS_MARK for mark in marks)

    grade = grade_for(percentage) if passed else "F"
    status = "PASS" if passed else "FAIL"

    current_result = {
        "name": name,
        "roll": roll,
        "marks": marks,
        "total": total,
        "percentage": percentage,
        "grade": grade,
        "status": status
    }

    result_lines = [
        f"Student       : {name}",
        f"Roll Number   : {roll}",
        "-" * 42,
        *[
            f"{subject:<17}: {mark:>3} / 100"
            for subject, mark in zip(SUBJECTS, marks)
        ],
        "-" * 42,
        f"Total         : {total} / 500",
        f"Percentage    : {percentage:.2f}%",
        f"Grade         : {grade}",
        f"Final Result  : {status}"
    ]

    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.insert("1.0", "\n".join(result_lines))
    output_text.config(state="disabled")

    status_value.config(
        text=status,
        foreground="#15803d" if passed else "#b91c1c"
    )

    try:
        save_to_csv(current_result)
    except OSError as error:
        messagebox.showerror(
            "Save Error",
            f"Could not save results.csv:\n{error}"
        )
        return

    pdf_button.config(state="normal")

    messagebox.showinfo(
        "Success",
        "Result calculated and saved successfully!"
    )


# -------------------- PDF Report --------------------

def export_pdf():
    if current_result is None:
        messagebox.showwarning(
            "No Result",
            "Calculate a result before exporting PDF."
        )
        return

    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import (
            getSampleStyleSheet,
            ParagraphStyle
        )
        from reportlab.lib.enums import TA_CENTER
        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            Table,
            TableStyle
        )

    except ImportError:
        messagebox.showerror(
            "PDF Package Missing",
            "Install ReportLab using:\n\n"
            "python -m pip install reportlab"
        )
        return

    result = current_result

    safe_roll = "".join(
        ch for ch in result["roll"]
        if ch.isalnum() or ch in "-_ "
    ).strip().replace(" ", "_")

    suggested_name = f"Result_{safe_roll or 'student'}.pdf"

    output_path = filedialog.asksaveasfilename(
        title="Save Student Result PDF",
        initialdir=str(PROJECT_DIR),
        initialfile=suggested_name,
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")]
    )

    if not output_path:
        return

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ProjectTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#17365D"),
        fontSize=19,
        spaceAfter=8
    )

    story = [
        Paragraph("STUDENT RESULT CALCULATOR", title_style),
        Paragraph(
            "Student Academic Result",
            ParagraphStyle(
                "SubTitle",
                parent=styles["Normal"],
                alignment=TA_CENTER,
                textColor=colors.HexColor("#64748B"),
                fontSize=10
            )
        ),
        Spacer(1, 22)
    ]

    details = [
        ["Student Name", result["name"]],
        ["Roll Number", result["roll"]],
        [
            "Date Generated",
            datetime.now().strftime("%d-%m-%Y %I:%M %p")
        ]
    ]

    detail_table = Table(details, colWidths=[125, 350])

    detail_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1),
         colors.HexColor("#EAF1F8")),
        ("TEXTCOLOR", (0, 0), (0, -1),
         colors.HexColor("#17365D")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1),
         0.5, colors.HexColor("#D7E0EA")),
        ("PADDING", (0, 0), (-1, -1), 9)
    ]))

    story += [detail_table, Spacer(1, 18)]

    rows = [
        ["Subject", "Marks Obtained", "Maximum Marks"]
    ]

    rows += [
        [subject, str(mark), "100"]
        for subject, mark in zip(SUBJECTS, result["marks"])
    ]

    rows += [["TOTAL", str(result["total"]), "500"]]

    marks_table = Table(
        rows,
        colWidths=[250, 110, 115]
    )

    marks_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0),
         colors.HexColor("#1769AA")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, -1), (-1, -1),
         colors.HexColor("#EAF1F8")),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1),
         0.5, colors.HexColor("#D7E0EA")),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("PADDING", (0, 0), (-1, -1), 9)
    ]))

    story += [marks_table, Spacer(1, 18)]

    summary = [
        ["Percentage", f"{result['percentage']:.2f}%"],
        ["Grade", result["grade"]],
        ["Final Result", result["status"]]
    ]

    summary_table = Table(
        summary,
        colWidths=[125, 350]
    )

    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1),
         colors.HexColor("#EAF1F8")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (0, 0), (0, -1),
         colors.HexColor("#17365D")),
        ("TEXTCOLOR", (1, 2), (1, 2),
         colors.HexColor(
             "#15803D"
             if result["status"] == "PASS"
             else "#B91C1C"
         )),
        ("FONTNAME", (1, 2), (1, 2), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1),
         0.5, colors.HexColor("#D7E0EA")),
        ("PADDING", (0, 0), (-1, -1), 9)
    ]))

    story += [
        summary_table,
        Spacer(1, 28),
        Paragraph(
            "Pass mark: 35 in each subject. "
            "Generated by Student Result Calculator.",
            ParagraphStyle(
                "Foot",
                parent=styles["Normal"],
                fontSize=8,
                textColor=colors.grey,
                alignment=TA_CENTER
            )
        )
    ]

    try:
        SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=55,
            leftMargin=55,
            topMargin=55,
            bottomMargin=55
        ).build(story)

    except Exception as error:
        messagebox.showerror(
            "PDF Error",
            f"Could not create PDF:\n{error}"
        )
        return

    messagebox.showinfo(
        "PDF Saved",
        f"Student result PDF saved successfully:\n{output_path}"
    )


# -------------------- Clear Fields --------------------

def clear_fields():
    global current_result

    current_result = None

    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)

    for entry in mark_entries:
        entry.delete(0, tk.END)

    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)

    output_text.insert(
        "1.0",
        "Your calculated result will appear here.\n\n"
        "Enter student details and marks, then select Calculate Result."
    )

    output_text.config(state="disabled")

    status_value.config(
        text="Waiting",
        foreground="#64748B"
    )

    pdf_button.config(state="disabled")
    name_entry.focus()


# ==========================================================
#                  MODERN USER INTERFACE
# ==========================================================

root = tk.Tk()

root.title("Student Result Management System")
root.geometry("1200x750")
root.minsize(1000, 650)
root.configure(bg="#F1F5F9")


# Create named fonts to avoid Windows/Tk font parsing errors.

FONT_TITLE = tkfont.Font(
    root=root,
    family="Segoe UI",
    size=23,
    weight="bold"
)

FONT_SUB = tkfont.Font(
    root=root,
    family="Segoe UI",
    size=10
)

FONT_FIELD = tkfont.Font(
    root=root,
    family="Segoe UI",
    size=10,
    weight="bold"
)

FONT_SECTION = tkfont.Font(
    root=root,
    family="Segoe UI",
    size=11,
    weight="bold"
)

FONT_ENTRY = tkfont.Font(
    root=root,
    family="Segoe UI",
    size=10
)

FONT_BUTTON = tkfont.Font(
    root=root,
    family="Segoe UI",
    size=10,
    weight="bold"
)

FONT_STATUS = tkfont.Font(
    root=root,
    family="Segoe UI",
    size=9,
    weight="bold"
)

FONT_RESULT = tkfont.Font(
    root=root,
    family="Consolas",
    size=10
)


# -------------------- Theme and Styles --------------------

style = ttk.Style()

try:
    style.theme_use("clam")
except tk.TclError:
    pass

style.configure(
    "TFrame",
    background="#F3F6FB"
)

style.configure(
    "Card.TFrame",
    background="#FFFFFF"
)

style.configure(
    "Title.TLabel",
    background="#F3F6FB",
    foreground="#17365D",
    font=FONT_TITLE
)

style.configure(
    "Sub.TLabel",
    background="#F3F6FB",
    foreground="#64748B",
    font=FONT_SUB
)

style.configure(
    "Field.TLabel",
    background="#FFFFFF",
    foreground="#243247",
    font=FONT_FIELD
)

style.configure(
    "Section.TLabel",
    background="#FFFFFF",
    foreground="#1769AA",
    font=FONT_SECTION
)

style.configure(
    "TEntry",
    padding=8,
    font=FONT_ENTRY
)

style.configure(
    "Primary.TButton",
    font=FONT_BUTTON,
    padding=(18, 10),
    background="#1769AA",
    foreground="#FFFFFF"
)

style.map(
    "Primary.TButton",
    background=[("active", "#12558A")],
    foreground=[("disabled", "#CBD5E1")]
)

style.configure(
    "Secondary.TButton",
    font=FONT_BUTTON,
    padding=(18, 10),
    background="#E2E8F0",
    foreground="#243247"
)

style.map(
    "Secondary.TButton",
    background=[("active", "#CBD5E1")]
)

style.configure(
    "Pdf.TButton",
    font=FONT_BUTTON,
    padding=(18, 10),
    background="#15803D",
    foreground="#FFFFFF"
)

style.map(
    "Pdf.TButton",
    background=[("active", "#166534")]
)


# -------------------- Header --------------------

header = ttk.Frame(root)

header.pack(
    fill="x",
    padx=32,
    pady=(24, 16)
)

ttk.Label(
    header,
    text="STUDENT RESULT CALCULATOR",
    style="Title.TLabel"
).pack()

ttk.Label(
    header,
    text="Enter student details and marks to calculate the academic result",
    style="Sub.TLabel"
).pack(pady=(5, 0))


# -------------------- Student Details Card --------------------

form = ttk.Frame(
    root,
    style="Card.TFrame",
    padding=24
)

form.pack(
    fill="x",
    padx=32,
    pady=(0, 16)
)

form.columnconfigure(1, weight=1)

ttk.Label(
    form,
    text="STUDENT DETAILS",
    style="Section.TLabel"
).grid(
    row=0,
    column=0,
    columnspan=2,
    sticky="w",
    pady=(0, 10)
)

ttk.Label(
    form,
    text="Student Name",
    style="Field.TLabel"
).grid(
    row=1,
    column=0,
    sticky="w",
    pady=7
)

name_entry = ttk.Entry(form)

name_entry.grid(
    row=1,
    column=1,
    sticky="ew",
    padx=(22, 0),
    pady=7
)

ttk.Label(
    form,
    text="Roll Number",
    style="Field.TLabel"
).grid(
    row=2,
    column=0,
    sticky="w",
    pady=7
)

roll_entry = ttk.Entry(form)

roll_entry.grid(
    row=2,
    column=1,
    sticky="ew",
    padx=(22, 0),
    pady=7
)

ttk.Label(
    form,
    text="SUBJECT MARKS (0–100)",
    style="Section.TLabel"
).grid(
    row=3,
    column=0,
    columnspan=2,
    sticky="w",
    pady=(20, 8)
)


# -------------------- Subject Marks --------------------

marks_grid = ttk.Frame(
    form,
    style="Card.TFrame"
)

marks_grid.grid(
    row=4,
    column=0,
    columnspan=2,
    sticky="ew"
)

for col in range(5):
    marks_grid.columnconfigure(col, weight=1)

mark_entries = []

for index, subject in enumerate(SUBJECTS):

    cell = ttk.Frame(
        marks_grid,
        style="Card.TFrame"
    )

    cell.grid(
        row=0,
        column=index,
        sticky="ew",
        padx=(0 if index == 0 else 10, 0)
    )

    ttk.Label(
        cell,
        text=subject,
        style="Field.TLabel"
    ).pack(
        anchor="w",
        pady=(0, 6)
    )

    entry = ttk.Entry(
        cell,
        width=10,
        justify="center"
    )

    entry.pack(fill="x")

    mark_entries.append(entry)


# -------------------- Action Buttons --------------------

buttons = ttk.Frame(root)

buttons.pack(pady=(0, 16))

ttk.Button(
    buttons,
    text="Calculate Result",
    style="Primary.TButton",
    command=calculate_result
).grid(
    row=0,
    column=0,
    padx=6
)

ttk.Button(
    buttons,
    text="Clear",
    style="Secondary.TButton",
    command=clear_fields
).grid(
    row=0,
    column=1,
    padx=6
)

pdf_button = ttk.Button(
    buttons,
    text="Download Result PDF",
    style="Pdf.TButton",
    command=export_pdf,
    state="disabled"
)

pdf_button.grid(
    row=0,
    column=2,
    padx=6
)


# -------------------- Result Summary Card --------------------

result_card = ttk.Frame(
    root,
    style="Card.TFrame",
    padding=22
)

result_card.pack(
    fill="both",
    expand=True,
    padx=32,
    pady=(0, 16)
)

result_card.columnconfigure(0, weight=1)
result_card.rowconfigure(1, weight=1)

result_header = ttk.Frame(
    result_card,
    style="Card.TFrame"
)

result_header.grid(
    row=0,
    column=0,
    sticky="ew",
    pady=(0, 10)
)

ttk.Label(
    result_header,
    text="RESULT SUMMARY",
    style="Section.TLabel"
).pack(side="left")

status_value = tk.Label(
    result_header,
    text="Waiting",
    bg="#E2E8F0",
    fg="#64748B",
    font=FONT_STATUS,
    padx=12,
    pady=5
)

status_value.pack(side="right")


# -------------------- Result Display --------------------

output_text = tk.Text(
    result_card,
    height=12,
    wrap="word",
    font=FONT_RESULT,
    bg="#F8FAFC",
    fg="#243247",
    relief="flat",
    padx=14,
    pady=12,
    borderwidth=0,
    state="disabled"
)

output_text.grid(
    row=1,
    column=0,
    sticky="nsew"
)

output_text.config(state="normal")

output_text.insert(
    "1.0",
    "Your calculated result will appear here.\n\n"
    "Enter student details and marks, then select Calculate Result."
)

output_text.config(state="disabled")


# -------------------- Footer --------------------

footer = ttk.Label(
    root,
    text="Pass mark: 35 in each subject  •  Results are saved in results.csv",
    style="Sub.TLabel"
)

footer.pack(pady=(0, 14))


# -------------------- Start Application --------------------

name_entry.focus()

root.mainloop()
