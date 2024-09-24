from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
import os
from werkzeug.utils import secure_filename
from yolo_integration import YOLOIntegration

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'mp4'}

yolo = YOLOIntegration("yolov8n.pt")  # Use a pre-trained model or your custom trained model

# In-memory storage for products (replace with database in production)
products = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/add_product', methods=['POST'])
def add_product():
    product_name = request.form.get('product_name')
    if product_name and product_name not in products:
        products[product_name] = []
        return jsonify({"success": True, "message": f"Product '{product_name}' added successfully"})
    return jsonify({"success": False, "message": "Invalid product name or product already exists"})

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files or 'product_name' not in request.form:
        return jsonify({"success": False, "message": "No file part or product name"})

    file = request.files['file']
    product_name = request.form['product_name']

    if file.filename == '' or product_name not in products:
        return jsonify({"success": False, "message": "No selected file or invalid product"})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], product_name, filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)
        products[product_name].append(filename)
        return jsonify({"success": True, "message": "Image uploaded successfully"})

    return jsonify({"success": False, "message": "Invalid file type"})

@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file part"})

    file = request.files['file']

    if file.filename == '':
        return jsonify({"success": False, "message": "No selected file"})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(video_path)

        output_filename = f"processed_{filename}"
        output_path = os.path.join(app.config['PROCESSED_FOLDER'], output_filename)

        inventory_changes = yolo.process_video(video_path, output_path)
        updated_inventory = yolo.update_inventory(inventory_changes)

        return render_template('results.html', inventory=updated_inventory, video_filename=output_filename)

    return jsonify({"success": False, "message": "Invalid file type"})

@app.route('/processed_video/<filename>')
def processed_video(filename):
    return send_file(os.path.join(app.config['PROCESSED_FOLDER'], filename), mimetype='video/mp4')

@app.route('/get_products')
def get_products():
    return jsonify(products)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)
    app.run(debug=True, port=5001)
