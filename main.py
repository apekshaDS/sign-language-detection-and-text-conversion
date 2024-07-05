import cv2
import numpy as np

def detect_hand(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    
    # Threshold the image to get binary image
    _, thresholded = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Find contours
    contours, _ = cv2.findContours(thresholded.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Find the contour with maximum area (hand)
    if len(contours) > 0:
        hand_contour = max(contours, key=cv2.contourArea)
        
        # Return the bounding box of the hand contour
        return cv2.boundingRect(hand_contour)
    
    return None

# Example usage:
cap = cv2.VideoCapture(0)  # Initialize webcam capture
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip the frame horizontally for intuitive display
    frame = cv2.flip(frame, 1)
    
    # Detect hand
    hand_rect = detect_hand(frame)
    
    # Draw bounding rectangle if hand is detected
    if hand_rect is not None:
        x, y, w, h = hand_rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Display the frame
    cv2.imshow('Hand Detection', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
