# crop-yield-prediction

Is is important to be able to approximately predict the crop yield. This has several implications for governments, farmers and others.

- Farmers can plan their finances better
- Governments may prepare for any potential food shortages
- Scientists can improve crop yield prediction models by gathering more data and comparing them to the existing crop yield prediction models
- Planning crop yield (and preparing accordingly by, for example, importing more from other countries) may aid in fighting food shortages

This is the project structure

```bash
├── data
│   ├── pesticides.csv
│   ├── rainfall.csv
│   ├── temp.csv
│   ├── yield.csv
│   └── yield_df.csv
├── Dockerfile
├── __init__.py
├── LICENSE
├── model.bin
├── notebook.ipynb
├── Pipfile
├── Pipfile.lock
├── predict.py
├── predict-test.py
├── README.md
├── serializer.py
└── train.py
```

The [data](./data/) folder contains the source data from the [Kaggle dataset](https://www.kaggle.com/datasets/patelris/crop-yield-prediction-dataset).

[model.bin](model.bin) is the final - `GradientBoostingRegressor` trained model that's also deployed.

[notebook.ipynb](notebook.ipynb) contains the actions taken to explore the dataset, train different models and eventually arrive at the final model that is used in production for making the predictions.

## The model

It's main purpose is to create a prediction about the crop yield, using the `hg/ha` unit of measurement.

### Input

The data for making the prediction should follow the following schema:

```json
{
    "area": "kenya",
    "item": "cassava",
    "year": 1996,
    "average_rain_fall_mm_per_year": 630.0,
    "pesticides_tonnes": 6344.0,
    "avg_temp": 16.44
}
```
#### Important

<details>
  <summary>See valid values for the `area` field</summary>

  - albania
  - algeria
  - angola
  - argentina
  - armenia
  - australia
  - austria
  - azerbaijan
  - bahamas
  - bahrain
  - bangladesh
  - belarus
  - belgium
  - botswana
  - brazil
  - bulgaria
  - burkina_faso
  - burundi
  - cameroon
  - canada
  - central_african_republic
  - chile
  - colombia
  - croatia
  - denmark
  - dominican_republic
  - ecuador
  - egypt
  - el_salvador
  - eritrea
  - estonia
  - finland
  - france
  - germany
  - ghana
  - greece
  - guatemala
  - guinea
  - guyana
  - haiti
  - honduras
  - hungary
  - india
  - indonesia
  - iraq
  - ireland
  - italy
  - jamaica
  - japan
  - kazakhstan
  - kenya
  - latvia
  - lebanon
  - lesotho
  - libya
  - lithuania
  - madagascar
  - malawi
  - malaysia
  - mali
  - mauritania
  - mauritius
  - mexico
  - montenegro
  - morocco
  - mozambique
  - namibia
  - nepal
  - netherlands
  - new_zealand
  - nicaragua
  - niger
  - norway
  - pakistan
  - papua_new_guinea
  - peru
  - poland
  - portugal
  - qatar
  - romania
  - rwanda
  - saudi_arabia
  - senegal
  - slovenia
  - south_africa
  - spain
  - sri_lanka
  - sudan
  - suriname
  - sweden
  - switzerland
  - tajikistan
  - thailand
  - tunisia
  - turkey
  - uganda
  - ukraine
  - united_kingdom
  - uruguay
  - zambia
  - zimbabwe
</details>

<details>
  <summary>See valid values for the `item` field</summary>

  - maize
  - potatoes
  - rice_paddy
  - sorghum
  - soybeans
  - wheat
  - cassava
  - sweet_potatoes
  - plantains_and_others
  - yams
</details>

### Output

The result is given in three units of measurement and the response looks like this:

```json
{
    "predicted_yield": {
        "hectograms_per_hectare": 97422.99,
        "kilograms_per_hectare": 9742.3,
        "tonnes_per_hectare": 9.74
    }
}
```


### Running the model locally
0. Make sure you have `pipenv` installed
   - `pipenv --version` should return the `pipenv` version information
   - If you get an error, you need to install `pipenv`
     - `pip install pipenv`
1. Install the project dependencies, using `pipenv`
   - Go to project root
   - Run `pipenv install`
2. Run the Flask app
   - `python predict.py`
3. Test if model works by running `python predict-test.py` in a new terminal window

### Running the model locally using Docker container
0. Make sure you have `docker` installed
   - `docker --version` should return the `docker` version information
   - If you get an error, you need to install Docker engine, follow instructions for your OS [here](https://docs.docker.com/engine/install/)
1. Build the "predict" model image from project root dir with
   - `docker build -t crop-predict .`
2. Run the docker container with
   - `docker run -it --rm -p 9696:9696 crop-predict`
3. Test if model works by running `python predict-test.py` in a new terminal window

### Deploy the model using AWS ElasticBeanstalk
- Follow [Running the model locally](#running-the-model-locally) instructions 0.-1.
- Follow [Running the model locally using Docker container](#running-the-model-locally-using-docker-container) instructions 0.
- Run AWS Elastic Beanstalk locally and check if you are able to make predictions
  - `eb local run --port 9696 --debug --verbose`
  - `python predict.py`
- When you've made sure the app works locally, you can publish it to the world
  - `eb create`
    - Accepting the default options in CLI is OK
  - You can check application status with `eb status`
    - If app is successfully deployed, it would show
      - Status: Ready
      - Health: Green
  - Open the deployed app in browser with `eb open`
  - Check the last logs from the deployed app with `eb logs`
  - Check other available methods `eb --help`
  - You should be able to make predictions, using the URL pattern `http://<CNAME>/predict`
  - Remember to terminate your app if it's no longer needed with `eb terminate`

