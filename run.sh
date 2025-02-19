#!/bin/bash
uvicorn app.main:appAPI --host 0.0.0.0 --port 8000 --reload