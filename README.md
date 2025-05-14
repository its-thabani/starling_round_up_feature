# Project Details
**Author**: Thabani Sibanda
**Email**: thabs2@gmail.com
**Date**: 2025-05-14


# Starling Round-Up Tool

A Python Flask app that uses the Starling Bank API to round up your weekly spending and save the difference into a savings goal.

## Features
- Fetches transactions for the last week
- Rounds up each to the nearest pound
- Transfers the total into a savings goal
- Simple Flask web interface

## Source structure

`app/static` - Static files (CSS, JS, images)

`app/templates` - HTML templates

`app/__init__.py` - Flask app setup

`app/views.py` - Flask routes

`app/roundup_service.py` - Roundup logic

`app/api_client.py` - API client for Starling Bank

`tests` - Unit tests and functional tests for the app

## Setup

`pip install -r requirements.txt`

- Add your STARLING_AUTH_TOKEN in .env

`python run.py`

- Then open `http://localhost:5000` in your browser.

## Tests
- Run `pytest` from root to execute the tests.


## Notes
- All API calls are raw (no SDK)
- Errors, timeouts, and retries are handled
- Avoids float rounding errors with `Decimal`

