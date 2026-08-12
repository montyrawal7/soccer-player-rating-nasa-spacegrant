# **Soccer Player Rating App**
### **NASA New York Space Grant Consortium — Research Initiative (2026–2027)**



## **1. Title and Abstract**

* **Title:** Using Machine Learning to Standardize Amateur Soccer Ratings Against Professional Benchmarks
* **Abstract:**
  Amateur and youth soccer players often struggle to accurately judge their own skills, frequently overestimating their speed, strength, or technical control. This project addresses that problem with a Streamlit web application that lets players self-report their physical and technical performance and compare it directly against a database of over 16,000 professional players. Users enter scores for position-specific attributes — informed by sourced, real-world benchmark tests (e.g., cone-weave drills for dribbling, shot-speed standards for finishing) — and the app statistically places them against professional players at the same position using Z-scores. An XGBoost regression model then predicts an overall talent rating on the standard 1–99 scale, giving players a data-driven look at their athletic standing relative to professionals.



## **2. Problem Statement & Objectives**

* **The Problem:**
  Amateur soccer players often have inflated views of their own skills, assigning themselves arbitrary ratings (like a "90 Pace" or "85 Dribbling") without any real proof. This lack of objective testing makes it difficult for players to know where they actually need to improve.
* **The Objective:**
  Use regression to predict a rating on a continuous **1 to 99 scale**, given a player's self-reported physical and technical attributes. The current implementation uses an **XGBoost regressor** trained on the professional player dataset; it takes user-entered metrics (e.g., sprint speed, dribbling, passing) and outputs a predicted overall rating, alongside a statistical (Z-score) comparison to professional players at the same position.



## **3. Background & Literature Review**

* **Context:**
  Data analytics is a massive part of modern professional soccer, but the high-tech gear (like GPS vests and optical cameras) is far too expensive for grassroots players. Apps like *Techne Futbol* have proven that amateur players like logging their drills, but no existing app anchors those personal scores to real-world, elite database distributions.
* **Prior Work & Limitations:**
  * **Traditional Match Winner/Transfer Valuation Models:** Many machine learning models focus solely on high-level team metrics (goals, possession percentages, or market values) to predict match results or transfer fees, which fails to help a single player standing on a local field looking to evaluate their own athleticism.
  * **EPL Performance Evolution Study (Bush et al., UK):** A landmark study on the evolution of physical demands in the English Premier League showed that high-intensity sprinting distance increased by ~35% and overall sprint frequency increased by ~85% over a seven-season period, and confirmed physical baselines vary significantly by position. While this proves elite standards are rising and position-specific, its data relies on expensive, stadium-grade tracking systems inaccessible to amateur players.
  * **Data Source Limitations:** This project's benchmark dataset (EA Sports FC ratings) is compiled using a global scouting and data-reviewer network, but coverage is not uniform across leagues. Players in Europe's top five leagues are more heavily scouted and reviewed than those in less-covered leagues elsewhere in the world, which can make ratings for under-scouted regions noisier or less reliable as a benchmark. This is an acknowledged limitation of using this dataset as a global standard, and is discussed further in Section 4.
* **My Contribution:**
  This app bridges the gap identified in prior work by taking position-specific physical and technical thresholds and making them testable at the grassroots level using self-reported inputs and standard data science libraries, delivering pro-grade benchmarking for free — without requiring expensive tracking hardware.



## **4. Data Sourcing & Description**

* **Data Sources:**
  * **Local database:** relational database (`data/soccer_research.db`) powered by SQLite3.
  * **Source dataset:** mapped from the EA Sports FC 26 Player Ratings dataset, containing 16,228 professional player records.
* **A Note on Data Quality:**
  EA's player ratings combine statistical data with subjective scouting judgment from a global network of reviewers. Coverage and scouting intensity are not equal across all leagues and regions — players from more prominent leagues tend to have more reliable ratings than those from less-covered leagues. This project treats the dataset as a benchmark against *EA's rating system*, not as a perfectly objective measure of footballing ability, and this limitation is acknowledged in the methodology.
* **Features Used:**
  * **Physical:** `Height`, `Weight`, `Weak Foot`, `Skill Moves`, Acceleration, Sprint Speed, Strength, Stamina, Agility, Jumping.
  * **Technical:** Dribbling, Ball Control, Passing, Vision, Finishing, Shot Power, Long Shots, Crossing, Curve, Free Kick Accuracy, Standing Tackle, Sliding Tackle, Interceptions, Heading Accuracy, Positioning, Composure, Penalties.
  * **Contextual:** Position (Forward, Midfielder, Defender) used to ensure fair, position-specific comparisons and to determine which technical attributes a user is asked to self-rate.



## **5. Methodology (The Technical Plan)**

* **Data Preprocessing:**
  Filter the professional dataset by position, and use position-specific means and standard deviations to calculate Z-scores — showing how a user's self-reported stats compare statistically to professional players at their same position.
* **Feature Engineering:**
  Convert user self-assessments (guided by sourced benchmark tests, e.g., cone-weave drill times, shot-speed ranges, tackle success rates) into the same attribute scale used by the professional dataset, so they can be fed directly into the model.
* **Algorithm:**
  * **XGBoost Regressor** — trained on the full professional dataset to predict overall rating from player attributes; currently the only model implemented and in use.
  * **Planned/Future Work:** training and comparing Linear Regression and Random Forest models against XGBoost, to evaluate whether a simpler or different model performs comparably.



## **6. Evaluation Metrics**

To verify that the predictive rating system is statistically sound and doesn't wildly overestimate or underestimate a user, we evaluate the model using:
* **RMSE (Root Mean Squared Error):** To penalize large mathematical misses and ensure ratings stay realistic.
* **MAE (Mean Absolute Error):** To track the average difference between predicted and actual player ratings.



## **7. Current Status & Next Steps**

* Completed: SQLite database setup (16,228 professional player records), XGBoost regression model training, Streamlit app with position-specific self-assessment inputs, Z-score comparison against professional players by position, sourced benchmark guidance for each self-rated attribute.
* In Progress: Public deployment (Streamlit Community Cloud), model comparison (evaluating Random Forest and Linear Regression alongside XGBoost), UI/visual refinement, data-quality review of feature importance.
* Planned: Final research report and evaluation write-up for the Consortium.



## **How to Run Locally**

```bash
git clone <repo-url>
cd soccer-player-rating-nasa-spacegrant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run src/app.py
```
