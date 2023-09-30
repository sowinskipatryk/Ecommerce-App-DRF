from PIL import Image
from io import BytesIO


def create_thumbnail(instance, data):
    if 'photo' in data:
        image = Image.open(BytesIO(data['photo'].read()))

        max_width = 200
        width_percent = (max_width / float(image.size[0]))
        new_height = int((float(image.size[1]) * float(width_percent)))

        image.thumbnail((max_width, new_height), Image.ANTIALIAS)

        thumb_io = BytesIO()
        image.save(thumb_io, format='JPEG')

        instance.photo.save(instance.photo.name, thumb_io)
