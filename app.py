# api for insurance type prediction model
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pandas as pd 
from schema.user_input import UserInput
from model.predict import predict_output,MODEL_VERSION,model

app = FastAPI()

@app.get('/')
def home():
    return {'message: Insurance Preimium ApI'}
@app.get('/health')
def health_check():
    return {
        'status' : 'OK',
        'version':MODEL_VERSION,
        'model_loaded': model is not None    }
#----------------------------------post-------------------------------------------------------------
@app.post('/predict')
def predict_premium(data : UserInput):
    user_input_dict = pd.DataFrame([{
        'bmi':data.bmi,
        'lifestyle_risk':data.lifestyle_risk,
        'age_group':data.age_group,
        'city_tier': data.city_tier,
        'occupation': data.occupation,
        'income_lpa':data.income_lpa
    }])
    try: 
        prediction = predict_output(user_input_dict)
        return JSONResponse(status_code=200,content=[f'Predicted category:{prediction} '])
    except Exception as e:
        return JSONResponse(status_code=500,content=str(e))
    