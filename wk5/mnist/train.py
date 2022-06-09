import sys
import tensorflow as tf

def train(filename=None):
    # Importing the Mnist DataSet
    dataset = tf.keras.datasets.mnist

    # Preparing the Data
    (x_train, y_train), (x_test, y_test) = dataset.load_data()
    x_train, x_test = x_train/255, x_test/255

    # print('y value before passing to to_categorical(): ' + str(y_train[0]))
    """Converts classifications as '3' to [0,0,0,0,0,0,0,0,0]"""
    y_train, y_test = tf.keras.utils.to_categorical(y_train), tf.keras.utils.to_categorical(y_test)
    # print('y value After passing to to_categorical(): ' + str(y_train[0]))

    # print('x value before passing to reshape: ' + str(x_train[0]))
    # print('x shape value before passing to reshape: ' + str(x_train[0].shape))
    """Converts the dataset input into arrays. :)"""
    x_train, x_test = x_train.reshape(x_train.shape[0], x_train.shape[1], x_train.shape[2], 1), x_test.reshape(x_test.shape[0], x_test.shape[1], x_test.shape[2], 1)
    # print('x value After passing to reshape: ' + str(x_train[0]))

    # Preparing the Neural Network.
    model = tf.keras.Sequential([

        # Convolution layer :)
        tf.keras.layers.Conv2D(
            32, (3,3), activation='relu', input_shape=(28, 28, 1)
        ),

        # Max Pooling with 2x2 kernel
        tf.keras.layers.MaxPool2D(
            pool_size= (2,2)
        ),

        # Flattening remaining Inputs :)
        tf.keras.layers.Flatten(),

        # Single Hidden Layer with 128 nodes
        tf.keras.layers.Dense(
            128, activation='relu'
        ),

        # Dropout layer with factor=0.5
        tf.keras.layers.Dropout(0.5),

        # The Output Layer
        tf.keras.layers.Dense(10, activation='softmax')
        
    ])

    # Compiling the Model.
    model.compile(optimizer='adam',
    loss = tf.keras.losses.CategoricalCrossentropy(),
    metrics = ['accuracy'])

    # Training the Model
    model.fit(x_train, y_train, epochs=10)

    # Testing 
    model.evaluate(x_test, y_test, verbose=2)


    # Saving the model
    if filename:
        print('Saving Model to ' + str(filename))
        model.save(filename)

    return model


if __name__ == '__main__':
    train(filename= sys.argv[1] if len(sys.argv)==2 else None)