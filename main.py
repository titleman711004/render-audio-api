from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 設定 CORS，只允許你的 GitHub Pages 網址連線 (測試時可先用 "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 之後上線記得改成 "https://你的帳號.github.io"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    # 這裡之後會放入音訊分軌的 AI 邏輯
    # 現在我們先模擬「成功接收檔案」
    file_size = len(await file.read())
    
    return {
        "status": "success",
        "message": "Render 說：檔案接收成功！",
        "filename": file.filename,
        "size_bytes": file_size,
        "mock_file_url": f"https://render-storage.com/temp/{file.filename}" # 模擬暫存網址
    }