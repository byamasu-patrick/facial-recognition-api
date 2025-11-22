# **bf_facial_recognition_engine**

This project is a facial recognition API built with **Flask**, designed to perform both facial **recognition** and **verification**. The system leverages **TensorFlow** and a **pretrained deep learning model** to execute the core recognition tasks.

## **Model Architecture**

The API uses **FaceNet**, a Convolutional Neural Network architecture developed by Google in 2019 for high-accuracy facial recognition. In this project, we use a **pretrained FaceNet model**, integrated through TensorFlow with a Keras backend.

The pretrained model files are located in the `keras-facenet-h5` directory. This folder contains three key files:

* `model.json`
* `model.h5`
* `facenet_keras.h5`

These files define the core neural network architecture and contain the hyperparameters required to process and extract embeddings from RGB facial images.

## **Setup Instructions**

Before running the API, ensure that **Python 3.7** is installed on your machine. Then follow the steps below:

1. Upgrade pip:

```
python -m pip install --upgrade pip
```

2. Install all required dependencies:

```
pip install -r requirements.txt
```

Make sure you run this command from within the **bf_facial_recognition_engine** directory.

3. After all dependencies are installed, navigate to the **beneficiary-reference** folder and start the API by running:

```
python app.py
```

## **GPU vs CPU Execution**

When the application starts, it will automatically check whether your system has a properly configured GPU.

* If **no GPU** is detected or configured, TensorFlow will default to running on the **CPU**.
* CPU execution works but is significantly **slower**.
* For optimal performance, running the model on a **GPU** is highly recommended.

To enable GPU support, you must install and configure:

* **CUDA**
* **cuDNN**

Once these are installed correctly, TensorFlow will automatically make use of the GPU during execution.

## **Need Assistance?**

If you require help configuring TensorFlow to run on the GPU, please contact the author of this codebase for guidance. Proper GPU configuration substantially improves the performance of facial recognition operations.
