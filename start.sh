#!/bin/bash
python -m playwright install
uvicorn main:app --host=0.0.0.0 --port=10000
