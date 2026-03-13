# LedgerLogic

## Overview
A local-first personal finance tool designed for developers who want full control over their data. Automatically ingest, categorize, and analyze bank statements.

## Tech Stack
- Python 3.x
- SQLite (Persistence)
- PyYAML (Configuration)
- [Optional: FastAPI/Flask for Web UI]

## System Architecture
The app uses a modular ingestor-processor pattern. Data flows from raw CSVs -> Normalized Python Objects -> Categorized Records -> SQLite Storage.

## Installation
(Instructions for setting up the virtual environment and installing dependencies)