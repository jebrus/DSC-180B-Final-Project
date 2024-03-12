import numpy as np
import pandas as pd
from sklearn.decomposition import PCA, TruncatedSVD
import joblib
import json

class Predictor:
    def __init__(self):
        self.item_features = np.load('../data/item_features.npy')
        self.svd = joblib.load('../data/svd_model.joblib')
        self.popularity_rank = joblib.load('../data/popularity_rank.joblib')
        self.country_totals = joblib.load('../data/country_totals.joblib')
        self.artist_names = joblib.load('../data/artist_names.joblib')
        with open('../data/artist_location_codes.json', 'r') as file:
            self.artist_locations = json.load(file)
        self.priveleged_locations = ['US', 'GB', 'CA']
        self.idx_to_artist = joblib.load('../data/idx_to_artist.joblib')
        
        
    def recommend(self, 
        _user_liked_artists: list,
        top_n: int = 5,
        underrepresented_weight = 1,
        popularity_weight = 0
    ) -> list[str]:
        # Convert liked artists to user features
        _user_liked_artists = [artist.lower() for artist in _user_liked_artists]
        user_info_array = np.array([[int(artist.lower() in _user_liked_artists) for artist in self.artist_names]])
        user_features = self.svd.transform(user_info_array)
        # Predicted rating is the dot product of `user_factors` and `item_factors`. Will be the same shape as the original matrix, and the element will represent the predicted interaction (play count) with an artist.
        user_ratings = np.dot(user_features, self.item_features)
        # Calculate reweighting vector TODO: There has to be a less computationally intense way of calculating this
        reweighting_vec = np.array([(1 if self.artist_locations[artist] in self.priveleged_locations else underrepresented_weight) for artist in self.artist_names])
        popularity_weighting_vec = ((1 - self.popularity_rank / self.country_totals) ** popularity_weight).array
        reweighted_ratings = user_ratings * reweighting_vec * popularity_weighting_vec + (user_info_array * -1000) # Filter out artists user already likes
        recommended_item_idx = np.argsort(reweighted_ratings[0])[::-1]
        # This is horribly inefficient, optimize
        recommended_artist_names = [
            self.idx_to_artist[idx] for idx in recommended_item_idx
        ]
        # print(recommended_artist_names[:top_n])
        return recommended_artist_names[:top_n]