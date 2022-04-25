from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.models import Sequential, load_model
from constan import region
import constan
import dataSet as dst
import matplotlib.pyplot as plt


def createModel(shape, region = region.CANINE):
    model = Sequential()
    model.add(Conv2D(64, 3, input_shape = shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(2))
    model.add(Dropout(0.25))

    model.add(Conv2D(128, 3))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(2))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(64))
    model.add(Dropout(0.25))

    model.add(Dense(8))
    model.add(Activation('softmax'))

    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam',metrics=['accuracy'])
    #model.summary()
    saveModel = model.save(f'{constan.MODEL_FOLDER}{region}')
    return model

def trainingModel(X_train, y_train,X_test, y_test, region = region.CANINE, showPlot=False):
    model = load_model(f'{constan.MODEL_FOLDER}{region}')
    history = model.fit(X_train,y_train,epochs=constan.EPOCHS, verbose = showPlot, validation_data=(X_test, y_test))
    if showPlot:
        plt.plot(history.history['accuracy'], label='accuracy')
        plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.ylim([0.5, 1])
        plt.legend(loc='lower right')
        plt.show()
    return model

def evaluateModel(X_test, y_test, region = region.CANINE, verbose = False):
    model = load_model(f'{constan.MODEL_FOLDER}{region}')
    test_loss, test_acc = model.evaluate(X_test,y_test,verbose = verbose)
    with open(constan.TOOTH_JSON_PATH, 'r') as file:
        toohNumber = json.load(file)
        with open(constan.RESULT_JSON_PATH, 'r') as file:
            try: Tooth = json.load(file) 
            except: Tooth = {}
            Tooth[region] = toohNumber
            with open(constan.RESULT_JSON_PATH, 'w') as file: 
                json.dump(Tooth, file)    
    return model

def executeModels(REGION):
    dst.createDataSet(REGION)
    X_train, X_test, y_train, y_test = dst.loadDataSet(REGION)
    createModel(X_train.shape[1:], REGION)
    trainingModel(X_train, y_train,X_test, y_test, REGION, False)
    evaluateModel(X_test, y_test, REGION, False)

# import model as mdl
executeModels(region.CANINE)


