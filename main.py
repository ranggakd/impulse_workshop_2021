from flask import Flask, render_template
from flask import request, redirect, flash
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from urllib.parse import urlencode
from urllib import parse
from PIL import Image
from io import BytesIO
import numpy as np
import base64

app = Flask(__name__)

cloud_classes = ['Badai', 'Berawan', 'Cerah', 'Hujan', 'Hujan Badai']
crack_classes = ['Tidak Retak', 'Retak']

@app.route('/')
@app.route('/main')
def landing_page():
    return render_template('main.html')

@app.route('/service1', methods=['POST'])
def get_result_cloud_API():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("Tidak ada file")
            return redirect("/")
        files = request.files['file']
        if files.filename == "":
            flash("Tidak ada gambar yang dipilih")
            return redirect("/")
        else:
            model = load_model('model/cloud.h5')
            read_file = files.read()
            im = Image.open(BytesIO(read_file))
            im = im.resize(size=(224,224))
            img = image.img_to_array(im, data_format="channels_last", 
                                    dtype="float16")
            img = img / 255.
            img = img.astype('float16') 
            img = img.reshape((-1,224,224,3))
            prediction = model.predict(img)
            result = np.argmax(prediction, axis=-1)
            label_class = cloud_classes[result[0]]
            proba_class = round(prediction.tolist()[0][result[0]] * 100, 4)
            b64_img = base64.b64encode(read_file)
            params = {label_class:proba_class, "image":b64_img}
            url_params = urlencode(params)
            return redirect(f"/result/{url_params}")

@app.route('/service2', methods=['POST'])
def get_result_crack_API():
    if request.method == 'POST':
            if 'file' not in request.files:
                flash("Tidak ada file")
                return redirect("/")
            files = request.files['file']
            if files.filename == "":
                flash("Tidak ada gambar yang dipilih")
                return redirect("/")
            else:
                model = load_model('model/crack.h5')
                read_file = files.read()
                im = Image.open(BytesIO(read_file))
                im = im.resize(size=(224,224))
                img = image.img_to_array(im, data_format="channels_last", 
                                        dtype="float16")
                img = img / 255.
                img = img.astype('float16') 
                img = img.reshape((-1,224,224,3))
                prediction = model.predict(img)
                result = np.argmax(prediction, axis=-1)
                label_class = crack_classes[result[0]]
                proba_class = round(prediction.tolist()[0][result[0]] * 100, 4)
                b64_img = base64.b64encode(read_file)
                params = {label_class:proba_class, "image":b64_img}
                url_params = urlencode(params)
                return redirect(f"/result/{url_params}")

@app.route('/result/<path:params>')
def result(params):
    result_dict = dict(parse.parse_qsl(parse.urlsplit(params).path))
    result_dict['image'] = result_dict['image'].replace(" ","+")
    return render_template('result.html', result_dict=result_dict)

if __name__ == '__main__':
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.run(debug=True)