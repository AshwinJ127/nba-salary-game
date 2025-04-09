from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import csv
import os

app = Flask(__name__)
# Configure SQLAlchemy to use an SQLite database named data.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define models that match your CSV file structures
class NBAPlayerSalary(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player = db.Column(db.String(100))          # Player name
    season = db.Column(db.String(20))           # Season
    salary = db.Column(db.Float)                # Salary amount
    rank = db.Column(db.Integer, default=0)     # Rank (will be calculated)
    
    def __repr__(self):
        return f"<NBAPlayerSalary id={self.id}, player='{self.player}', season='{self.season}', salary={self.salary}, rank={self.rank}>"

class NBAPlayerStats(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unique_id = db.Column(db.Integer)           # Unique ID from CSV
    player = db.Column(db.String(100))          # Player name
    team = db.Column(db.String(10))             # Team abbreviation
    position = db.Column(db.String(10))         # Position
    age = db.Column(db.Integer)                 # Age
    games = db.Column(db.Integer)               # Games played
    minutes = db.Column(db.Float)               # Minutes per game
    points = db.Column(db.Float)                # Points per game
    rebounds = db.Column(db.Float)              # Rebounds per game
    assists = db.Column(db.Float)               # Assists per game
    steals = db.Column(db.Float)                # Steals per game
    blocks = db.Column(db.Float)                # Blocks per game
    season = db.Column(db.String(20))           # Season
    year = db.Column(db.Integer)                # Year
    rank = db.Column(db.Integer)                # Rank
    
    def __repr__(self):
        return f"<NBAPlayerStats id={self.id}, player='{self.player}', team='{self.team}', season='{self.season}'>"

# Create the database tables
with app.app_context():
    db.create_all()

def create_sample_salary_data():
    """Create a sample CSV file with player salary data if it doesn't exist"""
    csv_path = os.path.join(os.path.dirname(__file__), 'nba_player_salaries.csv')
    
    # Only create the file if it doesn't exist
    if not os.path.exists(csv_path):
        print("Creating sample player salary data CSV file...")
        
        # Sample player data
        players = [
            {"player": "LeBron James", "season": "2022-2023", "salary": 44474988},
            {"player": "Stephen Curry", "season": "2022-2023", "salary": 48070014},
            {"player": "Kevin Durant", "season": "2022-2023", "salary": 44119845},
            {"player": "Giannis Antetokounmpo", "season": "2022-2023", "salary": 42492492},
            {"player": "Damian Lillard", "season": "2022-2023", "salary": 42492492},
            {"player": "Kawhi Leonard", "season": "2022-2023", "salary": 42492492},
            {"player": "Paul George", "season": "2022-2023", "salary": 42492492},
            {"player": "Klay Thompson", "season": "2022-2023", "salary": 40600080},
            {"player": "Jimmy Butler", "season": "2022-2023", "salary": 37653300},
            {"player": "Kyrie Irving", "season": "2022-2023", "salary": 36934550},
            {"player": "Trae Young", "season": "2022-2023", "salary": 37096500},
            {"player": "Devin Booker", "season": "2022-2023", "salary": 33833400},
            {"player": "Joel Embiid", "season": "2022-2023", "salary": 33616770},
            {"player": "Anthony Davis", "season": "2022-2023", "salary": 37980720},
            {"player": "Nikola Jokic", "season": "2022-2023", "salary": 33047803},
            {"player": "Luka Doncic", "season": "2022-2023", "salary": 37096500},
            {"player": "Jayson Tatum", "season": "2022-2023", "salary": 30351780},
            {"player": "Zion Williamson", "season": "2022-2023", "salary": 13534817},
            {"player": "Ja Morant", "season": "2022-2023", "salary": 12119440},
            {"player": "Zach LaVine", "season": "2022-2023", "salary": 37096500},
            {"player": "Bradley Beal", "season": "2022-2023", "salary": 43279250},
            {"player": "Karl-Anthony Towns", "season": "2022-2023", "salary": 33833400},
            {"player": "Donovan Mitchell", "season": "2022-2023", "salary": 30913750},
            {"player": "Bam Adebayo", "season": "2022-2023", "salary": 30351780},
            {"player": "Deandre Ayton", "season": "2022-2023", "salary": 32459438},
            {"player": "Michael Porter Jr.", "season": "2022-2023", "salary": 30913750},
            {"player": "Shai Gilgeous-Alexander", "season": "2022-2023", "salary": 30913750},
            {"player": "Jaylen Brown", "season": "2022-2023", "salary": 28741071},
            {"player": "Ben Simmons", "season": "2022-2023", "salary": 35448672},
            {"player": "Pascal Siakam", "season": "2022-2023", "salary": 35448672},
            {"player": "Draymond Green", "season": "2022-2023", "salary": 25806469},
            {"player": "CJ McCollum", "season": "2022-2023", "salary": 33333333},
            {"player": "Rudy Gobert", "season": "2022-2023", "salary": 38172414},
            {"player": "Khris Middleton", "season": "2022-2023", "salary": 37948276},
            {"player": "Jrue Holiday", "season": "2022-2023", "salary": 32544000},
            {"player": "Brandon Ingram", "season": "2022-2023", "salary": 31650600},
            {"player": "De'Aaron Fox", "season": "2022-2023", "salary": 30351780},
            {"player": "Jamal Murray", "season": "2022-2023", "salary": 31650600},
            {"player": "Julius Randle", "season": "2022-2023", "salary": 23760000},
            {"player": "Kristaps Porzingis", "season": "2022-2023", "salary": 33833400},
            {"player": "John Wall", "season": "2022-2023", "salary": 47345760},
            {"player": "Russell Westbrook", "season": "2022-2023", "salary": 47063478},
            {"player": "Chris Paul", "season": "2022-2023", "salary": 28400000},
            {"player": "Kyle Lowry", "season": "2022-2023", "salary": 28333334},
            {"player": "Gordon Hayward", "season": "2022-2023", "salary": 30075000},
            {"player": "Tobias Harris", "season": "2022-2023", "salary": 37633050},
            {"player": "Kevin Love", "season": "2022-2023", "salary": 31258256},
            {"player": "DeMar DeRozan", "season": "2022-2023", "salary": 27300000},
            {"player": "Myles Turner", "season": "2022-2023", "salary": 17500000},
            {"player": "Jarrett Allen", "season": "2022-2023", "salary": 20000000},
        ]
        
        # Add more players with different seasons
        more_players = []
        for player in players[:25]:  # Use first 25 players
            more_players.append({
                "player": player["player"],
                "season": "2021-2022",
                "salary": int(player["salary"] * 0.95)  # 5% less than current season
            })
            more_players.append({
                "player": player["player"],
                "season": "2020-2021",
                "salary": int(player["salary"] * 0.9)   # 10% less than current season
            })
        
        players.extend(more_players)
        
        # Write to CSV
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['player', 'season', 'salary']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for player in players:
                writer.writerow(player)
        
        print(f"Created sample data with {len(players)} player records")
    else:
        print(f"Using existing player data file: {csv_path}")

def import_csv_to_db():
    # Create sample data if it doesn't exist
    create_sample_salary_data()
    
    # Use the CSV file in the current directory
    csv_path = os.path.join(os.path.dirname(__file__), 'nba_player_salaries.csv')
    
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Store all players to calculate ranks later
        all_players = []
        
        for row in reader:
            try:
                # Remove any commas or $ symbols from salary and convert to float
                salary_str = str(row.get('salary', '0')).replace(',', '').replace('$', '')
                salary_value = float(salary_str) if salary_str else 0.0
            except ValueError:
                salary_value = 0.0
            
            # Check if we have column_year instead of season
            season_value = row.get('season', '')
            if not season_value and 'column_year' in row:
                season_value = row.get('column_year', '')
            
            player = {
                'player': row.get('player', ''),
                'season': season_value,
                'salary': salary_value
            }
            
            all_players.append(player)
        
        # Sort players by salary within each season to calculate ranks
        seasons = set(p['season'] for p in all_players)
        ranked_players = []
        
        for season in seasons:
            season_players = [p for p in all_players if p['season'] == season]
            # Sort by salary in descending order
            season_players.sort(key=lambda x: x['salary'], reverse=True)
            
            # Assign ranks
            for i, player in enumerate(season_players):
                player['rank'] = i + 1
                ranked_players.append(player)
        
        # Now add all players to the database with their calculated ranks
        for player in ranked_players:
            record = NBAPlayerSalary(
                player=player['player'],
                season=player['season'],
                salary=player['salary'],
                rank=player['rank']
            )
            db.session.add(record)
        
        db.session.commit()
        print(f"Imported {len(ranked_players)} player records with ranks")

# Initialize the database tables
with app.app_context():
    # Create tables if they don't exist
    db.create_all()

# API endpoint to fetch the salary data
@app.route('/data')
def get_data():
    # Ensure data is loaded if accessing this endpoint directly
    with app.app_context():
        if NBAPlayerSalary.query.count() == 0:
            print("Loading salary data for API request...")
            import_csv_to_db()
    
    records = NBAPlayerSalary.query.all()
    
    data = [
        {
            "id": record.id,
            "rank": record.rank,
            "player": record.player,
            "season": record.season,
            "salary": record.salary
        }
        for record in records
    ]
    
    return jsonify(data)

# Function to create sample player stats data
def create_sample_player_stats():
    """Create a sample CSV file with player stats data if it doesn't exist"""
    import csv
    import os
    
    csv_path = os.path.join(os.path.dirname(__file__), 'nba_per_game_stats.csv')
    
    # Only create the file if it doesn't exist
    if not os.path.exists(csv_path):
        print("Creating sample player stats CSV file...")
        
        # Sample player stats data
        players = [
            {"Unique_ID": 1, "Rk": 1, "Player": "LeBron James", "Team": "LAL", "Pos": "SF", "Age": 38, "G": 55, "MP": 35.5, "PTS": 28.9, "TRB": 8.3, "AST": 6.8, "STL": 0.9, "BLK": 0.6, "Year": 2023},
            {"Unique_ID": 2, "Rk": 2, "Player": "Stephen Curry", "Team": "GSW", "Pos": "PG", "Age": 34, "G": 56, "MP": 34.7, "PTS": 29.4, "TRB": 6.1, "AST": 6.3, "STL": 0.9, "BLK": 0.4, "Year": 2023},
            {"Unique_ID": 3, "Rk": 3, "Player": "Kevin Durant", "Team": "PHX", "Pos": "PF", "Age": 34, "G": 47, "MP": 36.0, "PTS": 29.1, "TRB": 6.7, "AST": 5.0, "STL": 0.8, "BLK": 1.4, "Year": 2023},
            {"Unique_ID": 4, "Rk": 4, "Player": "Giannis Antetokounmpo", "Team": "MIL", "Pos": "PF", "Age": 28, "G": 63, "MP": 32.1, "PTS": 31.1, "TRB": 11.8, "AST": 5.7, "STL": 0.8, "BLK": 0.8, "Year": 2023},
            {"Unique_ID": 5, "Rk": 5, "Player": "Damian Lillard", "Team": "POR", "Pos": "PG", "Age": 32, "G": 58, "MP": 36.3, "PTS": 32.2, "TRB": 4.8, "AST": 7.3, "STL": 0.9, "BLK": 0.3, "Year": 2023},
            {"Unique_ID": 6, "Rk": 6, "Player": "Kawhi Leonard", "Team": "LAC", "Pos": "SF", "Age": 31, "G": 52, "MP": 33.6, "PTS": 23.8, "TRB": 6.5, "AST": 3.9, "STL": 1.4, "BLK": 0.5, "Year": 2023},
            {"Unique_ID": 7, "Rk": 7, "Player": "Paul George", "Team": "LAC", "Pos": "SF", "Age": 32, "G": 56, "MP": 34.6, "PTS": 23.8, "TRB": 6.1, "AST": 5.1, "STL": 1.5, "BLK": 0.4, "Year": 2023},
            {"Unique_ID": 8, "Rk": 8, "Player": "Klay Thompson", "Team": "GSW", "Pos": "SG", "Age": 33, "G": 69, "MP": 30.0, "PTS": 21.9, "TRB": 4.1, "AST": 2.4, "STL": 0.7, "BLK": 0.4, "Year": 2023},
            {"Unique_ID": 9, "Rk": 9, "Player": "Jimmy Butler", "Team": "MIA", "Pos": "SF", "Age": 33, "G": 64, "MP": 33.3, "PTS": 22.9, "TRB": 5.9, "AST": 5.3, "STL": 1.8, "BLK": 0.3, "Year": 2023},
            {"Unique_ID": 10, "Rk": 10, "Player": "Kyrie Irving", "Team": "DAL", "Pos": "PG", "Age": 30, "G": 60, "MP": 37.4, "PTS": 27.1, "TRB": 5.1, "AST": 5.5, "STL": 1.1, "BLK": 0.8, "Year": 2023},
            {"Unique_ID": 11, "Rk": 11, "Player": "Trae Young", "Team": "ATL", "Pos": "PG", "Age": 24, "G": 73, "MP": 34.8, "PTS": 26.2, "TRB": 3.0, "AST": 10.2, "STL": 1.1, "BLK": 0.1, "Year": 2023},
            {"Unique_ID": 12, "Rk": 12, "Player": "Devin Booker", "Team": "PHX", "Pos": "SG", "Age": 26, "G": 53, "MP": 34.6, "PTS": 27.8, "TRB": 4.5, "AST": 5.5, "STL": 1.0, "BLK": 0.3, "Year": 2023},
            {"Unique_ID": 13, "Rk": 13, "Player": "Joel Embiid", "Team": "PHI", "Pos": "C", "Age": 29, "G": 66, "MP": 34.6, "PTS": 33.1, "TRB": 10.2, "AST": 4.2, "STL": 1.0, "BLK": 1.7, "Year": 2023},
            {"Unique_ID": 14, "Rk": 14, "Player": "Anthony Davis", "Team": "LAL", "Pos": "C", "Age": 30, "G": 56, "MP": 34.0, "PTS": 25.9, "TRB": 12.5, "AST": 2.6, "STL": 1.1, "BLK": 2.0, "Year": 2023},
            {"Unique_ID": 15, "Rk": 15, "Player": "Nikola Jokic", "Team": "DEN", "Pos": "C", "Age": 28, "G": 69, "MP": 33.7, "PTS": 24.5, "TRB": 11.8, "AST": 9.8, "STL": 1.3, "BLK": 0.7, "Year": 2023},
            {"Unique_ID": 16, "Rk": 16, "Player": "Luka Doncic", "Team": "DAL", "Pos": "PG", "Age": 24, "G": 66, "MP": 36.2, "PTS": 32.4, "TRB": 8.6, "AST": 8.0, "STL": 1.4, "BLK": 0.5, "Year": 2023},
            {"Unique_ID": 17, "Rk": 17, "Player": "Jayson Tatum", "Team": "BOS", "Pos": "SF", "Age": 25, "G": 74, "MP": 36.9, "PTS": 30.1, "TRB": 8.8, "AST": 4.6, "STL": 1.1, "BLK": 0.7, "Year": 2023},
            {"Unique_ID": 18, "Rk": 18, "Player": "Zion Williamson", "Team": "NOP", "Pos": "PF", "Age": 22, "G": 29, "MP": 33.0, "PTS": 26.0, "TRB": 7.0, "AST": 4.6, "STL": 1.1, "BLK": 0.6, "Year": 2023},
            {"Unique_ID": 19, "Rk": 19, "Player": "Ja Morant", "Team": "MEM", "Pos": "PG", "Age": 23, "G": 61, "MP": 31.9, "PTS": 26.2, "TRB": 5.9, "AST": 8.1, "STL": 1.1, "BLK": 0.3, "Year": 2023},
            {"Unique_ID": 20, "Rk": 20, "Player": "Zach LaVine", "Team": "CHI", "Pos": "SG", "Age": 28, "G": 77, "MP": 35.9, "PTS": 24.8, "TRB": 4.5, "AST": 4.2, "STL": 0.9, "BLK": 0.2, "Year": 2023},
            {"Unique_ID": 21, "Rk": 21, "Player": "Bradley Beal", "Team": "WAS", "Pos": "SG", "Age": 29, "G": 50, "MP": 33.5, "PTS": 23.2, "TRB": 3.9, "AST": 5.4, "STL": 0.9, "BLK": 0.7, "Year": 2023},
            {"Unique_ID": 22, "Rk": 22, "Player": "Karl-Anthony Towns", "Team": "MIN", "Pos": "C", "Age": 27, "G": 29, "MP": 33.0, "PTS": 20.8, "TRB": 8.1, "AST": 4.8, "STL": 0.8, "BLK": 0.7, "Year": 2023},
            {"Unique_ID": 23, "Rk": 23, "Player": "Donovan Mitchell", "Team": "CLE", "Pos": "SG", "Age": 26, "G": 68, "MP": 35.8, "PTS": 28.3, "TRB": 4.3, "AST": 4.4, "STL": 1.5, "BLK": 0.4, "Year": 2023},
            {"Unique_ID": 24, "Rk": 24, "Player": "Bam Adebayo", "Team": "MIA", "Pos": "C", "Age": 25, "G": 75, "MP": 34.6, "PTS": 20.4, "TRB": 9.2, "AST": 3.2, "STL": 1.2, "BLK": 0.8, "Year": 2023},
            {"Unique_ID": 25, "Rk": 25, "Player": "Deandre Ayton", "Team": "PHX", "Pos": "C", "Age": 24, "G": 67, "MP": 30.4, "PTS": 18.0, "TRB": 10.0, "AST": 1.7, "STL": 0.6, "BLK": 0.8, "Year": 2023},
            {"Unique_ID": 26, "Rk": 26, "Player": "Michael Porter Jr.", "Team": "DEN", "Pos": "SF", "Age": 24, "G": 62, "MP": 29.0, "PTS": 17.4, "TRB": 5.5, "AST": 1.0, "STL": 0.6, "BLK": 0.5, "Year": 2023},
            {"Unique_ID": 27, "Rk": 27, "Player": "Shai Gilgeous-Alexander", "Team": "OKC", "Pos": "SG", "Age": 24, "G": 68, "MP": 35.5, "PTS": 31.4, "TRB": 4.8, "AST": 5.5, "STL": 1.6, "BLK": 1.0, "Year": 2023},
            {"Unique_ID": 28, "Rk": 28, "Player": "Jaylen Brown", "Team": "BOS", "Pos": "SG", "Age": 26, "G": 67, "MP": 35.9, "PTS": 26.6, "TRB": 6.9, "AST": 3.5, "STL": 1.1, "BLK": 0.4, "Year": 2023},
            {"Unique_ID": 29, "Rk": 29, "Player": "Ben Simmons", "Team": "BKN", "Pos": "PG", "Age": 26, "G": 42, "MP": 26.3, "PTS": 6.9, "TRB": 6.3, "AST": 6.1, "STL": 1.3, "BLK": 0.6, "Year": 2023},
            {"Unique_ID": 30, "Rk": 30, "Player": "Pascal Siakam", "Team": "TOR", "Pos": "PF", "Age": 29, "G": 71, "MP": 37.4, "PTS": 24.2, "TRB": 7.8, "AST": 5.8, "STL": 0.9, "BLK": 0.5, "Year": 2023}
        ]
        
        # Add more players with different seasons
        more_players = []
        for player in players[:15]:  # Use first 15 players
            # 2022 season
            more_players.append({
                "Unique_ID": player["Unique_ID"] + 100,
                "Rk": player["Rk"],
                "Player": player["Player"],
                "Team": player["Team"],
                "Pos": player["Pos"],
                "Age": player["Age"] - 1,
                "G": max(41, player["G"] - 5),
                "MP": round(player["MP"] * 0.98, 1),
                "PTS": round(player["PTS"] * 0.95, 1),
                "TRB": round(player["TRB"] * 0.97, 1),
                "AST": round(player["AST"] * 0.96, 1),
                "STL": round(player["STL"] * 0.98, 1),
                "BLK": round(player["BLK"] * 0.99, 1),
                "Year": 2022
            })
            
            # 2021 season
            more_players.append({
                "Unique_ID": player["Unique_ID"] + 200,
                "Rk": player["Rk"],
                "Player": player["Player"],
                "Team": player["Team"],
                "Pos": player["Pos"],
                "Age": player["Age"] - 2,
                "G": max(41, player["G"] - 10),
                "MP": round(player["MP"] * 0.95, 1),
                "PTS": round(player["PTS"] * 0.9, 1),
                "TRB": round(player["TRB"] * 0.93, 1),
                "AST": round(player["AST"] * 0.92, 1),
                "STL": round(player["STL"] * 0.95, 1),
                "BLK": round(player["BLK"] * 0.97, 1),
                "Year": 2021
            })
        
        players.extend(more_players)
        
        # Write to CSV
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Unique_ID', 'Rk', 'Player', 'Team', 'Pos', 'Age', 'G', 'MP', 'PTS', 'TRB', 'AST', 'STL', 'BLK', 'Year']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for player in players:
                writer.writerow(player)
        
        print(f"Created sample player stats data with {len(players)} player records")
    else:
        print(f"Using existing player stats file: {csv_path}")

# Function to import player stats from CSV to database
def import_player_stats_to_db():
    import pandas as pd
    import os
    
    # Create sample data if it doesn't exist
    create_sample_player_stats()
    
    # Load the CSV file
    csv_path = os.path.join(os.path.dirname(__file__), 'nba_per_game_stats.csv')
    
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Filter players with G >= 41 and Rk <= 100
    filtered_df = df[(df['G'] >= 41) & (df['Rk'] <= 100)]
    
    # Convert to list of dictionaries
    player_stats = filtered_df.to_dict('records')
    
    # Clear existing data
    NBAPlayerStats.query.delete()
    
    # Add all players to the database
    for stat in player_stats:
        # Convert Year to season format (e.g., 2014 -> 2013-14)
        year = int(stat.get('Year', 0))
        season = f"{year-1}-{str(year)[-2:]}" if year > 0 else ""
        
        # Create new record
        record = NBAPlayerStats(
            unique_id=stat.get('Unique_ID', 0),
            player=stat.get('Player', ''),
            team=stat.get('Team', ''),
            position=stat.get('Pos', ''),
            age=stat.get('Age', 0),
            games=stat.get('G', 0),
            minutes=stat.get('MP', 0.0),
            points=stat.get('PTS', 0.0),
            rebounds=stat.get('TRB', 0.0),
            assists=stat.get('AST', 0.0),
            steals=stat.get('STL', 0.0),
            blocks=stat.get('BLK', 0.0),
            season=season,
            year=year,
            rank=stat.get('Rk', 0)
        )
        db.session.add(record)
    
    db.session.commit()
    print(f"Imported {len(player_stats)} player stats records to database")

# API endpoint to fetch the player stats data
@app.route('/player-stats')
def get_player_stats():
    # Ensure data is in the database if accessing this endpoint directly
    with app.app_context():
        if NBAPlayerStats.query.count() == 0:
            print("Loading player stats data for API request...")
            import_player_stats_to_db()
    
    # Query the database
    records = NBAPlayerStats.query.all()
    
    # Format the data for the frontend
    formatted_stats = []
    for record in records:
        formatted_stat = {
            "id": record.unique_id,
            "rank": record.rank,
            "player": record.player,
            "team": record.team,
            "position": record.position,
            "age": record.age,
            "games": record.games,
            "mpg": record.minutes,
            "ppg": record.points,
            "rpg": record.rebounds,
            "apg": record.assists,
            "spg": record.steals,
            "bpg": record.blocks,
            "season": record.season
        }
        formatted_stats.append(formatted_stat)
    
    return jsonify(formatted_stats)

# Route to serve the main portal page
@app.route('/')
def index():
    return render_template('index.html')

# Route to serve the NBA salary game page
@app.route('/nba-salary-game')
def nba_salary_game():
    # Ensure salary data is loaded only when accessing this game
    with app.app_context():
        if NBAPlayerSalary.query.count() == 0:
            print("Loading salary game data...")
            import_csv_to_db()
    return render_template('nba-salary-game.html')

# Route to serve the NBA guess player game page
@app.route('/nba-guess-player')
def nba_guess_player():
    # Ensure player stats data is loaded only when accessing this game
    with app.app_context():
        if NBAPlayerStats.query.count() == 0:
            print("Loading guess player game data...")
            import_player_stats_to_db()
    return render_template('nba-guess-player.html')

if __name__ == '__main__':
    app.run(debug=True)
