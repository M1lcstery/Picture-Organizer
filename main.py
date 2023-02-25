import os
import shutil
from PIL import Image
from tkinter import filedialog, Label, Radiobutton, StringVar, Tk, Button

def Organize_Pictures(folder_path, organization_method):
    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg') or filename.endswith('.png'): # Only process image files
            filepath = os.path.join(folder_path, filename)
            with Image.open(filepath) as img:
                if organization_method == 'date':
                    # Get the date the photo was taken
                    exif_data = img._getexif()
                    if exif_data:
                        date = exif_data.get(36867)
                        if date:
                            year, month, day = date.split()[0].split(':')
                            # Create a new folder for the date if it doesn't exist
                            new_folder_path = os.path.join(folder_path, f'{year}-{month}-{day}')
                            if not os.path.exists(new_folder_path):
                                os.makedirs(new_folder_path)
                            # Move the file to the new folder
                            new_filepath = os.path.join(new_folder_path, filename)
                            try:
                                shutil.move(filepath, new_filepath)
                            except PermissionError:
                                print(f"PermissionError: could not move file '{filepath}'")
                elif organization_method == 'location':
                    # Get the location data
                    if img._getexif() is not None:
                        location_data = img._getexif().get(271)
                    if location_data:
                        lat, lon = location_data[2][0], location_data[4][0]
                        # Create a new folder for the location if it doesn't exist
                        new_folder_path = os.path.join(folder_path, f'{lat},{lon}')
                        if not os.path.exists(new_folder_path):
                            os.makedirs(new_folder_path)
                        # Move the file to the new folder
                        new_filepath = os.path.join(new_folder_path, filename)
                        try:
                            shutil.move(filepath, new_filepath)
                        except PermissionError:
                            print(f"PermissionError: could not move file '{filepath}'")

# Create the Tkinter app
root = Tk()
root.title('Photo Organizer')
root.geometry("400x300")

# Add a label to describe the purpose of the app and provide instructions
app_label = Label(root, text='Photo Organizer App\n\nSelect a folder containing photos and choose how to organize them:')
app_label.pack()

# Add a button to select the folder to organize
def select_folder():
    global selected_folder
    selected_folder = filedialog.askdirectory()
    folder_path_label.config(text=selected_folder)

select_folder_button = Button(root, text='Select Folder', command=select_folder)
select_folder_button.pack(pady=10)

# Add a label to display the path of the selected folder
folder_path_label = Label(root, text='No folder selected.')
folder_path_label.pack()

# Add a radio button group to choose the organization method
organization_method_label = Label(root, text='Organize photos by:')
organization_method_label.pack()

organization_method = StringVar(value='date')
date_button = Radiobutton(root, text='Date', variable=organization_method, value='date')
location_button = Radiobutton(root, text='Location', variable=organization_method, value='location')
date_button.pack()
location_button.pack()

# Add a button to organize the photos
def Organize_Button():
    if selected_folder:
        organization_method_value = organization_method.get()
        Organize_Pictures(selected_folder, organization_method_value)
        done_label.config(text='Done!')
    else:
        done_label.config(text='Please select a folder first.')

def Exit_App():
    root.destroy()

organize_button = Button(root, text='Organize Photos', command=Organize_Button)
organize_button.pack(pady=10)

# Add a label to display a message when the organization is complete
done_label = Label(root, text='')
done_label.pack()

exit_button = Button(root, text="Exit", command=Exit_App)
exit_button.pack()

# Start the main event loop
root.mainloop()
