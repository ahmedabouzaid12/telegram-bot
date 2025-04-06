import json
import os

def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f)

def load_data(filename, default):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                content = f.read().strip()  # نقرأ المحتوى ونزيل المسافات البيضاء
                if content:  # لو فيه بيانات
                    return json.loads(content)
                else:  # لو الملف فاضي
                    return default
        except (json.JSONDecodeError, ValueError) as e:
            print(f"خطأ في قراءة {filename}: {e}. بيتم استخدام القيمة الافتراضية.")
            return default
    return default