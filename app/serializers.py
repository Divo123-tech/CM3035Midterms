from .models import Team, Player
from rest_framework import serializers


class TeamSerializer(serializers.ModelSerializer):
    """
    Serializer for the Team model to convert Team instances to JSON 
    and validate data for team-related API operations.

    Automatically handles serialization of all specified fields from the Team model.
    """
    class Meta:
        # Specify the model to be serialized
        model = Team

        # Define the fields that will be included in the serialized representation
        # This allows controlled exposure of model data through the API
        fields = ['id', 'name', 'code', 'payroll']


class PlayerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Player model to convert Player instances to JSON
    and validate data for player-related API operations.

    Automatically handles serialization of all specified fields from the Player model.
    """
    class Meta:
        # Specify the model to be serialized
        model = Player

        # Define the fields that will be included in the serialized representation
        # This allows controlled exposure of model data through the API
        fields = ['id', 'name', 'team', 'salary', 'free_agent']
