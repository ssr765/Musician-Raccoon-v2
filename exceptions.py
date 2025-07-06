class MusicianRaccoonError(Exception):
    """Custom exception for Musician Raccoon application errors."""

    def __init__(self, message="error lolololo."):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message
