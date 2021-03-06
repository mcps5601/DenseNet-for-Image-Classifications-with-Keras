# -*- coding: utf-8 -*-
"""
Created on Fri May 25 09:01:50 2018

@author: Dean
"""
import keras
import argparse
import numpy as np

from keras import backend as K
from keras.layers import Input, Conv2D, MaxPooling2D, Conv2DTranspose, Dropout, Add
from keras.activations import softmax
from keras.models import Model
from keras.utils import to_categorical
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard
from keras.preprocessing.image import ImageDataGenerator
from keras.applications import DenseNet121
from keras.utils import multi_gpu_model

from keras import layers
from keras.layers import Dense
from keras.layers import Activation
from keras.layers import Flatten
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import GlobalMaxPooling2D
from keras.layers import ZeroPadding2D
from keras.layers import AveragePooling2D
from keras.layers import GlobalAveragePooling2D
from keras.layers import BatchNormalization
from keras.engine.topology import get_source_inputs

dir_path = '/home/data/dean/imagebank/PXR/'
output_dir = '/home/data/dean/weights/'
batch_size = 8
epochs = 1000

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DeanKerasModel')
    parser.add_argument('action', choices=['train','test'])
    args = parser.parse_args()


# Image Preprocessing
print("** create image generators **")
train_generator = ImageDataGenerator(
        horizontal_flip=True,
        vertical_flip=True,
        rotation_range=10,
        zoom_range=0.1)

validation_generator = ImageDataGenerator(
        horizontal_flip=True,
        vertical_flip=True,
        rotation_range=10,
        zoom_range=0.1)

test_generator = ImageDataGenerator()

# callbacks
callbacks = [
    ModelCheckpoint(dir_path, monitor='val_loss', 
                    verbose=0, save_best_only=False, 
                    save_weights_only=False, mode='auto', period=1),
    TensorBoard(log_dir='./logs', histogram_freq=0, batch_size,
                write_graph=True, write_grads=False, write_images=False, 
                embeddings_freq=0, embeddings_layer_names=None,
                embeddings_metadata=None)]

if args.action == 'train':
    train_batches = ImageDataGenerator().flow_from_directory(dir_path, 
                                  target_size=(512,512), batch_size,
                                  color_mode = 'grayscale', class_mode = 'categorical')
    
if args.action == 'test':
    test_batches = ImageDataGenerator().flow_from_directory(dir_path, 
                                  target_size=(512,512), batch_size,
                                  color_mode = 'grayscale', class_mode = 'categorical')

# create the model
print("** load model **")
model = DenseNet121(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=2)
# multi_gpu_model(model, gpus='none')

# compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['categorical_accuracy'])

# fit the model with data
print("** start training **")
model.fit_generator(
        generator=train_generator.flow_from_directory(
                dir_path, target_size=(512,512), batch_size,
                color_mode = 'grayscale', class_mode = 'categorical'),
        steps_per_epochs = round(1000/batch_size)*2, epochs = epochs,
        validation_data = validation_generator.flow_from_directory(
                dir_path, target_size=(512,512), batch_size,
                color_mode = 'grayscale', class_mode = 'categorical'),
        callbacks = callbacks)

# evaluation
print("** start evaluating test set **")
#results = new_model.evaluate_generator(test_generator.flow_from_directory(

model.save(os.path.join(output_dir, "final_weights.h5"))

