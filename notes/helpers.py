from PIL import Image


def image_resize(img_input, img_output, max_size):
    """
    Resizes input image so that longest side is equal to max_size
    img_input, img_output - pathes for input and output files
    max_size - length in pixels
    """

    # Read file
    image = Image.open(img_input).convert('RGB')
    image_size = image.size

    # Resize
    ratio = max_size / max(image_size[0], image_size[1])
    new_size = (int(image_size[0]*ratio), int(image_size[1]*ratio))
    image = image.resize(new_size, Image.ANTIALIAS)

    # Save to disk
    image.save(img_output, format='JPEG')

    return image
