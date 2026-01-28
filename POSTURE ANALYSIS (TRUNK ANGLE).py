import cv2
import numpy as np
import mediapipe as mp
import math

# ==============================
# 1. USER SETTINGS
# ==============================
# >>>>>>> PUT YOUR INPUT IMAGE PATH HERE <<<<<<<
IMAGE_PATH = r"C:\Users\ACER\PycharmProjects\PythonProject-Mintech_Robotics\Descend-26-9kg-Foot Placement.png"  # e.g. r"C:\Users\You\Pictures\staircase_26deg.png"

# Choose whether to use RIGHT side or LEFT side for trunk angle
USE_RIGHT_SIDE = True  # True = right shoulder/hip, False = left shoulder/hip

# ==============================
# 2. MEDIAPIPE INITIALIZATION
# ==============================
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

pose = mp_pose.Pose(
    static_image_mode=True,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.5
)

# ==============================
# 3. HELPER FUNCTIONS
# ==============================
def angle_from_vertical(p1, p2):
    """
    Compute the angle (in degrees) of the segment p1->p2 with respect to the vertical.
    p1, p2: (x, y) in image coordinates.
    Angle = 0° means perfectly vertical, increasing as it leans.
    """
    x1, y1 = p1
    x2, y2 = p2

    # Vector from hip to shoulder (for example)
    dx = x2 - x1
    dy = y2 - y1

    # Angle w.r.t horizontal:
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)

    # Angle from vertical = 90 - |angle w.r.t horizontal|
    angle_from_vert = 90.0 - abs(angle_deg)
    return angle_from_vert, angle_deg


def get_landmark_xy(landmarks, index, image_width, image_height):
    """
    Convert normalized landmark to pixel coordinates.
    """
    lm = landmarks[index]
    x_px = int(lm.x * image_width)
    y_px = int(lm.y * image_height)
    return x_px, y_px


# ==============================
# 4. LOAD IMAGE AND RUN POSE
# ==============================
image_bgr = cv2.imread(IMAGE_PATH)
if image_bgr is None:
    raise FileNotFoundError(f"Could not read image at: {IMAGE_PATH}")

image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
h, w, _ = image_bgr.shape

results = pose.process(image_rgb)

if not results.pose_landmarks:
    print("No person / pose detected in the image.")
    cv2.imshow("Pose Estimation", image_bgr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    pose.close()
    exit()

# ==============================
# 5. DRAW FULL BODY SKELETON
# ==============================
annotated = image_bgr.copy()
mp_drawing.draw_landmarks(
    annotated,
    results.pose_landmarks,
    mp_pose.POSE_CONNECTIONS,
    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(),
    connection_drawing_spec=mp_drawing.DrawingSpec(thickness=2)
)

# ==============================
# 6. COMPUTE TRUNK ANGLE
# ==============================
landmarks = results.pose_landmarks.landmark

if USE_RIGHT_SIDE:
    shoulder_index = mp_pose.PoseLandmark.RIGHT_SHOULDER.value
    hip_index = mp_pose.PoseLandmark.RIGHT_HIP.value
    side_text = "RIGHT"
else:
    shoulder_index = mp_pose.PoseLandmark.LEFT_SHOULDER.value
    hip_index = mp_pose.PoseLandmark.LEFT_HIP.value
    side_text = "LEFT"

hip_xy = get_landmark_xy(landmarks, hip_index, w, h)
shoulder_xy = get_landmark_xy(landmarks, shoulder_index, w, h)

# Draw line for trunk
cv2.line(annotated, hip_xy, shoulder_xy, (0, 255, 0), 3)
cv2.circle(annotated, hip_xy, 6, (0, 0, 255), -1)
cv2.circle(annotated, shoulder_xy, 6, (255, 0, 0), -1)

angle_vert, angle_raw = angle_from_vertical(hip_xy, shoulder_xy)

text = f"{side_text} trunk angle from vertical: {angle_vert:.2f} deg"
print(text)

# Put text on image
cv2.putText(
    annotated,
    text,
    (30, 40),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.8,
    (255, 255, 255),
    2,
    cv2.LINE_AA
)

# ==============================
# 7. SHOW OUTPUT IMAGE
# ==============================
cv2.imshow("Pose Estimation with Trunk Angle", annotated)
cv2.waitKey(0)
cv2.destroyAllWindows()
pose.close()
