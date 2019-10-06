import tensorflow as tf
import os
import re
# import pandas as pd
import csv


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


def _float_feature(value):
    if not isinstance(value, list):
        value = [value]

    return tf.train.Feature(float_list=tf.train.FloatList(value=value))

def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def _convert_to_example(row, directory, coder):
    colorspace = 'RGB'
    channels = 3
    image_format = 'JPEG'
    image_buffer = _process_image(os.path.join(directory, row['filename']), coder)
    xmin = float(row['xmin']) / float(row['width'])
    ymin = float(row['ymin']) / float(row['height'])
    xmax = float(row['xmax']) / float(row['width'])
    ymax = float(row['ymax']) / float(row['height'])

    example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': _int64_feature(int(row['height'])),
        'image/width': _int64_feature(int(row['width'])),
        'image/colorspace': _bytes_feature(tf.compat.as_bytes(colorspace)),
        'image/channels': _int64_feature(channels),
        'image/class/label': _int64_feature(int(row['label'])),
        'image/class/text': _bytes_feature(tf.compat.as_bytes(row['text'])),
        'image/format': _bytes_feature(tf.compat.as_bytes(image_format)),
        'image/filename': _bytes_feature(tf.compat.as_bytes(os.path.basename(row['filename']))),
        'image/object/bbox/xmin': _float_feature(xmin),
        'image/object/bbox/xmax': _float_feature(xmax),
        'image/object/bbox/ymin': _float_feature(ymin),
        'image/object/bbox/ymax': _float_feature(ymax),
        'image/encoded': _bytes_feature(tf.compat.as_bytes(image_buffer))}))

    return example

def _process_image(filename, coder):

    with tf.gfile.FastGFile(filename, 'rb') as f:
        image_data = f.read()

    image = coder.decode_jpeg(image_data)

    assert len(image.shape) == 3
    assert image.shape[2] == 3

    return image_data


if __name__ == '__main__':
    metadata_csv_fp = "./data.csv"

    coder = ImageCoder()
    writer = tf.python_io.TFRecordWriter("data.record")

    with open(metadata_csv_fp) as f:
        reader = csv.reader(f, delimiter=",")
        first = True

        for row in reader:
            if first:
                first = False
                continue
            dict_row = {
                "filename": row[0],
                "width": row[1],
                "height": row[2],
                "label": row[3],
                "text": row[4],
                "xmin": row[5],
                "ymin": row[6],
                "xmax": row[7],
                "ymax": row[8]
            }
            example = _convert_to_example(dict_row, "./raw_jpgs", coder)
            writer.write(example.SerializeToString())

    writer.close()
