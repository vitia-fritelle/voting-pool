from typing import Union

class VoteCard:

    
    def __init__(self, 
                 score: Union[int,None]=None, 
                 title: Union[str,None]=None, 
                 image: Union[str,None]=None, 
                 index: Union[int,None]=None):
        self.score = score
        self.title = title
        self.image = image
        self.index = index

    def upvote(self) -> None:
        self.score += 1
        return None
    
    def downvote(self) -> None:
        self.score -= 1
        return None
