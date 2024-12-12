from rest_framework.generics import ListAPIView
from ..models import Team, Player
from ..serializers import TeamSerializer, PlayerSerializer
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


class TeamView(ListAPIView):
    """
    API view to retrieve and list all teams.

    Provides an endpoint that returns a JSON representation 
    of all teams in the database.

    - Uses ListAPIView for automatic list rendering
    - Retrieves all Team objects
    - Serializes teams using TeamSerializer
    """
    # Retrieve all Team objects from the database
    queryset = Team.objects.all()

    # Use TeamSerializer to convert Team objects to JSON
    serializer_class = TeamSerializer


def team_list_view(request):
    """
    Render a template with a list of all teams.

    Fetches all teams from the database and passes them 
    to the team list template for rendering.

    Args:
        request: HTTP request object

    Returns:
        Rendered HTML template with team list
    """
    # Retrieve all Team objects from the database
    teams = Team.objects.all()

    # Render the team list template with teams context
    return render(request, '../templates/team_list.html', {'teams': teams})


class SingleTeamView(APIView):
    """
    API view to retrieve detailed information about a specific team.

    Provides an endpoint that returns:
    - Detailed team information
    - List of non-free agent players on the team

    Retrieves team by unique team code.
    """

    def get(self, request, team_code, *args, **kwargs):
        """
        Handle GET request for a specific team.

        Args:
            request: HTTP request object
            team_code: Unique identifier for the team

        Returns:
            JSON response with team and player information
        """
        try:
            # Retrieve the team by its unique code
            team = Team.objects.get(code=team_code)

            # Serialize the team data
            serialized_team = TeamSerializer(team)

            # Retrieve non-free agent players for this team
            players = Player.objects.filter(
                team=serialized_team.data['id'], free_agent=False)

            # Serialize the players
            serialized_players = PlayerSerializer(players, many=True)

            # Return team and players data in the response
            return Response({
                "team": serialized_team.data,
                "players": serialized_players.data
            }, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"error": "Cannot find team"}, status=status.HTTP_404_NOT_FOUND)


def single_team_view(request, team_code):
    """
    Render a template with details of a specific team and its players.

    Fetches team information and non-free agent players for the given team.

    Args:
        request: HTTP request object
        team_code: Unique identifier for the team

    Returns:
        Rendered HTML template with team and player details
    """
    # Retrieve the team by its unique code
    team = Team.objects.get(code=team_code)

    # Serialize the team data (optional in this view, but kept for consistency)
    serialized_team = TeamSerializer(team)

    # Retrieve non-free agent players for this team
    players = Player.objects.filter(
        team=serialized_team.data['id'], free_agent=False)

    # Render the team players template with team and players context
    return render(request, 'team_players.html', {'team': team, 'players': players})
