def get_recommendations(title, df, cosine_sim, top_n=10):
    indices = df[df['anime_title'].str.lower() == title.lower()].index
    if len(indices) == 0:
        return f"No anime found with title: {title}"

    idx = indices[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    anime_indices = [i[0] for i in sim_scores]

    recommendations = df.iloc[anime_indices].copy()

    # Make sure all required columns are present
    required_columns = ['anime_title', 'anime_overview', 'anime_genres',
                        'anime_mal_score', 'popularity_score',
                        'anime_poster', 'anime_urls']

    # Add missing columns with default values
    for col in required_columns:
        if col not in recommendations.columns:
            recommendations[col] = "N/A"

    return recommendations[required_columns]
