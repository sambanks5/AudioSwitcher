import sounddevice as sd
import subprocess
import os
from tkinter import messagebox, Tk

def get_default_output_device():
    try:
        default_device = sd.query_devices(kind='output')
        return default_device
    except Exception as e:
        messagebox.showerror("Error", f"Error getting default output device: {e}")
        return None

def switch_audio(device_name):
    try:
        subprocess.run(["nircmd.exe", "setdefaultsounddevice", device_name], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error switching audio device: {e}")

def get_output_devices():
    try:
        devices = sd.query_devices()
        output_devices = [device for device in devices if device['max_output_channels'] > 0]
        return output_devices
    except Exception as e:
        messagebox.showerror("Error", f"Error getting output devices: {e}")
        return []

def write_devices_to_file(devices, filename="devices.txt"):
    try:
        with open(filename, "w") as f:
            for device in devices:
                f.write(f"{device['name']} (Index: {device['index']})\n")
    except Exception as e:
        messagebox.showerror("Error", f"Error writing devices to file: {e}")

def read_devices_from_file(filename="devices.txt"):
    try:
        with open(filename, "r") as f:
            devices = [line.split(' (')[0].strip() for line in f.readlines()]
        return devices
    except Exception as e:
        messagebox.showerror("Error", f"Error reading devices from file: {e}")
        return []

def get_next_device(current_device_name, devices):
    try:
        current_index = devices.index(current_device_name)
        next_index = (current_index + 1) % len(devices)
        return devices[next_index]
    except ValueError:
        messagebox.showerror("Error", f"Current device name '{current_device_name}' not found in devices list.")
        return devices[0]
    except Exception as e:
        messagebox.showerror("Error", f"Error getting next device: {e}")
        return devices[0]

if __name__ == "__main__":
    root = Tk()
    root.withdraw()

    default_device = get_default_output_device()
    if default_device is None:
        messagebox.showerror("Error", "No default output device found. Exiting.")
        exit(1)

    current_device_name = default_device['name'].split(' (')[0].strip()
    print(f"Current device: {current_device_name}")

    if not os.path.exists("devices.txt"):
        output_devices = get_output_devices()
        if not output_devices:
            messagebox.showerror("Error", "No output devices found. Exiting.")
            exit(1)

        print("Available output devices:")
        for device in output_devices:
            print(f" - {device['name']} (Index: {device['index']})")

        write_devices_to_file(output_devices)
        messagebox.showinfo("Info", "devices.txt created. Please edit the file to include only the devices you want to switch between.")
    else:
        devices_from_file = read_devices_from_file()
        if not devices_from_file:
            messagebox.showerror("Error", "No devices found in devices.txt. Exiting.")
            exit(1)

        print("Devices from file:")
        for device in devices_from_file:
            print(f" - {device}")

        next_device = get_next_device(current_device_name, devices_from_file)
        print(f"Switching from {current_device_name} to {next_device}")

        # Switch!
        switch_audio(next_device)
