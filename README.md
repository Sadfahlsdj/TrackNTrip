**TrackNTrip**

**Inspiration**

**TrackNTrip** was born from a classic road trip dilemma—the driver asking their passenger where the nearest gas station is. Inspired by the challenge of balancing fuel costs, time, and environmental impact, we set out to create a **smarter** way to travel. We combined **eco-conscious travel**, **budget optimization**, and **immersive discovery** into one seamless experience. **TrackNTrip** not only helps travelers make cost-effective and sustainable choices but also transforms every journey into an **engaging and educational** adventure.

**What It Does**
**TrackNTrip** is a web-based application designed to optimize and elevate the road trip experience.

Key features include:

**Optimal Fuel Stops:**
Users input their destination, and the app calculates the most cost-effective gas stations along the route.
The optimization considers **three** metrics: **fuel price**, **detour distance**, and **added travel time**, allowing users to prioritize based on their preferences via **adjustable weighting**.

**CO2 Emissions Estimation:**
The app estimates the **additional CO2 emissions incurred** during the detour for each suggested fuel stop, helping users make **eco-conscious** choices.

**AI-Powered Landmark Storytelling:**
Using **LLMs**, the app generates **engaging descriptions** about nearby historical landmarks, blending **education and entertainment** into the journey.

**Gamification:**
Users earn points for **low mileage** and compete on **leaderboards** (weekly, monthly, and all-time). **Badges and achievements** encourage exploration and sustainable travel habits.

**TNT Mode:**
A hidden toggle in the form of an **Angry Bird** unleashes **whimsical and creative** app features to entertain users on long drives.

**How We Built It**

**Backend:**

**Python:** Data processing, model training (**74% accuracy**)

_Model:_ **XGBoost** was chosen for its high predictive accuracy, ability to model complex relationships between gas station features and optimality, and reasonable speed/scalability. It's well-suited to the numerical data and the need for reliable gas station recommendations.

**LLM**-generated descriptions (**Meta Llama 3.2.1b**): Responsible for feature engineering, scaling, and exporting trained models.

Libraries: pandas, osmnx (for route calculations), scikit-learn, joblib, shap, geopy (finding latitude/longitude)

**Node.js (Express)**:
Handles API endpoints for the frontend.
Loads models, applies preprocessing steps **(e.g., OSMnx for routing)**, and performs predictions.
Manages real-time data handling and response generation.

****Process:****

**Data Ingestion & Preprocessing**: Load gas station and landmark data, handle missing values, and convert coordinates to usable formats (DMS to DD).

**Feature Engineering:** Create new features such as a weighted cost-benefit score (combining mileage, time, price), fuel cost (if MPG available), distances/times to/from start/end points (using **OSMnx**), and potentially traffic/amenity features.

**Feature Scaling:** Scale numerical features using **StandardScaler** (and importantly, save the fitted scaler for later use in the backend).

**Target Variable Creation:** Define "optimal" gas stations based on a cost-benefit threshold and create a binary target variable (optimal/not optimal).

**Model Training:** Train a machine learning model (**XGBoost**) on the prepared data, tune hyperparameters, and evaluate performance.

**Model Persistence:** Save the trained model and the **StandardScaler** object to files for use in the backend API.

**Landmark Descriptions:** Use a large language model (**Meta Llama**) separately to generate descriptions for landmarks. This process is separate, not part of the gas station ranking model.

**Frontend:**

**React:**
Built a dynamic and responsive user interface to display interactive features.

**Leaflet.js:**
Powered the map functionality to render routes, gas station locations, and nearby landmarks.
Provided a lightweight and customizable alternative to Google Maps.

**HTML/CSS with Tailwind CSS:**
Structured the application layout with responsive styling for a clean, user-friendly design.

**Tanstack query:**
Simplified asynchronous data fetching, caching, and updating in the React frontend, improving performance and streamlining API interactions for data like gas station and landmark information.

**Data Sources:**

**Gas Station Data:** CSV or APIs like GasBuddy for price and location details.

**Landmark Data:** Historical datasets or APIs like WikiData.

**OSMnx:** For accurate route and detour calculations.

**Challenges We Faced**

**Defining “Optimal”:**
Balancing **fuel cost, distance, time, and CO2 emissions** required extensive experimentation and refinement of weighting algorithms.

**Model Integration:**
Ensuring consistent feature scaling between **Python** (model training) and **Node.js** (runtime prediction) demanded meticulous handling of the **StandardScaler**.

**AI Storytelling:**
Generating engaging and relevant landmark blurbs required fine-tuning **LLM prompts** and handling edge cases where historical data was limited.

**Data Preprocessing:**
Cleaning and formatting datasets (e.g., converting latitude/longitude from DMS to DD) was critical for accurate routing.

**Accomplishments**

**Functional Prototype:** Delivered a working app showcasing core features.

**Seamless AI Integration:** Successfully incorporated AI storytelling, offering an engaging travel experience.

**Gamification:** Developed a leaderboard system to drive user engagement.

**Intuitive UI:** Designed a clean, user-friendly interface with smooth navigation.

**What We Learned**

**Model Selection and Evaluation:** We honed our skills in selecting appropriate machine learning models (RandomForest vs. XGBoost), tuning their hyperparameters, and evaluating their performance using relevant metrics.

**API/Library Mastery:** Improved understanding of Leaflet.js, OSMnx, and other integrations.

**The Importance of Recognizing History:** This project highlighted the importance of recognizing history, both in the context of the landmarks we explored and in the broader sense of understanding the historical context of the environment, innovation, and infrastructure.

**Impact of AI to Shape History:** We also realized the power of AI to not only analyze history but also to shape it. By providing tools for optimizing travel and fuel consumption, we can contribute to a more sustainable future, influencing the history of transportation and environmental impact. Our project demonstrated how AI can be used to promote more responsible and informed decision-making.

**AI Integration Challenges:** We learned about the challenges of integrating ML models into web applications, including managing dependencies, ensuring data consistency, and handling the computational demands of the models.

**Cross-Team Collaboration:** Enhanced our ability to divide responsibilities and communicate effectively under tight deadlines.

**What’s Next for TrackNTrip**

**Enhanced Gas Price Data:** Integrate with a real-time gas price API for more reliable updates.

**Mobile App Development:** Expand functionality to iOS and Android for greater accessibility.

**User Testing:** Conduct feedback sessions to refine usability and prioritize feature requests.

**Expanded Features:**

1) Add user reviews for gas stations, detailed trip planning tools, and integrations with other travel services like weather updates.

2) Add sustainable restaurant recommendations

3) Expand gamification features

4) AI Autofill/suggestions for searching locations


Dataset citation:
Hannah Ritchie, Pablo Rosado and Max Roser (2023) - “CO₂ and Greenhouse Gas Emissions” Published online at OurWorldinData.org. Retrieved from: 'https://ourworldindata.org/co2-and-greenhouse-gas-emissions' [Online Resource]

Link to dataset used: https://github.com/owid/co2-data/blob/master/README.md
