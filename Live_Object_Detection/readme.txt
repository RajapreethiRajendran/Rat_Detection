
The “Object detection using deep learning with OpenCV and Python” by Arun Ponnusamy  is taken as a
reference and the rat detection is developed. The rat detection in the edge node is imple-
mented by multithreading using Python and OpenCV.

Thread 1 is a capture thread that captures the live feed and processes one frame per second and adds it to the queue. Thread 2 is a detection thread that fetches a frame from the queue and passes it to the YOLOv4 detection model. In the detection model, the model's weights, configuration, and classes are given and the network is loaded into the OpenCV DNN(Deep Neural Network) module. In the OpenCV DNN module, the output layers for object detection tasks are typically calculated by forward propagating an input image through a pre-trained deep neural network model. The output layers of the network produce a set of predictions that describe the locations and class probabilities of objects in the image. The model then returns the bounding boxes around the detected rat  along with the class label rat and confidence scores. 
