from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Azure endpoint URL and authentication key
Endpoint = "https://yukeshwar-bank-ws-bzlpk.eastus.inference.ml.azure.com/score"
Auth_key = "BlLjuBicn1SdluWVxoeItd1OGXrufZpb"

@app.route('/', methods=['POST', 'GET'])
def home():
    # Pass 'enumerate' to the template
    return render_template('Index.html', enumerate=enumerate)

@app.route('/predict', methods=['POST'])
def predict():
    # Collect data from form
    data_row = [
        int(request.form.get('age')),  # age (numeric)
        request.form.get('job'),  # job (categorical)
        request.form.get('marital'),  # marital (categorical)
        request.form.get('education'),  # education (categorical)
        request.form.get('default'),  # default (categorical)
        request.form.get('housing'),  # housing (categorical)
        request.form.get('loan'),  # loan (categorical)
        request.form.get('contact'),  # contact (categorical)
        request.form.get('month'),  # month (categorical)
        int(request.form.get('duration')),  # duration (numeric)
        int(request.form.get('campaign')),  # campaign (numeric)
        int(request.form.get('pdays')),  # pdays (numeric)
        int(request.form.get('previous')),  # previous (numeric)
        request.form.get('poutcome'),  # poutcome (categorical)
        float(request.form.get('emp_var_rate')),  # emp.var.rate (numeric)
        float(request.form.get('cons_price_idx')),  # cons.price.idx (numeric)
        float(request.form.get('cons_conf_idx')),  # cons.conf.idx (numeric)
        float(request.form.get('euribor3m')),  # euribor3m (numeric)
        float(request.form.get('nr_employed'))  # nr.employed (numeric)
    ]

    # Prepare data InputData for API
    InputData = {
        "input_data": {
            "columns": [
                "age", "job", "marital", "education", "default", "housing", "loan", 
                "contact", "month", "duration", "campaign", "pdays", "previous", 
                "poutcome", "emp.var.rate", "cons.price.idx", "cons.conf.idx", 
                "euribor3m", "nr.employed"
            ],
            "index": [0],
            "data": [data_row]
        }
    }

    # Set headers with bearer token
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {Auth_key}'}

    try:
        # Make request to Azure endpoint
        response = requests.post(url=Endpoint, json=InputData, headers=headers)
        print("Response content:", response.content)  # Print response content for debugging

        # Process prediction result
        if response.status_code == 200:
            prediction = response.json()
            return render_template('Index.html', prediction=prediction, enumerate=enumerate)
        else:
            error_message = f"Error: {response.status_code}. Prediction failed."
            return render_template('Index.html', error_message=error_message, enumerate=enumerate)
    except Exception as e:
        error_message = str(e)
        return render_template('Index.html', error_message=error_message, enumerate=enumerate)

if __name__ == '__main__':
    app.run(debug=True)
