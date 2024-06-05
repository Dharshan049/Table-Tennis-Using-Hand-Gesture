import mediapipe as mp
import cv2
import numpy as np
from sklearn.metrics import precision_recall_fscore_support

# Load the MediaPipe hand tracking model
mp_hands = mp.solutions.hands.Hands()

# Load the ground truth dataset
# This is an example and you should replace it with your own dataset
ground_truth_positions = np.array([[100, 200], [300, 400], [500, 600]])

# Define the threshold for determining true positives and false positives
threshold = 50

# Create empty lists to store the true positives, false positives, and false negatives
true_positives = []
false_positives = []
false_negatives = []

# Create a VideoCapture object to capture frames from the camera
cap = cv2.VideoCapture(0)

while True:
    # Capture a frame from the camera
    ret, frame = cap.read()

    if not ret:
        print('Failed to capture frame from camera')
        break

    # Convert the frame to RGB format
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Run the hand tracking model
    results = mp_hands.process(image)

    # Extract the detected hand positions
    detected_positions = []
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for landmark in hand_landmarks.landmark:
                x, y = int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0])
                detected_positions.append([x, y])

    # Compare the detected positions with the ground truth positions
    if len(detected_positions) > 0:
        true_positive_indices = []
        for i in range(len(ground_truth_positions)):
            for j in range(len(detected_positions)):
                distance = np.linalg.norm(np.array(detected_positions[j]) - ground_truth_positions[i])
                if distance <= threshold:
                    true_positive_indices.append(j)
                    true_positives.append(detected_positions[j])
                    break
            else:
                false_negatives.append(ground_truth_positions[i])
        for j in range(len(detected_positions)):
            if j not in true_positive_indices:
                false_positives.append(detected_positions[j])
    else:
        false_negatives.extend(ground_truth_positions)

    # Calculate the precision, recall, and F1-score
    if len(true_positives) > 0:
        precision, recall, f1_score, _ = precision_recall_fscore_support(
            [1] * len(true_positives) + [0] * len(false_positives) + [0] * len(false_negatives),
            [1] * len(true_positives) + [0] * len(false_positives) + [1] * len(false_negatives),
            average='micro'
        )

        # Print the precision, recall, and F1-score
        print('Precision:', precision*100)
        print('Recall:', recall*100)
        print('F1-score:', f1_score*100)

    # Display the frame with the detected hand positions
    annotated_image = image.copy()
    if detected_positions:
        for position in detected_positions:
            cv2.circle(annotated_image, tuple(position), 5, (0, 255, 0), -1)
    cv2.imshow('Hand Tracking', annotated_image)

    # Wait for a key press and check if the 'q' key was pressed to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close all windows
cap.release()
cv2.destroyAllWindows()