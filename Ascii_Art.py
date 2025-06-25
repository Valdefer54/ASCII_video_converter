import cv2
import numpy as np

char_replacement = ["o",".", "+", "*", "#",":"]#characters which will replace the color

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

def get_binary_frame(video, frame_number, target_width=None, target_height=None):
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = video.read()
    if not ret:
        return None
    if target_width and target_height:
        frame = cv2.resize(frame, (target_width, target_height))
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    binary_frame = cv2.threshold(gray_frame, 128, 255, cv2.THRESH_BINARY)[1]
    return binary_frame

def Gen_Ascii_Art(binary_frame, width, height):
    n = len(char_replacement) 
    intervals = np.linspace(0, 256, n + 1, dtype=int)#create intervals for grayscale values an replace them with characters from char_replacement
    intervals_char = list(zip(intervals[:-1], intervals[1:], char_replacement))
    asciiArt = ""
    for y in range(0, height):
        for x in range(0, width):
            pixel = binary_frame[y, x]
            # Encuentra el intervalo correspondiente
            for i in range(n):
                if intervals[i] <= pixel < intervals[i + 1]:
                    asciiArt += char_replacement[i]
                    break
        asciiArt += "\n"
    return asciiArt

def ascii_to_image(ascii_art, width, height, font_scale=0.4, font=cv2.FONT_HERSHEY_SIMPLEX):
    img = np.ones((height, width, 3), dtype=np.uint8) * 255  # Imagen blanca
    y0, dy = 20, 15  # posición inicial y salto de línea
    for i, line in enumerate(ascii_art.split('\n')):
        y = y0 + i * dy
        cv2.putText(img, line, (5, y), font, font_scale, (0, 0, 0), 1, cv2.LINE_AA)
    return img



def gen_Video(totalFrame, fps, width, height):
    small_width = width // 4
    small_height = height // 4
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('ASCIIvideo.mp4', fourcc, fps, (width, height))

    for i in range(totalFrame):
        print(f"Procesando frame {i+1}/{totalFrame}...")
        binary_frame = get_binary_frame(video, i, small_width, small_height)
        if binary_frame is None:
            print(f"Frame {i} no disponible, se omite.")
            continue
        ascii_art = Gen_Ascii_Art(binary_frame, small_width, small_height)
        img = ascii_to_image(ascii_art, width, height)
        out.write(img)
    out.release()

gen_Video(V_Tframe, Vframe, width, height)
video.release()
print("generated succesfully: ASCIIvideo.mp4")