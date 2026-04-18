"""
EcoTrace API - FastAPI Backend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import sqlite3
import json
from datetime import datetime, timedelta
import numpy as np
import joblib
import os

app = FastAPI(
    title="EcoTrace API",
    description="AI-Powered Sustainability Traceability for Fashion",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE = "data/ecotrace.db"

def init_db():
    """Create SQLite database"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS facilities (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            lat REAL NOT NULL,
            lon REAL NOT NULL,
            country TEXT NOT NULL,
            region TEXT NOT NULL,
            type TEXT NOT NULL,
            capacity_mtpy INTEGER
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS risk_scores (
            id INTEGER PRIMARY KEY,
            facility_id INTEGER NOT NULL,
            score_date DATE NOT NULL,
            water_stress REAL,
            overall_risk REAL,
            FOREIGN KEY (facility_id) REFERENCES facilities(id)
        )
    ''')
    
    conn.commit()
    conn.close()

@app.on_event("startup")
async def startup():
    init_db()
    print("✓ EcoTrace API initialized")

@app.get("/")
async def health_check():
    """Health check"""
    return {"status": "ok", "service": "EcoTrace API"}

@app.get("/facilities")
async def list_facilities():
    """Get all facilities"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute('''
        SELECT f.id, f.name, f.lat, f.lon, f.country, f.region, f.type,
               COALESCE((SELECT overall_risk FROM risk_scores 
                WHERE facility_id = f.id 
                ORDER BY score_date DESC LIMIT 1), 50) as latest_risk
        FROM facilities f
        ORDER BY f.id
    ''')
    
    facilities = []
    for row in c.fetchall():
        facilities.append({
            "id": row["id"],
            "name": row["name"],
            "lat": row["lat"],
            "lon": row["lon"],
            "country": row["country"],
            "region": row["region"],
            "type": row["type"],
            "latest_risk": row["latest_risk"]
        })
    
    conn.close()
    return facilities if facilities else [{"message": "No facilities yet"}]

@app.get("/facility/{facility_id}")
async def get_facility(facility_id: int):
    """Get facility details"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute("SELECT * FROM facilities WHERE id = ?", (facility_id,))
    facility = c.fetchone()
    
    if not facility:
        conn.close()
        raise HTTPException(status_code=404, detail="Facility not found")
    
    c.execute("SELECT * FROM risk_scores WHERE facility_id = ? ORDER BY score_date DESC LIMIT 1", (facility_id,))
    score = c.fetchone()
    
    conn.close()
    
    return {
        "id": facility["id"],
        "name": facility["name"],
        "lat": facility["lat"],
        "lon": facility["lon"],
        "country": facility["country"],
        "region": facility["region"],
        "type": facility["type"],
        "latest_scores": {
            "water_stress": score["water_stress"] if score else None,
            "overall_risk": score["overall_risk"] if score else None,
            "date": score["score_date"] if score else None
        } if score else {}
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
