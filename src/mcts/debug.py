import numpy as np
from .uct_search import UCTNode

def render_board(node: UCTNode):
    html_string = ""
    for child in node.children.values():
        board = np.rot90(child.board_state.game_state()[0])
        classes = ["connect4-container"]
        if child.chosen:
            classes.append("chosen")

        html_string += "<div class='{}'>".format(" ".join(classes))
        for row in board:
            html_string += "<div class='connect4-row'>"
            for cell in row:
                html_string += "<div class='connect4-cell "
                if cell == 0:
                    html_string += "player1"
                elif cell == 1:
                    html_string += "player2"
                html_string += "'></div>"
            html_string += "</div>"
        html_string += "</div>"
    return html_string


def render_tree(node: UCTNode):

    depth = 0

    while node.parent:

        node = node.parent
        depth += 1

    print("Depth: ", depth)

    html_string = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"/>
    <title>Connect4 Board</title>
</head>
<body>
    <style>
      .connect4-container {
        display: inline-block;
        border: 2px solid #333;
        background-color: #4444FF;
        padding: 5px;
      }
      .connect4-row {
        display: flex;
      }
      .connect4-cell {
        width: 10px;
        height: 10px;
        margin: 2px;
        border-radius: 50%;
        background-color: white;
      }
      .player1 {
        background-color: red;
      }
      .player2 {
        background-color: yellow;
      }
      .chosen {
        border: 6px solid blue;
      }
    </style>

    <body>

    """

    while node:
        html_string += "<div>" + render_board(node) + "</div><br/>"

        node = [x for x in node.children.values() if x.chosen]
        if len(node) == 0:
            break
        node = node[0]

    html_string += "</body></html>"

    return html_string
