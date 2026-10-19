# Oura Ring 4: Bass Model Diffusion Analysis

**Course:** Marketing Analytics  
**Instructor:** Karen Hovhannisyan  
**Assignment:** Innovation Diffusion Analysis Based on TIME's Best Inventions List  
**Selected innovation:** Oura Ring 4  
**Look-alike innovation:** Fitbit activity trackers  
**Forecast scope:** United States  
**Forecast period:** 2025–2035  

---

## Executive Summary

This project applies the Bass diffusion model to historical Fitbit device-sales data and uses the estimated parameters to construct illustrative adoption scenarios for Oura Ring 4 in the United States. Oura Ring 4 was selected from TIME's Best Inventions of 2025. Fitbit activity trackers were chosen as a historical analogue because both products use wearable technology to collect health and activity information.

Annual Fitbit device-sales observations from 2011 to 2019 were used to estimate the Bass model over two time windows. The resulting parameter estimates differ across the windows, demonstrating that the estimates are sensitive to the observation period. The longer-window estimates were then used to construct low-, medium-, and high-market-potential scenarios for Oura Ring 4.

The forecast is a scenario analysis rather than a verified prediction of Oura Ring 4 sales. Fitbit device sales are not identical to first-time adopters, and the assumed U.S. market potentials are hypothetical. These limitations are considered when interpreting the results.

## 1. Selected Innovation


The selected innovation is **Oura Ring 4**, a smart ring designed to monitor health and wellness indicators through sensors and a connected mobile application. Its features include sleep analysis, heart-rate monitoring, blood-oxygen sensing, temperature trends, and activity tracking.

TIME included Oura Ring 4 in its Best Inventions of 2025 collection. The product represents the development of wearable health technology in a compact, screen-free form. Rather than requiring users to wear a conventional wrist-based tracker, it places sensors in a ring and presents insights through a smartphone application.

**Official TIME link:**  
https://time.com/collections/best-inventions-2025/7318554/oura-ring-4/

## 2. Similar Innovation from the Past: Fitbit Activity Trackers

A similar past innovation is the Fitbit activity tracker. Fitbit devices became popular as consumer wearables that collected activity and health-related data, including steps, heart rate, and sleep information on supported models. Like Oura Ring 4, Fitbit devices connect personal sensor measurements with a digital application, helping users understand patterns in their everyday behavior and wellness. Both innovations make personal health information more accessible through wearable technology.

The main difference is their form factor and product positioning. Fitbit trackers are generally worn on the wrist and have historically emphasized activity and fitness tracking, while Oura Ring 4 uses a ring design and emphasizes sleep, recovery, and continuous wellness monitoring. Fitbit is a useful historical analogue because it provides a time series of commercial device sales that can be used to estimate a Bass model. However, Fitbit sales are only a proxy for adoption: purchases may include replacement devices, and Fitbit customers are not necessarily representative of Oura Ring 4 customers.

## 3. Historical Data

The historical dataset contains annual Fitbit device sales from 2011 through 2019. Values are expressed in millions of devices.

| Year | Devices sold (millions) |
|---:|---:|
| 2011 | 0.200 |
| 2012 | 1.300 |
| 2013 | 4.476 |
| 2014 | 10.904 |
| 2015 | 21.355 |
| 2016 | 22.295 |
| 2017 | 15.343 |
| 2018 | 13.939 |
| 2019 | 15.988 |

The dataset is stored in `data/fitbit_devices_sold.csv`. The earlier observations are attributed to Fitbit's registration statement and annual filings; the 2017–2019 observations are reported in Fitbit's 2019 Form 10-K. The SEC filing reports 15.343 million devices sold in 2017, 13.939 million in 2018, and 15.988 million in 2019.

The series increases rapidly through 2016, then declines in 2017 and 2018 before rising in 2019. This pattern illustrates an important challenge for diffusion modelling: actual sales may respond to product launches, competition, changing consumer preferences, and replacement purchases, while the basic Bass model assumes a smooth diffusion process.

The observations represent **devices sold**, not verified unique first-time adopters. This is a limitation of the available proxy data and is considered when interpreting the estimates.

## 4. Bass Model Parameter Estimation

### 4.1 Model specification

The Bass model describes the adoption of a new product through innovation and imitation effects. Its parameters are:

- \(p\): coefficient of innovation, representing adoption influenced by external factors.
- \(q\): coefficient of imitation, representing adoption influenced by previous adopters.
- \(M\): market potential, or the total number of potential adopters.

