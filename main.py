import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk
import pandas as pd
import numpy as np
from tkinter import filedialog, messagebox, simpledialog, OptionMenu
from urllib.parse import urljoin
import io
import os
import requests
from bs4 import BeautifulSoup
from pyproj import Proj
import customtkinter
from PIL import Image, ImageTk
import customtkinter as ctk
from tkinter import ttk





def show_about():
    messagebox.showinfo("About Us", "DataRefiner Version 1.01\nDeveloped by: Er Sahitya Dulal\nFor more information, visit our website.")


def show_info(event):
    global info_box
    info_text = """
    you can get general idea of zone number from this:
    """
    info_box = tk.Toplevel(window)
    info_box.geometry("530x484")  # Adjusted size to fit image below the text
    info_label = tk.Label(info_box, text=info_text, justify='left')
    info_label.pack()

    # Load and display the image
    image_path = "C:/Users/Admin/Desktop/Tkinter/pratices/venv/image/Zone.png"
    zone_image = Image.open(image_path)
    zone_image = zone_image.resize((526, 384), Image.LANCZOS)
    zone_image_tk = ImageTk.PhotoImage(zone_image)

    image_label = tk.Label(info_box, image=zone_image_tk)
    image_label.image = zone_image_tk  # Keep a reference to avoid garbage collection
    image_label.pack()
def hide_info(event):
    info_box.destroy()





    
#..................................................shift window..........................................................................................................................................
def open_shift_info():
    info_window = tk.Toplevel(window)
    info_window.title("Shift Data Information")
    info_window.geometry("600x720")
    info_window.configure(bg="#ADD8E6")

    info_label_top = tk.Label(info_window, text="From this feature you can now shift all your data relative to constant easting and northing .", bg="#ADD8E6", fg="black")
    info_label_top.pack(pady=10)

    img1_path = "C:/Users/Admin/Desktop/Tkinter/pratices/venv/image/Bsft.png"
    img2_path = "C:/Users/Admin/Desktop/Tkinter/pratices/venv/image/Asft.png"
    img3_path = "C:/Users/Admin/Desktop/Tkinter/pratices/venv/image/inputsample.png"

    img1 = Image.open(img1_path)
    img1 = img1.resize((200, 200), Image.Resampling.LANCZOS)
    img1_photo = ImageTk.PhotoImage(img1)

    img2 = Image.open(img2_path)
    img2 = img2.resize((200, 200), Image.Resampling.LANCZOS)
    img2_photo = ImageTk.PhotoImage(img2)

    images_frame = tk.Frame(info_window, bg="#ADD8E6")
    images_frame.pack(pady=10)

    label_img1 = tk.Label(images_frame, image=img1_photo, bg="#ADD8E6")
    label_img1.pack(side=tk.LEFT, padx=10)

    label_img2 = tk.Label(images_frame, image=img2_photo, bg="#ADD8E6")
    label_img2.pack(side=tk.LEFT, padx=10)

    label_img1.image = img1_photo
    label_img2.image = img2_photo

    info_label_bottom = tk.Label(info_window, text="As shown in above image all four shifted to a new position by constant easting and northing \n In order to  perform this action you must have a csv file of format as shown below", bg="#ADD8E6", fg="black")
    info_label_bottom.pack(pady=10)

    img3 = Image.open(img3_path)
    img3 = img3.resize((345, 247), Image.Resampling.LANCZOS)
    img3_photo = ImageTk.PhotoImage(img3)

    label_img3 = tk.Label(info_window, image=img3_photo, bg="#ADD8E6")
    label_img3.pack(pady=10)
    label_img3.image = img3_photo




    shift_icon_path = "C:/Users/Admin/Desktop/Tkinter/pratices/venv/image/shift.png"
    shift_icon = Image.open(shift_icon_path)
    shift_icon_resized = shift_icon.resize((20, 20), Image.LANCZOS)
    shift_icon_tk = ctk.CTkImage(shift_icon_resized)
    button_shift = ctk.CTkButton(info_window, text="Shift Now", image=shift_icon_tk, compound="left", fg_color="#663399", width=20, command=lambda: open_shift_window(info_window))
    button_shift.pack(pady=10)


def shift_coordinates(easting, northing, base_x, base_y):
    # Implement your coordinate shift logic here
    shifted_easting = easting + base_x  # Simple shift for now
    shifted_northing = northing + base_y  # Simple shift for now
    return shifted_easting, shifted_northing

