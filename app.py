from flask import Flask, request, send_from_directory, render_template, url_for
import torch
from diffusers import PixArtAlphaPipeline
from PIL import Image
import os
import uuid


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
    gmail = request.form['gmail']
    phone = request.form['phone']
    address = request.form['address']

    
    
# รับไฟล์รูปภาพ (ถ้ามี) 
    photo = request.files['photo']
    if photo and photo.filename != '':
        # สร้างชื่อไฟล์สำหรับรูปภาพ (ใช้ uuid หรือ timestamp เพื่อป้องกันชื่อซ้ำ)
        photo_filename = f"{uuid.uuid4().hex}_{photo.filename}"
        
        # บันทึกไฟล์รูปภาพลงในโฟลเดอร์ UPLOAD_FOLDER
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
        photo.save(photo_path)

        # สร้าง URL สำหรับรูปภาพ
        photo_url = url_for('uploaded_file', filename=photo_filename)
    else:
        return "กรุณาอัปโหลดรูปภาพ"

    # รับรูปไลน์
    Line = request.files['Line']
    if Line and Line.filename != '':
        # สร้างชื่อไฟล์สำหรับรูปภาพ (ใช้ uuid หรือ timestamp เพื่อป้องกันชื่อซ้ำ)
        Line_filename = f"{uuid.uuid4().hex}_{Line.filename}"
        
        # บันทึกไฟล์รูปภาพลงในโฟลเดอร์ UPLOAD_FOLDER
        Line_path = os.path.join(app.config['UPLOAD_FOLDER'], Line_filename)
        Line.save(Line_path)

        # สร้าง URL สำหรับรูปภาพ
        Line_url = url_for('uploaded_file', filename=Line_filename)
    else:
        return "กรุณาอัปโหลดรูปภาพ"

    
    
    # สร้างภาพใหม่โดยใช้ PixArtAlphaPipeline
    pipe = PixArtAlphaPipeline.from_pretrained("PixArt-alpha/PixArt-LCM-XL-2-1024-MS", use_safetensors=True)
    pipe.scheduler.set_timesteps(42)  # Adjust timesteps for faster image generation (optional)
    prompt = request.form['prompt']
    generator = torch.Generator().manual_seed(42)

    
    generated_image = pipe(prompt, guidance_scale=0.0, num_inference_steps=4, generator=generator,height=512 , width=1024).images[0]

    # สร้างชื่อไฟล์สำหรับภาพที่สร้าง
    generated_image_filename = "generated_image.png"
    generated_image_path = os.path.join(app.config['UPLOAD_FOLDER'], generated_image_filename)
    generated_image.save(generated_image_path)

    # สร้าง URL สำหรับภาพที่สร้าง
    generated_image_url = url_for('uploaded_file', filename=generated_image_filename)

    # ส่งข้อมูลไปยัง HTML template
    return render_template('card_result.html', name=name, photo_url=photo_url,workplace=workplace,gmail=gmail,phone=phone,address=address , generated_image_url=generated_image_url,Line_url=Line_url  )

# ให้บริการไฟล์ในโฟลเดอร์ uploads
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
