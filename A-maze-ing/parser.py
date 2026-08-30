from pydantic import Field, model_validator
from pydantic_settings import BaseSettings
import os
from typing import Any, Union, Optional


class Settings(BaseSettings):
    """Configuration settings for the maze generator.

    Attributes:
        WIDTH: Maze width, must be between 6 and 100 inclusive.
        HEIGHT: Maze height, must be between 6 and 100 inclusive.
        ENTRY: Entry point as a tuple (x, y) or a comma-separated string.
        EXIT: Exit point as a tuple (x, y) or a comma-separated string.
        OUTPUT_FILE: Path to the output file where the maze will be saved.
        PERFECT: Whether the maze should be a perfect maze (single path).
        SEED: Optional random seed for reproducible maze generation.
    """

    WIDTH: int = Field(gt=1, le=100)
    HEIGHT: int = Field(gt=1, le=100)
    ENTRY: str | tuple[int, int]
    EXIT: str | tuple[int, int]
    OUTPUT_FILE: str = Field(default="maze.txt")
    PERFECT: bool = Field(default=True)
    SEED: Optional[Any] = Field(default=None)

    @model_validator(mode="after")
    def validate_all(self) -> "Settings":
        """Validate and normalize all settings after model initialization.

        Parses ENTRY and EXIT from strings if necessary, checks that both
        coordinates are within maze bounds, ensures OUTPUT_FILE is not a
        directory, and verifies that ENTRY and EXIT are distinct.

        Returns:
            The validated Settings instance.

        Raises:
            ValueError: If coordinates are malformed, out of bounds, or
                ENTRY equals EXIT.
            IsADirectoryError: If OUTPUT_FILE points to a directory.
        """

        def in_bounds(name: str, c: tuple[int, int]) -> None:
            """Check that a coordinate lies within the maze boundaries.

            Args:
                name: The name of the coordinate field (for error messages).
                c: The (x, y) coordinate to validate.

            Raises:
                ValueError: If the coordinate is outside the maze dimensions.
            """
            x: int
            y: int
            x, y = c
            if not (0 <= x < self.WIDTH and 0 <= y < self.HEIGHT):
                raise ValueError(
                    f"{name} out of bounds: (x,y) must"
                    " be within WIDTH & HEIGHT"
                )

        def parse(name: str, v: Union[str, tuple[int, int]]
                  ) -> tuple[int, int]:
            """Parse a coordinate value from string or pass through if tuple.

            Args:
                name: The name of the coordinate field (for error messages).
                v: A coordinate as a tuple or a comma-separated string.

            Returns:
                A tuple of two integers (x, y).

            Raises:
                ValueError: If the string format is not 'x,y'.
            """
            if isinstance(v, tuple):
                return v
            parts = [p.strip() for p in v.split(",")]
            if len(parts) != 2:
                raise ValueError(f"{name} must be in format 'x,y'")
            return (int(parts[0]), int(parts[1]))

        self.ENTRY = parse("ENTRY", self.ENTRY)
        self.EXIT = parse("EXIT", self.EXIT)

        in_bounds("ENTRY", self.ENTRY)
        in_bounds("EXIT", self.EXIT)

        if os.path.isdir(self.OUTPUT_FILE):
            raise IsADirectoryError(
                "The OUTPUT_FILE should be a File.txt Not a Dir"
            )

        if self.ENTRY == self.EXIT:
            raise ValueError("ENTRY and EXIT must be different")

        return self
