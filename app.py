from flask import Flask, request, send_from_directory, render_template, url_for
import torch
from diffusers import PixArtAlphaPipeline
from PIL import Image
import os

app = Flask(__name__)

# กำหนดโฟลเดอร์ที่ใช้เก็บรูปภาพ
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# สร้างฟอร์มการอัปโหลด
@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    # รับข้อมูลจากฟอร์มและเก็บในตัวแปร
    name = request.form['name']
    workplace = request.form['workplace']
    other_info = request.form['other_info']
    
    # รับไฟล์รูปภาพ (ถ้ามี)
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

    # สร้างภาพใหม่โดยใช้ PixArtAlphaPipeline
    pipe = PixArtAlphaPipeline.from_pretrained("PixArt-alpha/PixArt-LCM-XL-2-1024-MS", use_safetensors=True)
    prompt = "dog"
    generator = torch.Generator().manual_seed(42)
    image = pipe(prompt, guidance_scale=0.0, num_inference_steps=4, generator=generator, height=512, width=1024).images[0]
    
    
   
    
    # สร้างชื่อไฟล์สำหรับภาพที่สร้าง
    generated_image_filename = "generated_image.png"
    generated_image_path = os.path.join(app.config['UPLOAD_FOLDER'], generated_image_filename)
    rectangular_image.save(generated_image_path)

    # สร้าง URL สำหรับภาพที่สร้าง
    generated_image_url = url_for('uploaded_file', filename=generated_image_filename)

    # ส่งข้อมูลไปยัง HTML template
    return render_template('card_result.html', name=name, photo_url=photo_url, generated_image_url=generated_image_url)

# ให้บริการไฟล์ในโฟลเดอร์ uploads
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
