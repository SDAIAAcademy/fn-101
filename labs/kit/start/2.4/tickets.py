"""The ticket queue of customer care: a record type and an order.

A line of data/tickets.jsonl is one ticket, for example:

    {"ticket_id": "T-20001", "opened": "2026-09-14", "district": "Al-Rabwa",
     "meter_id": "M-0311", "priority": "normal", "channel": "app", "status": "open",
     "phone": "...", "national_id": "...", "text": "..."}

The queue needs six of these fields. It does not need the phone number or the identity
number, so the record does not carry them.
"""

import json
from datetime import date

PRIORITY_RANK = {"urgent": 0, "high": 1, "normal": 2, "low": 3}
TODAY = date(2026, 10, 1)


# Step 1: a frozen data class named Ticket with the fields
#   ticket_id: str, opened: date, district: str, priority: str, status: str, text: str
# and a method age_days(self, today: date) -> int: whole days from opened to today.


def from_record(record: dict[str, str]) -> "Ticket":
    """Build a Ticket from one parsed line of the file. opened becomes a date."""
    raise NotImplementedError("step 2: date.fromisoformat turns '2026-09-14' into a date")


def queue(tickets: list["Ticket"]) -> list["Ticket"]:
    """The open tickets in working order: most urgent first, then oldest first, then by ticket id."""
    raise NotImplementedError("step 3: filter, then sorted() with a key that returns a tuple")


if __name__ == "__main__":
    with open("data/tickets.jsonl", encoding="utf-8") as file:
        tickets = [from_record(json.loads(line)) for line in file]
    waiting = queue(tickets)
    print(len(waiting), "open tickets of", len(tickets))
    for ticket in waiting[:5]:
        print(ticket.ticket_id, ticket.priority, ticket.opened, f"{ticket.age_days(TODAY)} days", ticket.district)
