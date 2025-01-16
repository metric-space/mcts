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


def extract_information_from_tree(node):
    """

    Output: [number of children, ucb score of each child, action of chosen child, ...]

    """
    root = node
    while root.parent:
        root = root.parent

    info = []

    counter = 0

    while not root.is_terminal:
        temp = []
        next_root = None

        children = root.children.keys()
        children = sorted(children)

        l = len(children)

        if counter % 2 == 0:
          temp.append(l)
        for i in children:
            if counter % 2 == 0:
              temp.append(i)
              temp.append(root.children[i].ucb_score().item())

            if root.children[i].chosen:
                next_root = root.children[i]
        if counter % 2 == 0:
            temp.append(next_root.action)
        info += temp
        root = next_root

        counter += 1

    return info


def count_nodes(node):
    count = 1
    for child in node.children.values():
        count += count_nodes(child)
    return count


def depth(node):
    if not node.children:
        return 1
    return 1 + max(depth(child) for child in node.children.values())
