import trueskill
from player import Player

if __name__ == "__main__":
    p1 = trueskill.Rating()
    p2 = trueskill.Rating()
    print(p1, p2)
    p1, p2 = trueskill.rate_1vs1(p1, p2)
    print(p1, p2)
