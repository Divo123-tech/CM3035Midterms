from django.db import models

# Create your models here.


class Team(models.Model):
    """
    Represents a sports team in the database.

    This model stores essential information about teams, 
    serving as a core entity for team-related data management.
    """
    # Team name with a maximum length of 255 characters
    # Allows for full, descriptive team names
    name = models.CharField(max_length=255)

    # Short team code (typically 3 letters)
    # Used for quick identification and referencing
    code = models.CharField(max_length=3)

    # Total team payroll stored as an integer
    # Represents the team's total player salary expenditure
    payroll = models.IntegerField()

    def __str__(self):
        """
        String representation of the Team model.

        Returns the team's name when the object is converted to a string.
        Useful for admin interfaces and debugging.
        """
        return self.name


class Player(models.Model):
    """
    Represents an individual player in the database.

    This model stores player-specific information and maintains 
    a relationship with the Team model to track team associations.
    """
    # Player's full name with a maximum length of 255 characters
    name = models.CharField(max_length=255, unique=True)

    # Foreign key relationship to the Team model
    # on_delete=models.CASCADE ensures that if a team is deleted,
    # all associated players are also deleted
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE)

    # Player's salary stored as an integer
    salary = models.IntegerField()

    # Boolean flag to indicate if the player is a free agent
    # Defaults to False when not explicitly set
    free_agent = models.BooleanField(default=False)

    def __str__(self):
        """
        String representation of the Player model.

        Returns the player's name when the object is converted to a string.
        Useful for admin interfaces and debugging.
        """
        return self.name
