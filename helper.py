def moveHead(direction: str, head_position: dict[str, int]) -> dict[str, int]:
    if direction == "left":
        return {"x": head_position["x"]-1, "y": head_position["y"]}
    if direction == "up":
        return {"x": head_position["x"], "y": head_position["y"] + 1}
    if direction == "down":
        return {"x": head_position["x"], "y": head_position["y"] - 1}
    if direction == "right":
        return {"x": head_position["x"]+1, "y": head_position["y"]}
