from flask import Flask, request, jsonify, render_template
import numpy as np
import pickle
from datetime import datetime
from sklearn.preprocessing import LabelEncoder
import pandas as pd
app = Flask(__name__)

# Load the machine learning models
gb_classifier_model = pickle.load(open('gb_classifier.pkl', 'rb'))
random_forest_model = pickle.load(open('rf_class.pkl', 'rb'))
xgb_classifier_model = pickle.load(open('xg_Class.pkl', 'rb'))  # Corrected this line
logisticregression_model=pickle.load(open('lr_model.pkl', 'rb'))
knn_model=pickle.load(open('knn_model.pkl', 'rb'))
dt_model=pickle.load(open('dt_model.pkl', 'rb'))
mean_total_seconds =1692264000  
# Define label encoder for category feature
categories = ['entertainment', 'food_dining', 'gas_transport', 'grocery_net', 'grocery_pos', 'health_fitness', 'kids_pets', 'misc_net', 'misc_pos', 'personal_care', 'shopping_net', 'shopping_pos', 'travel', 'kids_', 'home']
encoder = LabelEncoder()
encoder.fit(categories)

def preprocess_data(data):
    try:
        # Convert date and time to total seconds since epoch
        date_obj = datetime.strptime(data['transactiondate'], '%Y-%m-%d')
        time_obj = datetime.strptime(data['transactiontime'], '%H:%M')
        total_seconds = int(date_obj.timestamp()) + time_obj.hour * 3600 + time_obj.minute * 60
        print(total_seconds)
        # Subtract mean total seconds
        diff_abs = total_seconds - mean_total_seconds

        # Encode category feature
        data['category'] = encoder.transform([data['category']])[0]

        # Convert amount to float
        data['amount'] = float(data['amount'])

        return np.array([[data['category'], data['amount'], time_obj.hour, diff_abs]])
    except KeyError as e:
        raise ValueError(f"Missing key in input data: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello', methods=['POST'])
def hello():
    try:
        # Get data from the request
        data = request.get_json()
        # Preprocess the data
        processed_data = preprocess_data(data)
        print(processed_data)
        # Make predictions using the selected model
        model_choice = data.get('model')
        if model_choice == "randomForest":
            prediction = random_forest_model.predict(processed_data)
        elif model_choice == "gradientboosting":
            prediction = gb_classifier_model.predict(processed_data)
        elif model_choice == "xgb":
            prediction = xgb_classifier_model.predict(processed_data)
        elif model_choice=="logisticregression":
            prediction=logisticregression_model.predict(processed_data)
        elif model_choice=="decisiontree":
            prediction=dt_model.predict(processed_data)
        elif model_choice=="knn":
            prediction=knn_model.predict(processed_data)
        else:
            return jsonify({'error': 'Invalid model choice'}), 400

        # Determine final prediction based on the model's output
        prediction_label = 'Fraudulent Transaction' if prediction == 1 else 'Not Fraudulent Transaction'

        return jsonify({'prediction': prediction_label})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred during prediction'}), 500

if __name__ == '__main__':
    app.run(debug=True)
