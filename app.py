import subprocess
from flask import Flask, request
from PIL import Image
import io
from flask_restx import Api,Resource
import os
from flask_cors import CORS


def model():
    command = "lpstat -a"
    process = subprocess.Popen(command, shell=True, executable="/bin/bash", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()   
    process.wait()
     
    output = output.decode('utf-8')
    error = error.decode('utf-8')
    if error:
        return error
    return output.split()[0]

def auto_orient(image):
    try:
        exif = image._getexif()
        if exif:
            orientation_tag = 274  # EXIF-тег ориентации
            if orientation_tag in exif:
                orientation = exif[orientation_tag]
                if orientation == 3:
                    image = image.rotate(180, expand=True)
                elif orientation == 6:
                    image = image.rotate(270, expand=True)
                elif orientation == 8:
                    image = image.rotate(90, expand=True)
    except Exception:
        pass  # Если EXIF нет, просто игнорируем
    return image
def startconfig():
    command = "lpstat -p"
    process = subprocess.Popen(command, shell=True, executable="/bin/bash", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()   
    process.wait()
     
    output = output.decode('utf-8')
    error = error.decode('utf-8')
    if error:
        return error
    return output 
def execute(command):
    process =subprocess.Popen(command, shell = True, executable="/bin/bash")
    process.wait()
    output, error = process.communicate()
    return output 
def check_file_type(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".docx":
        return "DOCX"
    elif ext == ".doc":
        return "DOC"
    elif ext == ".jpg" or ext == ".jpeg":
        return "JPG"
    elif ext == ".bmp":
        return "BMP"
    elif ext == ".png":
        return "PNG"
    elif ext == ".pdf":
        return "PDF"
    else:
        return "Unknown"
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)
ns = api.namespace('api', description='Печать документов')

@ns.route('/print')
class printDoc(Resource):
    @ns.doc('doc_print')
    @ns.response(200, 'Успешная печать')
    @ns.response(400, 'Некорректные данные')
    @ns.expect(ns.parser().add_argument('file', location='files', type='file', required=False))
    def post(self):
        if 'file' not in request.files:
            return {"error": "Отсутствует файл"}, 400
        file = request.files['file']
        if file.filename == '':
            return {"error": "Файл не выбран"}, 400
 
        try:
            if check_file_type(file.filename) in ["JPG","PNG","BMP"]:
                image = Image.open(file)
                image = image.convert("RGB") 
                
                image = auto_orient(image)
                img_width, img_height = image.size
                a4_width, a4_height = 2480, 3508
                img_ratio = img_width / img_height
                a4_ratio = a4_width / a4_height
                # Обрезка изображения, сохраняя соотношение сторон A4
                if img_ratio > a4_ratio:
                    new_width = int(img_height * a4_ratio)
                    offset = (img_width - new_width) // 2
                    image = image.crop((offset, 0, offset + new_width, img_height))
                else:
                    new_height = int(img_width / a4_ratio)
                    offset = (img_height - new_height) // 2
                    image = image.crop((0, offset, img_width, offset + new_height))
                # Изменение размера до A4 (300 DPI)
                image = image.resize((a4_width, a4_height), Image.LANCZOS)
                image.save(file.filename)
                name=file.filename.replace(" ", "\\ ")
                execute( f"""lp -d SCX-3200-Series ./{name}""")
                execute( f"""rm -f ./{name}""")
                answ = {"msg": "Файл является изображнием! Печать начинается", "type": check_file_type(file.filename)  }
            elif check_file_type(file.filename) in ["DOC","DOCX"]:
                answ = {"msg": "Файл является документом! Печать начинается", "type": check_file_type(file.filename)  }
                file.save(file.filename)
                name=file.filename.replace(" ", "\\ ")
                name2=os.path.splitext(file.filename)[0].replace(" ", "\\ ")
                execute(f"""libreoffice --headless --convert-to pdf ./{name}""")
                execute( f"""rm -f ./{name}""")
                execute( f"""lp -d SCX-3200-Series ./{name2}.pdf""")
                execute( f"""rm -f ./{name2}.pdf""")
            elif check_file_type(file.filename) in ["PDF"]:
                answ = {"msg": "Файл является документом! Печать начинается", "type": check_file_type(file.filename)  }
                file.save(file.filename)
                name=file.filename.replace(" ", "\\ ")
                execute( f"""lp -d SCX-3200-Series ./{name}""")
                execute( f"""rm -f ./{name}""")
            else:
                print(check_file_type(file.filename))
                answ = {"msg": "Документ неизвестного формата!", "type": check_file_type(file.filename)  }
                return answ, 500
            return answ
        except Exception as e:
            print(str(e))
            return {"error": str(e)}, 500
@ns.route('/status')
class status(Resource):
    @ns.doc('status')
    @ns.response(200, 'Успешно')
    @ns.response(400, 'Некорректные данные')
    def get(self):
        ch=startconfig()
        try:
            print(ch)
            if "idle" in ch:
                print(F"Принтер {model()} запущен!")
                answ = {"msg": f"Принтер {model()} запущен и готов к работе!"}
                return answ
            else:
                answ = {"msg": "Ошибка проверки статуса","return": ch}
                return answ, 500
        except Exception as e:
            return {"error": str(e)}, 500
if __name__ == '__main__':
    ns.add_resource(printDoc, '/print')
    ns.add_resource(status, '/status')
    startconfig()
    app.run(debug=False, host='0.0.0.0', port=5230, threaded=True)

