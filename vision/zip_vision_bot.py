from domain.zip.zip import Zip
from vision.vision_bot import VisionBot

class ZipVisionBot(VisionBot):
    """
    Base class for vision bot
    """
    
    def parse_screenshot(self) -> Zip:
        """
        Parse the screenshot and return a Puzzle object.
        """

        pass
    
    
    def apply_changes(self, puzzle: Zip):
        """
        Apply changes of puzzle to the screen.
        """

        pass