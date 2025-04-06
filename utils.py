import json
import os

def save_data(filename, data):
    try:
        with open(filename, "w") as f:
            json.dump(data, f)
        # تحقق إن الملف اتكتب فعلاً
        with open(filename, "r") as f:
            written_data = json.load(f)
            if written_data != data:
                print(f"خطأ: البيانات في {filename} لم تُكتب بشكل صحيح!")
    except Exception as e:
        print(f"خطأ في كتابة {filename}: {e}")

def load_data(filename, default):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
                else:
                    return default
        except (json.JSONDecodeError, ValueError) as e:
            print(f"خطأ في قراءة {filename}: {e}. بيتم استخدام القيمة الافتراضية.")
            return default
    else:
        # إذا الملف مش موجود، نكتبه بالقيمة الافتراضية
        save_data(filename, default)
        return default