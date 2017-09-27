# https://pypi.python.org/pypi/PyDrive

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

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


def getContent_byId(file_id, cipher):

    # Initialize GoogleDriveFile instance with file id.
    file = drive.CreateFile({'id': file_id})
    file_content = file.GetContentString()
    encrypted_text = file_content
    decrypted_text = cipher.decrypt(encrypted_text.encode(encoding='UTF-8'))
    file_content = decrypted_text.decode(encoding='UTF-8')

    return file_content


def putContent_byId(file_id, cipher, content, file_name=""):

    if file_name != "":
        file = drive.CreateFile({'title': file_name})
    else:
        file = drive.CreateFile({'id': file_id})

    bytes_text = content.encode(encoding='UTF-8')  #b'My super secret message'
    encrypted_text = cipher.encrypt(bytes_text)
    print(encrypted_text)

    file.SetContentString(encrypted_text.decode(encoding='UTF-8'))
    file.Upload()

    return


if __name__ == "__main__":

    FILE_NAME = 'MyData.txt'  # file name on google grive

    # cipher_key = Fernet.generate_key()
    cipher_key = b'u6I08Z2C38-4Hr4M5TRksehNLhbTPUwE55KSTz0EJHs='
    print('cipher_key=', cipher_key)
    cipher = Fernet(cipher_key)

    gauth = get_gauth()
    drive = GoogleDrive(gauth)

    file_id = getID_byName(FILE_NAME)

    if file_id is None:

        putContent_byId(file_id=None, cipher=cipher, content="empty file!", file_name=FILE_NAME)
    else:
        content = getContent_byId(file_id=file_id, cipher=cipher)
        print(content)
        # putContent_byId(file_id, cipher, "asdfdfsd")











