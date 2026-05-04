from flask import Flask, render_template, request # Flask is class # render_templete is function # requst is object created by flask automatically
import pickle
import numpy as np

app = Flask(__name__) # creating instance app from Flask class

# Load model
model = pickle.load(open("model2.pkl", "rb"))

# Home route
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# Prediction route
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get values from form
        state_florida = int(request.form.get("state_florida", 0))
        state_newyork = int(request.form.get("state_newyork", 0))

        rd_spend = float(request.form["rd_spend"])
        administration = float(request.form["administration"])
        marketing = float(request.form["marketing_spend"])

        # Prepare input for model
        final_input = np.array([[
            state_florida,
            state_newyork,
            rd_spend,
            administration,
            marketing
        ]])

        # Prediction
        prediction = model.predict(final_input)[0]

        return render_template(
            "index.html",
            prediction_text=f"💰 Predicted Profit: {prediction:,.2f}"
        )

    except Exception as e:
        return render_template(
            "index.html",
            prediction_text=f"❌ Error: {str(e)}"
        )

if __name__ == "__main__":
    app.run(debug=True)