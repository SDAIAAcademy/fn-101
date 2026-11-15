"""The ticket queue of customer care: a record type and an order.

The queue needs six of a ticket's fields. It does not need the phone number or the identity
number, so the record does not carry them.
"""

import json
from dataclasses import dataclass
from datetime import date

PRIORITY_RANK = {"urgent": 0, "high": 1, "normal": 2, "low": 3}
TODAY = date(2026, 10, 1)


@dataclass(frozen=True)
class Ticket:
    ticket_id: str
    opened: date
    district: str
    priority: str
    status: str
    text: str

    def age_days(self, today: date) -> int:
        """Whole days from the day the ticket was opened to today."""
        return (today - self.opened).days


def from_record(record: dict[str, str]) -> Ticket:
    """Build a Ticket from one parsed line of the file. opened becomes a date."""
    return Ticket(
        ticket_id=record["ticket_id"],
        opened=date.fromisoformat(record["opened"]),
        district=record["district"],
        priority=record["priority"],
        status=record["status"],
        text=record["text"],
    )


def queue(tickets: list[Ticket]) -> list[Ticket]:
    """The open tickets in working order: most urgent first, then oldest first, then by ticket id."""
    waiting = [ticket for ticket in tickets if ticket.status == "open"]
    return sorted(waiting, key=lambda t: (PRIORITY_RANK[t.priority], t.opened, t.ticket_id))


if __name__ == "__main__":
    with open("data/tickets.jsonl", encoding="utf-8") as file:
        tickets = [from_record(json.loads(line)) for line in file]
    waiting = queue(tickets)
    print(len(waiting), "open tickets of", len(tickets))
    for ticket in waiting[:5]:
        print(ticket.ticket_id, ticket.priority, ticket.opened, f"{ticket.age_days(TODAY)} days", ticket.district)
