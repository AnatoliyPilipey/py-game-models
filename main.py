import init_django_orm  # noqa: F401
import json

from db.models import Race, Skill, Player, Guild


def main() -> None:
    with open("players.json", "r") as players_file:
        players_info = json.load(players_file)
    for player_name, player_info in players_info.items():
        race_name = player_info["race"]["name"]
        try:
            Race.objects.get(name=race_name)
        except Race.DoesNotExist:
            Race.objects.create(
                name=race_name,
                description=player_info["race"]["description"]
            )
            for skill in player_info["race"]["skills"]:
                try:
                    Skill.objects.get(name=skill["name"])
                except Skill.DoesNotExist:
                    Skill.objects.create(
                        name=skill["name"],
                        bonus=skill["bonus"],
                        race=Race.objects.get(name=race_name)
                    )
        if isinstance(player_info["guild"], dict):
            guild_name = player_info["guild"]["name"]
            try:
                Guild.objects.get(name=guild_name)
                if guild_name is None:
                    raise Guild.DoesNotExist
            except Guild.DoesNotExist:
                Guild.objects.create(
                    name=player_info["guild"]["name"],
                    description=player_info["guild"]["description"]
                )

        try:
            Player.objects.get(nickname=player_name)
        except Player.DoesNotExist:
            player_guild = Guild.objects.get(
                name=player_info["guild"]["name"]
            ) if isinstance(player_info["guild"], dict) else None
            Player.objects.create(
                nickname=player_name,
                email=player_info["email"],
                bio=player_info["bio"],
                race=Race.objects.get(name=player_info["race"]["name"]),
                guild=player_guild

            )


if __name__ == "__main__":
    main()
