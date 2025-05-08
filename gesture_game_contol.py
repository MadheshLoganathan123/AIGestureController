import cv2
import mediapipe as mp
import pyautogui

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Open the webcam (try 0, 1, or 2 based on your device)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Cannot access the webcam")
    exit()
else:
    print("✅ Webcam is working")

# Detect gesture based on hand landmarks
def detect_gesture(landmarks):
    thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    wrist = landmarks.landmark[mp_hands.HandLandmark.WRIST]

    if index_tip.y < thumb_tip.y and middle_tip.y < thumb_tip.y:
        return "jump"
    elif index_tip.x < thumb_tip.x:
        return "left"
    elif index_tip.x > thumb_tip.x:
        return "right"

    elif index_tip.y > wrist.y and middle_tip.y > wrist.y:
        return "scroll_down"
    else:
        return "none"

# Main loop
while True:
    success, frame = cap.read()
    if not success:
        print("❌ Failed to read frame from webcam.")
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            gesture = detect_gesture(hand_landmarks)

            cv2.putText(frame, f'Gesture: {gesture}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            if gesture == "jump":
                pyautogui.press("up")
            elif gesture == "left":
                pyautogui.press("left")
            elif gesture == "right":
                pyautogui.press("right")
            if gesture == "scroll_down":
                pyautogui.scroll(-50)

    cv2.imshow("Gesture Controller", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
