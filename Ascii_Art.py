import cv2

char_replacement = {"o",".", "+", "*", "#",":"}#characters which will replace the color

video = cv2.VideoCapture('CURREN.mp4')
if not video.isOpened():
    print("video no disponible")
    quit()
else:
    Vframe = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    V_Tframe =int(video.get(cv2.CAP_PROP_FRAME_COUNT)) #total number of frames in the video
    V_Tseconds = V_Tframe / Vframe

def Gen_Video(frames, width, height)
    
