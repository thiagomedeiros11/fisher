import tkinter as tk
import pyautogui
import threading
import time
import random
from pynput import mouse, keyboard

water_pos = []
fishingrod_pos = None
fishing = False
pause = False
water_index = 0

def map_fishingrod_water():
    def on_click(x, y, button, pressed):
        global fishingrod_pos, water_pos 
        if not pressed:
            return
        if button == mouse.Button.right:
            fishingrod_pos = (x, y)
            print(f"[Mapping] Fishing Rod: {fishingrod_pos}")
        elif button == mouse.Button.left:
            water_pos.append((x, y))
            print(f"[Mapping] Water: {x}, {y}")

    def on_press(key):
        global pause, fishing
        if key == keyboard.Key.esc:
            pause = True
            fishing = False
            print("Leaving mapping mode. Bot paused.")
            listener_mouse.stop()
            listener_keyboard.stop()

    listener_mouse = mouse.Listener(on_click=on_click)
    listener_keyboard = keyboard.Listener(on_press=on_press)
    listener_mouse.start()
    listener_keyboard.start()

def loop_fishing():
    global fishing, pause, water_index
    while fishing:
        if pause:
            time.sleep(0.1)
            continue

        if not fishingrod_pos or not water_pos:
            print("Map at least one water position.")
            break

        pyautogui.moveTo(fishingrod_pos[0], fishingrod_pos[1], duration=random.uniform(0.1, 0.3))
        pyautogui.click(button='right')
        print(f"Right click on fishing rod pos: {fishingrod_pos}")
        time.sleep(random.uniform(0.3, 0.6))

        pos = water_pos[water_index]
        water_index = (water_index + 1) % len(water_pos)

        pyautogui.moveTo(pos[0], pos[1], duration=random.uniform(0.2, 0.5))
        time.sleep(random.uniform(0.1, 0.4))

        pyautogui.click(button='left')
        print(f"Left click on water pos: {pos}")

        time.sleep(random.uniform(4.5, 6.5))

def start_fishing():
    global fishing
    if not fishing:
        fishing = True
        threading.Thread(target=loop_fishing).start()
        print("Fishing started!")

def stop_fishing():
    global pause, fishing
    pause = True
    fishing = False
    print("Bot pause.")

def keep_fishing():
    global pause, fishing
    if not pause:
        return
    pause = False
    fishing = True
    threading.Thread(target=loop_fishing).start()
    print("Bot resumed.")

def leave():
    window.destroy()

window = tk.Tk()
window.title("Fisher")
window.geometry("300x300")

tk.Label(window, text="1. Click to 'Map' and use:\n → Right = fishing rod\n → Left = water\n → ESC = leave + pause").pack(pady=10)

tk.Button(window, text="Map Fishing Rod + Water", command=map_fishingrod_water).pack(pady=5)
tk.Button(window, text="Fishing ON", command=start_fishing).pack(pady=5)
tk.Button(window, text="Pause", command=stop_fishing).pack(pady=5)
tk.Button(window, text="Resume", command=keep_fishing).pack(pady=5)
tk.Button(window, text="Leave", command=leave, fg="white", bg="red").pack(pady=10)

window.mainloop()

