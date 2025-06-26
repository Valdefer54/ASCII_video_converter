# ASCII Video Converter

This project converts a video into a colored ASCII art video using Python and OpenCV. Each frame of the input video is transformed into ASCII characters, colored according to the original frame, and then reassembled into a new video.

## Features

- Converts any video to a colored ASCII art video.
- Customizable ASCII character set.
- Adjustable output resolution.
- Efficient frame processing using NumPy and OpenCV.

## Requirements

- Python 3.7+
- OpenCV (`opencv-python`)
- NumPy

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/ASCII_video_converter.git
    cd ASCII_video_converter
    ```

2. Install dependencies:
    ```bash
    pip install opencv-python numpy
    ```

## Usage

1. Place your input video in the project directory and rename it to `CURREN.mp4` (or change the filename in the script).

2. Run the script:
    ```bash
    python Ascii_Art.py
    ```

3. The output video will be saved as `ASCIIvideo_color.mp4` in the same directory.

## How It Works

- The script reads each frame of the input video.
- Each frame is resized and converted to grayscale.
- Grayscale values are mapped to ASCII characters based on intensity.
- The ASCII characters are colored using the original frame's color information.
- The colored ASCII frames are combined into a new video.

## Customization

- **ASCII Characters:**  
  Edit the `char_replacement` list in `Ascii_Art.py` to use different characters.

- **Resolution:**  
  Adjust the `small_width` and `small_height` variables in the `gen_Video_color_ascii` function for higher or lower output resolution.

## License

This project is licensed under the MIT License.

---

**Author:**  
Fernando Zapata Valderrama
