import requests
from pathlib import Path


if not Path("pixart_helper.py").exists():
    r = requests.get(url="https://raw.githubusercontent.com/openvinotoolkit/openvino_notebooks/latest/notebooks/pixart/pixart_helper.py")
    open("pixart_helper.py", "w").write(r.text)

if not Path("pixart_quantization_helper.py").exists():
    r = requests.get(url="https://raw.githubusercontent.com/openvinotoolkit/openvino_notebooks/latest/notebooks/pixart/pixart_quantization_helper.py")
    open("pixart_quantization_helper.py", "w").write(r.text)

import torch
from diffusers import PixArtAlphaPipeline

# โหลดโมเดล
pipe = PixArtAlphaPipeline.from_pretrained("PixArt-alpha/PixArt-LCM-XL-2-1024-MS", use_safetensors=True)

# กำหนดข้อความ และขนาดของภาพ
prompt = "mouse"
generator = torch.Generator().manual_seed(42)

# กำหนดขนาดภาพสี่เหลี่ยมผืนผ้า (เช่น 1024x512 พิกเซล)
width = 1024
height = 512

# สร้างภาพ
image = pipe(prompt, guidance_scale=0.0, num_inference_steps=4, generator=generator, height=height, width=width).images[0]

# บันทึกภาพ
image.save("output_rectangle_image.png")
print("บันทึกภาพเรียบร้อย!")
