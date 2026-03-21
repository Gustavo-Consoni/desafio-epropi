from core.utils import hashed_name


def product_image_path(instance, filename):
    return hashed_name(instance, filename, "product_images")
