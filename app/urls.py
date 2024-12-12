from django.urls import path
from .views import home_page, TeamView, team_list_view, single_team_view, CutPlayerView, free_agents_list_view, sign_player_view, FreeAgentView, SignPlayer, SingleTeamView, create_player_view, CreatePlayer

urlpatterns = [
    path("", home_page, name="home"),
    path("api/teams", TeamView.as_view(), name="teams"),
    path("teams", team_list_view, name="teams-html"),
    path("teams/<str:team_code>/players",
         single_team_view, name="teams-html-players"),
    path("api/teams/<str:team_code>/players",
         SingleTeamView.as_view(), name="team-players"),
    path("api/player/<int:player_id>/FA",
         CutPlayerView.as_view(), name="players"),
    path("free-agents", free_agents_list_view, name="all-free-agents"),
    path("api/free-agents", FreeAgentView.as_view(), name="all-free-agents"),
    path("player/<int:player_id>", sign_player_view, name="sign-player-html"),
    path("api/player/<int:player_id>", SignPlayer.as_view(), name="sign-player"),
    path("player/create", create_player_view, name="create-player-html"),
    path("api/player/create", CreatePlayer.as_view(), name="create-player")
]
