import cv2
import os
import mediapipe as mp
import pygame
import time
import sys
from gestures import detect_gesture

mp_hands = mp.solutions.hands


def run_debug(cap, hands):
    """OpenCV debug mode with landmarks drawn"""
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )
                gesture = detect_gesture(hand_landmarks.landmark, mp_hands)
                cv2.putText(frame, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("Hand Gesture Recognition (Debug)", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

def run_normal(cap, hands):
        # Pygame mode
        pygame.init()
        icon_path = os.path.join("assets", "icon.ico")
        print(icon_path)
        if os.path.exists(icon_path):
            pygame.display.set_icon(pygame.image.load(icon_path))
        screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Hand Gesture Recognition")
        font = pygame.font.SysFont(None, 36)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    gesture = detect_gesture(hand_landmarks.landmark, mp_hands)

                    # Compute bounding box
                    xs = [lm.x for lm in hand_landmarks.landmark]
                    ys = [lm.y for lm in hand_landmarks.landmark]
                    h, w, _ = frame.shape
                    x_min, x_max = int(min(xs) * w), int(max(xs) * w)
                    y_min, y_max = int(min(ys) * h), int(max(ys) * h)

                    # Draw bounding box
                    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0,255,0), 2)

                    # Draw gesture text above the box
                    cv2.putText(frame, gesture, (x_min, y_min - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2, cv2.LINE_AA)

            # Convert frame to pygame surface
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_surface = pygame.surfarray.make_surface(frame_rgb.swapaxes(0,1))
            screen.blit(frame_surface, (0,0))

            pygame.display.flip()

        cap.release()
        pygame.quit()

def output_code(cap):
    mp_hands = mp.solutions.hands
    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=10,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    ) as hands:
        ret, frame = cap.read()
        if not ret:
            return None

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        gestures = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                gestures.append(detect_gesture(hand_landmarks.landmark, mp_hands))

        return gestures if gestures else None

def ask_mode():
    """Simple pygame menu with dynamic text placement"""
    pygame.init()
    screen = pygame.display.set_mode((420, 240))
    pygame.display.set_caption("Choose Mode")
    font = pygame.font.SysFont(None, 40)
    clock = pygame.time.Clock()

    # Define options dynamically
    options = {
        pygame.K_d: ("Press D for Debug (OpenCV)", "debug"),
        pygame.K_n: ("Press N for Normal (Pygame)", "normal"),
        pygame.K_q: ("Press Q to Quit", "quit")
    }

    choice = None
    while choice is None:
        screen.fill((30, 30, 30))

        # Calculate vertical placement dynamically
        line_height = font.get_height() + 20   # spacing between lines
        total_height = len(options) * line_height
        start_y = (screen.get_height() - total_height) // 2  # center vertically

        for i, (key, (label, _)) in enumerate(options.items()):
            text_surface = font.render(label, True, (200, 200, 200))
            text_rect = text_surface.get_rect(center=(screen.get_width()//2,
                                                      start_y + i * line_height))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key in options:
                choice = options[event.key][1]

        clock.tick(30)

    pygame.quit()
    return choice

def goodbye_page(text = "Goodbye! See you soon!", caption="Goodbye"):
    """Display a goodbye screen before quitting"""
    pygame.init()
    screen = pygame.display.set_mode((500, 300))
    pygame.display.set_caption(caption)
    font = pygame.font.SysFont(None, 60)
    clock = pygame.time.Clock()

    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(screen.get_width()//2,
                                              screen.get_height()//2))

    running = True
    start_time = time.time()

    while running:
        screen.fill((30, 30, 30))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Auto-close after 3 seconds
        if time.time() - start_time > 3:
            running = False

        clock.tick(30)

    pygame.quit()
    sys.exit()


def main():
    mode = ask_mode()
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=10,   # 👈 allow up to 10 hands
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    ) as hands:
        if mode == "debug":
            run_debug(cap, hands)
        elif mode == "normal":
            run_normal(cap, hands)
        goodbye_page()

if __name__ == "__main__":
    main()
