#!/usr/bin/env python
from datetime import datetime, timedelta
from typing import List
from .io import load, loadkeogram, download  # noqa: F401


def datetimerange(start: datetime, stop: datetime, step: timedelta) -> List[datetime]:
    return [start + i * step for i in range((stop - start) // step)]