def shifted_csv(input_path, output_path, base_x, base_y):
    # Read CSV file into a pandas DataFrame
    df = pd.read_csv(input_path)
    
    # Extract Easting and Northing columns (assuming specific column order)
    serial_number = df.iloc[:, 0].astype(int)
    easting = df.iloc[:, 1].astype(float)
    northing = df.iloc[:, 2].astype(float)
    elevation = df.iloc[:, 3].astype(float) if len(df.columns) > 3 else None  # Handle optional elevation column
    remark = df.iloc[:, 4].astype(str) if len(df.columns) > 4 else None  # Handle optional remark column

    # Rotate coordinates
    shifted_easting, shifted_northing = shift_coordinates(easting, northing, base_x, base_y)

    # Create a new DataFrame with original heading and star rotation
    new_df = pd.DataFrame({
        df.columns[0]: serial_number,
        df.columns[1]: shifted_easting,
        df.columns[2]: shifted_northing,
    })

    # Check if elevation and/or remark columns exist in the original DataFrame
    if elevation is not None:
        new_df[df.columns[3]] = elevation
    if remark is not None:
        new_df[df.columns[4]] = remark

    # Extract and copy heading (assuming it's in the first row)
    original_heading = df.columns.tolist()
    new_df.columns = original_heading

    # Copy information from the second row (assuming star rotation is there)
    star_rotation_info = df.iloc[1, :]
    new_df.loc[1] = star_rotation_info

    # Save the result to a new CSV file
    new_df.to_csv(output_path, index=False)

def open_shift_window(prev_window):
    #prev_window.withdraw()
    
    def browse_file():
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        input_path_entry.delete(0, tk.END)
        input_path_entry.insert(0, filename)
    
    def perform_shift():
        input_path = input_path_entry.get()
        base_x = float(base_x_entry.get())
        base_y = float(base_y_entry.get())
        try:
            output_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if not output_path:
                messagebox.showwarning("Cancelled", "Output file save cancelled.")
                return
            shifted_csv(input_path, output_path, base_x, base_y)
            messagebox.showinfo("SUCCESSFULL!!", " Successfully Shifted \n CSV file has been shifted and saved")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    Shift_window = tk.Toplevel(window)
    Shift_window.title("Shift Data")
    Shift_window.geometry("585x400")
    Shift_window.configure(bg="#ADD8E6")
    
    tk.Label(Shift_window, text="Input CSV Path:", bg="#ADD8E6").grid(row=0, column=0, pady=5, padx=5, sticky='w')
    input_path_entry = tk.Entry(Shift_window, width=50)
    input_path_entry.grid(row=0, column=1, pady=5, padx=5)
    

    browse_icon_path = "C:/Users/Admin/Desktop/Tkinter/pratices/venv/image/browse.png"
    browse_icon = Image.open(browse_icon_path)
    browse_icon_ctk = ctk.CTkImage(browse_icon)
    button_browse = ctk.CTkButton(Shift_window, text="Browse", image=browse_icon_ctk, compound="left", width=15, command=browse_file)
    button_browse.grid(row=0, column=2, pady=5, padx=5)


    tk.Label(Shift_window, text="Constant Easting:", bg="#ADD8E6").grid(row=1, column=0, pady=5, padx=5, sticky='w')
    base_x_entry = tk.Entry(Shift_window)
    base_x_entry.grid(row=1, column=1, pady=5, padx=5)
    
    tk.Label(Shift_window, text="Constant Northing:", bg="#ADD8E6").grid(row=2, column=0, pady=5, padx=5, sticky='w')
    base_y_entry = tk.Entry(Shift_window)
    base_y_entry.grid(row=2, column=1, pady=5, padx=5)
    
    #ctk.CTkButton(Shift_window, text="Shift data", command=perform_shift).grid(row=3, columnspan=3, pady=20)
    shift_icon_path = "C:/Users/Admin/Desktop/Tkinter/pratices/venv/image/shift.png"
    shift_icon = Image.open(shift_icon_path)
    shift_icon_resized = shift_icon.resize((20, 20), Image.LANCZOS)
    shift_icon_tk = ctk.CTkImage(shift_icon_resized)
    button_shift = ctk.CTkButton(Shift_window, text="Shift", image=shift_icon_tk, compound="left", width=15, fg_color="green",   command= perform_shift)
    button_shift.grid(row=3, column=1, pady=10)


   
 #...............................Convert window section..............................................................................................................................................   










#..................KML to CSV Conversion ............................................................................................................................................................

