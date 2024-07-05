import cv2
import numpy as np
from gtts import gTTS
import os

# Function to recognize gestures based on contours
def recognize_gesture(contour):
    # Calculate convex hull
    hull = cv2.convexHull(contour, returnPoints=False)
    
    # Apply defects to find convexity defects
    defects = cv2.convexityDefects(contour, hull)
    
    if defects is not None:
        # Count defects
        num_defects = 0
        
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(contour[s][0])
            end = tuple(contour[e][0])
            far = tuple(contour[f][0])
            
            # Calculate triangle area using Heron's formula
            a = np.linalg.norm(np.array(start) - np.array(end))
            b = np.linalg.norm(np.array(start) - np.array(far))
            c = np.linalg.norm(np.array(end) - np.array(far))
            s = (a + b + c) / 2
            area = np.sqrt(s * (s - a) * (s - b) * (s - c))
            
            # Find distance between farthest point and convex hull
            dist = cv2.pointPolygonTest(contour, far, True)
            
            # Filter defects by depth and area
            if dist > 10 and area > 1000:
                cv2.circle(frame, far, 3, [0, 0, 255], -1)
                num_defects += 1
        
        # Return gesture based on number of defects
        if num_defects == 0:
            return 'Fist'
        elif num_defects == 1:
            return 'Peace'
        elif num_defects == 2:
            return 'Two'
        elif num_defects == 3:
            return 'Three'
        elif num_defects == 4:
            return 'Four'
    
    return 'Unknown'

# Function to convert text to speech
def text_to_speech(text):
    # Initialize gTTS (Google Text-to-Speech) with English language
    tts = gTTS(text=text, lang='en')
    
    # Save the speech to a temporary file
    tts.save("output.mp3")
    
    # Play the speech using the default media player
    os.system("start output.mp3")

# Example usage:
cap = cv2.VideoCapture(0)  # Initialize webcam capture
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip the frame horizontally for intuitive display
    frame = cv2.flip(frame, 1)
    
    # Detect hand and find contours
    hand_rect = detect_hand(frame)
    if hand_rect is not None:
        x, y, w, h = hand_rect
        hand_region = frame[y:y+h, x:x+w]
        
        # Convert hand region to grayscale
        gray_hand = cv2.cvtColor(hand_region, cv2.COLOR_BGR2GRAY)
        
        # Threshold the grayscale image
        _, thresh = cv2.threshold(gray_hand, 70, 255, cv2.THRESH_BINARY)
        
        # Find contours in the thresholded image
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) > 0:
            # Find the largest contour
            max_contour = max(contours, key=cv2.contourArea)
            
            # Recognize gesture based on the largest contour
            gesture = recognize_gesture(max_contour)
            
            # Convert gesture to text
            text = gesture
            
            # Display recognized gesture
            cv2.putText(frame, gesture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            
            # Convert text to speech and play
            text_to_speech(text)
    
    # Display the frame
    cv2.imshow('Gesture Recognition', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
