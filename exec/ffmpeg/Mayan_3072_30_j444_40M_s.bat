
ffmpeg ^
-framerate 30 ^
-i "Mayan Archaeoastronomy\MAA-show\JPG SEQ\pic_%%05d.jpg" ^
-s 3072x3072 ^
-pix_fmt yuvj444p ^
-y ^
-vcodec libx264 ^
-b:v 40M -minrate 40M -maxrate 40M -bufsize 80M ^
"Mayan_Archaeoastronomy_3072_40M.mp4"


ffmpeg ^
-i "Mayan_Archaeoastronomy_3072_40M.mp4" ^
-i "Mayan Archaeoastronomy\MAA-show\JPG SEQ\sound.wav" ^
-vcodec copy -acodec ac3 ^
-shortest -y ^
"Mayan_Archaeoastronomy_3072_ac3_40M.mp4"

Pause

::-start_number 300 -vframes 500 ^
