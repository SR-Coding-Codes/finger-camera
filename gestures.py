def detect_gesture(landmarks,mphands):
    tips = {
        "thumb": landmarks[mphands.HandLandmark.THUMB_TIP],
        "index": landmarks[mphands.HandLandmark.INDEX_FINGER_TIP],
        "middle": landmarks[mphands.HandLandmark.MIDDLE_FINGER_TIP],
        "ring": landmarks[mphands.HandLandmark.RING_FINGER_TIP],
        "pinky": landmarks[mphands.HandLandmark.PINKY_TIP],
    }
    mcps = {
        "index": landmarks[mphands.HandLandmark.INDEX_FINGER_MCP],
        "middle": landmarks[mphands.HandLandmark.MIDDLE_FINGER_MCP],
        "ring": landmarks[mphands.HandLandmark.RING_FINGER_MCP],
        "pinky": landmarks[mphands.HandLandmark.PINKY_MCP],
    }
    fingers_extended = {f: tips[f].y < mcps[f].y for f in mcps}
    thumb_extended = tips["thumb"].x < landmarks[mphands.HandLandmark.THUMB_IP].x

    if all(fingers_extended.values()) and thumb_extended:
        return "Open Palm"
    elif not any(fingers_extended.values()) and not thumb_extended:
        return "Fist"
    elif thumb_extended and not any(fingers_extended.values()):
        return "Thumbs Up"
    elif fingers_extended["index"] and fingers_extended["middle"] and not fingers_extended["ring"] and not fingers_extended["pinky"]:
        return "Peace"
    elif not fingers_extended["index"] and not fingers_extended["middle"] and not fingers_extended["ring"] and fingers_extended["pinky"] and not thumb_extended:
        return "Pinky"
    elif abs(tips["thumb"].x - tips["index"].x) < 0.05 and abs(tips["thumb"].y - tips["index"].y) < 0.05:
        return "OK"
    elif fingers_extended["index"] and not fingers_extended["middle"] and not fingers_extended["ring"] and fingers_extended["pinky"]:
        return "Rock'n Roll"
    elif fingers_extended["index"] and not fingers_extended["middle"] and not fingers_extended["ring"] and not fingers_extended["pinky"] and thumb_extended:
        return "L shape"
    elif fingers_extended["index"] and not fingers_extended["middle"] and not fingers_extended["ring"] and not fingers_extended["pinky"] and not thumb_extended:
        return "Pointing"
    else:
        return "Unknown"
