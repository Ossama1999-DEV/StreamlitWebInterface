# 📊 Streamlit Web Interface

A modern, user-friendly web interface for exploring and filtering equipment data from Excel files. Built with **Streamlit** for rapid deployment and ease of use across **Linux** and **Windows** platforms.

---

## 📁 Project Structure

```
.
├── app.py                # Main Streamlit application
├── asetup.py             # Setup script for the application
├── requirements.txt      # Python dependencies
├── runLinux.sh           # Linux launcher script
├── runWindows.bat        # Windows launcher script
├── file.xlsx             # Default Excel data file
├── .streamlit/
│   └── config.toml       # Optional Streamlit configuration
├── .envrc                # Auto-generated for direnv (if missing)
└── .direnv/              # Optional direnv folder
```

---

## 🚀 Key Features

- **Excel File Support:**       Load and preview `.xlsx` files with ease
- **Multi-Sheet Detection:**    Automatically handles multiple sheets per file
- **Column Filtering:**         Filter data by column values (with `contains`)
- **Default & Custom Files:**   Uses `file.xlsx` by default, or specify your own
- **One-Click Launch:**         Opens automatically in your browser
- **Environment Variable:**     Set `STREAMLIT_XLS_FILE` to choose a file programmatically
- **Cross-Platform:**           Ready-to-use launchers for Linux and Windows
- **Clean Logging:**            Errors and output are logged for easy troubleshooting

---

## 🔧 Getting Started

### 1. Prerequisites

- **Python 3.8+**  
    Check your Python version:
    ```bash
    python3 --version
    ```

- **Virtual Environment (Recommended)**
    - **Linux:**
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```
    - **Windows:**
        ```cmd
        python -m venv .venv
        .venv\Scripts\activate
        ```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```
If using `direnv`, your environment will activate automatically via `.envrc`.

---

## 🏁 Running the Application

### 🐧 Linux

```bash
./runLinux.sh
```
- Sets up environment and dependencies
- Prompts for custom Excel file (optional)
- Launches Streamlit in your browser
- Logs output to `streamlit_output.log` and errors to `streamlit_error.log`

### 🪟 Windows

```cmd
runWindows.bat
```
- Installs dependencies
- Optionally prompts for Excel file
- Opens Streamlit in your browser
- Logs output and errors as above

---

## ⚙️ Configuration

- **Custom Excel File:**  
    Set the environment variable before launching:
    ```bash
    export STREAMLIT_XLS_FILE=/path/to/your_file.xlsx
    streamlit run app.py
    ```
    (Handled automatically by the launch scripts.)

- **Streamlit Settings:**  
    Customize `.streamlit/config.toml` as needed:
    ```toml
    [server]
    headless = false
    enableCORS = false

    [browser]
    gatherUsageStats = false
    serverAddress = "localhost"
    serverPort = 8501
    ```

---

## 🧪 Code Quality

- **Linting:**      `pylint app.py`
- **Formatting:**   `black app.py`

---

## 🛠️ Troubleshooting

- **PyArrow datetime conversion errors** are logged silently in `streamlit_error.log`.
- Closing the browser tab will stop the Streamlit app.

---

## 🧼 Clean Up

Remove logs and generated files:
```bash
rm -f streamlit_output.log streamlit_error.log
```

---

## 🙋 FAQ

- **Can I deploy this on a server?**  
    Yes! Ensure port 8501 is open and use `--server.headless=true` for remote access.

- **How do I reset to the default Excel file?**  
    When prompted by the launcher, press `n` to keep the default.

---

## 📃 License

MIT License © DBIBIH Oussama (2025)
[LICENSE](LICENSE)

---

## ✨ Credits

Built with **Streamlit**, **pandas**, and **Python**. Automated launch scripts ensure a seamless user experience.
