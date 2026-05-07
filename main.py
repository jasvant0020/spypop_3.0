from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from cryptography.fernet import Fernet
import os
from pathlib import Path
import shutil
from datetime import datetime  # ✅ for timestamp-based filenames
import zipfile

app = FastAPI()

# Directories
UPLOAD_DIR = Path("uploads")
PAYLOAD_DIR = Path("payload")
ZIP_DIR = Path("zips")  # ✅ New ZIP directory
UPLOAD_DIR.mkdir(exist_ok=True)
PAYLOAD_DIR.mkdir(exist_ok=True)
ZIP_DIR.mkdir(exist_ok=True)  # ✅ Ensure it exists

# Templates
templates = Jinja2Templates(directory="templates")

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/payload", StaticFiles(directory=PAYLOAD_DIR), name="payload")
app.mount("/zips", StaticFiles(directory=ZIP_DIR), name="zips")  # ✅ Serve zipped folders

# ========= ENCRYPTION CORE LOGIC =========

def save_key():
    key = Fernet.generate_key()
    key_path = PAYLOAD_DIR / "secret.key"
    with open(key_path, "wb") as key_file:
        key_file.write(key)
    return key

def encrypt_data(data: bytes, key: bytes):
    cipher = Fernet(key)
    return cipher.encrypt(data)

# ========= ROUTES =========

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.post("/api/create-payload")
async def create_payload(
    request: Request,
    message_type: str = Form(...),
    custom_timer: str = Form(...),
    covert_message: str = Form(None),
    media_file: UploadFile = File(None)
):
    try:
        # Step 1: Determine input source
        if message_type == "text" and covert_message:
            input_path = UPLOAD_DIR / "secret.txt"
            input_path.write_text(covert_message)
        elif media_file:
            input_path = UPLOAD_DIR / media_file.filename
            with open(input_path, "wb") as f:
                shutil.copyfileobj(media_file.file, f)
        else:
            return {"success": False, "message": "No valid data provided."}

        # Step 2: Encrypt
        with open(input_path, "rb") as f:
            raw_data = f.read()

        key = save_key()
        encrypted = encrypt_data(raw_data, key)

        enc_path = PAYLOAD_DIR / "secret.enc"
        with open(enc_path, "wb") as ef:
            ef.write(encrypted)

        # Step 3: Save metadata
        with open(PAYLOAD_DIR / "secret.type", "w") as tf:
            tf.write(message_type)
        with open(PAYLOAD_DIR / "timer.temp", "w") as tf:
            tf.write(custom_timer if custom_timer else "10")

        # ✅ Step 4: Create ZIP with timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_name = f"payload_{timestamp}.zip"
        zip_path = ZIP_DIR / zip_name

        files_to_include = [
            PAYLOAD_DIR / "secret.enc",
            PAYLOAD_DIR / "secret.key",
            PAYLOAD_DIR / "secret.type",
            PAYLOAD_DIR / "timer.temp",
            PAYLOAD_DIR / "decrypt.exe",  # Optional
        ]

        with zipfile.ZipFile(zip_path, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            for p in files_to_include:
                if p.exists():
                    zf.write(p, arcname=p.name)

        # ✅ Build download URL under /zips/
        download_url = f"/zips/{zip_name}"

        return {
            "success": True,
            "message": f"{message_type.capitalize()} payload encrypted successfully.",
            "download_url": download_url,
            "filename": zip_name
        }

    except Exception as e:
        return {"success": False, "message": str(e)}

@app.get("/api/download")
async def download_encrypted():
    enc_path = PAYLOAD_DIR / "secret.enc"
    if enc_path.exists():
        return HTMLResponse(
            content=f"<a href='/payload/secret.enc' download>Click to Download Encrypted File</a>",
            status_code=200
        )
    return {"success": False, "message": "No encrypted file found."}

