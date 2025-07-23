from vision.vision_bot import VisionBot
from domain.queens.queens import Queens
from domain.queens.cell import Cell
import numpy as np
import cv2
from PIL import Image, ImageDraw

"""
Vision bot for Tango puzzles.
"""
class QueensVisionBot(VisionBot):

    def __init__(self):
        super().__init__()
        self.cell_coordinates = []
        self.whole_screenshot = None
        self.offsets = []

    """
    Detect the game board in the screenshot.
    """
    def detect_game_board(self):
        
        # TODO: Implement the game board detection logic.
        # General idea is to start in the center and keep expanding outwards
        # until we have 6 pieces detected.
        # After that crop image

        padding = 300
        center = (self.screenshot.width // 2, self.screenshot.height // 2)
        self.offsets.append((center[0] - padding, center[1] - padding))
        new_image_array = np.array(self.screenshot)[center[1] - padding:center[1] + padding, center[0] - padding:center[0] + padding]
        self.whole_screenshot = self.screenshot.copy()
        self.screenshot = Image.fromarray(new_image_array)
        self.screenshot.save("screenshot_cropped.png")

        # Convert to grayscale for easier processing
        gray = cv2.cvtColor(new_image_array, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold to separate the board from background
        _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Find the largest contour (should be the board)
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Get bounding rectangle
        x, y, w, h = cv2.boundingRect(largest_contour)
        self.offsets.append((x, y))
        
        # Crop the image
        cropped = new_image_array[y:y+h, x:x+w]
        self.screenshot = Image.fromarray(cropped)
        self.screenshot.save("screenshot_board.png")

    """
    Get the color of the cell based on its image.
    """
    def get_color_code(self, cell : Image.Image, color_map : dict) -> str:
        height, width = cell.size
        bgr_color = np.array(cell)[height // 2, width // 2]
        rgb_color = bgr_color[::-1]  # Convert BGR to RGB
        color_hex = "#{:02x}{:02x}{:02x}".format(rgb_color[0], rgb_color[1], rgb_color[2])
        if color_hex in color_map:
            return color_map[color_hex]
        else:
            next = chr(ord('A') + len(color_map))
            color_map[color_hex] = next
            return next

    """
    Convert screenshot to Tango object.
    """
    def parse_screenshot(self) -> Queens:
        if self.screenshot is None:
            raise ValueError("No screenshot taken. Please take a screenshot before parsing.")
        
        # Split in 8 * 8 grid
        grid_size = 8
        piece_width = self.screenshot.width // grid_size
        piece_height = self.screenshot.height // grid_size
        pieces = []
        for i in range(grid_size):
            for j in range(grid_size):
                piece = self.screenshot.crop((j * piece_width, i * piece_height, (j + 1) * piece_width, (i + 1) * piece_height))
                pieces.append(piece)
        color_map = {}
        colors = [self.get_color_code(piece, color_map) for piece in pieces]
        grid = np.array(colors).reshape((grid_size, grid_size))
        self.cell_coordinates = []
        for i in range(grid_size):
            row_coords = []
            for j in range(grid_size):
                x = self.offsets[0][0] + self.offsets[1][0] + j * piece_width + piece_width // 2
                y = self.offsets[0][1] + self.offsets[1][1] + i * piece_height + piece_height // 2
                row_coords.append((x, y))
            self.cell_coordinates.append(row_coords)
        cells = []
        for i in range(grid_size):
            row = []
            for j in range(grid_size):
                row.append(Cell(i, j, grid[i][j], -1))
            cells.append(row)
        return Queens(cells)

    """
    Based on the cells of the solved puzzle, apply changes to the screen.
    """
    def apply_changes(self, puzzle: Queens):
        cells = puzzle.get_cells()
        marked_image = self.whole_screenshot.copy()
        draw = ImageDraw.Draw(marked_image)
        for i in range(len(cells)):
            for j in range(len(cells[i])):
                if cells[i][j].get_value_str() == "Q":
                    coords = self.cell_coordinates[i][j]
                    size = 30
                    print(f"Placing queen at ({i}, {j}) with coordinates {coords}")
                    self.click(coords[0], coords[1])
                    self.click(coords[0], coords[1])  # Double click to place the queen
                    draw.ellipse([coords[0] - size//2, coords[1] - size//2, coords[0] + size//2, coords[1] + size//2], 
                    outline=(0, 0, 0), width=3)
        marked_image.save("marked_screenshot.png")
                    