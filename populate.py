import os
import django
import csv  # noqa - suppress import unused warning

# Configure Django environment
# Set the Django settings module to connect to the project's configuration
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tradeMachine.settings')
django.setup()

# Import Django models for database operations
from app.models import Player, Team  # noqa - suppress import unused warning

# Specify the path to the CSV file containing team information
csv_file_path = 'csv/teams.csv'

# Open and process the teams CSV file
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    # Use DictReader to easily access CSV columns by their headers
    reader = csv.DictReader(csvfile)

    # Iterate through each row in the CSV file
    for row in reader:
        # Extract team information from the CSV row
        team_name = row['Team'].strip()  # Remove leading/trailing whitespace
        team_code = row['Code'].strip()  # Unique identifier for the team
        payroll = int(row['Payroll'].strip())  # Convert payroll to integer

        # Use Django's update_or_create to handle both new and existing teams
        # This method will create a new team or update an existing one if found
        team, created = Team.objects.update_or_create(
            code=team_code,  # Use team code as the unique identifier
            defaults={
                'name': team_name,  # Team's full name
                'payroll': payroll  # Team's total payroll
            }
        )

        # Provide feedback on whether a team was created or updated
        if created:
            print(f"Created team: {team_name}")
        else:
            print(f"Updated team: {team_name}")

# Indicate completion of team database population
print("Team Database population complete.")

# Update the CSV file path for player data
csv_file_path = 'csv/players.csv'

# Open and process the players CSV file
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    # Use DictReader to easily access CSV columns by their headers
    reader = csv.DictReader(csvfile)

    # Iterate through each row in the CSV file
    for row in reader:
        # Extract player information from the CSV row
        # Remove leading/trailing whitespace
        player_name = row['Player'].strip()
        team_name = row['Team'].strip()  # Team code for the player
        salary = int(row['salary'].strip())  # Convert salary to integer

        # Attempt to retrieve the corresponding team from the database
        try:
            # Find the team using the team code
            team = Team.objects.get(code=team_name)
        except Team.DoesNotExist:
            # Handle cases where the team is not found in the database
            print(
                f"Team '{team_name}' not found in the database. Skipping player '{player_name}'.")
            continue

        # Use Django's update_or_create to handle both new and existing players
        # This method will create a new player or update an existing one if found
        player, created = Player.objects.update_or_create(
            name=player_name,  # Use player name as the unique identifier
            defaults={
                'team': team,  # Associate player with their team
                'salary': salary,  # Player's individual salary
            }
        )

        # Provide feedback on whether a player was created or updated
        if created:
            print(f"Created player: {player_name}")
        else:
            print(f"Updated player: {player_name}")

# Indicate completion of player database population
print("Player database population complete.")
