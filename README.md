# Student Result Calculator

A beginner-friendly Python mini project built with **Tkinter**. It calculates a student's total marks, percentage, grade, and pass/fail status for five subjects. Results are saved to a CSV file, and the latest result can be exported as a PDF.

## Features

- Simple, modern desktop interface
- Student name and roll number input
- Marks entry for English, Mathematics, Physics, Chemistry, and Computer Science
- Input validation (each mark must be a whole number from 0 to 100)
- Automatic total, percentage, grade, and pass/fail calculation
- A student must score at least 35 in every subject to pass
- Saves calculated results to `results.csv`
- Exports the latest calculated result as a PDF

## Requirements

- Windows, macOS, or Linux
- Python 3.10 or newer
- Tkinter (included with most standard Python installations)
- ReportLab (installed in the next step for PDF export)

## Run in VS Code

1. Extract this project ZIP file.
2. Open VS Code and choose **File → Open Folder**. Select the `Student_Result_Calculator` folder (the folder containing `app.py`).
3. Open **Terminal → New Terminal**.
4. Check Python is installed:

   ```bash
   python --version
   ```

5. Install the PDF dependency:

   ```bash
   python -m pip install -r requirements.txt
   ```

6. Start the application:

   ```bash
   python app.py
   ```

7. Enter the student details and five subject marks, then click **Calculate Result**. Click **Download Result PDF** to save a PDF copy of the latest result.

> If `python` is not recognized on Windows, try `py` instead: `py -m pip install -r requirements.txt` and `py app.py`.

## Grade calculation

| Percentage | Grade |
|---:|:---:|
| 90–100 | A+ |
| 80–89.99 | A |
| 70–79.99 | B |
| 60–69.99 | C |
| 50–59.99 | D |
| 35–49.99 | E |
| Below 35, or any subject below 35 | F / FAIL |

## Project files

```text
Student_Result_Calculator/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── Project_Report.docx
└── Project_Presentation.pptx
```

`results.csv` is created automatically after the first calculation. It is excluded from Git by `.gitignore` so student data is not accidentally published.

## Upload to GitHub

Create an empty repository on GitHub named `Student-Result-Calculator`. Do not initialize it with a README (this folder already has one). Then run these commands in the VS Code terminal from this project folder, replacing the URL with your own repository URL:

```bash
git init
git add .
git commit -m "Add Student Result Calculator project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/Student-Result-Calculator.git
git push -u origin main
```

Before pushing, check that `results.csv` and any real student personal data are not being uploaded.

## Author

Add your name, college, branch, and academic year here before submitting the project.
