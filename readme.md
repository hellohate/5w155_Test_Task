# FastAPI Calendar: Finding the next available slot

This project allows you to find the next available time slot that does not overlap with events in Google Calendar (in the `.ics' format).

## 🧰 Requirements

- Python 3.9 or later
- pip (Python package manager)

## 📦 Installation.

### 1. Clone the repository or save the project locally:
    git clone <your repository
    cd <project folder>.
    
### 2. Create a virtual environment (optional, but recommended):
    python -m venv venv
    source venv/bin/activate  # For Linux/macOS
    venv\Scripts\activate     # For Windows

### 3. Install dependencies
    pip install -r requirements.txt

## ▶️ Starting the server
Start the development server with an automatic reboot:
```bash
   uvicorn main:app --reload
```

## 🔍 Usage
🔗 Endpoint: `/next-available-slot`
Find the next available slot by specifying the start date and duration.

Request parameters:

*`start_date`* - start date in ISO format (for example: 2025-05-06T09:00:00+00:00)

`duration` - duration in minutes (for example: 30)

Example:
```bash
  curl "http://127.0.0.1:8000/next-available-slot?start_date=2025-05-06T09:00:00%2B00:00&duration=30"
```
Output:
```json
{
  "start": "2025-05-06T09:00:00+00:00",
  "end": "2025-05-06T09:30:00+00:00"
}
```
## 📚 Notes
The calendar is connected via a public Google Calendar link in .ics format.

Only events with specified start and end dates are processed.
