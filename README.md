# SpyPop Payload Encryptor

A FastAPI-based payload encryption tool that allows users to:

- Encrypt text or uploaded media files
- Generate encrypted payload packages
- Automatically create downloadable ZIP archives
- Store encryption metadata and keys
- Serve encrypted payloads via FastAPI static routes

---

# Project Structure

```bash
SpyPop_scratch/
│
├── main.py
├── requirements.txt
├── .gitignore
│
├── templates/
│   └── index.html
│
├── static/
│
├── uploads/
├── payload/
└── zips/
```

---

# Setup & Run (Windows)

## 1. Clone Repository

```bash
git clone https://github.com/jasvant0020/spypop_3.0.git
cd SpyPop_scratch
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

---

## 3. Activate Virtual Environment

### CMD

```bash
venv\Scripts\activate
```

### PowerShell

```bash
.\venv\Scripts\Activate.ps1
```

---

## 4. Install Dependencies

```bash
pip install fastapi uvicorn cryptography python-multipart jinja2
```

---

## 5. Create Required Folders

```bash
mkdir templates
mkdir static
mkdir uploads
mkdir payload
mkdir zips
```

---

## 6. Run Server

```bash
uvicorn main:app --reload
```

Server will start at:

```bash
http://127.0.0.1:8000
```

---

# API Endpoints

## Home Page

```bash
GET /
```

Loads the frontend UI from:

```bash
templates/index.html
```

---

## Create Encrypted Payload

```bash
POST /api/create-payload
```

### Form Fields

| Field | Type | Description |
|---|---|---|
| message_type | text | `text` or file type |
| custom_timer | text | Timer value |
| covert_message | text | Secret text |
| media_file | file | Uploaded media |

---

## Download Latest Encrypted File

```bash
GET /api/download
```

---

# Features

- Fernet AES encryption
- ZIP payload generation
- Timestamp-based filenames
- File upload support
- Static file serving
- FastAPI backend
- Jinja2 template rendering

---

# Example Run

```bash
uvicorn main:app --reload
```

Expected output:

```bash
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

# requirements.txt

```txt
fastapi
uvicorn
cryptography
python-multipart
jinja2
```

---

# .gitignore

```gitignore
__pycache__/
*.pyc
venv/
.env
uploads/
payload/
zips/
.vscode/
.idea/
```

---

# Notes

- Place frontend files inside `templates/` and `static/`
- `decrypt.exe` is optional
- Generated ZIP payloads are stored in `zips/`
- Encryption keys are stored temporarily in `payload/`

---

# Run Directly Using Python (Optional)

Add this at the bottom of `main.py`:

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
```

Then run:

```bash
python main.py
```

---

# Demo Usage

You can download the demo ZIP file from the `zips/` folder.

Steps:

```bash
1. Open the zips folder
2. Extract the ZIP file
3. Double-click the .exe file
```

Windows Defender or antivirus software may sometimes flag the executable because it is generated/custom packed, but the demo is intended for educational testing purposes only.

---

# Disclaimer

This project is created for educational and learning purposes only.

- It is not intended to harm users or systems
- It does not contain destructive functionality
- It is designed only to demonstrate encryption, payload packaging, and FastAPI integration
- Use responsibly and only in authorized environments
- The author is not responsible for misuse of this project
