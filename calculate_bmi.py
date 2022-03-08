from distutils.log import ERROR, debug
from http.client import OK
from threading import Thread
import flask
from flask_cors import CORS
import json

input_data = {}
OK_RESPONSE_CODE = {"responseCode": "200"}
response_output = {}

app = flask.Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['DEBUG'] = True

@app.route("/get-bmi")
def get_bmi():
    sample_return = {}
    global input_data
    try:
        input_file = open('./person_details.json')
        input_data = json.load(input_file)
        print(input_data)
        for data in input_data:
            bmi = round(data["WeightKg"] / (float(data["HeightCm"]/100))**2, 2)
            data["bmi"] = bmi 
            if bmi <= 18.4:
                data["BMI Category"] = "Underweight" 
                data["Health risk"] = "Malnutrition risk"
            elif bmi >=18.5 and bmi <= 24.9:
                data["BMI Category"] = "Normalweight" 
                data["Health risk"] = "Low risk"
            elif bmi>=25 and bmi<=29.9:
                data["BMI Category"] = "Overweight" 
                data["Health risk"] = "Enhanced risk"
            elif bmi>=30 and bmi<=34.9:
                data["BMI Category"] = "Moderately obese" 
                data["Health risk"] = "Medium risk"
            elif bmi>=35 and 40:
                data["BMI Category"] = "Severely obese" 
                data["Health risk"] = "High risk"
            elif bmi >= 40:
                data["BMI Category"] = "Very severely obese" 
                data["Health risk"] = "Very high risk"
        sample_return["data"] = input_data
    except Exception as e:
        print(e)
    return sample_return


@app.route("/get-count")
def get_count():
    try:
        overweight_count = 0
        # get count of total number of overweight people
        if "BMI Category" in input_data[0]:
            print("Inside IF")
            for dic in input_data:
                print(dic)
                if dic["BMI Category"] == "Overweight":
                    print("here")
                    overweight_count += 1
            response_output["OverweightCount"] = overweight_count
        else:
            sample_data = get_bmi()
            print("Sample Data",sample_data)
            get_count()
        print("Overweight", overweight_count)
        return response_output
    except Exception as e:
        print(e)
        return ERROR

def instanciate_class():
    global input_data
    try:
        input_file = open('./person_details.json')
        input_data = json.load(input_file)
    except Exception as e:
        print(e)
    return OK_RESPONSE_CODE

if __name__ == '__main__':
    Thread(target=instanciate_class).start()
    app.run(debug=False)

