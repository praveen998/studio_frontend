from PIL import Image
import os
import json
import requests


def reducesize(projectpath):
    img = Image.open(projectpath)
    width, height = img.size
    img_resized = img.resize((width//2,height//2))
    img_resized.save(projectpath, quality=20, optimize=True)
    return True


def is_folder_empty(folder_path):
    # List all items in the folder
    if not os.path.exists(folder_path):
        return False  # Folder doesn't exist
    return len(os.listdir(folder_path)) == 0


#add project details into json file
def add_to_json(file_path,new_data):
    try:
        if not os.path.exists(file_path):
            # Create a new file with an empty list if it doesn't exist
            with open(file_path, 'w') as file:
                json.dump([], file)
        data=read_json(file_path)
        # Append the new data
    
        data.append(new_data)
        # Write the updated data back to the JSON file
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)  # Use indent for pretty-printing
        return True
    except Exception as e:
        return False
    

def read_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
   
        return data
    except Exception as e:
        return None
    
'''
json_path = 'static/project.json'
data=read_json(json_path)
print(len(data))
'''

#after compressed send images to backend--------------------------
def send_image_to_backend(folder_path,url):
    total_images=0
    send_images=0
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            total_images+=1
            with open(file_path, 'rb') as image_file:
                files = {'file': (filename, image_file, 'multipart/form-data')}
                response = requests.post(url, files=files)
                if response.status_code == 200:
                    total_images+=1
                    print(f'Successfully uploaded {filename}')
                else:
                    print(f'Failed to upload {filename}. Status code: {response.status_code}')
    return total_images,send_images


#return all projects names