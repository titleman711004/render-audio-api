import os
import tempfile
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import replicate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    try:
        # 1. 將使用者上傳的檔案暫存到 Render 伺服器上
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name

        # 2. 讀取暫存檔，發送給 Replicate 進行分軌
        with open(temp_file_path, "rb") as audio_file:
            # 🌟 這裡換成了 Replicate 官方最新、正確的 Demucs 模型版本號
            output = replicate.run(
                "cjwbw/demucs:25a173108cff36ef9f80f854c162d01df9e6528be175794b81158fa03836d953",
                input={"audio": audio_file}
            )
        
        # 3. 處理完成後，刪除暫存檔以節省空間
        os.remove(temp_file_path)

        # 回傳 4 個音軌的網址給前端
        return {
            "status": "success",
            "message": "AI 分軌大功告成！",
            "tracks": output 
        }

    except Exception as e:
        return {
            "status": "error", 
            "message": f"處理過程中發生錯誤：{str(e)}"
        }
