# Oura Ring 4: Bass Model Diffusion Analysis

## Project Overview

This project applies the Bass diffusion model to historical Fitbit device-sales data and uses the estimated parameters to construct illustrative U.S. adoption scenarios for Oura Ring 4, selected from TIME's Best Inventions of 2025.

## Repository Structure

- `bass_analysis.ipynb` — analysis, parameter estimation, plots, and forecast scenarios.
- `data/fitbit_devices_sold.csv` — annual Fitbit device sales from 2011 to 2019.
- `data/fitbit_bass_parameters.csv` — estimated Bass parameters for two fitting windows.
- `data/oura_us_forecast.csv` — annual and cumulative adoption scenarios for 2025–2035.
- `img/fitbit_bass_fit.png` — historical sales and fitted Bass curves.
- `img/oura_us_forecast.png` — U.S. adoption scenario graph.
- `report/report_source.md` — written report in Markdown.
- `report/report.pdf` — PDF report.
- `references/references.md` — source list.

## Run the Analysis

Create and activate a Python virtual environment, install the packages in `requirements.txt`, and run `bass_analysis.ipynb` from top to bottom.

The notebook uses Python, pandas, NumPy, Matplotlib, and SciPy.

## Interpretation and Limitations

Fitbit device sales are a proxy for wearable adoption, not a count of unique first-time adopters. Fitbit parameters are used as an analogy for Oura Ring 4 rather than as Oura-specific estimates. The 5-million, 10-million, and 20-million market-potential values are hypothetical scenarios, not verified market statistics. Forecast results should therefore be interpreted as illustrative scenarios rather than certain predictions.

## References

See [`references/references.md`](references/references.md) for the data sources and methodological reference.
