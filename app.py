from src.constants import APP_HOST, APP_PORT
from src.pipeline.training_pipeline import TrainPipeline
from src.pipeline.prediction_pipeline import VehicleData, VehicleDataClassifer
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse
from uvicorn import run
from src.logger import logging

from typing import Optional

# Initialize FastAPI app
app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class DataForm:
    """
    Helper class to parse and store form data from the request.
    """
    def __init__(self, request: Request):
        self.request: Request = request
        self.Gender: Optional[str] = None
        self.Age: Optional[int] = None
        self.Driving_License: Optional[int] = None
        self.Region_Code: Optional[float] = None
        self.Previously_Insured: Optional[int] = None
        self.Annual_Premium: Optional[float] = None
        self.Policy_Sales_Channel: Optional[float] = None
        self.Vintage: Optional[int] = None
        self.Vehicle_Age: Optional[int] = None
        self.Vehicle_Damage: Optional[int] = None

    async def get_vehicle_data(self):
        """
        Asynchronously parse form data from the request and populate attributes.
        """
        form = await self.request.form()
        self.Gender = form.get("Gender")
        self.Age = form.get("Age")
        self.Driving_License = form.get("Driving_License")
        self.Region_Code = form.get("Region_Code")
        self.Previously_Insured = form.get("Previously_Insured")
        self.Annual_Premium = form.get("Annual_Premium")
        self.Policy_Sales_Channel = form.get("Policy_Sales_Channel")
        self.Vintage = form.get("Vintage")
        self.Vehicle_Age = form.get("Vehicle_Age")
        self.Vehicle_Damage = form.get("Vehicle_Damage")

@app.get("/", tags=["authentication"])
async def index(request: Request):
    """
    Render the main vehicle data input form.
    """
    logging.info("Rendering vehicle data input form.")
    return templates.TemplateResponse(
        "vehicledata.html", {"request": request, "context": "Rendering"}
    )

@app.get("/train")
async def trainRouteClient():
    """
    Trigger the model training pipeline.
    """
    try:
        logging.info("Training pipeline initiated.")
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        logging.info("Training pipeline completed successfully.")
        return Response("Training Successfull")
    except Exception as e:
        logging.error(f"Error occurred during training: {e}")
        return Response(f"Error Occurred {e}")

@app.post("/")
async def predictRouteClient(request: Request):
    """
    Handle form submission, make prediction, and render result.
    """
    try:
        logging.info("Prediction request received.")
        form = DataForm(request)
        await form.get_vehicle_data()
        logging.info("Form data parsed successfully.")

        # Create VehicleData instance from form data
        vehicle_data = VehicleData(
            Gender=form.Gender,
            Age=form.Age,
            Driving_License=form.Driving_License,
            Region_Code=form.Region_Code,
            Previously_Insured=form.Previously_Insured,
            Annual_Premium=form.Annual_Premium,
            Policy_Sales_Channel=form.Policy_Sales_Channel,
            Vintage=form.Vintage,
            Vehicle_Age=form.Vehicle_Age,
            Vehicle_Damage=form.Vehicle_Damage
        )

        # Convert input data to DataFrame
        vehicle_df = vehicle_data.get_vehicle_input_dataframe()
        logging.info("Vehicle input data converted to DataFrame.")

        # Load model and make prediction
        model_predictor = VehicleDataClassifer()
        value = model_predictor.predict(dataframe=vehicle_df)[0]
        logging.info(f"Prediction made successfully: {value}")

        # Interpret prediction result
        status = "Yes" if value == 1 else "No"

        # Render result in template
        return templates.TemplateResponse(
            "vehicledata.html",
            {"request": request, "context": status}
        )
    except Exception as e:
        logging.error(f"Error occurred during prediction: {e}")
        return {"status": False, "error": f"{e}"}

if __name__ == "__main__":
    # Start the FastAPI app using uvicorn
    logging.info(f"Starting app at {APP_HOST}:{APP_PORT}")
    run(app, host=APP_HOST, port=APP_PORT)