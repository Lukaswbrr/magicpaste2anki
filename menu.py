from PySide6 import QtWidgets, QtCore
from pynput import keyboard
import pyperclip
import requests

clipboard_text = ""

question_text = ""
answer_text = ""

# anki requests
def add_note_to_anki(question, answer, deck="Default", model="Básico"):
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck,
                "modelName": model,
                "fields": {
                    "Frente": question,
                    "Verso": answer
                },
                "options": {
                    "allowDuplicate": True
                },
                "tags": []
            }
        }
    }
    response = requests.post("http://localhost:8765", json=payload)
    return response.json()

# keyboard related functions
current_keys = set()


def on_activate_ctrl_c():
    global clipboard_text
    global question_text
    global answer_text

    clipboard_text = pyperclip.paste().strip()
    print(f"Clipboard text captured: {clipboard_text}")

    if question_text == "":
        question_text = clipboard_text
        print(f"Question text set to: {question_text}")
    else:
        answer_text = clipboard_text
        print(f"Answer text set to: {answer_text}")

        print(f"Added question and answer: {question_text} -> {answer_text}")
        result = add_note_to_anki(question_text.strip(), answer_text.strip())
        print(f"Anki response: {result}")
        
        question_text = ""
        answer_text = ""

def on_press(key):
    # Captura Ctrl+C
    if {keyboard.Key.ctrl_l, keyboard.KeyCode.from_char('c')}.issubset(current_keys):
        on_activate_ctrl_c()
    # Captura ESC
    if key == keyboard.Key.esc:
        print("ESC Pressed, quitting...")
        return False  # Para o listener


def on_press_wrapper(key):
    current_keys.add(key)
    # Ctrl+C
    if keyboard.Key.ctrl_l in current_keys and keyboard.KeyCode.from_char('c') in current_keys:
        on_activate_ctrl_c()
    # ESC
    if key == keyboard.Key.esc:
        print("ESC Pressed, quitting...")
        return False

def on_release_wrapper(key):
    if key in current_keys:
        current_keys.remove(key)

with keyboard.Listener(
        on_press=on_press_wrapper,
        on_release=on_release_wrapper) as listener:
    print("Press CTRL+C to capture or ESC to exit.")
    listener.join()