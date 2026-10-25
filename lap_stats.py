"""Small lap-time helpers for the pace summary (not yet used by app.py)."""

import os


def average_lap_time(lap_times):
    """Mean lap time in seconds."""
    return sum(lap_times) / len(lap_times)


def fastest_lap(lap_times):
    """Index and time of the fastest lap."""
    best = min(lap_times)
    return lap_times.index(best), best
