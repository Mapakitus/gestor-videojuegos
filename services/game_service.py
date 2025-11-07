from abc import ABC, abstractmethod
#algunos metodos que podrían existir en el servicio de juegos, cambia según tus necesidades

class IGameService(ABC):
    @abstractmethod
    def get_game_by_id(self, game_id: str):
        pass
    @abstractmethod
    def get_all_games(self):
        pass

    @abstractmethod
    def create_game(self, game_data: dict):
        pass

    @abstractmethod
    def update_game(self, game_id: str, game_data: dict):
        pass

    @abstractmethod
    def delete_game(self, game_id: str):
        pass
    @abstractmethod
    def search_games(self, query: str):
        pass
    @abstractmethod
    def filter_games_by_genre(self, genre: str):
        pass
    @abstractmethod
    def add_genre_to_game(self, game_id: str, genre: str):
        pass
    
    #class GameService(IGameService):