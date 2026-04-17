from PIL import Image


def set_background(app, ctk, config):
    global bg_label

    image_path = config.get("background", "assets/image.png")

    try:
        image = Image.open(image_path)
    except:
        image = Image.open("assets/image.png")

    bg_image = ctk.CTkImage(
        image,
        size=(app.winfo_screenwidth(), app.winfo_screenheight())
    )

    bg_label = ctk.CTkLabel(app, image=bg_image, text="")
    bg_label.image = bg_image

    bg_label.place(x=0, y=0, relwidth=1, relheight=1)


    bg_label.lower()