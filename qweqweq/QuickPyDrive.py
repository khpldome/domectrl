# https://pypi.python.org/pypi/PyDrive

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
ENCRYPT = False   # False - without encription (for android!!!)
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

if ENCRYPT:
    import cryptography
    from cryptography.fernet import Fernet



# gauth = GoogleAuth()
#
# #---------------------------------------------
# # gauth.LocalWebserverAuth()
#
# # https://stackoverflow.com/questions/24419188/automating-pydrive-verification-process
# #---------------------------------------------
# # Try to load saved client credentials
# gauth.LoadCredentialsFile("mycreds.txt")
# if gauth.credentials is None:
#     # Authenticate if they're not there
#     gauth.LocalWebserverAuth()
# elif gauth.access_token_expired:
#     # Refresh them if expired
#     gauth.Refresh()
# else:
#     # Initialize the saved creds
#     gauth.Authorize()
# # Save the current credentials to a file
# gauth.SaveCredentialsFile("mycreds.txt")
# #---------------------------------------------

# drive = GoogleDrive(gauth)
#
#
# file1 = drive.CreateFile({'title': 'Hello.txt'})
# file1.SetContentString('Hello')
# file1.Upload() # Files.insert()
#
# file1['title'] = 'HelloWorld.txt'  # Change title of the file
# file1.Upload()  # Files.patch()
#
# content = file1.GetContentString()  # 'Hello'
# file1.SetContentString(content+' World!')  # 'Hello World!'
# file1.Upload()  # Files.update()

# file2 = drive.CreateFile()
# file2.SetContentFile('hello.png')
# file2.Upload()
# print('Created file %s with mimeType %s' % (file2['title'],
# file2['mimeType']))
# # Created file hello.png with mimeType image/png
#
# file3 = drive.CreateFile({'id': file2['id']})
# print('Downloading file %s from Google Drive' % file3['title']) # 'hello.png'
# file3.GetContentFile('world.png')  # Save Drive file as a local file
#
# # or download Google Docs files in an export format provided.
# # downloading a docs document as an html file:
# docsfile.GetContentFile('test.html', mimetype='text/html')


def get_gauth():

    gauth = GoogleAuth()

    # Try to load saved client credentials
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")

    return gauth


def getID_byName(file_name):

    # Auto-iterate through all files in the root folder.
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

    file_id = None
    for file in file_list:
        # print('title: %s, id: %s' % (file['title'], file['id']))
        if file['title'] == file_name:
            file_id = file['id']
            print('title: %s, id: %s' % (file['title'], file['id']))
            break

    return file_id


def getContent_byId(file_id):

    # Initialize GoogleDriveFile instance with file id.
    file = drive.CreateFile({'id': file_id})
    text = file.GetContentString()

    if ENCRYPT:
        file_content = "... can not decrypt content ..."
        try:
            decrypted_text = cipher.decrypt(text.encode(encoding='UTF-8'))  # encripted_text
            file_content = decrypted_text.decode(encoding='UTF-8')
        except cryptography.fernet.InvalidToken:
            pass
    else:
        file_content = text

    return file_content


def putContent_byId(file_id, content, file_name=""):

    if file_name == "":
        file = drive.CreateFile({'id': file_id})
    else:
        file = drive.CreateFile({'title': file_name})

    if ENCRYPT:
        bytes_text = content.encode(encoding='UTF-8')  #b'My super secret message'
        text = cipher.encrypt(bytes_text).decode(encoding='UTF-8')  # encrypted_text
        # print(text)
    else:
        text = content

    file.SetContentString(text)
    file.Upload()

    return


if ENCRYPT:
    # cipher_key = Fernet.generate_key()
    cipher_key = b'u6I08Z2C38-4Hr4M5TRksehNLhbTPUwE55KSTz0EJHs='
    print('cipher_key=', cipher_key)
    cipher = Fernet(cipher_key)

gauth = get_gauth()
drive = GoogleDrive(gauth)
print('ENCRYPT=', ENCRYPT, 'gauth=', gauth.DEFAULT_SETTINGS)

if ENCRYPT:
    FILE_NAME = 'MyData_enc.txt'  # file name on Google Drive
else:
    FILE_NAME = 'MyData.txt'  # file name on Google Drive

file_id = getID_byName(FILE_NAME)


if __name__ == "__main__":

    import json

    json_init_data = {
        "name": "John",
        "age": 30,
        "cars": [
            {"name": "Ford", "models": ["Fiesta", "Focus", "Mustang"]},
            {"name": "BMW", "models": ["320", "X3", "X5"]},
            {"name": "Fiat", "models": ["500", "Panda"]}
        ]
    }
    str_data = json.dumps(json_init_data, indent=4, sort_keys=True)

    if file_id is None:

        putContent_byId(file_id=None, content=str_data, file_name=FILE_NAME)
    else:
        # content = getContent_byId(file_id=file_id)
        # print(content)
        putContent_byId(file_id=file_id, content='{"a": 12, "b": 13}')










