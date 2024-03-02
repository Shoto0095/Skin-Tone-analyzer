import cv2
from PIL import Image
from colorthief import ColorThief
import matplotlib.pyplot as plt

def capture_photo(camera_index=0, photo_filename="captured_photo.jpg"):
    # Open the camera
    cap = cv2.VideoCapture(camera_index)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Wait for the user to press the "Space" key to capture a photo
    print("Press the 'Space' key to capture a photo...")
    while True:
        ret, frame = cap.read()
        cv2.imshow("Capture Photo", frame)

        # Wait for the user to press a key
        key = cv2.waitKey(1) & 0xFF
        if key == 32:  # "Space" key
            cv2.imwrite(photo_filename, frame)
            break

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()

def crop_photo(image_path, crop_filename="cropped_photo.jpg"):
    # Load the captured photo
    img = cv2.imread(image_path)

    # Select ROI using cv2.selectROI
    roi = cv2.selectROI(img)

    # Crop image
    cropped_img = img[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]

    # Save the cropped photo
    cv2.imwrite(crop_filename, cropped_img)

    # Display the cropped image
    cv2.imshow("Cropped Image", cropped_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def analyze_skin_tone(image_path):
    # Create a ColorThief object
    color_thief = ColorThief(image_path)

    # Get the dominant color
    dominant_color = color_thief.get_color(quality=1)  # Increase quality for more accurate results

    # Display the original image and the color swatch in the same dialog
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    # Original image
    img = Image.open(image_path)
    ax1.imshow(img)
    ax1.set_title("Original Image")
    ax1.axis("off")

    # Dominant color swatch
    color_swatch = [[dominant_color]]
    ax2.imshow(color_swatch)
    ax2.set_title(f"Skin Tone is: {dominant_color}")
    ax2.axis("off")

    plt.show()

if __name__ == "__main__":
    # Capture a photo from the camera
    capture_photo()

    # Crop the captured photo
    crop_photo("captured_photo.jpg")

    # Analyze the skin tone of the cropped photo
    analyze_skin_tone("cropped_photo.jpg")
