import pyaudio
import subprocess
import os
from tkinter import messagebox, Tk

def get_default_output_device():
    try:
        p = pyaudio.PyAudio()
        default_device_index = p.get_default_output_device_info()['index']
        default_device = p.get_device_info_by_index(default_device_index)
        p.terminate()
        return default_device
    except Exception as e:
        messagebox.showerror("Error", f"Error getting default output device: {e}")
        return None

def switch_audio(device_name):
    try:
        subprocess.run(["nircmd.exe", "setdefaultsounddevice", device_name], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error switching audio device: {e}")

def get_enabled_output_devices():
    try:
        p = pyaudio.PyAudio()
        devices = []
        seen_devices = set()
        for i in range(p.get_device_count()):
            device = p.get_device_info_by_index(i)
            if device['maxOutputChannels'] > 0 and "Primary Sound Driver" not in device['name'] and "Microsoft Sound Mapper" not in device['name']:
                if device['name'] not in seen_devices:
                    devices.append(device)
                    seen_devices.add(device['name'])
        p.terminate()
        return devices
    except Exception as e:
        messagebox.showerror("Error", f"Error getting enabled output devices: {e}")
        return []

def get_next_device(current_device_index, devices):
    for i, device in enumerate(devices):
        if device['index'] == current_device_index:
            next_index = (i + 1) % len(devices)
            return devices[next_index]
    return devices[0]

if __name__ == "__main__":
    root = Tk()
    root.withdraw()

    default_device = get_default_output_device()
    if default_device is None:
        messagebox.showerror("Error", "No default output device found. Exiting.")
        exit(1)

    current_device_index = default_device['index']
    print(f"Current device: {repr(default_device['name'])} (Index: {current_device_index})")

    enabled_output_devices = get_enabled_output_devices()
    if not enabled_output_devices:
        messagebox.showerror("Error", "No enabled output devices found. Exiting.")
        exit(1)

    print("Enabled output devices:")
    for device in enabled_output_devices:
        print(f" - {repr(device['name'])} (Index: {device['index']})")

    next_device = get_next_device(current_device_index, enabled_output_devices)
    next_device_name = next_device['name'].split("(")[0].strip()    
    next_device_index = next_device['index']
    print(f"Switching from {repr(default_device['name'])} to {repr(next_device_name)} (Index: {next_device_index})")

    # Switch the audio device
    switch_audio(next_device_name)
    # messagebox.showinfo("Info", "Successfully switched")