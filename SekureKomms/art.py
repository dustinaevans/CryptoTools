def randomArt():
    arts = {
    '1':'IyMjIyAgIyMjIyMgIyMjIyMgICMjIyMgIyMjIyMgIyAgICMgCiMgICAjICMgICAgICAgIyAgICMgICAgICMgICAgICMgICAjIAojIyMjICAjIyMjICAgICMgICAjICAgICAjIyMjICAgIyMjIwojICAgIyAjICAgICAgICMgICAjICAgICAjICAgICAgICAgIyAKIyMjIyAgIyMjIyMgICAjICAgICMjIyMgIyMjIyMgICAgICMK',
    '2':"b29vb29vICAgICBvb29vICAgICAgICAgICAgICAgLiAgICAub29vb29vLi5vClxgODg4LiAgICAgLjgnICAgICAgICAgICAgICAubzggICBkOFAnICAgIFxgWTgKICBgODg4LiAgIC44JyAgICAub29vb28uICAubzg4OG9vIFk4OGJvLiAgICAgICAub29vb28uICAgLm9vb29vLgogICBgODg4LiAuOCcgICAgZDg4JyBgODhiICAgODg4ICAgIGAiWTg4ODhvLiAgZDg4JyBgODhiIGQ4OCcgYFk4CiAgICBgODg4LjgnICAgICA4ODhvb284ODggICA4ODggICAgICAgIGAiWTg4YiA4ODhvb284ODggODg4CiAgICAgYDg4OCcgICAgICA4ODggICAgLm8gICA4ODggLiBvbyAgICAgLmQ4UCA4ODggICAgLm8gODg4ICAgLm84CiAgICAgIGA4JyAgICAgICBgWThib2Q4UCcgICAiODg4IiA4IiI4ODg4OFAnICBgWThib2Q4UCcgYFk4Ym9kOFAnCg==",
    '3':'Li4uLSAuIC0gLi4uIC4gLS4tLgo=',
    '4':''
    }
    from base64 import b64decode
    from random import randrange
    randomart = str(randrange(1,len(arts)))
    print(b64decode(arts[randomart].encode()).decode())
