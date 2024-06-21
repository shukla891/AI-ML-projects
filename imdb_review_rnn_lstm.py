# -*- coding: utf-8 -*-
"""IMDB Review_RNN_LSTM.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1T2_V7eb0hSVMhyH9Y8e0vLSYuXm-5eBI

Reviews have been given to movies in a sentence may bei in many no of words and then these reviews have been clasified as a positive(1) and negative(0). Reviews shown here in form of integers.

**Importing libraries**
"""

import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""**Data Preprocessing**"""

#importing dataset
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences

#loading dataset
(x_train,y_train),(x_test,y_test)=imdb.load_data(num_words=20000) #selecting 20000 more frequently unique words

x_train #this is bag of words, in bag of words, model words are encoded in numbers

#padding- making all reviews of fixed length
x_train=pad_sequences(x_train,maxlen=100)
x_test=pad_sequences(x_test,maxlen=100)

x_train.shape,x_test.shape  # 25000 no of reviews in each training and testing dataset and each reviews of max 100 words

"""**Building the model**"""

#defining object(initializing CNN)
model=tf.keras.models.Sequential()

#Embedding layer - use to compress input feature space into smaller one
model.add(tf.keras.layers.Embedding(input_dim=20000,output_dim=128,input_shape=(100,)))

#LSTM layer - use to understand the relationship between different words in reviews
model.add(tf.keras.layers.LSTM(units=128,activation='tanh'))

#output layer
model.add(tf.keras.layers.Dense(units=1,activation='sigmoid'))

model.summary()

#Compiling
model.compile(optimizer='rmsprop',loss='binary_crossentropy',metrics=['accuracy']) #'rmsprop' better optimizer than 'adam' for sequence layers

"""**Training the model**"""

#es=tf.keras.callbacks.EarlyStopping(monitor='loss',mode='min',verbose=1,patience=10,min_delta=0)
history=model.fit(x_train,y_train,validation_data=(x_test,y_test),epochs=3,batch_size=32)#,callbacks=[es])

def learning_curve(history,epoch):
  #training vs validation accuracy
  epoch_range=range(1,epoch+1)
  plt.plot(epoch_range,history.history['accuracy'])
  plt.plot(epoch_range,history.history['val_accuracy'])
  plt.title('model accuracy')
  plt.xlabel('epoch')
  plt.ylabel('accuracy')
  plt.legend(['Train','val'],loc='upper left')
  plt.show()

  #training vs validation loss
  epoch_range=range(1,epoch+1)
  plt.plot(epoch_range,history.history['loss'])
  plt.plot(epoch_range,history.history['val_loss'])
  plt.title('model loss')
  plt.xlabel('epoch')
  plt.ylabel('loss')
  plt.legend(['Train','val'],loc='upper right')
  plt.show()

learning_curve(history,3)

# evaluation=pd.DataFrame(model.history.history)
# evaluation[['accuracy', 'val_accuracy']].plot()
# evaluation[['loss', 'val_loss']].plot()