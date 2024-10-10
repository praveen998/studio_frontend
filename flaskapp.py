from flask import Flask, render_template,jsonify,request,redirect
import os 
import sys
import json
from imgconv import add_to_json,read_json,send_image_to_backend,reducesize
import webview
import threading

app = Flask(__name__)

if hasattr(sys, '_MEIPASS'):
    # If running in a PyInstaller bundle, change template_folder and static_folder paths
    app = Flask(__name__, 
                template_folder=os.path.join(sys._MEIPASS, 'templates'),
                static_folder=os.path.join(sys._MEIPASS, 'static'))

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS 
else:
    base_path = os.path.dirname(os.path.abspath(__file__))


#app.template_folder = os.path.join(base_path, 'templates')
#app.static_folder = os.path.join(base_path, 'static')
selected_project=''
json_path =os.path.join(base_path,'project.json')
auth_json_path =os.path.join(base_path,'auth.json')
current_project=''
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/show_projects')
def show_projects():
    return render_template('index.html')


@app.route('/upload',methods=['POST'])
def upload():
    global current_project
    current_project=os.path.join(os.getcwd(), selected_project)
    if 'files' not in request.files:
        return redirect(request.url)
    files = request.files.getlist('files')
    for file in files:
        if file.filename == '' or not allowed_file(file.filename):
            continue
        filename = file.filename
        imagepath=os.path.join(current_project, filename)
        file.save(os.path.join(current_project, filename))
        status=reducesize(imagepath)
        print(status)
    return "success", 200


#create new folder in localmachine and save details into json file ----------------------------------------
@app.route('/create_project', methods=['POST'])
def create_project():
    print('project created project name:',request.form['project_name'])
    project_name = request.form['project_name']
    if project_name:
        print(project_name)
        data=read_json(os.path.join(os.getcwd(),'project.json'))
        print(data)
        projects=[data[i]['project_name'] for i in range(len(data))]
        if project_name not in projects:
            print('project not in list')
            BASE_DIR = os.getcwd()
            project_path = os.path.join(BASE_DIR, project_name)
            print(project_path)
            try:
                os.makedirs(project_path, exist_ok=False) 
                data=read_json(os.path.join(os.getcwd(),'project.json'))
                if len(data)==0:
                    id =1
                else:
                    id=int(data[(len(data)-1)]['project_id'])
                    id+=1
                new_data = {'project_id':f'{id}','project_name': f'{project_name}', 'date_created': '2024-10-04','project_path':f'{project_path}'}
                #add project details into json ----------
                if add_to_json(os.path.join(os.getcwd(),'project.json'),new_data):
                    return jsonify({
                        "success": True,
                        "message": f'Project "{project_name}" created successfully!'
                    }), 200  # Created
                else:
                    return jsonify({
                    "success": False,
                    "message": "Error occure while add json data!."
                    }), 400  # Bad Request
            except FileExistsError:
                    return jsonify({
                    "success": False,
                    "message": "Project already exists!"
                    }), 400  # Bad Request
        else:
              return jsonify({
                    "success": False,
                    "message": "Project already exists!"
                    }), 400  
    else:
        return jsonify({
        "success": False,
        "message": "Project name is required."
    }), 400  



#set project name path for uploading images
@app.route('/select_project',methods=['POST'])
def select_project():
    global current_project
    BASE_DIR = os.getcwd()
    current_project = request.form['project_name']
    current_project=os.path.join(BASE_DIR,current_project)
    print(current_project)
    return 'success',200



@app.route('/project_names')
def project_names():
    global json_path
    print('project name called')
    data=read_json(json_path)
    projects=[data[i]['project_name'] for i in range(len(data))]
    print(projects)
    return jsonify(projects)
    

@app.route('/project_page',methods=['POST'])
def project_page():
    global selected_project
    project_name=request.form.get('project_name') 
    selected_project=project_name
    if project_name:
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False}), 400


@app.route('/project_page_render')
def project_page_render():
    global selected_project
    print(selected_project)
    return render_template('project_page.html')


'''
@app.route('/login')
def login():
    jdata=read_json(os.path.join(os.getcwd(), 'auth.json'))
    if len(jdata)!=0:
        return render_template('index.html')
    else:
        return render_template('login.html')
'''

'''
@app.route('/login_auth',methods=['POST'])
def login_auth():
    u="praveen"
    p="12345"
    jdata=read_json(os.path.join(os.getcwd(), 'auth.json'))
    data = request.get_json()
    print(jdata)
    print(data['username'])
    print(data['password'])
    if data:
        if u==str(data['username']) and p==str(data['password']):
            with open(auth_json_path, 'w') as json_file:
                json.dump([], json_file)
            add_to_json(os.path.join(os.getcwd(), 'auth.json'),{"username":data['username'],"password":data['password']})
            return jsonify({"success": True}), 200
        else:
            return jsonify({"success": False}), 400
    else:
        return jsonify({"success": False}), 400
'''


@app.route('/check_images_uploaded')
def check_images_uploaded():
    global selected_project
    if len(os.listdir( os.path.join( os.getcwd(),selected_project))) == 0:
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False}), 400


def run_flask():
    """Run the Flask app."""
    app.run(port=5000, debug=True, use_reloader=False)

def start_webview():
    webview.create_window('studiowebview','http://127.0.0.1:5000')
    webview.start()

    os._exit(0)


def checkfile_exist():
    if not os.path.exists(os.path.join(os.getcwd(),'auth.json')) and not os.path.exists(os.path.join(os.getcwd(),'project.json')):
        default_data = []
        with open(os.path.join(os.getcwd(),'auth.json'), 'w') as json_file:
            json.dump(default_data, json_file, indent=4)
        with open(os.path.join(os.getcwd(),'project.json'), 'w') as json_file:
            json.dump(default_data, json_file, indent=4)
checkfile_exist()


if __name__ == '__main__':
    # Start the Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Start the webview window and wait for it to close
    start_webview()
