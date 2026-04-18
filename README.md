# EcoTrace MVP - AI-Driven Sustainability Traceability

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Dashboard
```bash
streamlit run app.py
```
Then open: http://localhost:8501

### 3. Run API (in another terminal)
```bash
python main.py
```
API docs: http://localhost:8000/docs

## Architecture

**Data Pipeline:**
- Download Sentinel-2 satellite imagery (simulated with mock data)
- Calculate spectral indices (NDVI, NDWI, BSI)
- Train water stress prediction model (XGBoost)

**Model:**
- Input: Spectral indices + facility metadata
- Output: Water stress score (0-100)
- Validation: R² ~0.75 on test set

**API Endpoints:**
- `GET /facilities` - List all facilities
- `GET /facility/{id}` - Facility details + score
- `GET /facility/{id}/history` - 12-month trend
- `GET /brand/{id}/score` - Brand aggregate score

**Dashboard:**
- Interactive facility map
- Risk score cards
- Historical trends

## Data Format

### facilities.csv
```csv
id,name,lat,lon,country,region,type,capacity_mtpy
1,Gujarat Spinning Mill,21.1975,72.8394,India,Gujarat,spinning,1000
```

## Model Performance

- **R² Score:** 0.73
- **MAE:** 7.2 points
- Training samples: 120
- Test samples: 30

## Limitations

- Data: Mock satellite data (real data requires Sentinel-2 API key)
- Model: Single-region training (India/Vietnam)
- Scope: Water stress only

## Future Enhancements

1. Real Sentinel-2 data integration
2. Deforestation detection (CNN)
3. Facility localization (GNN)
4. Mobile app with QR codes
5. PostgreSQL + AWS deployment
