from flask import Flask
from flask import request
from flask_cors import CORS
import crop_optimization as co
import pandas as pd
import os
import requests
import json

app  = Flask("__name__")
CORS(app)

beansYieldURL = "http://govirukulasystem-env.eba-biwfkcgd.us-east-2.elasticbeanstalk.com/getBeansPrice"
carrotYieldURL = "http://govirukulasystem-env.eba-biwfkcgd.us-east-2.elasticbeanstalk.com/getCarrotPrice"
tomatoYieldURL = "http://govirukulasystem-env.eba-biwfkcgd.us-east-2.elasticbeanstalk.com/getTomatoPrice"
# pumpkinYieldURL = ""
# capsicumYieldURL = ""
# potatoYieldURL = ""

beansPriceURL = "https://govirukulaapi.herokuapp.com/getBeansPrice"
carrotPriceURL = "https://govirukulaapi.herokuapp.com/getCarrotPrice"
tomatoPriceURL = "https://govirukulaapi.herokuapp.com/getTomatoPrice"
# pumpkinPriceURL = ""
# capsicumPriceURL = ""
# potatoPriceURL = ""

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
csv_path = current_path+"\\crop.csv"

@app.route('/')
def main():
    return ''

#function to identify language
@app.route('/getBestOptimization', methods=['POST']) 
def insertPredtictValues():
        data = request.get_data()
        data = json.loads(data)   

        params ={"temperature": 15,"humidity": 10,"rainfall": 10,"wind": 20}
        paramsPrice = {"date": "2018-01-12"}

        # Tomato Yield
        responseTomato = requests.post(tomatoYieldURL, json=params)
        jsonResTomYield = responseTomato.json()
        tomato_yield = jsonResTomYield['yield-output']
     
        # Tomato Price
        responseTomato = requests.post(tomatoPriceURL, json=paramsPrice)
        jsonResTomPrice = responseTomato.json()
        tomato_price = jsonResTomPrice['price-output']
        print(tomato_yield,tomato_price)
        # Beans Yield
        responseBeans = requests.post(beansYieldURL, json=params)
        jsonResBnsYield = responseBeans.json()
        beans_yield = jsonResBnsYield['yield-output']
        
        # Beans Price
        responseBeans = requests.post(beansPriceURL, json=paramsPrice)
        jsonResBnsPrice = responseBeans.json()
        beans_price = jsonResBnsPrice['price-output']
        print(beans_yield,beans_price)
        # Carrots Yield
        responseCarrot = requests.post(carrotYieldURL, json=params)
        jsonResCrtYield = responseCarrot.json()
        carrot_yield = jsonResCrtYield['yield-output']

        # Carrots Price
        responseCarrot = requests.post(carrotPriceURL, json=paramsPrice)
        print(responseCarrot)
        jsonResCrtPrice = responseCarrot.json()
        carrot_price = jsonResCrtPrice['price-output']
        print(carrot_yield,carrot_price)
        # Pumpkin Yield
        # responsePumpkin = requests.post(pumpkinYieldURL, json=params)
        # jsonResPumYield = responsePumpkin.json()
        # pumpkin_yield = jsonResPumYield['yield-output']

        # # Pumpkin Price
        # responsePumpkin = requests.post(pumpkinPriceURL, json=paramsPrice)
        # jsonResPumPrice = responsePumpkin.json()
        # pumpkin_price = jsonResPumPrice['price-output']

        # # Capsicum Yield
        # responseCapsicum = requests.post(capsicumYieldURL, json=params)
        # jsonResCapYield = responseCapsicum.json()
        # capsicum_yield = jsonResCapYield['yield-output']

        # # Capsicum Price
        # responseCapsicum = requests.post(capsicumPriceURL, json=paramsPrice)
        # jsonResCapPrice = responseCapsicum.json()
        # capsicum_price = jsonResCapPrice['price-output']

        # # Potato Yield
        # responsePotato = requests.post(potatoYieldURL, json=params)
        # jsonResPotYield = responsePotato.json()
        # potato_yield = jsonResPotYield['yield-output']

        # # Potato Price
        # responsePotato = requests.post(potatoPriceURL, json=paramsPrice)
        # jsonResPotPrice = responsePotato.json()
        # potato_price = jsonResPotPrice['price-output']

        # making data frame from the csv file 
        dataframe = pd.read_csv(csv_path) 
    
        # updating the column value
        dataframe.loc[0, 'Pred. Yield'] = int(round(tomato_yield))
        dataframe.loc[0, 'Pred. Price'] = int(tomato_price)

        dataframe.loc[1, 'Pred. Yield'] = int(round(beans_yield))
        dataframe.loc[1, 'Pred. Price'] = int(beans_price)

        dataframe.loc[2, 'Pred. Yield'] = int(round(carrot_yield))
        dataframe.loc[2, 'Pred. Price'] = int(carrot_price)

        # dataframe.loc[3, 'Pred. Yield'] = int(round(pumpkin_yield))
        # dataframe.loc[3, 'Pred. Price'] = int(pumpkin_price)

        # dataframe.loc[4, 'Pred. Yield'] = int(round(capsicum_yield))
        # dataframe.loc[4, 'Pred. Price'] = int(capsicum_price)

        # dataframe.loc[5, 'Pred. Yield'] = int(round(potato_yield))
        # dataframe.loc[5, 'Pred. Price'] = int(potato_price)

        # writing the dataframe to csv file
        dataframe.to_csv(csv_path, index = False)

        print("Data updating complete")
        print("Optimization start")
        result = co.cropOptimization(data)
        print("Optimization Complete")

        return str(result)

if __name__ == '__main__':
        app.run(debug=True)