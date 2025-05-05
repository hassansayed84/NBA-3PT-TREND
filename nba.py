from nba_api.stats.endpoints import leaguedashteamstats
import pandas as pd
import time
import matplotlib.pyplot as plt

# Function to fetch FG and FT attempts for multiple seasons
def get_attempts_data(start_year, end_year):
    all_seasons_data_3pa = []
    all_seasons_data_2pa = []
    all_seasons_data_fta = []
    
    for year in range(start_year, end_year + 1):
        season = f"{year}-{str(year+1)[-2:]}"  # Format: '2003-04'
        print(f"Fetching data for {season}...")

        # API request for team stats
        stats = leaguedashteamstats.LeagueDashTeamStats(
            season=season,
            per_mode_detailed="PerGame",
            measure_type_detailed_defense="Base"
        ).get_data_frames()[0]

        # Compute 2PA (Total FGA - FG3A)
        stats["FG2A"] = stats["FGA"] - stats["FG3A"]

        # Separate datasets for 3PA, 2PA, and FTA
        stats_3pa = stats[['TEAM_NAME', 'FG3A']].copy()
        stats_3pa.loc[:, 'SEASON'] = season
        all_seasons_data_3pa.append(stats_3pa)

        stats_2pa = stats[['TEAM_NAME', 'FG2A']].copy()
        stats_2pa.loc[:, 'SEASON'] = season
        all_seasons_data_2pa.append(stats_2pa)

        stats_fta = stats[['TEAM_NAME', 'FTA']].copy()
        stats_fta.loc[:, 'SEASON'] = season
        all_seasons_data_fta.append(stats_fta)

        time.sleep(1)  # To avoid API rate limits

    return (
        pd.concat(all_seasons_data_3pa, ignore_index=True),
        pd.concat(all_seasons_data_2pa, ignore_index=True),
    )

# Fetch data from 2003-04 to 2023-24
df_3pa, df_2pa = get_attempts_data(2003, 2023)

# Save to CSV files
df_3pa.to_csv("NBA_3PA_2003_2023.csv", index=False)
df_2pa.to_csv("NBA_2PA_2003_2023.csv", index=False)


# Load the datasets
df_3pa = pd.read_csv("NBA_3PA_2003_2023.csv")
df_2pa = pd.read_csv("NBA_2PA_2003_2023.csv")


# Aggregate the average attempts per season
df_3pa_grouped = df_3pa.groupby("SEASON")["FG3A"].mean()
df_2pa_grouped = df_2pa.groupby("SEASON")["FG2A"].mean()


# Plot the trend of Three-Point Attempts (3PA)
plt.figure(figsize=(10, 5))
plt.plot(df_3pa_grouped.index, df_3pa_grouped.values, marker="o", linestyle="-")
plt.xlabel("Season")
plt.ylabel("Average 3PA per Game")
plt.title("Trend of Three-Point Attempts Per Game (2003-2023)")
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# Plot the trend of Two-Point Attempts (2PA)
plt.figure(figsize=(10, 5))
plt.plot(df_2pa_grouped.index, df_2pa_grouped.values, marker="o", linestyle="-", color="red")
plt.xlabel("Season")
plt.ylabel("Average 2PA per Game")
plt.title("Trend of Two-Point Attempts Per Game (2003-2023)")
plt.xticks(rotation=45)
plt.grid(True)
plt.show()



