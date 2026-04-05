# MO3MK API - Vercel Deployment

واجهة برمجية (API) لتحويل الفيديو إلى صوت باستخدام مكتبة MO3MK على منصة Vercel.

## 🚀 النقاط النهائية (Endpoints)

### 1. الصفحة الرئيسية
```
GET /
```
معلومات عن الخدمة والنقاط النهائية المتاحة.

### 2. التحقق من صحة الخدمة
```
GET /health
```
التحقق من أن الخدمة تعمل بشكل صحيح.

### 3. تحويل الفيديو إلى صوت
```
POST /convert
```
رفع ملف فيديو والحصول على ملف صوتي MP3.

**المعاملات:**
- `file`: ملف الفيديو (مطلوب)

**الصيغ المدعومة:**
- MP4, AVI, MOV, MKV, FLV, WMV

**الإخراج:**
- ملف MP3

### 4. معلومات الخدمة
```
GET /info
```
معلومات مفصلة عن الخدمة والمكتبة المستخدمة.

## 📝 أمثلة الاستخدام

### استخدام Python
```python
import requests

url = "https://your-vercel-url.vercel.app/convert"
files = {'file': open('video.mp4', 'rb')}

response = requests.post(url, files=files)

with open('audio.mp3', 'wb') as f:
    f.write(response.content)
print("تم استخراج الصوت بنجاح!")
```

### استخدام cURL
```bash
curl -X POST "https://your-vercel-url.vercel.app/convert" \
     -F "file=@video.mp4" \
     --output audio.mp3
```

### استخدام JavaScript/Fetch
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('https://your-vercel-url.vercel.app/convert', {
    method: 'POST',
    body: formData
})
.then(response => response.blob())
.then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'audio.mp3';
    a.click();
});
```

## 🛠️ التثبيت المحلي

```bash
pip install -r requirements.txt
python api.py
```

ثم اذهب إلى `http://localhost:8000/docs` لاستخدام الواجهة التفاعلية.

## 📦 التبعيات

- FastAPI
- Uvicorn
- MoviePy
- Pillow
- ImageIO

## 📄 الترخيص

MIT License
