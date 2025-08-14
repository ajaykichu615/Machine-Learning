import gradio as gr
import joblib

model = joblib.load("text_classifier.pkl")

# Define prediction function
def predict(text):
    prediction = model.predict([text])[0]
    probability = model.predict_proba([text])[0].max()
    return f"Prediction: {prediction} (Confidence: {probability:.2f})"

# Create Gradio interface
interface = gr.Interface(
    fn=predict,
    inputs=gr.Textbox(lines=5, placeholder="Enter your text here..."),
    outputs="text",
    title="Text Classification with Logistic Regression",
    description="Enter a piece of text and the model will classify it."
)

# Launch the app
interface.launch(share=True)