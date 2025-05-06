import uvicorn
from datetime import datetime, timedelta, timezone
from typing import List, Tuple

import httpx
import ics
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

app = FastAPI()

ICS_URL = (
    "https://calendar.google.com/calendar/ical/"
    "c_fc454d3b94103c61498ddce39fd6314987c44c0a055642e2a4af7cdde24ff978"
    "%40group.calendar.google.com/public/basic.ics"
)


async def fetch_calendar() -> str:
    """
    Fetch the ICS calendar data from a public URL.

    Returns:
        str: The raw ICS calendar data.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(ICS_URL)
        response.raise_for_status()
        return response.text


def parse_events(ics_text: str) -> List[Tuple[datetime, datetime]]:
    """
    Parse ICS calendar text into a list of event start and end times.

    Args:
        ics_text (str): The raw ICS calendar data.

    Returns:
        List[Tuple[datetime, datetime]]: A sorted list of (start, end) datetimes.
    """
    calendar = ics.Calendar(ics_text)
    events: List[Tuple[datetime, datetime]] = []

    for event in calendar.events:
        if event.begin and event.end:
            start = event.begin.datetime
            end = event.end.datetime
            events.append((start, end))

    return sorted(events)


def find_next_available_slot(
        events: List[Tuple[datetime, datetime]],
        start_dt: datetime,
        duration_min: int
) -> datetime:
    """
    Find the next available time slot that doesn't overlap with existing events.

    Args:
        events (List[Tuple[datetime, datetime]]): A list of (start, end) event times.
        start_dt (datetime): The starting point to look for availability.
        duration_min (int): Desired duration in minutes.

    Returns:
        datetime: Start time of the next available slot.
    """
    duration = timedelta(minutes=duration_min)
    now = start_dt

    for event_start, event_end in events:
        if now + duration <= event_start:
            return now
        now = max(now, event_end)

    return now  # Available after last event


@app.get("/next-available-slot")
async def next_available_slot(
        start_date: datetime = Query(..., description="Start date in ISO format"),
        duration: int = Query(..., description="Duration in minutes")
) -> JSONResponse:
    """
    Endpoint to find the next available time slot given a start date and duration.

    Args:
        start_date (datetime): ISO formatted start datetime.
        duration (int): Duration of the slot in minutes.

    Returns:
        JSONResponse: The start and end time of the next available slot.
    """
    try:
        if start_date.tzinfo is None:
            start_date = start_date.replace(tzinfo=timezone.utc)

        ics_text = await fetch_calendar()
        events = parse_events(ics_text)
        available_slot_start = find_next_available_slot(events, start_date, duration)
        available_slot_end = available_slot_start + timedelta(minutes=duration)

        return JSONResponse({
            "start": available_slot_start.isoformat(),
            "end": available_slot_end.isoformat()
        })

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

