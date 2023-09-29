from diagrams.custom import Custom
from PIL import ImageFont, ImageDraw, Image
import os
import tempfile
import atexit


class Icon(Custom):
    
    def __init__(self, label, icon=None, border=True):
        """Create a node but with autogenerated icon/image if none provided.
        
        This extends the `diagrams.custom.Custom` class meaning that it can be 
        used just like a normal node.

        Args:
            label (str): The name/label for the node.
            icon (str, optional): Optional file path to the icon/image to use
                for the node. If not given, then the icon/image will be 
                automatically generated based on the `label` text, and the 
                label will be made invisible.
            border (bool, optional): Whether to draw a border around the 
                generated icon or not. Defaults to True.
        """
        self.icon_generated = False
        if icon is not None:
            super().__init__(label, icon)
        else:
            icon_fp = self._generate_icon(label, border)
            
            @atexit.register
            def cleanup():
                os.remove(icon_fp)
            
            label = ""
            super().__init__(label, icon_fp)
    
    
    def _maybe_hyphenate_word(self, word, font, max_length):
        """Convert a word into a list of possibly hyphenated parts.
        
        Whether and where to hyphenate is determined by the bounding width set 
        by the `max_length` and the size of the word when rendered in the 
        given `font`.

        Args:
            word (str): Word which may need to be hyphenated.
            font (`PIL.ImageFont.FreeTypeFont`): Font that will be used to 
                render the `word`.
            max_length (int): Bounding box in pixels.

        Returns:
            list of str: List of possibly hyphenated parts.
        """
        if font.getlength(word) <= max_length:
            return [word]
        
        hyphenated = []
        construction = ""
        for character in word:
            if font.getlength(construction + character + "-") <= max_length:
                construction += character
            else:
                # Avoid adding another hyphen where one already exists in the
                # word.
                if construction.endswith("-"):
                    hyphenated.append(construction)
                else:
                    hyphenated.append(construction + "-")
                construction = character
        
        hyphenated.append(construction)
        return hyphenated
    
    def _hyphenate(self, words, font, max_length):
        """Hyphenate any of the words in a list that are too long.
        
        Words are hyphenated based on the bounding width set by the 
        `max_length` and the size of the word when rendered in the given 
        `font`.

        Args:
            words (list of str): Collection of words.
            font (`PIL.ImageFont.FreeTypeFont`): Font that will be used to 
                render the `word`.
            max_length (int): Bounding box in pixels.

        Returns:
            list of str: List of words that are no longer than the 
                `max_length`.
        """
        hyphenated = [
            hyph_word
            for word in words
            for hyph_word in self._maybe_hyphenate_word(word, font, max_length)
        ]
        return hyphenated
    
    def _squarify_text(self, text, font, max_size):
        """Split text into lines with optional hyphenation.
        
        Ensure that each line fits within the bounding width specified by the
        `max_size`, taking a new line and hyphenating where necessary.

        Args:
            text (str): Text to be squared.
            font (`PIL.ImageFont.FreeTypeFont`): Font that will be used to 
                render the `word`.
            max_size (int): Maximum width in pixels that the text must fit 
                inside.

        Returns:
            str
        """
        words = text.strip().split()
        
        margin = 50
        max_length = max_size - margin
        normalised_words = self._hyphenate(words, font, max_length)
        
        if len(normalised_words) == 1:
            return normalised_words[0]
        
        lines = []
        this_line = []
        for word in normalised_words:
            built_line = this_line + [word]
            built_line_length = font.getlength(" ".join(built_line))
            if built_line_length > max_length:
                lines.append(" ".join(this_line))
                this_line = [word]
            else:
                this_line = built_line
        
        lines.append(" ".join(this_line))
        squared_text = "\n".join(lines)
        return squared_text
        
        
    def _generate_icon(self, label, border):
        """Draw an icon .png file containing the given text.

        Args:
            label (str): Text to be written inside the icon.
            border (bool): If true, a border will be drawn around the outside
                of the icon.
        
        Returns:
            str: File path to the location of the temporary .png generated.
        """
        icon_fp = tempfile.mkstemp(suffix=".png")[1]
        
        dpi = 300
        icon_size = round(1.4 * dpi)
        font_size = round((dpi / 72) * 13)
        
        font = ImageFont.truetype("Arial", size=font_size)
        text = self._squarify_text(label, font, icon_size)
        colour = "black"
        
        draw_text_kwargs = dict(
            xy = [icon_size / 2] * 2,
            text = text,
            font = font,
            align = "center"
        )
        
        img = Image.new("RGBA", [icon_size] * 2)
        draw = ImageDraw.Draw(img)
        
        draw.text(fill=colour, anchor="mm", **draw_text_kwargs)
        
        if border:
            draw.rounded_rectangle(
                [(0, 0), [icon_size] * 2],
                radius=30,
                outline=colour,
                width=5
            )
        
        img.save(icon_fp, dpi=[dpi] *2)
        return icon_fp