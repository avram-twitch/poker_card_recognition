import tensorflow as tf
import os
import re


class ImageCoder(object):

    def __init__(self):
        self._sess = tf.Session()
        self._decode_jpeg_data = tf.placeholder(dtype=tf.string)
        self._decode_jpeg = tf.image.decode_jpeg(self._decode_jpeg_data, channels=3)

    def decode_jpeg(self, image_data):
        image = self._sess.run(
            self._decode_jpeg,
            feed_dict={self._decode_jpeg_data: image_data})
        assert len(image.shape) == 3
        assert image.shape[2] == 3
        return image



def _int64_feature(value):
    if not isinstance(value, list):
        value = [value]

    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))


def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def _convert_to_example(filename, image_buffer, label, text, height, width):
    colorspace = 'RGB'
    channels = 3
    image_format = 'JPEG'

    example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': _int64_feature(height),
        'image/width': _int64_feature(width),
        'image/colorspace': _bytes_feature(tf.compat.as_bytes(colorspace)),
        'image/channels': _int64_feature(channels),
        'image/class/label': _int64_feature(label),
        'image/class/text': _bytes_feature(tf.compat.as_bytes(text)),
        'image/format': _bytes_feature(tf.compat.as_bytes(image_format)),
        'image/filename': _bytes_feature(tf.compat.as_bytes(os.path.basename(filename))),
        'image/encoded': _bytes_feature(tf.compat.as_bytes(image_buffer))}))

    return example


def _process_image(filename, coder):

    with tf.gfile.FastGFile(filename, 'rb') as f:
        image_data = f.read()

    image = coder.decode_jpeg(image_data)

    assert len(image.shape) == 3
    height = image.shape[0]
    width = image.shape[1]
    assert image.shape[2] == 3

    return image_data, height, width


def _get_label_text(filename, text_to_label_mapping):
    text = re.search(r'cards-\[([HDCSW].)\].*jpg', filename).group(1)
    if "W" in text:
        return None, None
    label = text_to_label_mapping[text.lower()]
    return int(label), text

def _get_mapper(map_fp):
    out = {}
    with open(map_fp) as f:
        for line in f:
            label, text = line.split(": ")
            out[text.strip().lower()] = label
    return out


def _get_filenames(in_directory):
    out = []
    for start, dirs, files in os.walk(in_directory):
        for name in files:
            out.append(os.path.join(in_directory, name))
    
    return out

if __name__ == '__main__':
    coder = ImageCoder()
    directory = "./raw_jpgs"
    out_directory = "./out_jpgs/"
    files = _get_filenames(directory)
    mapper = _get_mapper("./labels.txt")
    output_file = os.path.join(out_directory, "data.tfr")
    writer = tf.python_io.TFRecordWriter(output_file)

    for fp in files:
        label, text = _get_label_text(fp, mapper)
        if label is None:
            continue
        image_buffer, height, width = _process_image(fp, coder)
        example = _convert_to_example(fp, image_buffer, label, text, height, width)
        writer.write(example.SerializeToString())

    writer.close()
