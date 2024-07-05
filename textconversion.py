def gesture_to_text(gesture):
    # Define mappings for gestures to text
    gesture_map = {
        'Fist': 'A',
        'Peace': 'B',
        'Two': 'C',
        'Three': 'D',
        'Four': 'E',
        'Unknown': ''
    }
    
    # Return corresponding text for the recognized gesture
    return gesture_map.get(gesture, '')

# Example usage:
recognized_gesture = 'Peace'  # Replace with actual recognized gesture
text = gesture_to_text(recognized_gesture)
print("Recognized Gesture:", text)
