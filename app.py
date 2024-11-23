from flask import Flask, request, send_from_directory, render_template, url_for
import os

app = Flask(__name__)

# กำหนดโฟลเดอร์ที่ใช้เก็บรูปภาพ
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    # รับข้อมูลจากฟอร์มและเก็บในตัวแปร
    name = request.form['name']
    workplace = request.form['workplace']
    other_info = request.form['other_info']
    
    # รับไฟล์รูปภาพ
    photo = request.files['photo']
    if photo and photo.filename != '':
        # สร้างชื่อไฟล์สำหรับรูปภาพ
        photo_filename = f"new_{photo.filename}"
        # บันทึกไฟล์รูปภาพลงในโฟลเดอร์ UPLOAD_FOLDER
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
        photo.save(photo_path)

        # สร้าง URL สำหรับรูปภาพ
        photo_url = url_for('uploaded_file', filename=photo_filename)
    else:
        return "กรุณาอัปโหลดรูปภาพ"

    # ส่งข้อมูลไปยัง HTML template
    return render_template('card_result.html', name=name, photo_url=photo_url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # ให้บริการไฟล์ในโฟลเดอร์ uploads
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
