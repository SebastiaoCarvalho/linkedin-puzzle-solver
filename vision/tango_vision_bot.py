from domain.tango.tango import Tango
from domain.tango.cell import Cell
from domain.tango.border import Border
from vision.vision_bot import VisionBot
import numpy as np
import cv2
from PIL import Image, ImageDraw

class TangoVisionBot(VisionBot):
    """
    Vision bot for Tango puzzles.
    """

    def __init__(self):
        super().__init__()
        self.cell_coordinates = []
        self.whole_screenshot = None
        self.offsets = []
        self.sun_color_range = {
            'lower': np.array([10, 130, 130]),  # Orange/yellow lower bound
            'upper': np.array([25, 255, 255])   # Orange/yellow upper bound
        }
        
        self.moon_color_range = {
            'lower': np.array([100, 90, 90]),   # Blue lower bound
            'upper': np.array([130, 255, 255])  # Blue upper bound
        }


        # self.x_templates = [
        #     np.array(Image.open(f"vision/samples/x_horiz.png")),
        #     np.array(Image.open(f"vision/samples/x_vert.png"))
        # ]
        # self.eq_templates = [
        #     np.array(Image.open(f"vision/samples/equals_horiz.png")),
        #     np.array(Image.open(f"vision/samples/equals_vert.png"))
        # ]
        # self.empty_templates = [
        #     np.array(Image.open(f"vision/samples/empty_horiz.png")),
        #     np.array(Image.open(f"vision/samples/empty_vert.png"))
        # ]

        self.x_templates = [ 
            self.convert_to_binary(Image.open(f"vision/samples/x_horiz.png")), 
            self.convert_to_binary(Image.open(f"vision/samples/x_vert.png"))
        ]
        self.eq_templates = [
            self.convert_to_binary(Image.open(f"vision/samples/equals_horiz.png")),
            self.convert_to_binary(Image.open(f"vision/samples/equals_vert.png"))
        ]
        self.empty_templates = [
            self.convert_to_binary(Image.open(f"vision/samples/empty_horiz.png")),
            self.convert_to_binary(Image.open(f"vision/samples/empty_vert.png"))
        ]
        for (i, template) in enumerate(self.x_templates):
            cv2.imwrite(f"x_template_{i}.png", template)
        for (i, template) in enumerate(self.eq_templates):
            cv2.imwrite(f"eq_template_{i}.png", template)
        for (i, template) in enumerate(self.empty_templates):
            cv2.imwrite(f"empty_template_{i}.png", template)

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
        new_image_array = np.array(self.screenshot)[center[1] - padding:center[1] + padding, center[0] - padding:center[0] + padding]
        self.offsets.append((center[0] - padding, center[1] - padding))
        self.whole_screenshot = self.screenshot.copy()
        self.screenshot = Image.fromarray(new_image_array)
        self.screenshot.save("screenshot_cropped.png")

        # Convert to HSV
        hsv = cv2.cvtColor(new_image_array, cv2.COLOR_RGB2HSV)

        cv2.imwrite("screenshot_hsv.png", hsv)

        # Create masks for sun and moon colors
        sun_mask = cv2.inRange(hsv, self.sun_color_range['lower'], self.sun_color_range['upper'])
        moon_mask = cv2.inRange(hsv, self.moon_color_range['lower'], self.moon_color_range['upper'])

        # Find first sun or moon position in hsv
        combined_mask = cv2.bitwise_or(sun_mask, moon_mask)

        # Save combined mask into black and white image
        cv2.imwrite("screenshot_combined_mask.png", combined_mask)

        non_zero_points = cv2.findNonZero(combined_mask)

        # Ignore height, since it may detect text below
        x, y, w, _ = cv2.boundingRect(non_zero_points)
        image_padding = 15
        top_left = (x - image_padding, y - image_padding)
        bottom_right = (x + w + image_padding, y + w + image_padding)
        
        cropped_array = np.array(self.screenshot)[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
        self.offsets.append(top_left)
        self.screenshot = Image.fromarray(cropped_array)
        self.screenshot.save("screenshot_final.png")
    
    def classify_cell(self, cell_image: Image.Image) -> int:
        """
        Get the classification of a cell image. 1 for sun, 0 for moon, -1 for emoty.
        """

        # Convert to numpy array and then to HSV
        cell_array = np.array(cell_image)
        hsv_cell = cv2.cvtColor(cell_array, cv2.COLOR_RGB2HSV)

        # Create masks for sun and moon colors
        sun_mask = cv2.inRange(hsv_cell, self.sun_color_range['lower'], self.sun_color_range['upper'])
        moon_mask = cv2.inRange(hsv_cell, self.moon_color_range['lower'], self.moon_color_range['upper'])

        # Save masks for debugging
        cv2.imwrite("sun_mask.png", sun_mask)
        cv2.imwrite("moon_mask.png", moon_mask)

        # Check if there are any non-zero pixels in the masks
        if np.any(sun_mask):
            return 1
        
        elif np.any(moon_mask):
            return 0
        
        else:
            return -1
        
    def classify_border(self, border_image : Image.Image, i, j, is_horizontal : bool) -> int:
        """
        Classify the border image. Returns 1 for x, 0 for =, -1 for - or |.
        """

        binary = self.convert_to_binary(border_image)
        #border_image.save(f"border_image_{i}_{j}.png")
        #cv2.imwrite(f"border_binary_{i}_{j}.png", binary)

        all_results = []
        best_score = 0
        best_index = 0
        template_index = 0 if is_horizontal else 1
        templates = [self.x_templates[template_index], self.eq_templates[template_index], self.empty_templates[template_index]]
        for index, template in enumerate(templates):
            different_pixels = np.sum(template != binary)
            total_pixels = binary.size
            score = 1.0 - (different_pixels / total_pixels)
            if score > best_score:
                best_score = score
                best_index = index
            all_results.append(score)
        print(f"Border classification for ({i}, {j}, {'horizontal' if is_horizontal else 'vertical'}): {all_results}, best index: {best_index}, score: {best_score}")
        #cv2.imwrite(f"border_binary_{i}_{j}_best.png", templates[best_index])
        if best_index == 0:
            return 1  # x
        elif best_index == 1:
            return 0 # =
        return - 1
    
    def get_borders(self, grid_size : int, piece_width : float, piece_height : float) -> list[list[Border]]:
        hsv = cv2.cvtColor(np.array(self.screenshot), cv2.COLOR_RGB2HSV)

        # Create masks for sun and moon colors
        sun_mask = cv2.inRange(hsv, self.sun_color_range['lower'], self.sun_color_range['upper'])
        moon_mask = cv2.inRange(hsv, self.moon_color_range['lower'], self.moon_color_range['upper'])

        combined_mask = cv2.bitwise_or(sun_mask, moon_mask)

        image_array = np.array(self.screenshot)
        # Remove sun and moon pixels from the image
        non_zero_points = cv2.findNonZero(combined_mask)
        if non_zero_points is not None:
            for point in non_zero_points:
                x, y = point[0]
                image_array[y, x] = [255, 255, 255]
        image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)

        # Filter to have only = and x
        MASK_OPERATORS = 155
        image_array[image_array < MASK_OPERATORS] = 0  # Set dark pixels to black
        image_array[image_array >= MASK_OPERATORS] = 255  # Set light pixels to white
        cv2.imwrite("screenshot_mask.png", image_array)

        min_length = 7
        # Create structural elements for different line orientations
        # Horizontal lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (min_length, 1))
        # Diagonal lines (45 degrees)
        diagonal1_kernel = np.eye(min_length, dtype=np.uint8)
        # Anti-diagonal lines (-45 degrees)
        diagonal2_kernel = np.fliplr(np.eye(min_length, dtype=np.uint8))

        inverted_image = cv2.bitwise_not(image_array)
        
        # Extract lines using morphological opening
        horizontal_lines = cv2.morphologyEx(inverted_image, cv2.MORPH_OPEN, horizontal_kernel)
        diagonal1_lines = cv2.morphologyEx(inverted_image, cv2.MORPH_OPEN, diagonal1_kernel)
        diagonal2_lines = cv2.morphologyEx(inverted_image, cv2.MORPH_OPEN, diagonal2_kernel)

        # Cross is two diagonals combined
        cross = diagonal1_lines + diagonal2_lines
        cross = np.clip(cross, 0, 1)

        cross_image = Image.fromarray(cv2.bitwise_not(np.where(cross == 1, 255, 0).astype(np.uint8)))
        cross_image.save("screenshot_cross_lines.png")

        horizontal_lines_image = Image.fromarray(cv2.bitwise_not(np.where(np.clip(horizontal_lines, 0, 1) == 1, 255, 0).astype(np.uint8)))
        horizontal_lines_image.save("screenshot_horizontal_lines.png")

        borders = []
        for i in range(grid_size):
            vertical_borders = []
            horizontal_borders = []
            # Vertical borders
            for j in range(grid_size - 1):
                center = ((j + 1) * piece_width, (i + 0.5) * piece_height)
                padding = 15
                horizontal_piece = horizontal_lines_image.crop((center[0] - padding, center[1] - padding, center[0] + padding, center[1] + padding))
                cross_piece = cross_image.crop((center[0] - padding, center[1] - padding, center[0] + padding, center[1] + padding))
                val = -1
                if np.any(np.array(horizontal_piece) == 0): # =
                    val = 0
                elif np.any(np.array(cross_piece) == 0): # x
                    val = 1
                print(f"Border classification for ({i}, {j}, vertical): {val}")
                vertical_borders.append(Border(i, j, val, False))
            borders.append(vertical_borders)
            if i >= grid_size - 1:
                continue
            # Horizontal borders
            for j in range(grid_size):
                center = ((j + 0.5) * piece_width, (i + 1) * piece_height)
                padding = 15
                horizontal_piece = horizontal_lines_image.crop((center[0] - padding, center[1] - padding, center[0] + padding, center[1] + padding))
                cross_piece = cross_image.crop((center[0] - padding, center[1] - padding, center[0] + padding, center[1] + padding))
                val = -1
                if np.any(np.array(horizontal_piece) == 0): # =
                    val = 0
                elif np.any(np.array(cross_piece) == 0): # x
                    val = 1
                print(f"Border classification for ({i}, {j}, horizontal): {val}")
                horizontal_borders.append(Border(i, j, val, True))
            borders.append(horizontal_borders)
        return borders

    
    def convert_to_binary(self, image: Image.Image) -> np.ndarray:
        """
        Convert an image to a binary numpy array.
        """

        # Convert to grayscale
        gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)

        # Remove light gray and convert it to white
        gray[gray > 200] = 255

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply adaptive thresholding for better edge detection
        binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                     cv2.THRESH_BINARY_INV, 15, 4)

        # Apply morphological operations to clean up the binary image
        kernel = np.ones((2, 2), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        return binary

    def parse_screenshot(self) -> Tango:
        """
        Convert screenshot to Tango object.
        """

        if self.screenshot is None:
            raise ValueError("No screenshot taken. Please take a screenshot before parsing.")
        
        # Split in 6 * 6 grid
        grid_size = 6
        piece_width = self.screenshot.width // grid_size
        piece_height = self.screenshot.height // grid_size
        pieces = []
        for i in range(grid_size):
            for j in range(grid_size):
                piece = self.screenshot.crop((j * piece_width, i * piece_height, (j + 1) * piece_width, (i + 1) * piece_height))
                pieces.append(piece)
        border_pieces = []
        for i in range(grid_size):
            vertical_borders = []
            horizontal_borders = []
            # Vertical borders
            for j in range(grid_size - 1):
                center = ((j + 1) * piece_width, (i + 0.5) * piece_height)
                padding = 10
                piece = self.screenshot.crop((center[0] - padding, center[1] - padding, center[0] + padding, center[1] + padding))
                vertical_borders.append(piece)
            border_pieces.append(vertical_borders)
            if i >= grid_size - 1:
                continue
            # Horizontal borders
            for j in range(grid_size):
                center = ((j + 0.5) * piece_width, (i + 1) * piece_height)
                padding = 10
                piece = self.screenshot.crop((center[0] - padding, center[1] - padding, center[0] + padding, center[1] + padding))
                horizontal_borders.append(piece)
            border_pieces.append(horizontal_borders)

        classifications = [self.classify_cell(piece) for piece in pieces]
        grid = np.array(classifications).reshape((grid_size, grid_size))
        cells = []
        for i in range(grid_size):
            row = []
            for j in range(grid_size):
                row.append(Cell(i, j, grid[i][j]))
            cells.append(row)
        self.cell_coordinates = []
        for i in range(grid_size):
            row_coords = []
            for j in range(grid_size):
                x = self.offsets[0][0] + self.offsets[1][0] + j * piece_width + piece_width // 2
                y = self.offsets[0][1] + self.offsets[1][1] + i * piece_height + piece_height // 2
                row_coords.append((x, y))
            self.cell_coordinates.append(row_coords)
        
        return Tango(cells, self.get_borders(grid_size, piece_width, piece_height))

    def apply_changes(self, puzzle: Tango):
        """
        Based on the cells of the solved puzzle, apply changes to the screen.
        """

        cells = puzzle.get_cells()
        marked_image = self.whole_screenshot.copy()
        draw = ImageDraw.Draw(marked_image)
        for i in range(len(cells)):
            for j in range(len(cells[i])):
                coords = self.cell_coordinates[i][j]
                size = 30
                if cells[i][j].get_value_str() == "S":
                    print(f"Placing sun at ({i}, {j}) with coordinates {coords}")
                    self.click(coords[0], coords[1])
                    self.click(coords[0], coords[1])  # Double click to place the queen
                    draw.ellipse([coords[0] - size//2, coords[1] - size//2, coords[0] + size//2, coords[1] + size//2], 
                    outline=(255, 0, 0), width=3)
                elif cells[i][j].get_value_str() == "M":
                    print(f"Placing moon at ({i}, {j}) with coordinates {coords}")
                    self.click(coords[0], coords[1])
                    self.click(coords[0], coords[1])
                    draw.ellipse([coords[0] - size//2, coords[1] - size//2, coords[0] + size//2, coords[1] + size//2],
                    outline=(0, 0, 255), width=3)
        marked_image.save("marked_screenshot.png")