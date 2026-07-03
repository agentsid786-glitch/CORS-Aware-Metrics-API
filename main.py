import time
import uuid
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ==========================================
# CORS Configuration
# ==========================================
# Only the assigned origin and the exam portal are allowed. No wildcards.
ALLOWED_ORIGINS = [
    "https://dash-g8nfml.example.com",
    "https://exam.sanand.workers.dev"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time"]
)

# ==========================================
# Middleware: Request ID & Process Time
# ==========================================
@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    start_time = time.time()
    req_id = str(uuid.uuid4())
    
    # Process the actual request
    response = await call_next(request)
    
    # Calculate duration
    process_time = time.time() - start_time
    
    # Attach required headers
    response.headers["X-Request-ID"] = req_id
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

# ==========================================
# Endpoint: /stats
# ==========================================
@app.get("/stats")
async def get_stats(values: str = ""):
    if not values:
        return JSONResponse({"error": "No values provided"}, status_code=400)
    
    try:
        # Parse comma-separated integers
        nums = [int(x.strip()) for x in values.split(",") if x.strip()]
    except ValueError:
        return JSONResponse({"error": "Invalid integers in input"}, status_code=400)
        
    if not nums:
        return JSONResponse({"error": "No valid numbers"}, status_code=400)
        
    # Compute statistics
    count = len(nums)
    total_sum = sum(nums)
    min_val = min(nums)
    max_val = max(nums)
    mean_val = total_sum / count
    
    # Return exactly the requested JSON format
    return {
        "email": "22ds2000150@ds.study.iitm.ac.in",
        "count": count,
        "sum": total_sum,
        "min": min_val,
        "max": max_val,
        "mean": mean_val
    }
