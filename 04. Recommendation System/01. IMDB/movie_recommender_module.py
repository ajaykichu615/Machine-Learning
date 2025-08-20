from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def recommend_movie(film, movie_dictionary, n=5):
    if film in movie_dictionary:
        dummy_dict = {}
        film_vector = np.array(movie_dictionary[film])
        for m, v in movie_dictionary.items():
            if m != film:
                cosine = cosine_similarity(film_vector.reshape(1, -1), np.array(v).reshape(1, -1))[0][0]
                dummy_dict[m] = cosine
        lst = sorted(dummy_dict.items(), key=lambda x: x[1], reverse=True)[:n]  # sorted movies with cosine similarity in descending order and returned only movie names.
        return [i[0] for i in lst]
    else:
        return 'No movie found'

def get_high_quality_image(url, width=600, height=900):
    if "UX" in url:
        url = url.replace("UX67", f"UX{width}")
    if "UY" in url:
        url = url.replace("UY98", f"UY{height}")  

    if "CR" in url:
        url = url.replace("CR0,0,67,98", f"CR0,0,{width},{height}")
        url = url.replace("CR2,0,67,98", f"CR2,0,{width},{height}")

    return url