def open_kml_csv(window):
    def convert_kml_to_csv(kml_file, utm_zone):
        url = "https://www.gpsvisualizer.com/convert_input?form=elevation"
        files = {'uploaded_file_1': open(kml_file, 'rb')}
        data = {
            'convert_format': 'text',
            'convert_delimiter': 'tab',
            'units': 'metric',
            'add_elevation': 'NASA1'
        }
        
        response = requests.post(url, files=files, data=data)
        soup = BeautifulSoup(response.content, 'html.parser')
        base_url = 'https://www.gpsvisualizer.com'
        link_tag = soup.find('a', href=lambda x: x and '/download/convert/' in x)
        
        if link_tag:
            download_link = link_tag['href']
            complete_url = base_url + download_link
            print(f"Complete URL: {complete_url}")
            
            response = requests.get(complete_url)
            
            if response.status_code == 200:
                file_content = io.BytesIO(response.content)
                print("File downloaded successfully")
                
                df = pd.read_csv(file_content, delimiter='\t')
                df_required = df[['latitude', 'longitude', 'altitude (m)']]
                df_required.columns = ['latitude', 'longitude', 'elevation']
                
                proj_utm = Proj(proj="utm", zone=int(utm_zone), datum="WGS84", south=False)
                
                def latlon_to_utm(lat, lon, proj_utm):
                    easting, northing = proj_utm(lon, lat)
                    return easting, northing
                
                utm_coords = [latlon_to_utm(lat, lon, proj_utm) for lat, lon in zip(df_required['latitude'], df_required['longitude'])]
                utm_coords_df = pd.DataFrame(utm_coords, columns=['easting', 'northing'])
                
                output_df = pd.DataFrame({
                    'serial_number': range(1, len(df_required) + 1),
                    'easting': utm_coords_df['easting'],
                    'northing': utm_coords_df['northing'],
                    'elevation': df_required['elevation'],
                    'remarks': 'GP'
                })
                
                output_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
                if output_file:
                    output_df.to_csv(output_file, index=False)
                    print(f"Output saved to {output_file}")
                    messagebox.showinfo("      Successful!    ", "converted successfully!! \n Saved to your selected location")
                else:
                    print("Save operation cancelled.")
            else:
                print(f"Failed to download the file. Status code: {response.status_code}")
        else:
            print("Download link not found.")
    
    def select_kml_file():
        kml_file = filedialog.askopenfilename(filetypes=[("KML files", "*.kml"), ("All files", "*.*")])
        if kml_file:
            label_selected_file.config(text=f"Selected file: {kml_file}")
            entry_zone_number.config(state=tk.NORMAL)
            button_convert.configure(state=tk.NORMAL, command=lambda: convert_kml_to_csv(kml_file, entry_zone_number.get()))

    





    window_kml_csv = tk.Toplevel(window)
    window_kml_csv.geometry("640x300")
    window_kml_csv.title("KML to CSV Converter")
    window_kml_csv.configure(bg="#008080")
    
    frame_kml_csv = tk.Frame(window_kml_csv, bg="#ADD8E6")
    frame_kml_csv.pack(fill=tk.BOTH, expand=True)









    
    # label_instruction = tk.Label(frame_kml_csv, text="Select a KML file and enter UTM zone number:", bg="#ADD8E6", fg="black")
    # label_instruction.grid(row=0, column=0, padx=10, pady=10, sticky='w')
    Info = ctk.CTkLabel(frame_kml_csv, text="For conversion Select KML file and Zone nuber.For nepal either(44 or 45)", font=("Helvetica", 14, "bold"), fg_color="#000000", bg_color='#ADD8E6')
    Info.grid(row=0, column=0, columnspan=2, padx=10, pady=10)


    label_zone_number = tk.Label(frame_kml_csv, text="Select KML file :", bg="#ADD8E6", fg="black", font=("Helvetica", 9, "bold"))
    label_zone_number.grid(row=1, column=0, padx=10, pady=10, sticky='w')
    input_path_entry = tk.Entry(frame_kml_csv, width=50)
    input_path_entry.grid(row=1, column=1, pady=5, padx=5)

