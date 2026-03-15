# OpenMandate Python SDK

The official Python SDK for [OpenMandate](https://openmandate.ai).
Post mandates, check status, and receive matches through the OpenMandate API.

OpenMandate helps founders find cofounders and early teammates beyond their
network. Describe what you need and what you offer. OpenMandate keeps evaluating
fit over time and introduces both sides when there is real mutual match.

## Installation

```bash
pip install openmandate
```

## Quick Start

```python
from openmandate import OpenMandate

client = OpenMandate(api_key="om_live_...")

# Create a mandate with want + offer
mandate = client.mandates.create(
    want="Looking for a technical cofounder for my SaaS",
    offer="8 years in sales and BD, 50+ enterprise relationships",
)
print(f"Created: {mandate.id}, status: {mandate.status}")

# Answer follow-up questions
while mandate.pending_questions:
    answers = []
    for q in mandate.pending_questions:
        answer = input(f"{q.text}: ")
        answers.append({"question_id": q.id, "value": answer})
    mandate = client.mandates.submit_answers(mandate.id, answers=answers)

# Wait for a match (polls until matched or timeout)
mandate = client.mandates.wait_for_match(mandate.id, timeout=600)
print(f"Matched! Match ID: {mandate.match_id}")

# View the match
match = client.matches.retrieve(mandate.match_id)
print(f"Grade: {match.compatibility.grade_label}")
print(f"Summary: {match.compatibility.summary}")

# Accept the match
match = client.matches.accept(match.id)
```

## Authentication

Pass your API key directly or set the `OPENMANDATE_API_KEY` environment variable:

```python
# Explicit
client = OpenMandate(api_key="om_live_...")

# From environment
import os
os.environ["OPENMANDATE_API_KEY"] = "om_live_..."
client = OpenMandate()
```

## Configuration

```python
client = OpenMandate(
    api_key="om_live_...",
    base_url="https://api.openmandate.ai",  # default
    timeout=120.0,                           # seconds, default 60
)
```

## API Reference

### Mandates

#### `client.mandates.create(*, want, offer)`

Create a new mandate with want and offer.

```python
mandate = client.mandates.create(
    want="Looking for a UX agency for our B2B dashboard",
    offer="Series A fintech, $1.8M ARR, two frontend engineers ready",
)
```

**Parameters:**
- `want` (str, required): What you are looking for. Minimum 20 characters.
- `offer` (str, required): What you bring to the table. Minimum 20 characters.

Primary verified contact is auto-selected.

**Returns:** `Mandate` with follow-up questions in `pending_questions`.

---

#### `client.mandates.retrieve(mandate_id)`

Get a mandate by ID.

```python
mandate = client.mandates.retrieve("mnd_abc123")
```

**Returns:** `Mandate`

---

#### `client.mandates.list(status=None, limit=None, next_token=None)`

List mandates with optional filtering. Returns open mandates by default (excludes closed). Supports auto-pagination.

```python
# List open mandates (default — excludes closed)
page = client.mandates.list()

# List only closed mandates
page = client.mandates.list(status="closed")

# Filter by specific status
page = client.mandates.list(status="active", limit=10)
for mandate in page.items:
    print(mandate.id)

# Auto-paginate across all pages
for mandate in client.mandates.list(status="active"):
    print(mandate.id)
```

**Parameters:**
- `status` (str, optional): Filter by status (`intake`, `active`, `pending_input`, `matched`, `closed`). Returns open mandates by default.
- `limit` (int, optional): Max items per page.
- `next_token` (str, optional): Pagination cursor.

**Returns:** `SyncPage[Mandate]`

---

#### `client.mandates.submit_answers(mandate_id, answers, corrections=None)`

Submit answers to pending intake questions.

```python
mandate = client.mandates.submit_answers(
    "mnd_abc123",
    answers=[
        {"question_id": "q_001", "value": "Looking for a technical co-founder"},
        {"question_id": "q_002", "value": "fintech"},
    ],
)
```

**Parameters:**
- `mandate_id` (str): The mandate ID.
- `answers` (list[AnswerParam]): Answers to submit. Each has `question_id` and `value`.
- `corrections` (list[CorrectionParam], optional): Corrections to previous answers.

**Returns:** `Mandate` (may contain new `pending_questions`)

---

#### `client.mandates.close(mandate_id)`

Close a mandate.

```python
mandate = client.mandates.close("mnd_abc123")
```

**Returns:** `Mandate`

---

#### `client.mandates.complete_intake(mandate_id, answer_fn)`

High-level helper that loops through intake until all questions are answered.

```python
def answer_questions(questions):
    """Automatically answer all pending questions."""
    return [
        {"question_id": q.id, "value": f"Answer for: {q.text}"}
        for q in questions
    ]

mandate = client.mandates.complete_intake("mnd_abc123", answer_questions)
```

**Parameters:**
- `mandate_id` (str): The mandate ID.
- `answer_fn` (callable): Receives a list of `Question` objects, returns a list of `AnswerParam` dicts.

**Returns:** `Mandate` with no remaining `pending_questions`

---

#### `client.mandates.wait_for_match(mandate_id, timeout=300, poll_interval=5)`

Poll a mandate until it reaches `matched` status.

```python
mandate = client.mandates.wait_for_match("mnd_abc123", timeout=600)
```

**Parameters:**
- `mandate_id` (str): The mandate ID.
- `timeout` (float): Max seconds to wait. Default 300.
- `poll_interval` (float): Seconds between polls. Default 5.

**Returns:** `Mandate` with status `matched`

**Raises:** `APITimeoutError` if timeout elapses

---

### Contacts

#### `client.contacts.list(limit=None, next_token=None)`

List your verified contacts.

```python
for contact in client.contacts.list():
    print(f"{contact.contact_value} ({contact.status})")
```

**Returns:** `SyncPage[VerifiedContact]`

---

#### `client.contacts.add(contact_type, contact_value, display_label=None)`

Add a new contact. Sends a verification code.

```python
contact = client.contacts.add("email", "work@example.com", display_label="Work")
# contact.status == "pending" — check email for OTP
```

**Returns:** `VerifiedContact` with `status: "pending"`

---

#### `client.contacts.verify(contact_id, code)`

Verify a contact with the OTP code.

```python
contact = client.contacts.verify("vc_abc123", "12345678")
```

**Returns:** `VerifiedContact` with `status: "verified"`

---

#### `client.contacts.update(contact_id, display_label=None, is_primary=None)`

Update a contact's label or set it as primary.

```python
client.contacts.update("vc_abc123", is_primary=True)
```

**Returns:** `VerifiedContact`

---

#### `client.contacts.delete(contact_id)`

Delete a contact. Cannot delete your last verified contact.

```python
client.contacts.delete("vc_abc123")
```

**Returns:** `dict`

---

#### `client.contacts.resend_otp(contact_id)`

Resend the verification code for a pending contact.

```python
client.contacts.resend_otp("vc_abc123")
```

**Returns:** `VerifiedContact`

---

### Matches

#### `client.matches.list(limit=None, next_token=None)`

List matches. Supports auto-pagination.

```python
for match in client.matches.list():
    print(f"{match.id}: {match.status}")
```

**Returns:** `SyncPage[Match]`

---

#### `client.matches.retrieve(match_id)`

Get a match by ID.

```python
match = client.matches.retrieve("m_abc123")
print(match.compatibility.grade_label)
```

**Returns:** `Match`

---

#### `client.matches.accept(match_id)`

Accept a match.

```python
match = client.matches.accept("m_abc123")
```

**Returns:** `Match`

---

#### `client.matches.decline(match_id)`

Decline a match.

```python
match = client.matches.decline("m_abc123")
```

**Returns:** `Match`

---

## Error Handling

All API errors inherit from `OpenMandateError`. HTTP errors are mapped to specific exception classes:

```python
from openmandate import (
    OpenMandate,
    BadRequestError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    APIError,
)

client = OpenMandate()

try:
    mandate = client.mandates.retrieve("mnd_nonexistent")
except NotFoundError:
    print("Mandate not found")
except BadRequestError as e:
    print(f"Bad request: {e.message}")
except AuthenticationError:
    print("Bad API key")
except ValidationError as e:
    print(f"Validation failed: {e.message}")
except RateLimitError:
    print("Slow down!")
except APIError as e:
    print(f"API error {e.status_code}: {e.message}")
```

### Exception Hierarchy

```
OpenMandateError
  APIError (status_code, code, details)
    BadRequestError (400)
    AuthenticationError (401)
    PermissionDeniedError (403)
    NotFoundError (404)
    ConflictError (409)
    ValidationError (422)
    RateLimitError (429)
    InternalServerError (5xx)
  APIConnectionError
    APITimeoutError
```

## Async Usage

The async client mirrors the sync API exactly:

```python
import asyncio
from openmandate import AsyncOpenMandate

async def main():
    async with AsyncOpenMandate(api_key="om_live_...") as client:
        # Create a mandate
        mandate = await client.mandates.create(want="Looking for a technical cofounder", offer="8 years in sales and BD")

        # Submit answers
        mandate = await client.mandates.submit_answers(
            mandate.id,
            answers=[{"question_id": "q_001", "value": "Technical co-founder"}],
        )

        # List with auto-pagination
        async for mandate in await client.mandates.list(status="active"):
            print(mandate.id)

        # Wait for match (async polling)
        mandate = await client.mandates.wait_for_match(mandate.id)

        # Accept match
        match = await client.matches.accept(mandate.match_id)

asyncio.run(main())
```

## Context Manager

Both clients support context managers for automatic cleanup:

```python
# Sync
with OpenMandate(api_key="om_live_...") as client:
    mandate = client.mandates.create(want="Looking for a technical cofounder", offer="8 years in sales and BD")

# Async
async with AsyncOpenMandate(api_key="om_live_...") as client:
    mandate = await client.mandates.create(want="Looking for a technical cofounder", offer="8 years in sales and BD")
```

## Types

All response models are Pydantic v2 `BaseModel` instances with full type information:

```python
from openmandate import Mandate, Match, Question, Compatibility

mandate: Mandate = client.mandates.retrieve("mnd_xxx")
mandate.id          # str
mandate.status      # "intake" | "processing" | "active" | ...
mandate.category    # str | None
mandate.contact_ids        # list[str]
mandate.pending_questions  # list[Question]
mandate.intake_answers     # list[IntakeAnswer]

match: Match = client.matches.retrieve("m_xxx")
match.compatibility        # Compatibility | None
match.compatibility.grade       # str ("good", "strong", "exceptional")
match.compatibility.grade_label # str ("Good Match", "Strong Match", "Exceptional Match")
match.compatibility.strengths  # list[Strength]
```

## Requirements

- Python 3.8+
- Dependencies (installed automatically): `httpx`, `pydantic`, `anyio`
