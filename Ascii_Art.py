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

def get_frame(video, frame_number, target_width=None, target_height=None):
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = video.read()
    if not ret:
        return None
    if target_width and target_height:
        frame = cv2.resize(frame, (target_width, target_height))
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return frame, gray_frame

def gen_ascii_matrix(gray_frame):
    n = len(char_replacement)
    intervals = np.linspace(0, 256, n + 1, dtype=int)
    height, width = gray_frame.shape
    ascii_matrix = []

   # Crear intervalos como array para usar searchsorted
    intervals_array = np.array(intervals)

    # Usar searchsorted para encontrar los índices de forma vectorizada
    indices = np.searchsorted(intervals_array[1:], gray_frame.flatten(), side='right')
    indices = np.clip(indices, 0, len(char_replacement) - 1)

    # Mapear índices a caracteres
    char_array = np.array(char_replacement)
    ascii_chars = char_array[indices]

    # Reshape para obtener la matriz
    ascii_matrix = ascii_chars.reshape(height, width).tolist()
    return ascii_matrix

def ascii_to_colored_image(ascii_matrix, color_frame, output_width, output_height, font_scale=0.4, font=cv2.FONT_HERSHEY_SIMPLEX):
    img = np.ones((output_height, output_width, 3), dtype=np.uint8) * 255  # fondo blanco
    cell_height = 15
    cell_width = 10
    # Crear arrays de coordenadas
    y_indices, x_indices = np.mgrid[0:len(ascii_matrix), 0:len(ascii_matrix[0])]
    pos_x = x_indices * cell_width
    pos_y = (y_indices + 1) * cell_height

    # Aplanar para iterar más eficientemente
    flat_chars = np.array(ascii_matrix).flatten()
    flat_colors = color_frame.reshape(-1, 3).astype(int)
    flat_pos_x = pos_x.flatten()
    flat_pos_y = pos_y.flatten()

    # Un solo bucle en lugar de anidado
    for i in range(len(flat_chars)):
        cv2.putText(img, flat_chars[i], (flat_pos_x[i], flat_pos_y[i]), 
                    font, font_scale, tuple(map(int, flat_colors[i])), 1, cv2.LINE_AA)
    return img

def gen_Video_color_ascii(totalFrame, fps, width, height):
    small_width = width // 10 #less res can make the video clearly, it depends of the video
    small_height = height // 10
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('ASCIIvideo_color.mp4', fourcc, fps, (width, height))

    for i in range(totalFrame):
        print(f"processing frame {i+1}/{totalFrame}...")
        result = get_frame(video, i, small_width, small_height)
        if result is None:
            print(f"Frame {i} not available, skipped")
            continue
        frame_color, frame_gray = result
        ascii_matrix = gen_ascii_matrix(frame_gray)
        img = ascii_to_colored_image(ascii_matrix, frame_color, width, height)
        out.write(img)
    out.release()


gen_Video_color_ascii(V_Tframe, Vframe, width, height)
video.release()
print("generated successfully: ASCIIvideo_color.mp4")
