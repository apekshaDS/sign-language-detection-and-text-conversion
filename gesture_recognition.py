import cv2
import numpy as np

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
            
            # Calculate triangle area usin
