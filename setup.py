import cx_Freeze
import sys
base = None
if sys.platform == "win32":
    base = "Win32GUI"
shortcut_table = [
    ("DesktopShortcut",  # Shortcut
     "DesktopFolder",  # Directory_
     "ANPR",  # Name
     "TARGETDIR",  # Component_
     "[TARGETDIR]\main.exe",  # Target
     None,  # Arguments
     None,  # Description
     None,  # Hotkey
     None,  # Icon
     None,  # IconIndex
     None,  # ShowCmd
     "TARGETDIR",  # WkDir
     )
]
msi_data = {"Shortcut": shortcut_table}

# Change some default MSI options and specify the use of the above defined tables
bdist_msi_options = {'data': msi_data}

executables = [cx_Freeze.Executable(script="main.py",icon='car.ico',base=base)]

cx_Freeze.setup(
    version="1.0",
    description="Automatic Number Plate Recognition (ANPR)",
    author="Group 2",
    name="ANPR",
    options={"build_exe": {"packages":["cv2", "tkinter", "tkinter.messagebox", "pandas", "os", "numpy", "imutils", "pytesseract", "tkinter.filedialog", "matplotlib", "mysql.connector", "tkinter.simpledialog"],
                           "include_files":['car.ico', 'bg_img.png']},
             "bdist_msi": bdist_msi_options,
             },
    executables = executables
    )