#def identity_block(input_tensor, kernel_size, filters, stage, block):
#  
#    filters1, filters2, filters3 = filters
#    if K.image_data_format() == 'channels_last':
#        bn_axis = 3
#    else:
#        bn_axis = 1
#    conv_name_base = 'res' + str(stage) + block + '_branch'
#    bn_name_base = 'bn' + str(stage) + block + '_branch'
#
#    x = Conv2D(filters1, (1, 1), name=conv_name_base + '2a')(input_tensor)
#    x = BatchNormalization(axis=bn_axis, name=bn_name_base + '2a')(x)
#    x = Activation('relu')(x)
#
#    x = Conv2D(filters2, kernel_size,
#               padding='same', name=conv_name_base + '2b')(x)
#    x = BatchNormalization(axis=bn_axis, name=bn_name_base + '2b')(x)
#    x = Activation('relu')(x)
#
#    x = Conv2D(filters3, (1, 1), name=conv_name_base + '2c')(x)
#    x = BatchNormalization(axis=bn_axis, name=bn_name_base + '2c')(x)
#
#    x = layers.add([x, input_tensor])
#    x = Activation('relu')(x)
#    return x
#
#def conv_block(input_tensor, kernel_size, filters, stage, block, strides=(2, 2)):
#   
#    filters1, filters2, filters3 = filters
#    if K.image_data_format() == 'channels_last':
#        bn_axis = 3
#    else:
#        bn_axis = 1
#    conv_name_base = 'res' + str(stage) + block + '_branch'
#    bn_name_base = 'bn' + str(stage) + block + '_branch'
#
#    x = Conv2D(filters1, (1, 1), strides=strides,
#               name=conv_name_base + '2a')(input_tensor)
#    x = BatchNormalization(axis=bn_axis, name=bn_name_base + '2a')(x)
#    x = Activation('relu')(x)
#
#    x = Conv2D(filters2, kernel_size, padding='same',
#               name=conv_name_base + '2b')(x)
#    x = BatchNormalization(axis=bn_axis, name=bn_name_base + '2b')(x)
#    x = Activation('relu')(x)
#
#    x = Conv2D(filters3, (1, 1), name=conv_name_base + '2c')(x)
#    x = BatchNormalization(axis=bn_axis, name=bn_name_base + '2c')(x)
#
#    shortcut = Conv2D(filters3, (1, 1), strides=strides,
#                      name=conv_name_base + '1')(input_tensor)
#    shortcut = BatchNormalization(axis=bn_axis, name=bn_name_base + '1')(shortcut)
#
#    x = layers.add([x, shortcut])
#    x = Activation('relu')(x)
#    return x
#
#def ResNet50(include_top=True, weights=None,
#             input_tensor=None, input_shape=None,
#             pooling=None,
#             classes=2):
#    """Instantiates the ResNet50 architecture.
#    Optionally loads weights pre-trained
#    on ImageNet. Note that when using TensorFlow,
#    for best performance you should set
#    `image_data_format="channels_last"` in your Keras config
#    at ~/.keras/keras.json.
#    The model and the weights are compatible with both
#    TensorFlow and Theano. The data format
#    convention used by the model is the one
#    specified in your Keras config file.
#    # Arguments
#        include_top: whether to include the fully-connected
#            layer at the top of the network.
#        weights: one of `None` (random initialization)
#            or "imagenet" (pre-training on ImageNet).
#        input_tensor: optional Keras tensor (i.e. output of `layers.Input()`)
#            to use as image input for the model.
#        input_shape: optional shape tuple, only to be specified
#            if `include_top` is False (otherwise the input shape
#            has to be `(224, 224, 3)` (with `channels_last` data format)
#            or `(3, 224, 244)` (with `channels_first` data format).
#            It should have exactly 3 inputs channels,
#            and width and height should be no smaller than 197.
#            E.g. `(200, 200, 3)` would be one valid value.
#        pooling: Optional pooling mode for feature extraction
#            when `include_top` is `False`.
#            - `None` means that the output of the model will be
#                the 4D tensor output of the
#                last convolutional layer.
#            - `avg` means that global average pooling
#                will be applied to the output of the
#                last convolutional layer, and thus
#                the output of the model will be a 2D tensor.
#            - `max` means that global max pooling will
#                be applied.
#        classes: optional number of classes to classify images
#            into, only to be specified if `include_top` is True, and
#            if no `weights` argument is specified.
#    # Returns
#        A Keras model instance.
#    # Raises
#        ValueError: in case of invalid argument for `weights`,
#            or invalid input shape.
#    """
#    if weights not in {'imagenet', None}:
#        raise ValueError('The `weights` argument should be either '
#                         '`None` (random initialization) or `imagenet` '
#                         '(pre-training on ImageNet).')
#
#    #if weights == 'imagenet' and include_top and classes != 15:
#    #    raise ValueError('If using `weights` as imagenet with `include_top`'
#    #                     ' as true, `classes` should be 15')
#
#    # Determine proper input shape
#    
#    input_shape = _obtain_input_shape(input_shape,
#                                      default_size=256,
#                                      min_size=197,
#                                      data_format=K.image_data_format(),
#                                      require_flatten=include_top)
#    
#
#    if input_tensor is None:
#        img_input = Input(shape=input_shape)
#    else:
#        if not K.is_keras_tensor(input_tensor):
#            img_input = Input(tensor=input_tensor, shape=input_shape)
#        else:
#            img_input = input_tensor
#    if K.image_data_format() == 'channels_last':
#        bn_axis = 3
#    else:
#        bn_axis = 1
#
#    x = ZeroPadding2D((3, 3))(img_input)
#    x = Conv2D(64, (7, 7), strides=(2, 2), name='conv1')(x)
#    x = BatchNormalization(axis=bn_axis, name='bn_conv1')(x)
#    x = Activation('relu')(x)
#    x = MaxPooling2D((3, 3), strides=(2, 2))(x)
#
#    x = conv_block(x, 3, [64, 64, 256], stage=2, block='a', strides=(1, 1))
#    x = identity_block(x, 3, [64, 64, 256], stage=2, block='b')
#    x = identity_block(x, 3, [64, 64, 256], stage=2, block='c')
#
#    x = conv_block(x, 3, [128, 128, 512], stage=3, block='a')
#    x = identity_block(x, 3, [128, 128, 512], stage=3, block='b')
#    x = identity_block(x, 3, [128, 128, 512], stage=3, block='c')
#    x = identity_block(x, 3, [128, 128, 512], stage=3, block='d')
#
#    x = conv_block(x, 3, [256, 256, 1024], stage=4, block='a')
#    x = identity_block(x, 3, [256, 256, 1024], stage=4, block='b')
#    x = identity_block(x, 3, [256, 256, 1024], stage=4, block='c')
#    x = identity_block(x, 3, [256, 256, 1024], stage=4, block='d')
#    x = identity_block(x, 3, [256, 256, 1024], stage=4, block='e')
#    x = identity_block(x, 3, [256, 256, 1024], stage=4, block='f')
#
#    x = conv_block(x, 3, [512, 512, 2048], stage=5, block='a')
#    x = identity_block(x, 3, [512, 512, 2048], stage=5, block='b')
#    x = identity_block(x, 3, [512, 512, 2048], stage=5, block='c')
#
#    x = AveragePooling2D((7, 7), name='avg_pool')(x)
#
#    if include_top:
#        x = Flatten()(x)
#        x = Dense(classes, activation='softmax', name='fc2')(x)
#    else:
#        if pooling == 'avg':
#            x = GlobalAveragePooling2D()(x)
#        elif pooling == 'max':
#            x = GlobalMaxPooling2D()(x)
#
#    # Ensure that the model takes into account
#    # any potential predecessors of `input_tensor`.
#    if input_tensor is not None:
#        inputs = get_source_inputs(input_tensor)
#    else:
#        inputs = img_input
#    # Create model.
#    model = Model(inputs, x, name='resnet50')
#
#    return model