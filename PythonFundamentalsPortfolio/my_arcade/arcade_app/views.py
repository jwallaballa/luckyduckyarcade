# arcade_app/views.py

import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .games.snake import AsciiSnakeGame
from .games.pong import AsciiPongGame
from .games.tic_tac_toe import TicTacToeGame
from .models import HighScore

# Session key to store game instances
SESSION_GAMES_KEY = 'current_games'


def get_game_instance(request, game_name):
    """
    Retrieve or initialize a game instance from the session.
    """
    games_data = request.session.get(SESSION_GAMES_KEY, {})
    game_data = games_data.get(game_name)
    game = None

    if game_name == 'snake_ascii':
        game = AsciiSnakeGame.from_dict(game_data) if game_data else AsciiSnakeGame()
    elif game_name == 'pong_ascii':
        game = AsciiPongGame.from_dict(game_data) if game_data else AsciiPongGame()
    elif game_name == 'tic_tac_toe':
        game = TicTacToeGame.from_dict(game_data) if game_data else TicTacToeGame()

    if game:
        games_data[game_name] = game.to_dict()
        request.session[SESSION_GAMES_KEY] = games_data
        request.session.modified = True

    return game, games_data


def get_top_high_score(game_name):
    """
    Get the top high score for a given game.
    This function remains generic but will only be used for 'snake_ascii'
    in the play_game logic.
    """
    try:
        top_score_entry = (
            HighScore.objects
            .filter(game_name=game_name)
            .order_by('-score')
            .first()
        )
        if top_score_entry:
            return {
                'initials': top_score_entry.player_name or '---',
                'score': top_score_entry.score
            }
    except Exception as e:
        print(f"Error fetching top high score for {game_name}: {e}")

    return {'initials': '---', 'score': 0}


@csrf_exempt
def play_game(request):
    """
    Main endpoint to handle game actions from the frontend.
    Modified to only pass high score data to Snake's render method
    and only include score in response for Snake.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)
        game_name = data.get('game_name')
        user_input = data.get('input', '').strip()
        snake_direction = data.get('snake_direction')
        paddle_a_move_direction = data.get('paddle_a_move_direction')

        game, games_data = get_game_instance(request, game_name)

        if not game:
            return JsonResponse({
                'output': 'Error: Game not found or not initialized in session.',
                'state': 'error'
            }, status=400)

        game_state_for_frontend = 'playing'
        output = ""
        extra_response_data = {}

        # Fetch high score ONLY if the game is Snake
        current_top_high_score = None
        if game_name == 'snake_ascii':
            current_top_high_score = get_top_high_score(game_name)

        # Handle 'start' input
        if user_input.lower() == 'start':
            game.reset()
            if hasattr(game, 'game_started'):
                game.game_started = True

            if game_name == 'tic_tac_toe':
                output = game.render()
            elif game_name == 'snake_ascii': # Pass high score data only for Snake
                output = game.render(high_score_data=current_top_high_score)
            else: # For Pong and other games, render without high score data
                output = game.render()

            if game_name == 'tic_tac_toe':
                extra_response_data.update({
                    'human_player': game.human_player,
                    'ai_player': game.ai_player,
                    'current_player': game.current_player,
                    'game_internal_state': game.state
                })
                game_state_for_frontend = game.state
            elif hasattr(game, 'game_over'):
                game_state_for_frontend = (
                    'game_over' if game.game_over else 'playing'
                )
                # Only include score in response for Snake for potential high score saving
                if game.game_over and hasattr(game, 'score') and game_name == 'snake_ascii':
                    extra_response_data['score'] = game.score

        # Handle Pong update
        elif game_name == 'pong_ascii' and user_input.lower() == 'update':
            if not game.game_over:
                if paddle_a_move_direction is not None:
                    game.change_paddle_direction('A', paddle_a_move_direction)
                game.update()

            # For Pong, render without high score data
            output = game.render()
            game_state_for_frontend = (
                'game_over' if game.game_over else 'playing'
            )
            # Do NOT include score in response for Pong for high score saving
            # if game.game_over and hasattr(game, 'score'):
            #     extra_response_data['score'] = game.score # Removed this line

        # Handle Snake update
        elif game_name == 'snake_ascii' and user_input.lower() == 'update':
            if not game.game_over:
                if snake_direction:
                    game.change_direction(snake_direction)
                game.update()

            # Pass high score data for Snake
            output = game.render(high_score_data=current_top_high_score)
            game_state_for_frontend = (
                'game_over' if game.game_over else 'playing'
            )
            # Include score in response for Snake for potential high score saving
            if game.game_over and hasattr(game, 'score'):
                extra_response_data['score'] = game.score

        # Default game play handler
        else:
            if hasattr(game, 'play'):
                output = game.play(user_input)

                if game_name == 'tic_tac_toe':
                    extra_response_data.update({
                        'human_player': game.human_player,
                        'ai_player': game.ai_player,
                        'current_player': game.current_player,
                        'game_internal_state': game.state
                    })
                    game_state_for_frontend = game.state
                elif hasattr(game, 'game_over'):
                    game_state_for_frontend = (
                        'game_over' if game.game_over else 'playing'
                    )
                    # Only include score in response for Snake for potential high score saving
                    if game.game_over and hasattr(game, 'score') and game_name == 'snake_ascii':
                        extra_response_data['score'] = game.score
            else:
                output = "Invalid command for this game."
                game_state_for_frontend = 'error'

        # Save updated game state to session
        if hasattr(game, 'to_dict'):
            games_data[game_name] = game.to_dict()
            request.session[SESSION_GAMES_KEY] = games_data
            request.session.modified = True

        response_data = {
            'output': output,
            'state': game_state_for_frontend,
            **extra_response_data
        }

        return JsonResponse(response_data)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)


def index(request):
    """
    Render the arcade homepage.
    """
    return render(request, 'arcade_app/index.html')


def get_high_scores(request):
    """
    Fetch top high scores for a specific game.
    This function remains generic but the frontend should only call it for Snake.
    """
    game_name = request.GET.get('game_name')
    limit = int(request.GET.get('limit', 10))

    if not game_name:
        return JsonResponse({'error': 'Missing game_name parameter'}, status=400)

    scores = (
        HighScore.objects
        .filter(game_name=game_name)
        .order_by('-score')[:limit]
    )

    data = {
        'high_scores': [
            {
                'initials': score.player_name or '---',
                'score': score.score,
                'achieved_at': score.achieved_at.isoformat()
            }
            for score in scores
        ]
    }
    return JsonResponse(data)


@csrf_exempt
def save_high_score(request):
    """
    Save a new high score entry.
    Modified to ONLY save high scores for 'snake_ascii'.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)
        game_name = data.get('game_name')
        player_name = data.get('initials', 'Anonymous')
        score = data.get('score')

        # Only save high scores for Snake
        if game_name != 'snake_ascii':
            return JsonResponse({'status': 'ignored', 'message': 'High score saving is only enabled for Snake.'})

        if not game_name or score is None:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        HighScore.objects.create(
            game_name=game_name,
            player_name=player_name,
            score=score
        )

        return JsonResponse({'status': 'success'})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
