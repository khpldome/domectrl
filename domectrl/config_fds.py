# -*- coding: utf-8 -*-


# windows hostname
import socket

HOSTNAME = socket.gethostname()
print(HOSTNAME)

# Load defaults ---------------------------------------------------------------
VIDEO_CARD_NAME = 'Empty'
PROJECTOR_AMOUNT = 1


# #############################################################################
# ######################## Custom settings ####################################
# #############################################################################
if HOSTNAME == 'fds-Kharkiv':
    VIDEO_CARD_NAME = 'NVS 810'
    PROJECTOR_AMOUNT = 8


elif HOSTNAME == 'fds-Kyiv':
    VIDEO_CARD_NAME = 'GTX 1070'
    PROJECTOR_AMOUNT = 12

# -----------------------------------------------------------------------------
