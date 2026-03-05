# Shared Python Package

Common types, utilities, and constants used across backend and core packages.

## Contents

- `types.py` - Pydantic models and enums
- `utils.py` - Utility functions

## Usage

```python
from packages.shared.types import ApplicationStatus, JobListing
from packages.shared.utils import clean_text, calculate_match_score

# Use shared types
status = ApplicationStatus.SUBMITTED

# Use shared utilities
cleaned = clean_text("  Hello   World  ")
```
