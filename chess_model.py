import instructor
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import os
import chess
import chess.engine

load_dotenv()

llm = instructor.from_openai(OpenAI())


class NextMove(BaseModel):
    move: str = Field(..., description="The next move contained in the input. It should be in standard algebraic notation.")
    reasoning: str = Field(..., description="Reasoning explaining why the move is the best one.")


class ChessModel:
    def __init__(self, name, provider, model_id):
        self.name = name
        self.provider = provider
        self.model_id = model_id
        self.rating = 1500  # Initial Elo rating

        if self.provider == 'openai':
            self.client = OpenAI()
        elif self.provider == 'openrouter':
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.environ.get("OPENROUTER_API_KEY"),
            )
        elif self.provider == 'stockfish':
            self.client = chess.engine.SimpleEngine.popen_uci("/opt/homebrew/Cellar/stockfish/16/bin/stockfish")

    def get_raw_response(self, board_state, legal_moves, history, feedback):

        if self.provider == 'stockfish':
            # Use Stockfish to generate the next move
            board = chess.Board(board_state)
            result = self.client.play(board, chess.engine.Limit(time=0.1))
            return result.move.uci()

        prompt = f"""
            You are a chess grandmaster. Given the current state of the chess board:
            {board_state}
            Legal moves: {legal_moves}
            History of moves so far: {history}
            Feedback on the previous move: {feedback}

            Generate the next move and explain your reasoning concisely.
            """
        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=[
                {"role": "user", "content": f"{prompt}"},
            ]
        )
        unstructured_response = response.choices[0].message.content
        return unstructured_response

    def parse_move_with_gpt(self, unstructured_response):

        if self.provider == 'stockfish':
            return unstructured_response

        """Use GPT-3.5 to parse the move from the unstructured response."""
        prompt = f"""
        You are a helpful assistant that extracts the next chess move from the given unstructured text.

        Unstructured response:
        \"\"\"
        {unstructured_response}
        \"\"\"

        Extract the next move in standard algebraic notation like e2e4, e7e5, c6d4, etc.
        """
        response = llm.chat.completions.create(
            model='gpt-3.5-turbo',
            response_model=NextMove,
            messages=[
                {"role": "user", "content": f"{prompt}"},
            ]

        )
        return response.move

    def get_next_move(self, board_state, legal_moves, history, feedback):
        unstructured_response = self.get_raw_response(board_state,
                                                      legal_moves,
                                                      history, feedback)

        # Use GPT-3.5 to parse the move
        move_text = self.parse_move_with_gpt(unstructured_response)
        return move_text
