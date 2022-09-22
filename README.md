# bf_facial_recognition_engine


This is a facial recognition api developed in flask to run facial recognition and verification. 

The API was implemented using in flask as well as using tensorflow, a pretrained neural network architecture was used to implement the verification and recognition process. 
The Convolution Neural Network Architecture implemented was the architecture developed and implemented by Google in 2019. The network is called FaceNet. So, in this project
We use a pretrained model.

The tensorflow model is used with Keras backend. The pretrained model is found inside keras-facenet-h5 directory where you will find three important files, namely model.json, 
model.h5 and facenet_keras.h5, these are the main important files that contains the hyperparameters for facial recognition process on a RGB Image. 

Before running the api, make sure that Python 3.7 is installed in your PC and then run the folowing commands:

python -m pip install --upgrade pip ( for upgrading pip version to the latest version)

pip install -r requirements.txt ( this will install all the important libraries that are needed to run the project), before running this command make sure you are located in the
bf_facial_recognition_engine directory and then run the command. After installing all the libraries, you then need to navigate to benefiary-reference folder where you will
have to run the following command in order to run the project.

python app.py

This command will check if you have GPU in your laptop and if it is already confired. If you don't have tensorflow will just execute the code and run on CPU, but if it run on 
CPU the performance of the api will also be slow, as such, the prefered way is to run it on GPU, before running it on GPU there are some few steps that you need to follow
especially to configure tensorflow to be selecting automatically the GPU if it is installed and well configured. 

For you to configure GPU, you need to install Cuda and cuDNN and tell tensorflow to use cuda when executing the code.

If you need more information about how to run it GPU please contact the author of the code to help you setup your environment. Because running tensorflow on GPU is much faster than CPU
