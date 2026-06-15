# منصة إنشاء الامتحانات بالذكاء الاصطناعي
# AI Exam Generator Platform

منصة ويب متكاملة لإنشاء امتحانات احترافية باستخدام الذكاء الاصطناعي.

## المميزات الرئيسية

✨ **رفع المحتوى**
- دعم ملفات Word (DOCX)، PDF، و TXT
- استخراج النص تلقائيًا وتحليله

🤖 **الذكاء الاصطناعي**
- تحليل المحتوى بواسطة OpenAI API
- استخراج المفاهيم الرئيسية والمصطلحات
- توليد أسئلة متوازنة وذكية

📝 **أنواع الأسئلة**
- اختيار من متعدد (MCQ)
- صح وخطأ
- أكمل الفراغ
- أسئلة مقالية
- أسئلة عملية

📊 **بنك الأسئلة**
- حفظ جميع الأسئلة المُنشأة
- منع التكرار (تشابه 80%)
- البحث والتصفية

📄 **التصدير**
- تصدير إلى Word (DOCX)
- تصدير إلى PDF
- نماذج متعددة (A, B, C, D)

🔐 **الأمان**
- التحقق من الملفات المرفوعة
- منع الملفات الضارة
- التحقق من الامتدادات

## المتطلبات

- Python 3.8+
- FastAPI
- SQLite
- OpenAI API Key

## التثبيت والتشغيل

### 1. استنساخ المشروع
```bash
git clone https://github.com/abosaad010280-sinai/ai-exam-generator.git
cd ai-exam-generator
```

### 2. إنشاء بيئة افتراضية
```bash
python -m venv venv
source venv/bin/activate  # على Linux/Mac
# أو
venv\Scripts\activate  # على Windows
```

### 3. تثبيت المكتبات
```bash
pip install -r requirements.txt
```

### 4. إعداد متغيرات البيئة
```bash
cp .env.example .env
# ثم قم بتعديل الملف وأضف OpenAI API Key
```

### 5. إنشاء قاعدة البيانات
```bash
python scripts/init_db.py
```

### 6. تشغيل التطبيق
```bash
uvicorn app.main:app --reload
```

التطبيق سيكون متاحًا على: `http://localhost:8000`

## هيكل المشروع

```
ai-exam-generator/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── uploads.py
│   │   │   ├── exams.py
│   │   │   ├── questions.py
│   │   │   └── dashboard.py
│   │   └── dependencies.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   └── logger.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── database.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── exam.py
│   │   ├── question.py
│   │   └── upload.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── file_processor.py
│   │   ├── ai_service.py
│   │   ├── exam_generator.py
│   │   ├── question_bank.py
│   │   └── export_service.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   └── helpers.py
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── main.js
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── upload.html
│   ├── exam_settings.html
│   ├── exam_preview.html
│   ├── question_bank.html
│   ├── dashboard.html
│   └── components/
│       ├── navbar.html
│       └── footer.html
├── database/
│   └── exam.db
├── uploads/
│   └── .gitkeep
├── exports/
│   └── .gitkeep
├── scripts/
│   ├── __init__.py
│   └── init_db.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## المتغيرات البيئية

أنشئ ملف `.env` بالمحتوى التالي:

```env
# FastAPI
FASTAPI_ENV=development
DEBUG=true

# OpenAI
OPENAI_API_KEY=your_api_key_here

# Database
DATABASE_URL=sqlite:///./database/exam.db

# Upload Settings
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_EXTENSIONS=pdf,docx,txt

# File Paths
UPLOAD_FOLDER=uploads
EXPORT_FOLDER=exports
```

## استخدام التطبيق

### الصفحة الرئيسية
- عنوان: منصة إنشاء الامتحانات بالذكاء الاصطناعي
- أزرار رئيسية: رفع ملف، إنشاء امتحان، عرض بنك الأسئلة

### رفع الملفات
1. انقر على "رفع ملف"
2. اختر ملف Word أو PDF أو TXT
3. سيتم استخراج النص تلقائيًا

### إعدادات الامتحان
- اسم المادة
- الفرقة الدراسية
- مدة الامتحان
- درجة الامتحان
- عدد الأسئلة
- أنواع الأسئلة المرغوبة

### توليد الامتحان
- سيتم تحليل المحتوى بالذكاء الاصطناعي
- توليد أسئلة متنوعة ومتوازنة
- إنشاء نموذج الطالب والمدرس

### التصدير
- تصدير النموذج إلى Word
- تصدير إلى PDF
- إنشاء نماذج متعددة (A, B, C, D)

## API Endpoints

### Uploads
- `POST /api/upload` - رفع ملف
- `GET /api/uploads` - قائمة الملفات المرفوعة

### Exams
- `POST /api/exams/create` - إنشاء امتحان جديد
- `GET /api/exams` - قائمة الامتحانات
- `GET /api/exams/{exam_id}` - تفاصيل امتحان
- `DELETE /api/exams/{exam_id}` - حذف امتحان

### Questions
- `GET /api/questions` - بنك الأسئلة
- `GET /api/questions/{question_id}` - تفاصيل سؤال
- `DELETE /api/questions/{question_id}` - حذف سؤال

### Dashboard
- `GET /api/dashboard/stats` - إحصائيات

## الترخيص

MIT License

## المساهمة

نرحب بمساهماتك! يرجى:
1. عمل Fork للمشروع
2. إنشاء فرع للميزة الجديدة
3. إرسال Pull Request

## الدعم

للمشاكل والاستفسارات، يرجى فتح issue جديد.

---

تم تطوير هذا المشروع بواسطة: **abosaad010280-sinai**
