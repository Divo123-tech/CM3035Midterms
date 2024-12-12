from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from ..models import Team, Player
from rest_framework import status
from django.contrib.auth import get_user_model


class PlayerTests(TestCase):
    """
    Unit tests for player-related views.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.team = Team.objects.create(
            name="Team A", code="TMA", payroll=1000000)
        self.player1 = Player.objects.create(
            name="Player One", team=self.team, salary=50000, free_agent=False)
        self.player2 = Player.objects.create(
            name="Player Two", team=self.team, salary=40000, free_agent=True)

        # Initialize the test client
        self.client = APIClient()

    def test_cut_player_view(self):
        """
        Test the endpoint that cuts (releases) a player and updates team payroll.
        """
        url = reverse('players', args=[self.player1.id]
                      )  # Assuming you have the correct URL name
        data = {
            # Set the free agent status to True (cut the player)
            'free_agent': "True",
        }

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.player1.refresh_from_db()  # Refresh player data from the DB
        self.assertTrue(self.player1.free_agent)
        self.team.refresh_from_db()  # Refresh team data from the DB
        # Ensure payroll is updated
        self.assertEqual(self.team.payroll, 950000)

    def test_free_agent_view(self):
        """
        Test the endpoint that lists all free agents.
        """
        url = reverse(
            'all-free-agents')  # Use the correct URL name for FreeAgentView
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if Player Two is in the response
        self.assertIn(self.player2.name, [player['name']
                      for player in response.data])
        # Player One should not be in the response
        self.assertNotIn(self.player1.name, [
                         player['name'] for player in response.data])

    def test_sign_player_view(self):
        """
        Test the endpoint that signs a free agent to a team and updates team payroll.
        """
        # Create another team for signing the player
        team_b = Team.objects.create(
            name="Team B", code="TMB", payroll=20000000)

        # Use reverse to get the URL for the sign player view
        url = reverse('sign-player', args=[self.player2.id])

        # Send the data as form-encoded data (not JSON)
        data = {
            'team': team_b.id,
            'salary': 6000000,
        }

        # Send POST request with form data
        response = self.client.post(url, data)

        # Check that the response is a redirect (302 Found)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        # Refresh player data and check the player's team and status
        self.player2.refresh_from_db()
        # Player should now be on Team B
        self.assertEqual(self.player2.team.id, team_b.id)
        # Player should no longer be a free agent
        self.assertFalse(self.player2.free_agent)

        # Refresh Team B's data and check payroll
        team_b.refresh_from_db()
        # Team B's payroll should be updated
        self.assertEqual(team_b.payroll, 26000000)

    def test_create_player_view(self):
        """
        Test the endpoint that creates a new player and updates team payroll.
        """
        url = reverse(
            'create-player')  # Get the correct URL for CreatePlayer view

        # Prepare the form data
        data = {
            'name': 'New Player',
            'team': self.team.id,
            'salary': 7000000
        }

        # Send the POST request with form-encoded data
        response = self.client.post(url, data)

        # Check that the response is a redirect (302 Found)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        # Ensure the new player was created
        new_player = Player.objects.get(name="New Player")

        # New player should be on the same team
        self.assertEqual(new_player.team.id, self.team.id)

        # Refresh the team data and check that the payroll is updated
        self.team.refresh_from_db()
        # Team payroll should be updated with new player's salary
        self.assertEqual(self.team.payroll, 8000000)
