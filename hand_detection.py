def gesture_to_text(gesture):
    # Define mappings for gestures to text
    gesture_map = {
        'thumbs_up': 'Good',
        'peace_sign': 'Peace',
        # Add more mappings as needed
    }
    
    # Return corresponding text for the recognized gesture
    return gesture_map.get(gesture, 'Unknown')

# Example usage:
recognized_gesture = 'thumbs_up'  # Replace with actual recognized gesture
text = gesture_to_text(recognized_gesture)
print("Recognized Gesture:", text)
