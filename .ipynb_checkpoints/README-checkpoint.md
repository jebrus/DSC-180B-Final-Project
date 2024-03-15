# Spotiversity (DSC 180B Capstone Project)

## Overview
This program leverages Last.fm user data and debiasing techniques to recommend music irrespective of its country of origin, showing users songs that fit their taste from countries whose music they've never heard before.

## Features
Our music recommender offers a unique set of features designed for personalized music discovery. Users can input their favorite artists to receive a curated list of recommended artists tailored to their individual tastes, focusing primarily on promoting musical diversity. Unlike conventional music recommenders, our system prioritizes suggestions from musically underrepresented countries, stepping away from the mainstream markets of the US, UK, and Canada. This approach not only broadens the spectrum of musical landscapes and cultures available to users but also highlights more obscure and emerging artists. By doing so, we provide an avenue for the exploration of unique sounds and styles not typically found in commercial charts, encouraging users to discover new music that they might not encounter elsewhere.

## Getting Started

### Prerequisites
Before setting up the program, ensure you have the following:
- Python 3.6 or higher
- Python packages: `numpy`, `matplotlib`, `pandas`, `scikit-learn`, `joblib`, `dash`, `plotly`, `dash_player`

### Installation
To get started with the Music Recommendation Program, follow these steps:

1. **Clone the Repository**
   Clone this repository to your local machine using the following command:
   ```bash
   git clone https://github.com/jebrus/DSC-180B-Final-Project.git
   cd DSC-180B-Final-Project
   ```

2. **Install Required Packages**
   Install the required Python packages by running:
   ```bash
   pip install numpy matplotlib pandas scikit-learn joblib dash plotly dash_player
   ```

### Setup

**Run Web App**:
   Navigate to the `src` directory and run web_app.py. Then from there, open the url given to access the web app.

**See the Process**:
   Navigate to the `demos` folder to find Jupyter Notebooks. These notebooks were used in the process of the app's development, and contain data acquisition, EDA and model development. However, some code may not be functional without a Last.fm API key or the user data dataset. Last.fm has requested that that dataset not be published publicly, so this will not be made accessible.
   
Notebook descriptions: 
- `data_acquisition.ipynb`: Acquisition of Last.fm user data.
- `data-cleaning.ipynb`: Acquisition of MusicBrainz location data and data cleaning.
- `country-privelege-eval.ipynb`: Analysis of which countries to mark as overrepresented or underrepresented.
- `DSC 180B EDA - Shivani.ipynb`, `EDA - Bivariate Analysis - Shivani.ipynb`, `user_eda-natalie.ipynb`, `final_EDA.ipynb`: Dataset analysis.
- `svd_debiasing.ipynb`: Model training and debiasing.

### Usage
Enter the names of artists you like, comma-separated with a space after each comma, into the bar and press the button. A list of recommended artists will be displayed below for you. Artist names are not case-sensitive, but spelling does matter. For best results, it is recommended to input multiple artist names to recommend by, preferably at least 10.

## Contributing
Development on this project is finished. However, if it continues, please follow these steps:

1. Fork the project.
2. Create a new feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add some YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Submit a pull request.

### Acknowledgements
Special thanks to Last.fm for allowing the use of their data in this project.