#here

    browse_icon_path = "C:/Users/Admin/Desktop/Tkinter/pratices/venv/image/browse.png"
    browse_icon = Image.open(browse_icon_path)
    browse_icon_ctk = ctk.CTkImage(browse_icon)
    button_select_file = ctk.CTkButton(frame_kml_csv, text="Browse", image=browse_icon_ctk, compound="left", width=15, command=select_kml_file)
    button_select_file.grid(row=1, column=2, pady=10, padx=10, sticky='W')
    

    
    label_selected_file = tk.Label(frame_kml_csv, text="", bg="#ADD8E6", fg="black")
    label_selected_file.grid(row=1, column=1, padx=10, pady=10, sticky='w')
    
    label_zone_number = tk.Label(frame_kml_csv, text="UTM Zone Number:", bg="#ADD8E6", fg="black", font=("Helvetica", 9, "bold"))
    label_zone_number.grid(row=2, column=0, padx=10, pady=10, sticky='w')
    
    entry_zone_number = tk.Entry(frame_kml_csv, bg="#D3D3D3", fg="black", width=10, state=tk.DISABLED)
    entry_zone_number.grid(row=2, column=1, padx=5, pady=10, sticky='w')







    info_iconn = "C:/Users/Admin/Desktop/Tkinter/pratices/venv/image/info_icon.png"
    info_icon = Image.open(info_iconn)
    info_icon_ctk =  ctk.CTkImage(info_icon)
 
    info_button =ctk.CTkButton(frame_kml_csv, image=info_icon_ctk, text="", width=4, fg_color="#ADD8E6")
    info_button.grid(row=2, column=0, columnspan=2, padx=(2,10), pady=10, sticky='w')

    info_button.bind("<Enter>", show_info)

    info_button.bind("<Leave>", hide_info)    


    
    convert_icon = Image.open("C:/Users/Admin/Desktop/Tkinter/pratices/venv/image/convert.png")
    convert_icon = convert_icon.resize((20, 20), Image.LANCZOS)
    convert_icon_ctk = ctk.CTkImage(convert_icon)
    button_convert = customtkinter.CTkButton(frame_kml_csv, text="Convert", fg_color="green", width=20, image=convert_icon_ctk,  state=tk.DISABLED)
    button_convert.grid(row=4, column=1, sticky='w', padx=10, pady=20 )


    
#....................................Latitude longitude to easting and northing..........................................................................................................................
def open_convert_info():
    info_window = tk.Toplevel(window)
    info_window.title("Convert Data Information")
    info_window.geometry("600x500")
    info_label = tk.Label(info_window, text="Information about converting data goes here.", bg="#ADD8E6", fg="black")
    info_label.pack(expand=True, fill=tk.BOTH)

    






#.................................for rotation windows..................................................................................................................................................
def open_rotate_info():
    info_window = tk.Toplevel(window)
    info_window.title("Rotate Data Information")
    info_window.geometry("600x720")
    info_window.configure(bg="#ADD8E6")

    info_label_top = tk.Label(info_window, text="You can rotate your surveyed data to your desired angle. Suppose your data is not aligned with a Google image \n or other feature you want to align. You can use this feature to make your data align with Google overlay.\n For this, you need a base coordinate and an angle of rotation.", bg="#ADD8E6", fg="black")
    info_label_top.pack(pady=10)

    img1_path = "C:/Users/Admin/Desktop/Tkinter/pratices/venv/image/Brot.png"
    img2_path = "C:/Users/Admin/Desktop/Tkinter/pratices/venv/image/Arot.png"
    img3_path = "C:/Users/Admin/Desktop/Tkinter/pratices/venv/image/inputsample.png"

    img1 = Image.open(img1_path)
    img1 = img1.resize((200, 200), Image.Resampling.LANCZOS)
    img1_photo = ImageTk.PhotoImage(img1)

    img2 = Image.open(img2_path)
    img2 = img2.resize((200, 200), Image.Resampling.LANCZOS)
    img2_photo = ImageTk.PhotoImage(img2)

    images_frame = tk.Frame(info_window, bg="#ADD8E6")
    images_frame.pack(pady=10)

    label_img1 = tk.Label(images_frame, image=img1_photo, bg="#ADD8E6")
    label_img1.pack(side=tk.LEFT, padx=10)

    label_img2 = tk.Label(images_frame, image=img2_photo, bg="#ADD8E6")
    label_img2.pack(side=tk.LEFT, padx=10)

    label_img1.image = img1_photo
    label_img2.image = img2_photo

    info_label_bottom = tk.Label(info_window, text="As shown in the above image, point ID 1, 2 & 4 are rotated by an angle of 33 degrees clockwise about\n the base of point ID 3, And in order to perform this action you much have a csv file as show below image.", bg="#ADD8E6", fg="black")
    info_label_bottom.pack(pady=10)

    img3 = Image.open(img3_path)
    img3 = img3.resize((345, 247), Image.Resampling.LANCZOS)
    img3_photo = ImageTk.PhotoImage(img3)

    label_img3 = tk.Label(info_window, image=img3_photo, bg="#ADD8E6")
    label_img3.pack(pady=10)
    label_img3.image = img3_photo


    rotate_icon = Image.open("C:/Users/Admin/Desktop/Tkinter/pratices/venv/image/rotate.png")
    rotate_icon = rotate_icon.resize((20, 20), Image.LANCZOS)
    rotate_icon_ctk = ctk.CTkImage(rotate_icon)
    button_RT = ctk.CTkButton(info_window, text="Rotate Now", fg_color="#663399", image=rotate_icon_ctk, compound="left", width=15, command=lambda: open_rotate_window(info_window))
    button_RT.pack(pady=10)

    # button_RT = customtkinter.CTkButton(info_window, text="Rotate Now", fg_color="#663399", width=15, command=lambda: open_rotate_window(info_window))
    # button_RT.pack(pady=10)

