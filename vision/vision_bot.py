from domain.puzzle import Puzzle
import pyautogui
from pynput import mouse

class VisionBot:
    """
    Base class for vision bot
    """

    def __init__(self):
        self.screenshot = None
        self.mouse = mouse.Controller()

    def take_screenshot(self):
        """
        Screenshot the current screen.
        """

        self.screenshot = pyautogui.screenshot()
        self.screenshot.save("screenshot.png")
    
    def parse_screenshot(self) -> Puzzle:
        """
        Parse the screenshot and return a Puzzle object.
        """

        raise NotImplementedError("This method should be implemented by subclasses.")
    
    def click(self, x: int, y: int):
        """
        Click on screen coordinates
        """

        self.mouse.position = (x, y)
        self.mouse.click(mouse.Button.left, 1)
    
    def apply_changes(self, puzzle: Puzzle):
        """
        Apply changes of puzzle to the screen.
        """

        raise NotImplementedError("This method should be implemented by subclasses.")