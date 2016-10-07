from trueskill import Rating


class Player:
    """
    default constructor for Player class
    tag - string that is the player's in-game-name
    rating - float that represents their TrueSkill rating

    """
    def __init__(self, tag, rating):
        self.tag = tag
        self.rating = Rating(rating)

    def __str__(self):
        return self.tag

    def __lt__(self, other):         
        return self.rating.mu < other.rating.mu