def open_rotate_window(prev_window):
    #prev_window.withdraw()
    rotate_window = tk.Toplevel(window)
    rotate_window.title("Rotate Data")
    rotate_window.geometry("580x400")
    rotate_window.configure(bg="#ADD8E6")

    def rotate_csv(input_path, output_path, base_x, base_y, angle, direction):
        if direction == "Clockwise":
            angle = -angle
        df = pd.read_csv(input_path)
        serial_number = df.iloc[:, 0].astype(int)
        easting = df.iloc[:, 1].astype(float)
        northing = df.iloc[:, 2].astype(float)
        elevation = df.iloc[:, 3].astype(float) if len(df.columns) > 3 else None
        remark = df.iloc[:, 4].astype(str) if len(df.columns) > 4 else None

        elevation_column = [] if elevation is None else elevation
        remark_column = [] if remark is None else remark

        rotated_easting, rotated_northing = rotate_coordinates(easting, northing, base_x, base_y, angle)

        new_df = pd.DataFrame({
            df.columns[0]: serial_number,
            df.columns[1]: rotated_easting,
            df.columns[2]: rotated_northing,
        })

        if len(df.columns) > 3:
            new_df["Elevation"] = elevation_column
        if len(df.columns) > 4:
            new_df["Remark"] = remark_column

        original_heading = df.columns.tolist()
        new_df.columns = original_heading

        star_rotation_info = df.iloc[1, :]
        new_df.loc[1] = star_rotation_info

        new_df.to_csv(output_path, index=False)

    def rotate_coordinates(easting, northing, base_x, base_y, angle):
        angle_rad = np.radians(angle)
        rotated_easting = (easting - base_x) * np.cos(angle_rad) - (northing - base_y) * np.sin(angle_rad) + base_x
        rotated_northing = (easting - base_x) * np.sin(angle_rad) + (northing - base_y) * np.cos(angle_rad) + base_y
        return rotated_easting, rotated_northing

    def rotate_data():
        input_path = entry_input_path.get()
        base_x = float(entry_base_x.get())
        base_y = float(entry_base_y.get())
        angle = float(entry_angle.get())
        direction = rotation_direction.get()

        output_path = asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if output_path:
            rotate_csv(input_path, output_path, base_x, base_y, angle, direction)
            messagebox.showinfo("SUCCESSFULL!!", "Successfully Rotated \n CSV data has been rotated and saved successfully.")
        else:
            messagebox.showwarning("Warning", "Output file not selected. Rotation cancelled.")

    def select_input_file():
        file_path = askopenfilename(filetypes=[("CSV files", "*.csv")])
        entry_input_path.delete(0, tk.END)
        entry_input_path.insert(0, file_path)

    # Labels and entry widgets
    # Info = tk.Label(rotate_window, text="Rotate your data from this window")
    # Info.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
    Info = ctk.CTkLabel(rotate_window, text="                    Rotate your data from this window                   ", font=("Helvetica", 14, "bold"), fg_color="#000000", bg_color='#ADD8E6')
    Info.grid(row=0, column=0, columnspan=2, padx=5, pady=5)


    label_input_path = tk.Label(rotate_window, text="Input CSV File:", background='#ADD8E6', font=("Helvetica", 9, "bold"))
    label_input_path.grid(row=1, column=0, padx=5, pady=5, sticky='e')
    entry_input_path = tk.Entry(rotate_window, width=40)
    entry_input_path.grid(row=1, column=1, padx=5, pady=5)

    browse_icon_path = "C:/Users/Admin/Desktop/Tkinter/pratices/venv/image/browse.png"
    browse_icon = Image.open(browse_icon_path)
    browse_icon_ctk = ctk.CTkImage(browse_icon)
    button_input_path = ctk.CTkButton(rotate_window, text="Browse", image=browse_icon_ctk, compound="left", width=15 , border_color='#FFCC70', command=select_input_file)
    button_input_path.grid(row=1, column=2, pady=5, padx=5)

    # button_input_path = tk.Button(rotate_window, text="Browse", command=select_input_file)
    # button_input_path.grid(row=0, column=2, padx=5, pady=5)

    label_base_x = tk.Label(rotate_window, text="Base Easting in (m):", background='#ADD8E6', font=("Helvetica", 9, "bold"))
    label_base_x.grid(row=2, column=0, padx=5, pady=5, sticky='e')
    entry_base_x = tk.Entry(rotate_window)
    entry_base_x.grid(row=2, column=1, padx=5, pady=5)

    label_base_y = tk.Label(rotate_window, text="Base Northing (m):", background='#ADD8E6', font=("Helvetica", 9, "bold"))
    label_base_y.grid(row=3, column=0, padx=5, pady=5, sticky='e')
    entry_base_y = tk.Entry(rotate_window)
    entry_base_y.grid(row=3, column=1, padx=5, pady=5)

    label_angle = tk.Label(rotate_window, text="Rotation Angle (degrees):", font=("Helvetica", 9, "bold"), background='#ADD8E6')
    label_angle.grid(row=4, column=0, padx=5, pady=5, sticky='e')
    entry_angle = tk.Entry(rotate_window)
    entry_angle.grid(row=4, column=1, padx=5, pady=5)

    label_direction = tk.Label(rotate_window, text="Rotation Direction:", font=("Helvetica", 9, "bold"), background='#ADD8E6')
    label_direction.grid(row=5, column=0, padx=5, pady=5, sticky='e')
    rotation_direction = ttk.Combobox(rotate_window, values=["Clockwise", "Anticlockwise"])
    rotation_direction.grid(row=5, column=1, padx=5, pady=5)
    rotation_direction.set("Clockwise")


    rotate_icon = Image.open("C:/Users/Admin/Desktop/Tkinter/pratices/venv/image/rotate.png")
    rotate_icon = rotate_icon.resize((20, 20), Image.LANCZOS)
    rotate_icon_ctk = ctk.CTkImage(rotate_icon)
    button_submit = ctk.CTkButton(rotate_window, text="Rotate Now", fg_color="green", image=rotate_icon_ctk, compound="left", width=15, command= rotate_data)
    button_submit.grid(row=6, column=1, pady=20)

    # button_submit =customtkinter.CTkButton (rotate_window, text="Rotate", fg_color="green", width=30,  command=rotate_data)
    # button_submit.grid(row=6, column=0, columnspan=3, pady=20)


