# -*- coding: utf-8 -*-


# windows hostname
import socket

HOSTNAME = socket.gethostname()
print(HOSTNAME)

# Load defaults ---------------------------------------------------------------
SERVER_NAME = HOSTNAME
VIDEO_CARD_NAME = 'Empty'
PROJECTOR_AMOUNT = 1
ABSPATH_DISPLAYPRO = 'c:\Program Files (x86)\Immersive Display PRO\ImmersiveDisplayPro.bat'
RELPATH_VLC = r'\exec\vlc-2.1.6\vlc.bat'
ALLOWED_IP = '127.0.0.1'

# #############################################################################
# ######################## Custom settings ####################################
# #############################################################################
if HOSTNAME == 'fds-Kharkiv':
    SERVER_NAME = HOSTNAME
    VIDEO_CARD_NAME = 'NVS 810'
    PROJECTOR_AMOUNT = 8
    ABSPATH_DISPLAYPRO = 'c:\Program Files (x86)\Immersive Display PRO\ImmersiveDisplayPro.bat'
    RELPATH_VLC = r'\exec\vlc-2.1.6\vlc.bat'
    ALLOWED_IP = '192.168.10.10'

elif HOSTNAME == 'fds-Kyiv':
    SERVER_NAME = HOSTNAME
    VIDEO_CARD_NAME = 'GTX 1070'
    PROJECTOR_AMOUNT = 12
    ABSPATH_DISPLAYPRO = 'c:\Program Files (x86)\Immersive Display PRO\ImmersiveDisplayPro.bat'
    RELPATH_VLC = r'\exec\vlc-2.1.6\vlc.bat'
    ALLOWED_IP = '192.168.1.11'
# -----------------------------------------------------------------------------
