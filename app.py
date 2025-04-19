import requests
import re
import os
import subprocess

# 1. جلب رابط ngrok الحالي من واجهة HTTP
def get_ngrok_url():
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        tunnels = response.json()['tunnels']
        for tunnel in tunnels:
            if tunnel['proto'] == 'https':
                return tunnel['public_url']
    except Exception as e:
        print("خطأ أثناء الحصول على رابط ngrok:", e)
        return None

# 2. تعديل ملف HTML
def update_html_file(ngrok_url, file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # استبدال الرابط داخل كود الجافاسكربت
        new_content = re.sub(
            r'var ngrokUrl = "https://.*?";',
            f'var ngrokUrl = "{ngrok_url}";',
            content
        )

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print("تم تحديث ملف HTML بنجاح.")
    except Exception as e:
        print("خطأ أثناء تعديل الملف:", e)

# 3. رفع التعديلات على GitHub
def push_to_github():
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "تحديث رابط ngrok تلقائي"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ تم رفع التعديلات إلى GitHub.")
    except subprocess.CalledProcessError as e:
        print("❌ خطأ أثناء رفع التعديلات:", e)

# مسار ملف HTML
html_file_path = "index.html"  # غيره حسب اسم المسار داخل المشروع

# تشغيل المهام
ngrok_url = get_ngrok_url()
if ngrok_url:
    update_html_file(ngrok_url, html_file_path)
    push_to_github()
else:
    print("لم يتم العثور على رابط ngrok.")
