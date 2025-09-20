import pandas as pd
from app.preprocess import basic_clean, select_features

def test_basic_clean_and_features():
    df = pd.DataFrame({
        'price': [1000000, 2500000],
        'model': [2010, 2018],
        'mileage': [50000, 30000],
        'fuel_type': ['Petrol', None],
        'transmission': ['Automatic', 'Manual'],
        'city': ['Lahore', 'Karachi'],
        'registered': ['Lahore', 'Sindh'],
        'assembly': ['Local', 'Imported']
    })
    cleaned = basic_clean(df)
    X, y = select_features(cleaned)
    assert 'age' in cleaned.columns
    assert X.shape[0] == 2
    assert y is not None
