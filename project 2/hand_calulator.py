import cv2
import mediapipe as mp

# MediaPipe Hands initialization
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Function to count fingers
def count_fingers(hand_landmarks):
    tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
    count = 0
    # Thumb
    if hand_landmarks.landmark[tips[0]].x < hand_landmarks.landmark[tips[0]-1].x:
        count += 1
    # Other fingers
    for i in range(1, 5):
        if hand_landmarks.landmark[tips[i]].y < hand_landmarks.landmark[tips[i]-2].y:
            count += 1
    return count

cap = cv2.VideoCapture(0)
numbers = []  # To store two numbers
operation = None  # '+' or '-'

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    finger_count = 0
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            finger_count = count_fingers(hand_landmarks)

    # Show instructions
    cv2.putText(frame, f"Show fingers for number", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
    cv2.putText(frame, f"Number detected: {finger_count}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)
    cv2.putText(frame, f"Press 'a' for addition, 's' for subtraction", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
    cv2.putText(frame, f"Press 'r' to reset", (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

    if len(numbers) < 2:
        cv2.putText(frame, f"Stored numbers: {numbers}", (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 2)

    if operation:
        if len(numbers) == 2:
            if operation == '+':
                result_val = numbers[0] + numbers[1]
            else:
                result_val = numbers[0] - numbers[1]
            cv2.putText(frame, f"Result: {numbers[0]} {operation} {numbers[1]} = {result_val}", (10, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

    cv2.imshow("Hand Calculator", frame)
    key = cv2.waitKey(1)

    # Press keys for actions
    if key == ord('q'):
        break
    elif key == ord('n'):
        if len(numbers) < 2:
            numbers.append(finger_count)
    elif key == ord('a'):
        operation = '+'
    elif key == ord('s'):
        operation = '-'
    elif key == ord('r'):
        numbers = []
        operation = None

cap.release()
cv2.destroyAllWindows()
