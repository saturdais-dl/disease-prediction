<p align="center">
  <img width="1200"  src="https://imagizer.imageshack.com/img922/7820/W5kxKY.png" alt="infarction prediction banner">
</p>

# Infarction Prediction

## Project overview

**Infarction Prediction** is an AI-powered tool designed to predict heart attacks (myocardial infarction) using ECG images. The main goal of this project is to provide emergency medical personnel with a quick and reliable tool for early detection of heart attacks, potentially saving lives through timely intervention.


## Dataset

For training the model, we utilized the [**PTB-XL dataset**](https://physionet.org/content/ptb-xl/1.0.3/), which comprises 21,837 clinical ECG records from 18,885 patients. Each record consists of 12-lead ECGs lasting 10 seconds.

## File descriptions

- **exploration_notebook.ipynb**: Exploratory Data Analysis (EDA)
- **data_loading_utils.py**: Data preprocessing utilities
- **model_training.ipynb**: Model training notebook
- **models/standard_scaler.pkl**: Data normalizer
- **models/cnn_model.h5**: Trained CNN model
- **app.py**: Interface for predicting infarction by uploading an ECG image
- **requirements.txt**: Required libraries for running the project


## How to run the project

1. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

2. Run the application:
    ```bash
    streamlit run app.py
    ```

2. Upload an ECG image to get the prediction.

## Authors

This project was created by a team from the 7th edition of Saturdays.AI Madrid:

- [Gabriela Calzadilla Rodriguez](https://www.linkedin.com/in/gabrielacalzadilla/)
- [Galyna Chupirova](https://www.linkedin.com/in/galyna-chupirova-447b6142/)
- [Karla Lamus Oliveros](https://www.linkedin.com/in/karla-lamus/)
- [Nicolás Martínez-Geijo Vila](https://www.linkedin.com/in/nicolasgeijo/)
- [Paloma García García de Castro](https://www.linkedin.com/in/paloma-garcia-data-science/)
