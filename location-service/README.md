# Location Service

Tracks the latest GPS coordinates for each driver and returns candidates near a pickup point.

## Run locally

Start Redis in Docker Desktop. If Redis is already running on port 6379, reuse it.

```powershell
docker run -d --name uber-location-redis -p 127.0.0.1:6379:6379 redis:7.4
```

From the repository root, run the FastAPI service.

```powershell
cd location-service
uv run location-service
```

The service defaults to port `8082` and Redis at `redis://localhost:6379/0`. Set `PORT` or `REDIS_URL` to override these defaults.

Open [Swagger UI](http://127.0.0.1:8082/docs) or use PowerShell to exercise the API.

```powershell
$locations = 'http://127.0.0.1:8082/api/v1/locations'
$driver = @{ driver_id = 'demo-driver'; latitude = 33.651; longitude = 73.156 } | ConvertTo-Json

Invoke-RestMethod 'http://127.0.0.1:8082/actuator/health'
Invoke-RestMethod -Method Post -Uri "$locations/drivers/update" -ContentType 'application/json' -Body $driver
Invoke-RestMethod "$locations/drivers/nearby?latitude=33.651&longitude=73.156"
Invoke-RestMethod -Method Delete -Uri "$locations/drivers/demo-driver"
Invoke-RestMethod 'http://127.0.0.1:8082/actuator/info'
```

The nearby endpoint defaults to a 5 km radius and returns up to 10 drivers, nearest first. Each result includes `driver_id`, `latitude`, `longitude`, and `distance_km`. Sending another update with the same ID replaces that driver's coordinates. After deletion, the driver disappears from subsequent searches.