The continuous-time cumulative adoption function used in this project is:

\[
N(t)=M\frac{1-e^{-(p+q)t}}
{1+\frac{q}{p}e^{-(p+q)t}}
\]

Annual modelled sales are calculated as the difference between cumulative adoption at the end and beginning of a period:

\[
S(t)=N(t)-N(t-1)
\]

The parameters are estimated by nonlinear least squares using SciPy's `curve_fit` function. Two windows are fitted to examine how the results change when the sample period changes.

### 4.2 Estimated parameters

| Fitting period | \(p\) | \(q\) | \(M\) (millions) | \(R^2\) |
|---|---:|---:|---:|---:|
| 2011–2016 | 0.0026 | 1.2108 | 80.4 | 0.999 |
| 2011–2019 | 0.0118 | 0.6744 | 121.7 | 0.821 |

The parameter estimates are saved in `data/fitbit_bass_parameters.csv`.

The shorter-window model fits the six observations very closely. However, a high \(R^2\) does not guarantee that its parameters will forecast other products reliably. With only six observations, the model may fit the historical pattern without providing robust estimates for a new market.

The longer-window model has a lower \(R^2\), partly reflecting the decline and subsequent increase in Fitbit sales. Its estimates are used for the illustrative Oura forecast because they incorporate the longer historical period. Neither fit should be interpreted as proof that Fitbit's adoption process will be replicated by Oura Ring 4.

**Figure 1:** Historical Fitbit device sales and fitted Bass curves are saved in `img/fitbit_bass_fit.png`.

## 5. Predicted Diffusion of Oura Ring 4

The forecast applies the longer-window Fitbit estimates, \(p=0.0118\) and \(q=0.6744\), as analogue parameters for Oura Ring 4. This approach assumes, for illustration, that Oura adoption may follow a diffusion pattern similar to a successful wearable device. It does not establish that Oura's actual innovation and imitation coefficients are equal to Fitbit's.

The forecast begins with 2025 as the first full calendar year following Oura Ring 4's October 2024 launch. Because reliable data on unique U.S. Oura Ring 4 adopters and total addressable adopters are not available in this analysis, the forecast uses three hypothetical market-potential scenarios.

| Scenario | Assumed U.S. market potential |
|---|---:|
| Low | 5 million potential adopters |
| Medium | 10 million potential adopters |
| High | 20 million potential adopters |

These values are scenario assumptions, not sourced estimates of actual U.S. demand. They are used to show how the diffusion path changes when the size of the potential market changes.

## 6. Geographic Scope: United States

The analysis focuses on the United States rather than the global market. A country-specific scope makes it possible to define a clearer potential-adopter population and is consistent with the availability of U.S.-specific demographic and wearable-market information.

Fitbit's 2019 Form 10-K reported U.S. revenue of approximately $799.0 million and international revenue of approximately $635.8 million for 2019, illustrating that the U.S. was a substantial market for the historical analogue. These are revenue figures, not counts of U.S. device adopters, and they are used only to provide context for the geographic choice.

The U.S. scope should not be interpreted as evidence that the forecast's assumed market potentials are established market statistics. The 5-million, 10-million, and 20-million values remain hypothetical scenario inputs and would need to be replaced with better market research if a validated market-size estimate became available.

## 7. Estimated Adopters by Period

The notebook calculates annual and cumulative modelled adopters from 2025 through 2035 for each market-potential scenario. The output is stored in `data/oura_us_forecast.csv`.

Selected results are shown below. Values are in millions and are rounded to two decimal places.

| Year | Low: new | Low: cumulative | Medium: new | Medium: cumulative | High: new | High: cumulative |
|---:|---:|---:|---:|---:|---:|---:|
| 2025 | 0.08 | 0.08 | 0.17 | 0.17 | 0.33 | 0.33 |
| 2026 | 0.16 | 0.24 | 0.32 | 0.48 | 0.63 | 0.96 |
| 2027 | 0.28 | 0.53 | 0.57 | 1.05 | 1.14 | 2.10 |
| 2028 | 0.48 | 1.00 | 0.95 | 2.00 | 1.90 | 4.00 |
| 2029 | 0.70 | 1.70 | 1.39 | 3.40 | 2.79 | 6.79 |
| 2030 | 0.85 | 2.55 | 1.70 | 5.09 | 3.40 | 10.19 |
| 2031 | 0.83 | 3.38 | 1.66 | 6.75 | 3.32 | 13.51 |
| 2032 | 0.65 | 4.03 | 1.30 | 8.06 | 2.61 | 16.11 |
| 2033 | 0.43 | 4.46 | 0.86 | 8.92 | 1.72 | 17.84 |
| 2034 | 0.25 | 4.71 | 0.51 | 9.43 | 1.01 | 18.85 |
| 2035 | 0.14 | 4.85 | 0.28 | 9.70 | 0.55 | 19.41 |

