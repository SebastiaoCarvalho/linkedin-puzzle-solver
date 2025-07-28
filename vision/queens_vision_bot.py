from vision.vision_bot import VisionBot
from domain.queens.queens import Queens
from domain.queens.cell import Cell
import numpy as np
import cv2
from PIL import Image, ImageDraw

class QueensVisionBot(VisionBot):
    """
    Vision bot for Tango puzzles.
    """

    def __init__(self):
        super().__init__()
        self.cell_coordinates = []
        self.whole_screenshot = None
        self.offsets = []

    def detect_game_board(self):
        """
        Detect the game board in the screenshot.
        """
        
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

    def get_color_code(self, cell : Image.Image, color_map : dict) -> str:
        """
        Get the color of the cell based on its image.
        """

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
        
    def get_grid_size(self) -> int:
        """
        Get the size of the grid.
        """

        if self.screenshot is None:
            raise ValueError("No screenshot taken. Please take a screenshot before getting grid size.")
        
        image_array = np.array(self.screenshot)
        image_array[image_array > 20] = 255  # Threshold to make sure we have a binary image
        image_array[image_array <= 20] = 0
        
        # Find a row where not all pixels are black
        row_index = self.screenshot.height // 2
        all_black = np.all(image_array[row_index, :] == 0)
        while all_black:
            row_index -= 1
            if row_index < 0:
                raise ValueError("Could not find a valid row in the screenshot.")
            all_black = np.all(image_array[row_index, :] == 0)
        
        # Find the sequences of black pixels in the row
        row = image_array[row_index, :]
        black_pixel_sequences = []
        current_sequence_length = 0
        for pixel in row:
            if np.all(pixel == 0):
                current_sequence_length += 1
            else:
                if current_sequence_length > 0:
                    black_pixel_sequences.append(current_sequence_length)
                current_sequence_length = 0
        if current_sequence_length > 0:
            black_pixel_sequences.append(current_sequence_length)
        
        return len(black_pixel_sequences) - 1

    def parse_screenshot(self) -> Queens:
        """
        Convert screenshot to Tango object.
        """

        if self.screenshot is None:
            raise ValueError("No screenshot taken. Please take a screenshot before parsing.")
        # Split in n * n grid
        grid_size = self.get_grid_size()
        print(grid_size)
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

    def apply_changes(self, puzzle: Queens):
        """
        Based on the cells of the solved puzzle, apply changes to the screen.
        """

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
                    