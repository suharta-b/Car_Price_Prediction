from flask import Flask, render_template, request
import pickle

app = Flask(__name__)
model = pickle.load(open("Price_prediction_Random_Forest_model.pkl", "rb"))

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        Year = int(request.form["Year"])
        Year = 2020 - Year

        Present_Price = float(request.form["Present_Price"])
        Kms_Driven = int(request.form["Kms_Driven"])
        Owner = int(request.form["Owner"])

        # Handling the encoded categorical feature Fuel_Type
        Fuel_Type_Petrol = request.form['Fuel_Type']
        if Fuel_Type_Petrol == 'Petrol':
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1

        # Handling the encoded categorical feature Seller_Type
        Seller_Type_Individual = request.form['Seller_Type']
        if Seller_Type_Individual == 'Individual':
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0

        # Handling the encoded categorical feature Transmission_Type
        Transmission_Manual = request.form['Transmission_Type']
        if Transmission_Manual == 'Manual':
            Transmission_Manual = 1
        else:
            Transmission_Manual = 0

        prediction = model.predict([[Present_Price, Kms_Driven, Owner, Year, Fuel_Type_Diesel, Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Manual]])
        output = round(prediction[0], 2)

        if output < 0:
            return render_template("index.html", prediction_text="Sorry! You cannot sell this car")
        else:
            return render_template('index.html', prediction_text="You can sell this car at {} lakhs !!".format(output))
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)