Under these assumptions, the modelled annual adoption peak occurs around 2030 in all three scenarios. The high-market-potential scenario has the greatest annual adoption and cumulative adoption because its assumed market potential is largest. The medium and low scenarios scale accordingly.

These results should be read as conditional scenarios: if the assumed market potential and transferred Fitbit parameters were reasonable approximations, the model would produce these paths. They are not observations of actual Oura Ring 4 sales and should not be presented as certain predictions.

**Figure 2:** The scenario forecast is saved in `img/oura_us_forecast.png`.

## Limitations

Several limitations affect this analysis.

1. **Sales are not the same as adoption.** Fitbit's reported device sales may include replacement purchases and do not directly measure unique first-time adopters.
2. **The analogue differs from the target product.** Fitbit wrist-worn trackers and Oura smart rings have different designs, prices, features, customer segments, and purchase motivations.
3. **Short time series.** Nine annual observations provide limited information for estimating three nonlinear parameters. The parameter estimates vary materially across fitting windows.
4. **Changing sales patterns.** Fitbit sales decline after 2016 and increase in 2019. A basic Bass curve cannot explicitly model product refreshes, competition, changing prices, or market saturation caused by multiple product generations.
5. **Market potential is hypothetical.** The 5-million, 10-million, and 20-million values are sensitivity scenarios rather than independently verified market-size estimates.
6. **No Oura-specific calibration.** This forecast does not use a reliable time series of unique U.S. Oura Ring 4 adopters. It therefore cannot validate the transferred Fitbit parameters.
7. **Uncertainty in the forecast horizon.** Forecasts through 2035 are sensitive to the chosen parameters and assumptions. The further the forecast extends, the more uncertainty accumulates.

A stronger future analysis would use U.S. smart-ring adoption or shipment data, distinguish new buyers from replacement purchases, and estimate the Bass parameters from observations specific to the target product or a closer analogue.

## Conclusion

The project demonstrates how the Bass diffusion model can be estimated from historical wearable-device sales and used to build conditional diffusion scenarios for a newer innovation. Fitbit provides a useful historical reference, while Oura Ring 4 offers a contemporary example of health-focused wearable technology.

The analysis suggests that the assumed market potential strongly affects the projected number of adopters. However, because the model uses Fitbit parameters and hypothetical U.S. market sizes, the forecast is best interpreted as an exploratory scenario analysis. The assumptions and limitations are central to interpreting the results responsibly.

## References

1. TIME. (2025). *Oura Ring 4*. TIME Best Inventions of 2025. https://time.com/collections/best-inventions-2025/7318554/oura-ring-4/

2. Bass, F. M. (1969). A new product growth for model consumer durables. *Management Science, 15*(5), 215–227. https://doi.org/10.1287/mnsc.15.5.215

3. Fitbit, Inc. (2015). *Registration Statement on Form S-1*. U.S. Securities and Exchange Commission. https://www.sec.gov/Archives/edgar/data/1447599/000119312515362595/d54385ds1.htm

4. Fitbit, Inc. (2017). *Annual Report on Form 10-K for the fiscal year ended December 31, 2016*. U.S. Securities and Exchange Commission. https://www.sec.gov/Archives/edgar/data/1447599/000144759917000010/fitbit1231201610k.htm

5. Fitbit, Inc. (2018). *Annual Report on Form 10-K for the fiscal year ended December 31, 2017*. U.S. Securities and Exchange Commission. https://www.sec.gov/Archives/edgar/data/1447599/000162828018002658/fitbit1231201710-k.htm

6. Fitbit, Inc. (2019). *Annual Report on Form 10-K for the fiscal year ended December 31, 2018*. U.S. Securities and Exchange Commission. https://www.sec.gov/Archives/edgar/data/1447599/000162828019002374/fitbit1231201810-k.htm

7. Fitbit, Inc. (2020). *Annual Report on Form 10-K for the fiscal year ended December 31, 2019*. U.S. Securities and Exchange Commission. https://www.sec.gov/Archives/edgar/data/1447599/000144759920000016/fit-20191231.htm

