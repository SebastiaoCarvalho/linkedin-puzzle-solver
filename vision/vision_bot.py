from domain.puzzle import Puzzle
import pyautogui
from pynput import mouse

"""
Base class for vision bot
"""
class VisionBot:

    def __init__(self):
        self.screenshot = None
        self.mouse = mouse.Controller()

    """
    Screenshot the current screen.
    """
    def take_screenshot(self):
        self.screenshot = pyautogui.screenshot()
        self.screenshot.save("screenshot.png")
    
    """
    Parse the screenshot and return a Puzzle object.
    """
    def parse_screenshot(self) -> Puzzle:
        raise NotImplementedError("This method should be implemented by subclasses.")
    
    """
    Click on screen coordinates
    """
    def click(self, x: int, y: int):
        self.mouse.position = (x, y)
        self.mouse.click(mouse.Button.left, 1)
    
    """
    Apply changes of puzzle to the screen.
    """
    def apply_changes(self, puzzle: Puzzle):
        raise NotImplementedError("This method should be implemented by subclasses.")