#...................................................this is for Lat long to east northing..............................................................


# Function to convert latitude and longitude to UTM
def latlon_to_utm(lat, lon, proj_utm):
    easting, northing = proj_utm(lon, lat)
    return easting, northing

# Function to handle the conversion
def convert_latlon_to_utm():
    # Check if the zone number is valid
    zone_number = utm_zone_entry.get()
    if not zone_number.isdigit():
        messagebox.showerror("Error", "Invalid UTM zone number")
        return

    zone_number = int(zone_number)

    # Define the projection for the given UTM zone
    proj_utm = Proj(proj="utm", zone=zone_number, datum="WGS84", south=False)

    # Convert the coordinates
    utm_coords = [latlon_to_utm(lat, lon, proj_utm) for lat, lon in zip(df['latitude'], df['longitude'])]
    utm_coords_df = pd.DataFrame(utm_coords, columns=['easting', 'northing'])

    # Create a new DataFrame with the required structure
    output_df = pd.DataFrame({
        'serial_number': range(1, len(df) + 1),
        'easting': utm_coords_df['easting'],
        'northing': utm_coords_df['northing'],
        'elevation': df['elevation'],
        'remarks': 'GP'
    })

    # Ask user for the location to save the output CSV file
    output_file = filedialog.asksaveasfilename(title="Save the output CSV file",
                                               defaultextension=".csv",
                                               filetypes=[("CSV Files", "*.csv")])
    if not output_file:
        messagebox.showerror("Error", "Output file not selected")
        return

    # Save the output to a new CSV file
    output_df.to_csv(output_file, index=False)
    messagebox.showinfo("Success", "File converted and saved successfully")

