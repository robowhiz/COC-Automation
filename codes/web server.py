import os
import cv2
import sys
import time
import pyautogui
import numpy as np
from PIL import ImageGrab
from flask import Flask, request, send_file, Response, render_template

program_status = True
current_program_number = 0 #returns what is happening in code
current_program = ["opening clash of clans",
                   "waiting for home page",
                   "collecting resources",
                   "removing obstacles",
                   "assingning builders",
                   "starting research",
                   "attacking multiplayer base : 1",
                   "attacking multiplayer base : 2",
                   "traning army",
                   "closing clash of clans",
                   "waiting for next loop"]
recording = True
time_out = False

def web_server():
    app = Flask(__name__)

    def html(body):
        html = \
    "<!DOCTYPE html>\n\
    <html>\n\
        <head>\n\
            <title>contents</title>\n\
        </head>\n\
        <body>\n\
            " + body + "\n\
        </body>\n\
    </html>\n"
        return html

    @app.route('/status')
    def get_status():
        global program_status
        return str(program_status)

    @app.route('/timeout')
    def time_out():
        global time_out
        return str(time_out)

    @app.route('/currentprogram')
    def get_current_program():
        global current_program, current_program_number
        return current_program[current_program_number]

    @app.route('/stop')
    def stop_program():
        global program_status
        program_status = False
        return "Program will stop at the next loop"

    @app.route('/start')
    def start_program():
        global program_status
        program_status = True
        return "Program will start at the next loop"

    @app.route('/restart')
    def restart():
        os.system(f"taskkill /PID {os.getpid()} /F & {sys.executable} \"{sys.argv[0]}\"")
    
    @app.route('/closebluestack')
    def closebluestack():
        pyautogui.hotkey("alt", "f4")
        time.sleep(1)
        pyautogui.click(x=1100, y=590)
        return "bluestack closed"
    
    @app.route('/stopall')
    def stop_all():
        pyautogui.hotkey("alt", "f4")
        time.sleep(1)
        pyautogui.click(x=1100, y=590)
        os._exit(1)
    
    @app.route('/')
    def stream():
        return render_template('web server/index.html')
    
    @app.route('/video_feed')
    def video_feed():
        def generate_frames():
            next = 0
            while True:
                if time.time() > next:
                    next = time.time() + 0.1
                    frame = ImageGrab.grab()
                    frame = np.array(frame)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    x, y = pyautogui.position()
                    cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)
                    frame = cv2.resize(frame, (960, 540))
                    ret = True
                    ret, buffer = cv2.imencode('.jpg', frame)

                    frame_bytes = buffer.tobytes()
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')  
    
    @app.route('/upload', methods=['POST'])
    def upload():
        file = request.files['file']
        file.save(file.filename)
        return f"{file.filename} upoladed"
    
    @app.route('/click')
    def click():
        x = int(request.args.get('x')) * 2
        y = int(request.args.get('y')) * 2
        pyautogui.click(x = x, y = y)
        return '', 200

    @app.route('/file')
    def file():
        body = ""
        for dir_content in os.listdir():
                body += f"<a href=\"file/{dir_content}\">{dir_content}</a><br>\n"
        return html(body)

    @app.route('/file/<path:link>')
    def display_content(link):
        body = ""
        if  link.find(".ico") > 0:
            return open("templates\\web server\\favicon.ico", "rb")
        
        elif link.find(".mp4") > 0 or link.find(".png") > 0 or link.find(".css") > 0:
            return send_file(link, as_attachment=True)
        
        elif link.find('.') > 0:
            return open(link.replace('/', '\\')).read(), {"Content-Type": "text/plain"}
        
        else:
            path = link.replace('/', '\\')
            for dir_content in os.listdir(path):
                body += f"<a href=\"{link[link.rfind('/') + 1:]}/{dir_content}\">{dir_content}</a><br>\n"

        return html(body)

    if __name__ == '__main__':
        app.run(host = '0.0.0.0', port = 8000)