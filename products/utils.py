from PIL import Image
from io import BytesIO


def create_thumbnail(instance, data):
    image_data = data['photo']
    image = Image.open(image_data)
    
    max_width = 200
    width_percent = (max_width / float(image.size[0]))
    new_height = int((float(image.size[1]) * float(width_percent)))

    image.thumbnail((max_width, new_height))

    thumb_io = BytesIO()
    image.save(thumb_io, format='JPEG')

    thumbnail_name = instance.photo.name.split('/')[-1]

    instance.photo_thumbnail.save(thumbnail_name, thumb_io)
