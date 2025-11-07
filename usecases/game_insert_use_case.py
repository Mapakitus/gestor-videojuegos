from abc import ABC, abstractmethod

class IGameInsertUseCase(ABC):
    @abstractmethod
    def exec(self, game_data: dict):
        pass
    
    
class GameInsertUseCase(IGameInsertUseCase):
    def __init__(self, game_service):
        self.game_service = game_service

    def exec(self, game_data: dict):
        return self.game_service.create_game(game_data)