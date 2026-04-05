from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import logging
import tempfile
from moviepy import VideoFileClip

# إعداد السجلات
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# إنشاء تطبيق FastAPI
app = FastAPI(
    title="MO3MK API",
    description="واجهة برمجية لتحويل الفيديو إلى صوت باستخدام مكتبة MO3MK",
    version="1.0.0"
)

# إضافة CORS middleware للسماح بالطلبات من أي مصدر
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# استخدام مجلد مؤقت آمن
UPLOAD_DIR = tempfile.gettempdir()

def extract_audio(video_path, output_audio_path=None):
    """
    استخراج الصوت من ملف الفيديو.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"الملف {video_path} غير موجود.")
        
    if output_audio_path is None:
        base_name = os.path.splitext(video_path)[0]
        output_audio_path = f"{base_name}.mp3"
        
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(output_audio_path, verbose=False, logger=None)
        video.close()
        return output_audio_path
    except Exception as e:
        raise Exception(f"حدث خطأ أثناء التحويل: {str(e)}")

@app.get("/")
async def root():
    """
    نقطة النهاية الرئيسية للـ API.
    """
    return {
        "message": "مرحباً بك في MO3MK API! 🎥🔊",
        "endpoints": {
            "convert": "/convert",
            "docs": "/docs",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """
    التحقق من صحة الخدمة.
    """
    return {
        "status": "healthy",
        "service": "MO3MK Audio Extractor API"
    }

@app.post("/convert")
async def convert_video(file: UploadFile = File(...)):
    """
    تحويل الفيديو المرسل إلى ملف صوتي MP3.
    
    Parameters:
    - file: ملف الفيديو المراد تحويله
    
    Returns:
    - ملف MP3 مع الصوت المستخرج
    """
    try:
        # التحقق من أن الملف موجود
        if not file.filename:
            raise HTTPException(status_code=400, detail="لم يتم تحديد ملف")
        
        # حفظ الملف المرسل مؤقتاً
        video_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"تم تحميل الملف: {file.filename}")
        
        # تحديد مسار ملف الصوت الناتج
        base_name = os.path.splitext(file.filename)[0]
        audio_path = os.path.join(UPLOAD_DIR, f"{base_name}.mp3")
        
        # استخراج الصوت
        logger.info(f"جاري استخراج الصوت من {file.filename}...")
        extract_audio(video_path, audio_path)
        
        logger.info(f"تم إنشاء ملف الصوت: {audio_path}")
        
        # إرسال ملف الصوت للمستخدم
        return FileResponse(
            path=audio_path,
            filename=f"{base_name}.mp3",
            media_type="audio/mpeg"
        )
    
    except Exception as e:
        logger.error(f"حدث خطأ: {str(e)}")
        raise HTTPException(status_code=500, detail=f"خطأ في المعالجة: {str(e)}")
    
    finally:
        # تنظيف الملفات المؤقتة
        if video_path and os.path.exists(video_path):
            try:
                os.remove(video_path)
            except:
                pass

@app.get("/info")
async def info():
    """
    معلومات عن الخدمة والمكتبة المستخدمة.
    """
    return {
        "service": "MO3MK Audio Extractor API",
        "version": "1.0.0",
        "library": "MO3MK",
        "library_version": "1.0.0",
        "description": "استخراج الصوت من الفيديوهات بسهولة",
        "supported_formats": ["mp4", "avi", "mov", "mkv", "flv", "wmv"],
        "output_format": "mp3"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
