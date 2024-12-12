from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from ..models import Team, Player  # Import your models
from rest_framework import status


class TeamViewTests(TestCase):
    """
    Unit tests for Team API views.
    """

    def setUp(self):
        """
        Set up test data.
        """
        # Create a team
        self.team1 = Team.objects.create(
            name='Team One', code='T01', payroll=500000)
        self.team2 = Team.objects.create(
            name='Team Two', code='T02', payroll=600000)

        # Create players for the team
        self.player1 = Player.objects.create(
            name='Player One', team=self.team1, free_agent=False, salary=5000000)
        self.player2 = Player.objects.create(
            name='Player Two', team=self.team2, free_agent=False, salary=5000000)

        # Initialize the test client
        self.client = APIClient()

    def test_list_teams(self):
        """
        Test the endpoint that lists all teams.
        """
        # URL for the team list view
        url = reverse('teams')  # Adjust according to your URL name

        # Send GET request to the view
        response = self.client.get(url)

        # Assert that the response is successful (status 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if both teams are in the response data
        self.assertIn('Team One', str(response.data))
        self.assertIn('Team Two', str(response.data))

    def test_single_team_view(self):
        """
        Test the endpoint that retrieves detailed information about a specific team.
        """
        # URL for the single team view, using the team code as parameter
        # Adjust according to your URL name
        url = reverse('team-players', args=[self.team1.code])

        # Send GET request to the view
        response = self.client.get(url)

        # Assert that the response is successful (status 202)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        # Assert that the team data is in the response
        self.assertEqual(response.data['team']['name'], 'Team One')

        # Check if the players list is present and contains the correct player
        self.assertEqual(len(response.data['players']), 1)
        self.assertEqual(response.data['players'][0]['name'], 'Player One')

    def test_single_team_view_not_found(self):
        """
        Test the case when a team does not exist.
        """
        # Use a non-existing team code
        # Adjust accordingly
        url = reverse('team-players', args=['NON_EXISTENT_CODE'])

        # Send GET request to the view
        response = self.client.get(url)

        # Assert that the response returns a 404 error
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_single_team_view_no_players(self):
        """
        Test the case where a team has no players.
        """
        # Create a new team with no players
        team3 = Team.objects.create(
            name='Team Three', code='T03', payroll=700000)

        # URL for the single team view
        url = reverse('team-players', args=[team3.code])

        # Send GET request to the view
        response = self.client.get(url)

        # Assert that the response is successful
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        # Check that the player list is empty
        self.assertEqual(len(response.data['players']), 0)

# Test for Players who are Free Agents
    def test_single_team_view_with_free_agents(self):
        """
        Test the case where some players are free agents.
        """
        # Add a free agent player to one of the teams
        player3 = Player.objects.create(
            name='Free Agent', team=self.team1, free_agent=True, salary=5000000)

        # URL for the single team view
        url = reverse('team-players', args=[self.team1.code])

        # Send GET request to the view
        response = self.client.get(url)

        # Assert that the response is successful
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        # Assert that the free agent player is not included in the response
        # Only non-free agents
        self.assertEqual(len(response.data['players']), 1)
        self.assertEqual(response.data['players'][0]['name'], 'Player One')
