from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)

# กำหนดโฟลเดอร์ที่ใช้เก็บรูปภาพ
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def form():
    return '''
    <form action="/submit" method="post" enctype="multipart/form-data">
        <label for="name">ชื่อ:</label>
        <input type="text" id="name" name="name" required><br><br>
        
        <label for="workplace">ที่ทำงาน:</label>
        <input type="text" id="workplace" name="workplace" required><br><br>
        
        <label for="other_info">ข้อมูลอื่น ๆ:</label>
        <textarea id="other_info" name="other_info" rows="4"></textarea><br><br>
        
        <label for="photo">รูปภาพ:</label>
        <input type="file" id="photo" name="photo" accept="image/*" required><br><br>
        
        <button type="submit">ส่งข้อมูล</button>
    </form>
    '''

@app.route('/submit', methods=['POST'])
def submit():
    # รับข้อมูลจากฟอร์มและเก็บในตัวแปร
    name = request.form['name']
    workplace = request.form['workplace']
    other_info = request.form['other_info']
    
    # รับไฟล์รูปภาพ
    photo = request.files['photo']
    if photo and photo.filename != '':
        # สร้างชื่อไฟล์สำหรับรูปภาพ (เปลี่ยนชื่อหรือใช้ชื่อใหม่ได้)
        photo_filename = f"new_{photo.filename}"  # เปลี่ยนชื่อไฟล์ตามต้องการ
        # บันทึกไฟล์รูปภาพลงในโฟลเดอร์ UPLOAD_FOLDER
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
        photo.save(photo_path)
    else:
        return "กรุณาอัปโหลดรูปภาพ"

    # เปลี่ยนหน้าไปที่แสดงรูปภาพในกรอบสี่เหลี่ยม
    return f"""
    <html>
    <head>
        <style>
            .image-container {{
                width: 500px;
                height: 300px;
                border: 5px solid black;
                position: relative;
                margin: auto;
                display: flex;
                align-items: flex-start; /* จัดให้อยู่ด้านบน */
                padding-top: 10px; /* เว้นระยะจากขอบบน */
            }}
            .uploaded-image {{
                max-width: 150px;
                max-height: 100%;
                object-fit: contain;
                margin-left: 10px;
            }}
            .image-name {{
                position: absolute;
                top: 10px;
                right: 10px;
                background-color: rgba(255, 255, 255, 0.7);
                padding: 5px;
                font-size: 16px;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <h1>ข้อมูลที่บันทึกแล้ว</h1>
        <div class="image-container">
            <img src="/uploads/{photo_filename}" alt="Uploaded Image" class="uploaded-image">
            <div class="image-name">{name}</div>
        </div>
        <p><a href="/">กลับไปหน้าฟอร์ม</a></p>
    </body>
    </html>
    """

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # ให้บริการไฟล์ในโฟลเดอร์ uploads
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
