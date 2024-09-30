import time
from fastapi import FastAPI, Request, BackgroundTasks
from starlette.responses import JSONResponse

app = FastAPI()


# Middleware for logging and measuring response time
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    try:
        # Process the request
        response = await call_next(request)
    except Exception as e:
        # Handle exceptions globally
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})

    # Measure response time for the request
    process_time = time.time() - start_time
    print(f"Request: {request.method} {request.url} completed in {process_time:.2f} secs")

    return response


# Background task for sending email
def send_email(email: str, message: str):
    start_time = time.time()
    # Simulate a time-consuming task
    time.sleep(5)
    process_time = time.time() - start_time
    print(f"Email sent to {email} with message: {message}. Time taken: {process_time:.2f} secs")


# Route to trigger sending email
@app.post("/send-email/")
async def trigger_email(email: str, background_tasks: BackgroundTasks):
    # Adding the email sending task to the background
    background_tasks.add_task(send_email, email, "This is your message")
    return {"message": f"Email will be sent in the background "}
