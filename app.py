from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import csv
import os

app = Flask(__name__)
# Configure SQLAlchemy to use an SQLite database named data.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a model that matches your CSV file structure
class NBAPlayerSalary(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player = db.Column(db.String(100))          # Player name
    season = db.Column(db.String(20))           # Season
    salary = db.Column(db.Float)                # Salary amount
    rank = db.Column(db.Integer, default=0)     # Rank (will be calculated)
    
    def __repr__(self):
        return f"<NBAPlayerSalary id={self.id}, player='{self.player}', season='{self.season}', salary={self.salary}, rank={self.rank}>"

# Create the database tables
with app.app_context():
    db.create_all()

def create_sample_player_data():
    """Create a sample CSV file with player data if it doesn't exist"""
    csv_path = os.path.join(os.path.dirname(__file__), 'nba_player_salaries.csv')
    
    # Only create the file if it doesn't exist
    if not os.path.exists(csv_path):
        print("Creating sample player data CSV file...")
        
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
    # Use the CSV file in the current directory
    csv_path = os.path.join(os.path.dirname(__file__), 'nba_player_salaries.csv')
    
    if not os.path.exists(csv_path):
        print(f"ERROR: CSV file not found at {csv_path}")
        return
    
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

# Reset the database and import fresh data
with app.app_context():
    # Drop all tables and recreate them
    db.drop_all()
    db.create_all()
    
    # Import the data
    import_csv_to_db()

# API endpoint to fetch the salary data
@app.route('/data')
def get_data():
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

# API endpoint to fetch the player stats data
@app.route('/player-stats')
def get_player_stats():
    import pandas as pd
    import os
    
    # Load the CSV file
    csv_path = os.path.join(os.path.dirname(__file__), 'nba_per_game_stats.csv')
    if not os.path.exists(csv_path):
        return jsonify({"error": "Stats file not found"}), 404
    
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Filter players with G >= 41 and Rk <= 100
    filtered_df = df[(df['G'] >= 41) & (df['Rk'] <= 100)]
    
    # Convert to list of dictionaries
    player_stats = filtered_df.to_dict('records')
    
    # Format the data for the frontend
    formatted_stats = []
    for stat in player_stats:
        # Convert Year to season format (e.g., 2014 -> 2013-14)
        year = int(stat.get('Year', 0))
        season = f"{year-1}-{str(year)[-2:]}" if year > 0 else ""
        
        # Create formatted stat object
        formatted_stat = {
            "id": stat.get('Unique_ID', ''),
            "rank": stat.get('Rk', ''),
            "player": stat.get('Player', ''),
            "team": stat.get('Team', ''),
            "position": stat.get('Pos', ''),
            "age": stat.get('Age', ''),
            "games": stat.get('G', ''),
            "mpg": stat.get('MP', ''),
            "ppg": stat.get('PTS', ''),
            "rpg": stat.get('TRB', ''),
            "apg": stat.get('AST', ''),
            "spg": stat.get('STL', ''),
            "bpg": stat.get('BLK', ''),
            "season": season
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
    return render_template('nba-salary-game.html')

# Route to serve the NBA guess player game page
@app.route('/nba-guess-player')
def nba_guess_player():
    return render_template('nba-guess-player.html')

if __name__ == '__main__':
    app.run(debug=True)
