def insights():

    import pandas as pd
    import random
    import streamlit as st
    import matplotlib.pyplot as plt
    import seaborn as sns
    import plotly.express as px
    import numpy as np
    from matplotlib.ticker import FuncFormatter

    st.title("Let's see some movies insights")
    st.image('./images/insights.jpg')
    st.markdown('Picture from https://www.vecteezy.com/free-photos')

    films = pd.read_csv('../films_NaNs_treated.csv')
    films_non_treated = pd.read_csv('../rotten_tomatoes_movies.csv')
    non_zero_scores_as = films['audienceScore'][films['audienceScore'] != 0]
    non_zero_scores_tm = films['tomatoMeter'][films['tomatoMeter'] != 0]

    st.write('Audience score insights: ')
    st.write('Summary Statistics for Audience Scores:')
    st.write(non_zero_scores_as.describe())

    st.write('Distribution of Audience Scores (when present):')
    fig, ax = plt.subplots()
    ax.hist(non_zero_scores_as, bins=20, edgecolor='black')
    ax.set_xlabel('Audience Score')
    ax.set_ylabel('Frequency')
    ax.set_title('Distribution of Audience Scores')
    st.pyplot(fig)
    
    st.write('Distribution of Tomato Meter (when present):')
    fig, ax = plt.subplots()
    ax.hist(non_zero_scores_tm, bins=20, edgecolor='black')
    ax.set_xlabel('Tomato Meter')
    ax.set_ylabel('Frequency')
    ax.set_title('Distribution of Tomato Meter')
    st.pyplot(fig)

    films_non_treated_copy = films_non_treated.copy()
    films_non_treated_copy.dropna(subset=['boxOffice'], inplace=True)

    def convert_dollars_to_floats(x):
        no_dollar = x.replace('$', '')
        if 'M' in no_dollar:
            float_n = float(no_dollar.replace('M', '')) * 1000000
        elif 'K' in no_dollar:
            float_n = float(no_dollar.replace('K', '')) * 1000
        else:
            float_n = float(no_dollar)   
        int_n = int(float_n)
        return int_n

    films_non_treated_copy['boxOffice'] = films_non_treated_copy['boxOffice'].apply(convert_dollars_to_floats)

    st.title('Box Office Analysis')

    # Box Plot
    st.write('Box Plot of Box Office Income:')
    fig_box, ax_box = plt.subplots()
    sns.boxplot(y=films_non_treated_copy['boxOffice'], ax=ax_box)
    ax_box.set_ylabel('Box Office')
    ax_box.set_title('Box Plot of Box Office Income')
    st.pyplot(fig_box)
    top_10_movies = films_non_treated_copy.sort_values(by='boxOffice', ascending=False).head(10)
    st.write('Top 10 Movies by Box Office:')
    st.write(top_10_movies[['title', 'boxOffice', 'audienceScore', 'tomatoMeter', 'releaseDateTheaters', 'genre', 'originalLanguage', 'director']], width=0, index=False)

    def exclude_language_variety(x):
        parts = x.split(' ')
        return parts[0]

    st.title("Distribution of Most Frequent Languages")

    films['originalLanguage'] = films['originalLanguage'].apply(exclude_language_variety)

    most_common_languages = []

    value_counts_original_language = films['originalLanguage'].value_counts().reset_index()
    value_counts_original_language.index += 1
    value_counts_original_language.columns = ['originalLanguage', 'count']

    st.write(value_counts_original_language)

    for i in range(10): 
        most_common_languages.append(value_counts_original_language.iloc[i])

    most_common_languages_df = pd.DataFrame(most_common_languages)
    most_common_languages_df = most_common_languages_df[most_common_languages_df['originalLanguage'] != 'unknown']

    language_colors = {
        'English': 'blue',
        'French': 'red',
        'Spanish': 'green',
        'Japanese': 'purple',
        'Hindi': 'orange',
        'Chinese': 'cyan',
        'Italian': 'magenta',
        'German': 'pink',
        'Korean': 'brown',
        'Portuguese': 'limegreen'
    }

    most_common_languages_df['color'] = most_common_languages_df['originalLanguage'].map(lambda x: language_colors.get(x, 'gray'))

    fig, ax = plt.subplots()
    sns.barplot(x='originalLanguage', y='count', data=most_common_languages_df, palette=most_common_languages_df['color'], ax=ax)
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
    plt.xlabel('Language')
    plt.ylabel('Frequency')
    plt.title('Distribution of Most Common Languages')
    st.pyplot(fig)

    languages = []
    means = []
    medians = []
    audience_means = []
    tomato_means = []

    most_common_languages = ['English',
    'French',
    'Spanish',
    'Japanese',
    'Hindi',
    'Chinese',
    'Italian',
    'German',
    'Korean',
    'Portuguese']


    for language in most_common_languages:
        subset = films[films['originalLanguage'] == language]

        non_zero_scores_box_office = subset['boxOffice'][subset['boxOffice'] != 0]
        non_zero_scores_audience = subset['audienceScore'][subset['audienceScore'] != 0]
        non_zero_scores_tomato = subset['tomatoMeter'][subset['tomatoMeter'] != 0]

        mean_score_box_office = non_zero_scores_box_office.mean()
        mean_score_audience = non_zero_scores_audience.mean()
        mean_score_tomato = non_zero_scores_tomato.mean()

        languages.append(language)
        means.append(mean_score_box_office)
        audience_means.append(mean_score_audience)
        tomato_means.append(mean_score_tomato)

    result_df = pd.DataFrame({
        'Language': languages,
        'BoxOffice_Mean': means,
        'AudienceScore_Mean': audience_means,
        'TomatoMeter_Mean': tomato_means
    })

    st.write('result_df.head')
    st.write(result_df.head(10))


    for col in result_df.columns[1:]:
        sorted_df = result_df.sort_values(by=col, ascending=False)
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Language', y=col, data=sorted_df, palette=language_colors)
        plt.title(f'{col} by Language (Descending Order)')
        plt.xlabel('Language')
        plt.ylabel(col)
        plt.xticks(rotation=45, ha='right')
        st.pyplot(plt)

    st.title('Release Dates')

    films['releaseDateTheaters'] = pd.to_datetime(films['releaseDateTheaters'])
    films['releaseDateStreaming'] = pd.to_datetime(films['releaseDateStreaming'])

    films['ReleaseYearTheaters'] = films['releaseDateTheaters'].dt.year
    films['ReleaseYearStreaming'] = films['releaseDateStreaming'].dt.year

    films['releaseDateTheaters'] = pd.to_datetime(films['releaseDateTheaters'])
    films['releaseDateStreaming'] = pd.to_datetime(films['releaseDateStreaming'])

    films['ReleaseYearTheaters'] = films['releaseDateTheaters'].dt.year
    films['ReleaseYearStreaming'] = films['releaseDateStreaming'].dt.year

    st.title('Movie Release Years Analysis')

    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    sns.histplot(films['ReleaseYearTheaters'][films['ReleaseYearTheaters'] != 1800], bins=20, kde=True, ax=ax[0])
    ax[0].set_title('Release Years in Theaters')
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Frequency')

    sns.histplot(films['ReleaseYearStreaming'][films['ReleaseYearStreaming'] != 1800], bins=20, kde=True, ax=ax[1])
    ax[1].set_title('Release Years on Streaming Platforms')
    ax[1].set_xlabel('Year')
    ax[1].set_ylabel('Frequency')

    st.pyplot(fig)

    films_back_up = films.copy()

    films['genre_list'] = films['genre'].str.split(', | & ')
    films['num_genres'] = films['genre_list'].apply(len)
    unique_genres = set(genre for genres in films['genre_list'] for genre in genres)

    for genre in unique_genres:
        films[genre] = films['genre_list'].apply(lambda x: 1 if genre in x else 0)

    for genre in unique_genres:
        films.rename(columns={genre: f'g_{genre}'}, inplace=True)
    
    genre_cols = films.filter(like='g_')
    g_cols = []
    g_count = []
    for col in genre_cols:
        count_of_ones = (films[col] == 1).sum()
        g_cols.append(col)
        g_count.append(count_of_ones)
    
    gen_count_df = pd.DataFrame({
        'Genre': g_cols,
        'Count': g_count
    })


    gen_count_df_sorted = gen_count_df.sort_values(by='Count', ascending=False)

    gen_count_df = gen_count_df[~gen_count_df['Genre'].isin(['g_Mystery', 'g_unkown'])]
    gen_count_df_sorted = gen_count_df.sort_values(by='Count', ascending=False)

    gen_count_df.columns = gen_count_df.columns.str.replace('g_', '')

    gen_count_df = gen_count_df[~gen_count_df['Genre'].isin(['Mystery', 'Unknown'])]
    gen_count_df_sorted = gen_count_df.sort_values(by='Count', ascending=False)
    gen_count_df_sorted = gen_count_df_sorted.head(7)

    gen_count_df_sorted.columns = gen_count_df_sorted.columns.str.replace('g_', '')

    plt.figure(figsize=(10, 6))
    sns.barplot(x=gen_count_df_sorted['Genre'], y=gen_count_df_sorted['Count'], order=gen_count_df_sorted['Genre'])
    plt.title(f'Genre frequency')
    plt.xlabel('Genre')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(plt)

    means_box_office = []
    means_tomato_meter = []
    means_audience_score = []


    for genre in gen_count_df_sorted['Genre']:
        subset = films[films[genre] == 1]
        
        non_zero_scores_box_office = subset['boxOffice'][subset['boxOffice'] != 0]    
        non_zero_scores_audience = subset['audienceScore'][subset['audienceScore'] != 0]
        non_zero_scores_tomato = subset['tomatoMeter'][subset['tomatoMeter'] != 0]
        
        mean_score_box_office = non_zero_scores_box_office.mean()  
        mean_score_audience = non_zero_scores_audience.mean()    
        mean_score_tomato = non_zero_scores_tomato.mean()

        means_box_office.append(mean_score_box_office)   
        means_audience_score.append(mean_score_audience)
        means_tomato_meter.append(mean_score_tomato)

    result_df_genres = pd.DataFrame({
        'Genre': gen_count_df_sorted['Genre'],
        'BoxOffice_Mean': means_box_office,
        'AudienceScore_Mean': means_audience_score,
        'TomatoMeter_Mean': means_tomato_meter
    })

    genre_palette = {
        'g_Documentary': 'blue',
        'g_Comedy': 'red',
        'g_thriller': 'green',
        'g_Horror': 'purple',
        'g_Romance': 'orange',
        'g_Drama': 'cyan',
        'g_Action': 'teal'
    }

    for col in result_df_genres.columns[1:]:
        sorted_df = result_df_genres.sort_values(by=col, ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='Genre', y=col, data=sorted_df, palette=genre_palette)
        plt.title(f'{col} by Genre (Descending Order)')
        plt.xlabel('Genre')
        plt.ylabel(col)
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)





    

















 
