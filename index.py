import random
import qrcode
from flask import Flask, request, render_template
from qiskit import QuantumCircuit, execute
from qiskit_aer import Aer
import io
import base64

app = Flask(__name__)

def generate_random_string(length=10):
    qrng = Aer.get_backend('qasm_simulator')
    qc = QuantumCircuit(5, 5)
    qc.h(range(5))
    qc.measure(range(5), range(5))
    job = execute(qc, qrng, shots=length)
    result = job.result().get_counts()
    random_string = max(result, key=result.get)
    return random_string

def generate_qr_code(text):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert the image to a base64 string
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return img_str

def generate_random_qr_code(text):
    random_text = generate_random_string()
    full_text = f"{text} - {random_text}"
    generate_qr_code(full_text)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr_code', methods=['POST'])
def generate_qr_code_endpoint():
    text = request.form['text']
    qr_code_img = generate_qr_code(text)
    return render_template('display_qr_code.html', qr_code_img=qr_code_img)

if __name__ == "__main__":
    app.run(debug=True)