# Function to open the lat/lon to UTM conversion window
def open_latlon_to_utm_window(parent):
    conversion_window = tk.Toplevel(parent)
    conversion_window.title("Lat/Lon to UTM Conversion")
    conversion_window.geometry("450x300")
    conversion_window.configure(bg="#008080")

    convert_frame = customtkinter.CTkFrame(conversion_window)
    convert_frame.pack(padx=20, pady=20)

    # UTM zone number input
    F_label = customtkinter.CTkLabel(convert_frame, text="CSV file should have three columns where \n latitude, longitude & elevation are 1st, 2nd& 3rd column respectively")
    F_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)



    utm_zone_label = customtkinter.CTkLabel(convert_frame, text="           Enter UTM Zone Number:")
    utm_zone_label.grid(row=1, column=0, padx=10, pady=10)
    global utm_zone_entry
    utm_zone_entry = customtkinter.CTkEntry(convert_frame)
    utm_zone_entry.grid(row=1, column=1, padx=10, pady=10)

    
    info_iconn = "C:/Users/Admin/Desktop/Tkinter/pratices/venv/image/info_icon.png"
    info_icon = Image.open(info_iconn)
    info_icon_ctk =  ctk.CTkImage(info_icon)
 
    info_button =ctk.CTkButton(convert_frame, image=info_icon_ctk, text="", width=4, fg_color= None)
    info_button.grid(row=1, column=0, columnspan=2, padx=(2,10), pady=10, sticky='w')

    info_button.bind("<Enter>", show_info)

    info_button.bind("<Leave>", hide_info)    

    # CSV file selection
    def select_csv_file():
        global input_file
        input_file = filedialog.askopenfilename(title="Select the input CSV file",
                                                filetypes=[("CSV Files", "*.csv")])
        if not input_file:
            messagebox.showerror("Error", "Input file not selected")
            return
        global df
        df = pd.read_csv(input_file)
        file_label.configure(text=input_file)


    File_label = customtkinter.CTkLabel(convert_frame, text="Select CSV file :")
    File_label.grid(row=2, column=0, padx=10, pady=10)

    browse_icon_path = "C:/Users/Admin/Desktop/Tkinter/pratices/venv/image/browse.png"
    browse_icon = Image.open(browse_icon_path)
    browse_icon_ctk = ctk.CTkImage(browse_icon)
    button_input_path = ctk.CTkButton(convert_frame, text="Browse", image=browse_icon_ctk, compound="left", width=15 , border_color='#FFCC70', command=select_csv_file)
    button_input_path.grid(row=2, column=1, pady=5, padx=5)

    # file_button = customtkinter.CTkButton(convert_frame, text="Browse", command=select_csv_file)
    # file_button.grid(row=1, column=1, padx=10, pady=10)



    file_label = customtkinter.CTkLabel(convert_frame, text="")
    file_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    convert_icon = Image.open("C:/Users/Admin/Desktop/Tkinter/pratices/venv/image/convert.png")
    convert_icon = convert_icon.resize((20, 20), Image.LANCZOS)
    convert_icon_ctk = ctk.CTkImage(convert_icon)
    button_kml = customtkinter.CTkButton(convert_frame, text="Convert", fg_color="#663399", width=20, image=convert_icon_ctk, compound="left", command=convert_latlon_to_utm)
    button_kml.grid(row=4, column=0, columnspan=2, pady=10)







#........................................................this is main window section..................................................................................   
window = tk.Tk()
main_icon_path = "C:/Users/Admin/Desktop/Tkinter/pratices/venv/image/Icon.png"
main_icon = Image.open(main_icon_path)
main_icon_resized = main_icon.resize((20, 20), Image.LANCZOS)

main_icon_photo = ImageTk.PhotoImage(main_icon_resized)
window.iconphoto(True, main_icon_photo )


window.geometry("600x550")
window.title("DataRefiner")
window.configure(bg="#008080")

frame = tk.Frame(window, bg="#008080")
frame.pack(fill=tk.BOTH, expand=True)





menu_bar = tk.Menu(window)
window.config(menu=menu_bar)

sub_heading1 = tk.Menu(menu_bar, tearoff=0)
sub_heading2 = tk.Menu(menu_bar, tearoff=0)
sub_heading3 = tk.Menu(menu_bar, tearoff=0)

sub_heading1.add_command(label="Rotate Data", command=lambda: open_rotate_window(window))
sub_heading2.add_command(label="Shift Data", command=lambda: open_shift_window(window))
sub_heading3.add_command(label="KML to CSV", command=lambda: open_kml_csv(window)) 

