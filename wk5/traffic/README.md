# The Process.

## So here's the Data (in chronological order) I obtained trying different settings.

1. loss: 3.4996 - accuracy: 0.0543
Layers:- Conv2D(32, (3,3), 'relu') -> MaxPool((2,2)) -> Flatten -> Dense(128) -> Dropout(0.5) -> Dense('softmax')
Optimizer: Adam, Loss: Categorical Crossentropy, Metrics: Accuracy

2. loss: 3.0446 - accuracy: 0.3265
Layers:- Conv2D(50, (3,3), 'relu') -> AvgPool((2,2)) -> Flatten -> Dense(300) -> Dense(300) -> Dropout(0.5) -> Dense('softmax')
Optimizer: Adam, Loss: Categorical Crossentropy, Metrics: Accuracy

3. loss: 2.5134 - accuracy: 0.2804
Layers:- Conv2D(100, (3,3), 'relu') -> AvgPool((2,2)) -> Flatten -> Dense(500) -> Dropout(0.4) -> Dense(500) -> Dropout(0.4) -> Dense('softmax')
Optimizer: Adam, Loss: Categorical Crossentropy, Metrics: Accuracy

4.  loss: 1.9990 - accuracy: 0.4060
Layers:- Conv2D(64, (5,5), 'relu') -> MaxPool((2,2)) -> Conv2D(64, (5,5), 'relu') -> MaxPool((2,2))  -> Flatten -> Dense(256) -> Dropout(0.4) -> Dense('softmax')
Optimizer: Adam, Loss: Categorical Crossentropy, Metrics: Accuracy

### And then I knew something was wrong, because no matter what I tried, the accuracy won't step up!
### I tried 'cv2.resize()' instead of 'image.resize()' because I had tried everything else in the last 5 hrs and this is what I had found someone post in the CS50ai channel on their discord!
### Actually the image.resize() cropped the image or added blank pixels instead of resizing, which effectively corrupted the dataset altogether 🤦‍♂️

1. loss: 0.0777 - accuracy: 0.9826
Layers:- Conv2D(64, (5,5), 'relu') -> MaxPool((2,2)) -> Conv2D(64, (5,5), 'relu') -> MaxPool((2,2))  -> Flatten -> Dense(256) -> Dropout(0.4) -> Dense('softmax')
Optimizer: Adam, Loss: Categorical Crossentropy, Metrics: Accuracy

### I guess that's a good spot to stop at ;p