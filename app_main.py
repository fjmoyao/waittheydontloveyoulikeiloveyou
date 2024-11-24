import streamlit as st
import time
from PIL import Image
import threading
from pygame import mixer
import random

# Initialize pygame mixer for audio playback
#mixer.init()


# Load images and cache them using st.cache_data
@st.cache_data
def load_images():
    hand_pose = Image.open("wait_mano.PNG")
    wait0 = Image.open("wait0.PNG")
    wait1 = Image.open("wait1.PNG")
    wait2 = Image.open("wait2.PNG")
    heart_image = Image.open("heart_image.png")  # The heart image with sparks
    return hand_pose, wait0, wait1, wait2, heart_image

# Load images
hand_pose, wait0, wait1, wait2, heart_image = load_images()

# Sidebar Controls for START and STOP
st.sidebar.title("Controles")
start_button = st.sidebar.button("Iniciar")
stop_button = st.sidebar.button("Detener")

# Title
st.title("Porque te amo, un trend para tí <3")

# Placeholder for animation and text input
placeholder = st.empty()
input_placeholder = st.empty()

# State variables to manage animation and audio
if "is_running" not in st.session_state:
    st.session_state.is_running = False

if "show_heart" not in st.session_state:
    st.session_state.show_heart = False

# Function to play audio
def play_audio():
    st.audio("wait_audio.mp3",autoplay=True)
    #mixer.music.load("wait_audio.mp3")  # Load your MP3 file
    #mixer.music.play(-1)  # Play in a loop

# Function to stop audio
def stop_audio():
    st.audio("wait_audio.mp3",autoplay=False)

# Handle START button
if start_button:
    st.session_state.is_running = True
    st.session_state.show_heart = False
    play_audio()
    #threading.Thread(target=play_audio).start()  # Start playing audio in a separate thread

# Handle STOP button
if stop_button:
    st.session_state.is_running = False
    st.session_state.show_heart = False
    placeholder.empty()  # Clear the placeholder
    input_placeholder.empty()  # Clear the input field
    stop_audio()
try: 
    # Animation loop
    while st.session_state.is_running:
        start_time = time.time()


        # Generate a random integer
        random_int = random.randint(1, 100)
        k = f"input{random_int}"


        # Show the text input for "amorcito" name
        amorcito_name = input_placeholder.text_input("¿Quién es mi amorcito?", key="k")

        # Check for specific names
        if any(name in amorcito_name.lower() for name in ["bri", "brigith", "vanessa","brigith vanessa","yo"]):
            st.session_state.is_running = False
            st.session_state.show_heart = True
            placeholder.empty()
            input_placeholder.empty()
            stop_audio()
            break

        while time.time() - start_time < 10:  # Loop for 10 seconds
            elapsed_time = time.time() - start_time

            if elapsed_time < 1.3:  # Show hand pose for 1.30 seconds
                placeholder.image(hand_pose)

            elif elapsed_time < 3.6:  # Show loop pattern for 2.30 seconds
                # Faster transitions: 0.1 seconds per frame
                pattern_time = (elapsed_time - 1.3) % 0.3
                if pattern_time < 0.1:
                    placeholder.image(wait1)
                elif pattern_time < 0.2:
                    placeholder.image(wait0)
                else:
                    placeholder.image(wait2)

            elif elapsed_time < 4.9:  # Show hand pose for another 1.30 seconds
                placeholder.image(hand_pose)

            elif elapsed_time < 7.2:  # Repeat the loop for 2.30 seconds
                # Faster transitions: 0.1 seconds per frame
                pattern_time = (elapsed_time - 4.9) % 0.3
                if pattern_time < 0.1:
                    placeholder.image(wait1)
                elif pattern_time < 0.2:
                    placeholder.image(wait0)
                else:
                    placeholder.image(wait2)

            else:  # End with hand pose
                placeholder.image(hand_pose)
                time.sleep(1.3)  # Hold for 1.30 seconds
                break

            time.sleep(0.1)  # Small delay for smooth updates

            # Check if STOP button is pressed during animation
            if not st.session_state.is_running:
                break

        # If STOP is pressed, clear the animation
        if not st.session_state.is_running:
            placeholder.empty()
            stop_audio()
            break
except Exception:
    pass

# Display the heart and message if the condition is met
if st.session_state.show_heart:
    placeholder.image(heart_image)
    st.balloons()
    st.write("<h3 style='text-align: center;'>Felicidades, te has ganado mi corazón!</h3>", unsafe_allow_html=True)