menu_bar.add_cascade(label="Rotate", menu=sub_heading1)
menu_bar.add_cascade(label="Shift", menu=sub_heading2)
menu_bar.add_cascade(label="Convert", menu=sub_heading3)
menu_bar.add_command(label="About Us", command=show_about)

frame_height = 150
frame.columnconfigure(0, weight=1)

font = tkFont.Font(family="Helvetica", size=12, weight="bold")

rotation_frame = tk.LabelFrame(frame, text="Rotate data", font=font, height=frame_height, bg="#ADD8E6", fg="black")
rotation_frame.grid(row=0, column=0, padx=5, pady=10, sticky='ew')
rotation_frame.grid_propagate(False)

information = tk.Label(rotation_frame, text="Rotate your data about the desired base and rotation angle of required.", bg="#ADD8E6", fg="black")
information.grid(row=0, column=0)



rotate_icon = Image.open("C:/Users/Admin/Desktop/Tkinter/pratices/venv/image/rotate.png")
rotate_icon = rotate_icon.resize((20, 20), Image.LANCZOS)
rotate_icon_ctk = ctk.CTkImage(rotate_icon)
button_rotate = ctk.CTkButton(rotation_frame, text="Rotate Data", fg_color="#663399", image=rotate_icon_ctk, compound="left", width=15, command=open_rotate_info)
button_rotate.grid(row=1, column=0, sticky='w')

for widget in rotation_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

Shift_frame = tk.LabelFrame(frame, text="Shift data", font=font, height=frame_height, bg="#ADD8E6", fg="black")
Shift_frame.grid(row=1, column=0, padx=5, pady=10, sticky='ew')
Shift_frame.grid_propagate(False)

information = tk.Label(Shift_frame, text="Shift your whole data by constant Easting and Northing.", bg="#ADD8E6", fg="black")
information.grid(row=0, column=0)



shift_icon = Image.open("C:/Users/Admin/Desktop/Tkinter/pratices/venv/image/shift.png")
shift_icon = shift_icon.resize((20, 20), Image.LANCZOS)
shift_icon_ctk = ctk.CTkImage(shift_icon)
button_shift = ctk.CTkButton(Shift_frame, text="Shift Data", fg_color="#663399", width=15, image=shift_icon_ctk, compound="left", command=open_shift_info)
button_shift.grid(row=1, column=0, sticky='w')



for widget in Shift_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

convert_frame = tk.LabelFrame(frame, text="Convert Data", font=font, height=frame_height, bg="#ADD8E6", fg="black")
convert_frame.grid(row=2, column=0, padx=5, pady=10, sticky='ew')
convert_frame.grid_propagate(False)

information = tk.Label(convert_frame, text="Conversion option available.", bg="#ADD8E6", fg="black")
information.grid(row=0, column=0)
information = tk.Label(convert_frame, text="Convert KML To NEZ", bg="#ADD8E6", fg="black")
information.grid(row=1, column=0)


convert_icon = Image.open("C:/Users/Admin/Desktop/Tkinter/pratices/venv/image/convert.png")
convert_icon = convert_icon.resize((20, 20), Image.LANCZOS)
convert_icon_ctk = ctk.CTkImage(convert_icon)
button_kml = customtkinter.CTkButton(convert_frame, text="Convert", fg_color="#663399", width=20, image=convert_icon_ctk, compound="left", command=lambda: open_kml_csv(window))
button_kml.grid(row=1, column=1, sticky='w')


information = tk.Label(convert_frame, text="Convert Lat/Lon To UTM(N,E)", bg="#ADD8E6", fg="black")
information.grid(row=2, column=0)


convert_icon = Image.open("C:/Users/Admin/Desktop/Tkinter/pratices/venv/image/convert.png")
convert_icon = convert_icon.resize((20, 20), Image.LANCZOS)
convert_icon_ctk = ctk.CTkImage(convert_icon)
button_kml = customtkinter.CTkButton(convert_frame, text="Convert", fg_color="#663399", width=20, image=convert_icon_ctk, compound="left", command=lambda: open_latlon_to_utm_window(window))#change function
button_kml.grid(row=2, column=1, sticky='w')

information = tk.Label(convert_frame, text="Convert Lat/Lon To UTM(N,E)", bg="#ADD8E6", fg="black")
information.grid(row=2, column=0)



for widget in convert_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)



footer = tk.Frame(window, bg="#008080")
footer.pack(side=tk.BOTTOM, fill=tk.X)
footer_label = tk.Label(footer, text="© 2024 DataRefiner | Version 1.0", bg="#008080", fg="white", font=font)
footer_label.pack(pady=5)







window.mainloop()
