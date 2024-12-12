from rest_framework.generics import ListAPIView
from ..models import Team, Player
from ..serializers import TeamSerializer, PlayerSerializer
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django import forms


class CutPlayerView(APIView):
    """
    API view to handle player status changes (cutting/releasing a player).

    Allows updating a player's free agent status and adjusting team payroll 
    accordingly when a player is cut or re-signed.
    """

    def patch(self, request, player_id, *args, **kwargs):
        # Retrieve the specific player to be modified
        player = Player.objects.get(id=player_id)

        # Validate and save player updates (e.g., free agent status)
        serialized_player = PlayerSerializer(
            player, request.data, partial=True)
        if serialized_player.is_valid():
            serialized_player.save()

        # Retrieve the player's team and its current serialized data
        team = Team.objects.get(id=serialized_player.data['team'])
        serialized_team = TeamSerializer(team)

        # Calculate new team payroll based on player's free agent status
        if request.data['free_agent'] == "True":
            # If player is cut, subtract their salary from team payroll
            print(request.data['free_agent'])
            new_payroll = serialized_team.data['payroll'] - \
                serialized_player.data['salary']
        else:
            # If player is re-signed, add their salary back to team payroll
            new_payroll = serialized_team.data['payroll'] + \
                serialized_player.data['salary']

        # Update team payroll
        new_serialized_team = TeamSerializer(
            team, {"payroll": new_payroll}, partial=True)
        if new_serialized_team.is_valid():
            new_serialized_team.save()

        # Return updated player data
        return Response(serialized_player.data, status=status.HTTP_202_ACCEPTED)


class FreeAgentView(ListAPIView):
    """
    API view to list all free agent players.

    Provides a filtered queryset of players who are currently free agents.
    """
    # Query only players marked as free agents
    queryset = Player.objects.filter(free_agent=True)
    serializer_class = PlayerSerializer


class FreeAgentForm(forms.Form):
    """
    Django form for handling free agent player signing.

    Provides form fields for selecting a team and setting a salary 
    when signing a free agent player.
    """
    # Dropdown to select team from existing teams
    team = forms.ModelChoiceField(
        queryset=Team.objects.all(), empty_label="Select Team", label="Set Team")

    # Salary input with value constraints
    salary = forms.IntegerField(
        min_value=2300000,
        max_value=60000000,
        label="Set Salary"
    )


def free_agents_list_view(request):
    """
    View to render the list of free agent players.

    Retrieves all free agent players and passes them to the template.
    """
    # Fetch all players marked as free agents
    players = Player.objects.filter(free_agent=True)

    # Render the free agents template with the player list
    return render(request, '../templates/free_agents.html', {'players': players})


def sign_player_view(request, player_id):
    """
    View to display the form for signing a specific free agent player.

    Prepopulates the form with the player's current salary information.
    """
    # Retrieve the specific free agent player
    player = Player.objects.get(id=player_id)

    # Create form with initial salary value
    form = FreeAgentForm(initial={'salary': player.salary})

    # Render the sign player template
    return render(request, '../templates/sign_player.html', {'form': form, 'player': player})


class SignPlayer(APIView):
    """
    API view to handle the process of signing a free agent player.

    Validates the form, updates player team and status, and adjusts team payroll.
    """

    def post(self, request, player_id, *args, **kwargs):
        # Retrieve the specific player to be signed
        player = Player.objects.get(id=player_id)

        # Validate the form submission
        form = FreeAgentForm(request.POST)
        if form.is_valid():
            # Extract form data
            team = form.cleaned_data['team']
            salary = form.cleaned_data['salary']

            # Update player information
            player.team = team
            player.salary = salary
            player.free_agent = False
            player.save()

            # Update team payroll
            team.payroll += salary
            team.save()

            # Redirect to teams page after successful signing
            return redirect("/teams")

        # Return error if form is invalid
        return Response({"error: error signing player!"}, status=status.HTTP_400_BAD_REQUEST)


class NewPlayerForm(forms.Form):
    """
    Django form for creating a new player.

    Provides form fields for entering player name, selecting a team, 
    and setting initial salary.
    """
    # Player name input
    name = forms.CharField(max_length=255, label="Player Name")

    # Team selection dropdown
    team = forms.ModelChoiceField(
        queryset=Team.objects.all(), empty_label="Select Team", label="Set Team")

    # Salary input with value constraints
    salary = forms.IntegerField(
        min_value=2300000,
        max_value=60000000,
        label="Set Salary"
    )


class CreatePlayer(APIView):
    """
    API view to handle the creation of a new player.

    Validates the form, creates a new player, and updates team payroll.
    """

    def post(self, request, *args, **kwargs):
        # Validate the form submission
        form = NewPlayerForm(request.POST)
        if form.is_valid():
            # Extract form data
            name = form.cleaned_data['name']
            team = form.cleaned_data['team']
            salary = form.cleaned_data['salary']

            # Create the new player
            player = Player.objects.create(
                name=name,
                team=team,
                salary=salary,
                free_agent=False
            )

            # Update team payroll
            team.payroll += salary
            team.save()

            # Redirect to teams page after successful creation
            return redirect("/teams")


def create_player_view(request):
    """
    View to display the form for creating a new player.

    Provides an empty form for entering new player details.
    """
    # Create an empty new player form
    form = NewPlayerForm()

    # Render the create player template
    return render(request, '../templates/create_player.html', {'form': form})
