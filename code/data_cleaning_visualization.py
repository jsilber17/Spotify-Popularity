import numpy as np
import pandas
import matplotlib.pyplot as plt
import seaborn as sns

def add_a_constant(df):
    df['counter'] = 1
    return df


def drop_duplicates(df):
    df.drop_duplicates(inplace=True)
    return df


def convert_time_to_seconds(df):
    df['time'] = df['time']//1000


def change_release_date_to_release_year(df):
    date_list = [date[0:4] for date in df['release_date']]
    df['release_date'] = date_list
    return df


def create_barplot_num_tracks(df):
    df_genre = df.groupby('genre').count().reset_index().sort_values(by='track', ascending=False)
    fig = plt.figure(figsize = (10, 5))
    sns.set(style="whitegrid")
    ax = sns.barplot(x='genre', y='track', data=df_genre, palette="Blues_d")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
    ax.set_title('Number of Tracks per Genre', fontsize=15)
    ax.set_xlabel('Number of Tracks', fontsize=15)
    ax.set_ylabel('Genre', fontsize=15)
    plt.tight_layout()
    # fig.savefig('NumberTracksGenre.png')


def create_average_popularity_per_genre_barplot(df):
    df_sum_pop = df.gropuby('genre').sum().reset_index()[['genre', 'popularity']]
    df_count_pop = df.groupby('genre').count().reset_index()[['genre', 'popularity']]

    merged_inner = df_sum_pop.merge(right=df_count_pop, left_on='genre', right_on='genre')
    merged_inner['average_popularity'] = merged_inner['popularity_x'] / merged_inner['popularity_y']
    chart_val = merged_inner.sort_values(by='average_popularity', ascending=False)[['genre', 'average_popularity']]

    fig = plt.figure(figsize = (10, 5))
    sns.set(style="whitegrid")
    ax = sns.barplot(x='genre', y='average_popularity', data=chart_val, palette="Blues_d")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
    ax.set_title('Average Popularity Per Genre', fontsize=15)
    ax.set_xlabel('Average Popularity', fontsize=15)
    ax.set_ylabel('Genre', fontsize=15)
    plt.tight_layout()
    # fig.savefig('AvgPopularityPerGenre.png')


def plot_distribution_of_popularity(df):
    fig = plt.figure(figsize = (10, 5))
    sns.set(style="whitegrid")
    ax = sns.distplot(df.popularity, bins=10, color='blue')
    ax.set_title("Distribution of Popularity", fontsize=15)
    ax.set_ylabel('Frequency', fontsize=15)
    ax.set_xlabel('Popularity', fontsize=15)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    # fig.savefig('DistributionOfPopularity.png')
    # print(df.popularity.mean())
    # print(df.popularity.std())


def plot_really_popular_songs(df):
    df_really_popular = df.query('popularity >= 90')
    pop_proportion = len(df_really_popular)/len(df *100
    print("Proportion of songs with a popularity rating of 90 or more: '{}'%".format(str(pop_proportion)[0:4]))
    fig = plt.figure(figsize = (10, 5))
    N, bins, patches = plt.hist(df['popularity'], 10)

    cmap = plt.get_cmap('jet')
    below = cmap(0.2)
    above =cmap(0.9)

    for i in range(0,9):
        patches[i].set_facecolor(below)
    for i in range(9, 10):
        patches[i].set_facecolor(above)

    plt.xlabel("Popularity", fontsize=15)
    plt.ylabel("Frequency", fontsize=15)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.title('Distribution of Popularity', fontsize=15)
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    # fig.savefig('Distribution of PopularityWTop10.png')


def plot_attribute_vs_popularity_for_popular_songs(df, attribute):
    df_really_popular = df.query('popularity >= 90')
    fig = plt.figure(figsize=(10, 5))
    fig.subplots_adjust(hspace=0.5, wspace=0.5)

    ax = fig.add_subplot((111))
    x = df_really_popular[attribute]
    y = df_really_popular['popularity']
    sns.regplot(x, y, color='red')
    sns.set(style="white")
    ax.set_ylabel('Popularity', fontsize=15)
    ax.set_xlabel(attribute, fontsize=15)
    ax.set_title(str(attribute) + ' ' + 'vs Popularity for Popularity Rating >90', fontsize=20)
    print('Danceability', linregress(x, y)[2], type(int(linregress(x,y)[2])))


def bootstrap_variables(df_column, df):
    number_list = [i for i in range(len(df))]
    data = list(zip(number_list, df_final[str(df_column)] , df_final['popularity']))
    return data


def bootstrap_sample_r(data, n_bootstrap_samples=10000):
    bootstrap_sample_r = []
    for i in range(n_bootstrap_samples):
        bootstrap_sample_r_2 = []
        bootstrap_sample = np.random.choice(data[random.randint(1, len(data)-1)][0], size=len(data), replace=True)
        x_array = [data[i][1] for i in bootstrap_sample]
        y_array = [data[i][2] for i in bootstrap_sample]
        bootstrap_sample_r.append(linregress(x_array, y_array))
        for i in bootstrap_sample_r:
            bootstrap_sample_r_2.append(i[2])
    return(bootstrap_sample_r_2)


def plot_bootstraped_correlation_values_for_attribute(df, df_column, n_bootstrap_samples):

    bootstrap_r = bootstrap_sample_r(bootstrap_variables(df_column, df_final))

    left_endpoint = np.percentile(bootstrap_r, 2.5)
    right_endpoint = np.percentile(bootstrap_r, 97.5)

    fig= plt.figure(figsize = (10, 5))
    sns.set(style="white")
    ax = sns.distplot(bootstrap_r, bins=100, color='green')
    ax.set_title("Bootstrapped R Values - + str(df_column) + ' ' + 'vs. Popularity', fontsize=15)
    ax.set_ylabel('Frequency', fontsize=15)
    ax.set_xlabel('R Value', fontsize=15)
    ax.set(xlim=(-0.25, 0.5))
    plt.axvline(left_endpoint)
    plt.axvline(right_endpoint)
    # fig.savefig('danceability_bootstrap.png')
