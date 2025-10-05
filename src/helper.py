import os

def getImgSource(file:str):
    current_path = os.getcwd()

    if os.name == 'nt':
        filepath = get_windows_format(file,current_path)
        return filepath

def get_windows_format(file:str, path:str):
    modified_path = os.path.join(path,"assets",file).replace("\\","/")
    return modified_path