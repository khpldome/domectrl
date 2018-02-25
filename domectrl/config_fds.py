# -*- coding: utf-8 -*-


# windows hostname
import socket

HOSTNAME = socket.gethostname()
print(HOSTNAME)

# Load defaults ---------------------------------------------------------------
SERVER_NAME = HOSTNAME
VIDEO_CARD_NAME = 'Empty'
PROJECTOR_AMOUNT = 1
# DISPLAYPRO_ABSPATH = 'c:\Program Files (x86)\ImmersiveDisplayPRO\ImmersiveDisplayPRO.exe'
DISPLAYPRO_ABSPATH = 'c:\Program Files (x86)\Immersive Display PRO\ImmersiveDisplayPro.bat'

VLC_EXE_RELPATH = r'\exec\vlc-2.1.6\vlc.exe'
VLC_BAT_RELPATH = r'\exec\vlc-2.1.6\vlc.bat'
VLC_BLACK = r'\exec\vlc-2.1.6\Black.jpg'
HOST_IP = '127.0.0.1'
VLC_WEB_DOMAIN = ':63933@127.0.0.1:8080'
POJECTORS_NUMS = 8

# #############################################################################
# ######################## Custom settings ####################################
# #############################################################################
if HOSTNAME == 'fds-Kharkiv':
    SERVER_NAME = HOSTNAME
    VIDEO_CARD_NAME = 'NVS 810'
    PROJECTOR_AMOUNT = 8
    # DISPLAYPRO_ABSPATH = r'c:\Program Files (x86)\ImmersiveDisplayPRO\ImmersiveDisplayPRO.exe'
    VLC_EXE_RELPATH = r'\exec\vlc-2.1.6\vlc.exe'
    HOST_IP = '192.168.10.10'
    POJECTORS_NUMS = 8

elif HOSTNAME == 'fds-Kyiv':
    SERVER_NAME = HOSTNAME
    VIDEO_CARD_NAME = 'GTX 1070'
    PROJECTOR_AMOUNT = 12
    # DISPLAYPRO_ABSPATH = r'c:\Program Files (x86)\ImmersiveDisplayPRO\ImmersiveDisplayPRO.exe'
    VLC_EXE_RELPATH = r'\exec\vlc-2.1.6\vlc.exe'
    HOST_IP = '192.168.1.128'
    POJECTORS_NUMS = 12
# -----------------------------------------------------------------------------
