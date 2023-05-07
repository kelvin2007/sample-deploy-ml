import tensorflow as tf
import numpy as np
from fastapi import FastAPI, Form
import uvicorn

app = FastAPI()

def model_forecast(model, series, window_size, batch_size):
    """Uses an input model to generate predictions on data windows

    Args:
      model (TF Keras Model) - model that accepts data windows
      series (array of float) - contains the values of the time series
      window_size (int) - the number of time steps to include in the window
      batch_size (int) - the batch size

    Returns:
      forecast (numpy array) - array containing predictions
    """

    # Generate a TF Dataset from the series values
    dataset = tf.data.Dataset.from_tensor_slices(series)

    # Window the data but only take those with the specified size
    dataset = dataset.window(window_size, shift=1, drop_remainder=True)

    # Flatten the windows by putting its elements in a single batch
    dataset = dataset.flat_map(lambda w: w.batch(window_size))
    
    # Create batches of windows
    dataset = dataset.batch(batch_size).prefetch(1)
    
    # Get predictions on the entire dataset
    forecast = model.predict(dataset)
    
    return forecast

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/predict")
def predict_time_series():
    model = tf.keras.models.load_model("model/tes_model.h5")
    dataset = [ 68.053764,  66.2601  ,  59.30633 ,  63.911392,  64.14101 ,
        58.376602,  71.69516 ,  68.57505 ,  63.09382 ,  64.34379 ,
        65.262314,  54.023083,  63.007553,  60.845512,  59.259632,
        62.87484 ,  73.28169 ,  67.5107  ,  61.464104,  67.19674 ,
        71.34472 ,  68.98552 ,  64.6752  ,  61.15736 ,  67.89844 ,
        66.390305,  68.91469 ,  67.6307  ,  69.71901 ,  61.81174 ,
        71.091835,  65.51008 ,  74.91588 ,  61.11138 ,  73.25516 ,
        65.58317 ,  61.35506 ,  62.21152 ,  63.048264,  66.79013 ,
        67.30303 ,  61.840164,  64.60695 ,  75.460365,  73.40727 ,
        66.971954,  65.00137 ,  65.43278 ,  67.9217  ,  59.761875,
        63.610905,  56.577053,  66.938515,  68.20101 ,  62.571968,
        72.88092 ,  58.905464,  57.73595 ,  66.20383 ,  70.34101 ,
        73.54933 ,  62.859653,  70.57207 ,  65.010925,  64.36533 ,
        69.671974,  68.5407  ,  57.42275 ,  72.71323 ,  72.256996,
        62.25493 ,  67.38817 ,  67.9059  ,  66.7659  ,  62.737984,
        62.15856 ,  65.41626 ,  71.43522 ,  68.31729 ,  63.774124,
        69.51377 ,  51.440834,  71.45582 ,  57.042038,  63.957195,
        60.20002 ,  59.354107,  71.66096 ,  63.547802,  67.648476,
        65.71117 ,  68.36095 ,  66.39001 ,  59.62124 ,  71.048   ,
        63.628506,  58.345173,  64.01845 ,  73.693924,  70.47248 ,
        64.50952 ,  64.538055,  64.707886,  76.73166 ,  68.2896  ,
        68.56229 ,  71.59581 ,  67.670784,  65.21421 ,  65.5604  ,
        66.21702 ,  66.421936,  70.27935 ,  66.93422 ,  70.37112 ,
       104.34642 , 105.18725 ,  94.8353  , 109.42832 , 106.587654,
       109.84198 ,  90.35556 , 115.25182 , 104.07336 , 110.26182 ,
        99.459274, 107.648895,  99.23254 , 101.28374 , 113.86416 ,
       103.2205  , 105.12953 , 108.249756, 106.22351 , 104.331604,
       105.2275  , 115.2318  , 102.72757 , 103.81108 , 107.83784 ,
       107.88033 , 108.04522 , 105.0504  ,  95.8778  , 109.485565,
        95.30185 , 102.25162 ,  96.66173 ,  99.79697 , 101.43604 ,
       101.06371 , 101.22145 , 106.82568 , 100.66054 ,  96.798416,
       102.456696, 103.19152 ,  90.705025,  99.42005 ,  99.520164,
        94.09911 , 102.02963 ,  93.956665,  94.88248 ,  92.928856,
        93.403854,  87.3686  ,  85.16617 ,  99.847984,  87.14242 ,
        85.91496 ,  79.59274 ,  86.64589 ,  82.69966 ,  96.99318 ,
        93.293945,  84.25978 ,  98.41249 ,  91.5032  ,  84.40873 ,
        72.96902 ,  96.348755,  77.36918 ,  75.50822 ,  88.26164 ,
        94.75669 ,  88.88419 ,  84.18323 ,  83.73445 ,  84.42108 ,
        83.33852 ,  80.33643 ,  78.835   ,  77.38166 ,  73.302765,
        75.044685,  67.356476,  74.70068 ,  69.61866 ,  68.41122 ,
        74.19472 ,  79.62008 ,  76.615395,  63.534176,  65.80074 ,
        74.8145  ,  64.55971 ,  67.71043 ,  70.94545 ,  62.715424,
        67.44654 ,  59.612816,  62.64036 ,  66.61152 ,  56.41444 ,
        65.95016 ,  63.01975 ,  65.25252 ,  62.98395 ,  68.06177 ,
        61.24646 ,  57.85537 ,  59.99892 ,  61.49212 ,  58.411503,
        57.765305,  53.451286,  53.04961 ,  48.75807 ,  63.930313,
        48.378975,  50.554333,  49.85229 ,  57.34949 ,  50.83594 ,
        57.99066 ,  47.831398,  52.046535,  45.93351 ,  60.300835,
        43.108288,  50.073074,  51.177227,  49.56854 ,  46.071312,
        45.85404 ,  46.23492 ,  44.80107 ,  49.88333 ,  55.652218,
        41.355762,  36.845936,  42.81353 ,  55.721863,  38.38186 ,
        50.181427,  49.968773,  38.41571 ,  43.641033,  48.559776,
        38.153183,  83.07987 ,  81.140755,  78.92756 ,  80.70794 ,
        77.78842 ,  84.03311 ,  79.96818 ,  84.9431  ,  75.951584,
        85.34313 ,  87.8148  ,  73.637634,  85.4365  ,  89.6652  ,
        77.44003 ,  91.8132  ,  85.50826 ,  79.85164 ,  83.06209 ,
        86.09752 ,  83.65156 ,  85.93164 ,  78.60151 ,  84.01937 ,
        76.072365,  82.55385 ,  78.56014 ,  79.37239 ,  89.20151 ,
        88.44926 ,  86.0107  ,  77.47638 ,  81.32946 ,  88.95117 ,
        83.569084,  94.43258 ,  84.77856 ,  83.74885 ,  81.22026 ,
        83.411385,  81.95976 ,  86.24167 ,  87.46423 ,  78.73095 ,
        75.98547 ,  73.441925,  85.144775,  77.07042 ,  71.805786,
        84.49666 ,  95.00284 ,  82.492096,  86.70006 ,  82.90244 ,
        81.985054,  87.061615,  81.002106,  83.7782  ,  84.038   ,
        79.07783 ,  87.367775,  81.52254 ,  78.60889 ,  85.06091 ,
        77.877266,  82.502235,  82.30793 ,  87.77568 ,  84.71284 ,
        82.20781 ,  86.41585 ,  89.272575,  85.10558 ,  82.36372 ,
        75.74865 ,  76.978584,  80.77479 ,  79.25055 ,  81.360886,
        82.57704 ,  84.94074 ,  81.93869 ,  84.723015,  82.61262 ,
        72.413055,  77.59427 ,  81.57147 ,  76.2448  ,  85.29468 ,
        89.95094 ,  88.39355 ,  81.23545 ,  89.75962 ,  83.05304 ,
        80.62834 ,  79.25122 ,  80.81071 ,  80.387375,  83.18591 ,
        83.14263 ,  82.36128 ,  84.53739 ,  88.312935,  87.11484 ,
        74.95027 ,  69.61321 ,  87.06281 ,  75.56555 ,  81.2852  ,
        76.56786 ,  73.41827 ,  85.14555 ,  86.244415,  79.576805,
        69.51519 ,  79.75054 ,  84.45246 ,  75.11088 ,  83.43453 ,
        82.4538  ,  85.43971 ,  83.15438 ,  77.70466 ,  88.56668 ,
        81.80529 ,  82.47583 ,  77.96071 ,  80.42564 ,  78.23331 ,
        81.80814 ,  91.24726 ,  75.84534 ,  74.653435,  90.09377 ,
        81.70825 ,  79.42672 ,  87.98909 ,  79.77924 ,  91.95539 ,
        86.23324 ,  80.4226  ,  93.667496,  79.87143 ,  86.62979 ,
        84.43532 ,  89.46738 ,  90.78627 ,  83.159035,  79.25247 ,
        85.340195,  79.67278 ,  93.14954 ,  83.78679 ,  81.29923 ,
        84.07119 ,  76.43435 ,  78.33432 ,  89.2171  ,  79.95344 ,
        78.02643 ,  85.96757 ,  89.236336,  86.92633 ,  88.33576 ,
        79.59572 ,  76.29502 ,  90.93533 ,  81.84007 ,  82.22431 ,
        90.144646,  86.31025 ,  85.83415 ,  94.40554 ,  80.38895 ,
        88.27194 ,  83.944214,  85.02871 ,  91.35487 ,  86.278694,
        86.45816 ,  89.15656 ,  81.9968  ,  79.653244,  78.65315 ,
        74.0735  ,  94.214584,  78.445946,  82.88434 ,  82.635345,
        85.5854  ,  88.156204,  88.40919 ,  81.22092 ,  83.330345,
        85.60867 ,  82.9823  ,  92.29262 ,  86.74107 ,  87.991066,
        87.6617  ,  90.24545 ,  85.314125,  77.95596 ,  86.46982 ,
        81.246   ,  81.891266,  87.49788 ,  90.78933 ,  84.73629 ,
        86.206245,  93.20547 ,  85.930595,  97.76784 ,  87.619705,
        76.02122 ,  88.624756,  86.79699 ,  91.37325 ,  88.32383 ]
    
    x_valid = [ 71.34472 ,  68.98552 ,  64.6752  ,  61.15736 ,  67.89844 ,
        66.390305,  68.91469 ,  67.6307  ,  69.71901 ,  61.81174 ,
        71.091835,  65.51008 ,  74.91588 ,  61.11138 ,  73.25516 ,
        65.58317 ,  61.35506 ,  62.21152 ,  63.048264,  66.79013 ,
        67.30303 ,  61.840164,  64.60695 ,  75.460365,  73.40727 ,
        66.971954,  65.00137 ,  65.43278 ,  67.9217  ,  59.761875,
        63.610905,  56.577053,  66.938515,  68.20101 ,  62.571968,
        72.88092 ,  58.905464,  57.73595 ,  66.20383 ,  70.34101 ,
        73.54933 ,  62.859653,  70.57207 ,  65.010925,  64.36533 ,
        69.671974,  68.5407  ,  57.42275 ,  72.71323 ,  72.256996,
        62.25493 ,  67.38817 ,  67.9059  ,  66.7659  ,  62.737984,
        62.15856 ,  65.41626 ,  71.43522 ,  68.31729 ,  63.774124,
        69.51377 ,  51.440834,  71.45582 ,  57.042038,  63.957195,
        60.20002 ,  59.354107,  71.66096 ,  63.547802,  67.648476,
        65.71117 ,  68.36095 ,  66.39001 ,  59.62124 ,  71.048   ,
        63.628506,  58.345173,  64.01845 ,  73.693924,  70.47248 ,
        64.50952 ,  64.538055,  64.707886,  76.73166 ,  68.2896  ,
        68.56229 ,  71.59581 ,  67.670784,  65.21421 ,  65.5604  ,
        66.21702 ,  66.421936,  70.27935 ,  66.93422 ,  70.37112 ,
       104.34642 , 105.18725 ,  94.8353  , 109.42832 , 106.587654,
       109.84198 ,  90.35556 , 115.25182 , 104.07336 , 110.26182 ,
        99.459274, 107.648895,  99.23254 , 101.28374 , 113.86416 ,
       103.2205  , 105.12953 , 108.249756, 106.22351 , 104.331604,
       105.2275  , 115.2318  , 102.72757 , 103.81108 , 107.83784 ,
       107.88033 , 108.04522 , 105.0504  ,  95.8778  , 109.485565,
        95.30185 , 102.25162 ,  96.66173 ,  99.79697 , 101.43604 ,
       101.06371 , 101.22145 , 106.82568 , 100.66054 ,  96.798416,
       102.456696, 103.19152 ,  90.705025,  99.42005 ,  99.520164,
        94.09911 , 102.02963 ,  93.956665,  94.88248 ,  92.928856,
        93.403854,  87.3686  ,  85.16617 ,  99.847984,  87.14242 ,
        85.91496 ,  79.59274 ,  86.64589 ,  82.69966 ,  96.99318 ,
        93.293945,  84.25978 ,  98.41249 ,  91.5032  ,  84.40873 ,
        72.96902 ,  96.348755,  77.36918 ,  75.50822 ,  88.26164 ,
        94.75669 ,  88.88419 ,  84.18323 ,  83.73445 ,  84.42108 ,
        83.33852 ,  80.33643 ,  78.835   ,  77.38166 ,  73.302765,
        75.044685,  67.356476,  74.70068 ,  69.61866 ,  68.41122 ,
        74.19472 ,  79.62008 ,  76.615395,  63.534176,  65.80074 ,
        74.8145  ,  64.55971 ,  67.71043 ,  70.94545 ,  62.715424,
        67.44654 ,  59.612816,  62.64036 ,  66.61152 ,  56.41444 ,
        65.95016 ,  63.01975 ,  65.25252 ,  62.98395 ,  68.06177 ,
        61.24646 ,  57.85537 ,  59.99892 ,  61.49212 ,  58.411503,
        57.765305,  53.451286,  53.04961 ,  48.75807 ,  63.930313,
        48.378975,  50.554333,  49.85229 ,  57.34949 ,  50.83594 ,
        57.99066 ,  47.831398,  52.046535,  45.93351 ,  60.300835,
        43.108288,  50.073074,  51.177227,  49.56854 ,  46.071312,
        45.85404 ,  46.23492 ,  44.80107 ,  49.88333 ,  55.652218,
        41.355762,  36.845936,  42.81353 ,  55.721863,  38.38186 ,
        50.181427,  49.968773,  38.41571 ,  43.641033,  48.559776,
        38.153183,  83.07987 ,  81.140755,  78.92756 ,  80.70794 ,
        77.78842 ,  84.03311 ,  79.96818 ,  84.9431  ,  75.951584,
        85.34313 ,  87.8148  ,  73.637634,  85.4365  ,  89.6652  ,
        77.44003 ,  91.8132  ,  85.50826 ,  79.85164 ,  83.06209 ,
        86.09752 ,  83.65156 ,  85.93164 ,  78.60151 ,  84.01937 ,
        76.072365,  82.55385 ,  78.56014 ,  79.37239 ,  89.20151 ,
        88.44926 ,  86.0107  ,  77.47638 ,  81.32946 ,  88.95117 ,
        83.569084,  94.43258 ,  84.77856 ,  83.74885 ,  81.22026 ,
        83.411385,  81.95976 ,  86.24167 ,  87.46423 ,  78.73095 ,
        75.98547 ,  73.441925,  85.144775,  77.07042 ,  71.805786,
        84.49666 ,  95.00284 ,  82.492096,  86.70006 ,  82.90244 ,
        81.985054,  87.061615,  81.002106,  83.7782  ,  84.038   ,
        79.07783 ,  87.367775,  81.52254 ,  78.60889 ,  85.06091 ,
        77.877266,  82.502235,  82.30793 ,  87.77568 ,  84.71284 ,
        82.20781 ,  86.41585 ,  89.272575,  85.10558 ,  82.36372 ,
        75.74865 ,  76.978584,  80.77479 ,  79.25055 ,  81.360886,
        82.57704 ,  84.94074 ,  81.93869 ,  84.723015,  82.61262 ,
        72.413055,  77.59427 ,  81.57147 ,  76.2448  ,  85.29468 ,
        89.95094 ,  88.39355 ,  81.23545 ,  89.75962 ,  83.05304 ,
        80.62834 ,  79.25122 ,  80.81071 ,  80.387375,  83.18591 ,
        83.14263 ,  82.36128 ,  84.53739 ,  88.312935,  87.11484 ,
        74.95027 ,  69.61321 ,  87.06281 ,  75.56555 ,  81.2852  ,
        76.56786 ,  73.41827 ,  85.14555 ,  86.244415,  79.576805,
        69.51519 ,  79.75054 ,  84.45246 ,  75.11088 ,  83.43453 ,
        82.4538  ,  85.43971 ,  83.15438 ,  77.70466 ,  88.56668 ,
        81.80529 ,  82.47583 ,  77.96071 ,  80.42564 ,  78.23331 ,
        81.80814 ,  91.24726 ,  75.84534 ,  74.653435,  90.09377 ,
        81.70825 ,  79.42672 ,  87.98909 ,  79.77924 ,  91.95539 ,
        86.23324 ,  80.4226  ,  93.667496,  79.87143 ,  86.62979 ,
        84.43532 ,  89.46738 ,  90.78627 ,  83.159035,  79.25247 ,
        85.340195,  79.67278 ,  93.14954 ,  83.78679 ,  81.29923 ,
        84.07119 ,  76.43435 ,  78.33432 ,  89.2171  ,  79.95344 ,
        78.02643 ,  85.96757 ,  89.236336,  86.92633 ,  88.33576 ,
        79.59572 ,  76.29502 ,  90.93533 ,  81.84007 ,  82.22431 ,
        90.144646,  86.31025 ,  85.83415 ,  94.40554 ,  80.38895 ,
        88.27194 ,  83.944214,  85.02871 ,  91.35487 ,  86.278694,
        86.45816 ,  89.15656 ,  81.9968  ,  79.653244,  78.65315 ,
        74.0735  ,  94.214584,  78.445946,  82.88434 ,  82.635345,
        85.5854  ,  88.156204,  88.40919 ,  81.22092 ,  83.330345,
        85.60867 ,  82.9823  ,  92.29262 ,  86.74107 ,  87.991066,
        87.6617  ,  90.24545 ,  85.314125,  77.95596 ,  86.46982 ,
        81.246   ,  81.891266,  87.49788 ,  90.78933 ,  84.73629 ,
        86.206245,  93.20547 ,  85.930595,  97.76784 ,  87.619705,
        76.02122 ,  88.624756,  86.79699 ,  91.37325 ,  88.32383 ,
       122.30772 ]
    x_valid = np.array(x_valid).astype(float)
    predict_array = np.array(dataset).astype(float)
    # Use helper function to generate predictions
    forecast = model_forecast(model, predict_array, 20, 32)

    # Drop single dimensional axis
    results = forecast.squeeze()
    return {"result": float(tf.keras.metrics.mean_squared_error(x_valid, results))}