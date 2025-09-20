import pytest
import os
import pickle
import numpy as np
import pandas as pd

from app.api import app

# create a tiny fake pipeline if model not present to ensure tests don't fail
@pytest.fixture(scope='session', autouse=True)
def ensure_model():
    path = os.environ.get("MODEL_PATH", "artifacts/car_price_model.pkl")
    if not os.path.exists(path):
        # build a tiny sklearn pipeline to satisfy API
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import OneHotEncoder
        from sklearn.compose import ColumnTransformer
        from sklearn.linear_model import LinearRegression

        cat = ['fuel_type', 'transmission', 'city', 'registered', 'assembly']
        num = ['age', 'mileage']
        pre = ColumnTransformer([("cat", OneHotEncoder(handle_unknown='ignore'), cat),
                                 ("num", "passthrough", num)])
        pipe = Pipeline([('pre', pre), ('model', LinearRegression())])

        # train on a tiny fake dataset to allow predict
        df = pd.DataFrame([{
            'age': 5, 'mileage': 20000, 'fuel_type': 'Petrol', 'transmission': 'Automatic',
            'city': 'Lahore', 'registered': 'Lahore', 'assembly': 'Local', 'price': 1000000
        }])
        X = df[['age','mileage','fuel_type','transmission','city','registered','assembly']]
        y = np.log1p(df['price'])
        pipe.fit(X, y)

        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump(pipe, f)
    yield

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_predict_missing_fields(client):
    res = client.post('/predict', json={'year':2020})
    assert res.status_code == 400

def test_predict_success_single(client):
    payload = {
        'model': 2019,   # used to compute age
        'mileage': 30000,
        'fuel_type': 'Petrol',
        'transmission': 'Automatic',
        'city': 'Lahore',
        'registered': 'Lahore',
        'assembly': 'Local'
    }
    # note API expects 'age' computed or 'model' will be used by preprocess basic_clean -> age
    res = client.post('/predict', json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert 'predicted_price' in data
    assert isinstance(data['predicted_price'], float)
    assert data['predicted_price'] >= 0.0
