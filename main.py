import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import math
from PIL import Image

charset = ['#', 'm', 'c', 'f', '1', '^', ':', "."]

default_font = ("Courier", 10)
small_default_font = ("Courier", 5)

def load_image():
    print("Loading image")
    filename = fd.askopenfilename()
    global loaded_image_path
    global load_image_label

    loaded_image_path = filename
    load_image_label.configure(text=loaded_image_path)


def generate_ascii():
    print("Generating ASC-II")
    global loaded_image_path
    global size_scale

    with Image.open(loaded_image_path) as im:
        im = im.convert('L')
        output_string = ""
        output_scaling = int((100/size_scale.get()))

        for i in range(0, im.height, output_scaling):
            for j in range(0, im.width, output_scaling):
                lum = im.getpixel((j, i))/255
                try:
                    value = charset[math.ceil(lum*len(charset))-1]
                except IndexError:
                    print(f"Error for i={i}, j={j}:\nvalue = charset[math.floor({lum}*{len(charset)}]\n"
                          f"-> value = charset[math.floor({lum*len(charset)})")
                output_string += value
            output_string += "\n"

        # cleaning previous output
        ascii_output.delete(1.0, tk.END)

        # prevents too large output
        if im.width/output_scaling > 200 or im.height/output_scaling > 100:
            infobox = mb.showinfo("Output too large", message="Output is too big for preview mode. Please use the "
                                                              ".txt file output method when generating ASC-II or "
                                                              "use a smaller resolution.")
        else:
            # resizing text widget to new size for output
            ascii_output.configure(width=math.ceil(im.width / output_scaling),
                                   height=math.floor(im.height / output_scaling))

            # insert new text
            ascii_output.insert(tk.END, output_string)

            # zoom-out if large output
            if im.width/output_scaling > 100 or im.height/output_scaling > 50:
                ascii_output.configure(font=small_default_font)
            else:
                ascii_output.configure(font=default_font)

        im.close()





loaded_image_path = ""

root = tk.Tk()
root.title("Pic to ASC-II")
root.geometry("1200x800")

main_frame = tk.Frame(root)
main_frame.pack(expand=True)

left_frame = tk.Frame(main_frame)
left_frame.grid(row=0, column=0)

load_image_button = tk.Button(left_frame)
load_image_button.configure(text="Load Image", command=lambda: load_image())
load_image_button.grid(row=0, column=0, pady=2)

load_image_label = tk.Label(left_frame)
load_image_label.configure(text="<...>")
load_image_label.grid(row=1, column=0, pady=0)

size_scale = tk.Scale(left_frame, length=120, tickinterval=100, label="output size (in %)", from_=1,
                      orient="horizontal", sliderlength=10)
size_scale.set(10)
size_scale.grid(row=2, column=0, pady=4)

generate_image_button = tk.Button(left_frame)
generate_image_button.configure(text="Generate ASC-II", command=lambda: generate_ascii())
generate_image_button.grid(row=3, column=0, pady=6)

ascii_frame = tk.Frame(main_frame)
ascii_frame.configure(relief="sunken", borderwidth=1)
ascii_frame.grid(row=0, column=1, padx=20, pady=12)
ascii_frame.grid_anchor("center")

ascii_output = tk.Text(ascii_frame)
ascii_output.configure(width=50, height=20, font=default_font)
ascii_output.pack()


root.mainloop()


