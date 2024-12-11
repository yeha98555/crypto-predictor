from typing import Any, Dict

from loguru import logger
from quixstreams import State


def update_candles(
    candle: Dict[str, Any], state: State, max_candles_in_state: int
) -> Dict[str, Any]:
    """
    Update the list of candles with the latest candle.
    If the lastest candle corresponds to a new window, and the total number of candles in the state is less than the number of candles we want to keep, we just append it to the list.
    If it corresponds to the last window, we replace the last candle in the list.

    Args:
        candle (Dict[str, Any]): The latest candle.
        state (State): The state of the streaming application.
        max_candles_in_state (int): The maximum number of candles we want to keep in the state.

    Returns:
        None
    """
    # Get the list of candles from our state
    candles = state.get('candles', default=[])

    if not candles:
        candles.append(candle)
    # If it corresponds to the last window, we replace the last candle in the list
    elif is_same_window(candle, candles[-1]):
        candles[-1] = candle
    # If the lastest candle corresponds to a new window, we just append it to the list
    else:
        candles.append(candle)

    # If the total number of candles in the state is greater than the number of
    # candles we want to keep, we remove the oldest candle
    if len(candles) > max_candles_in_state:
        candles.pop(0)

    # TODO: we should check the candles have no missing windows
    # This can happen for low volume pairs. In this case, we could interpolate the missing windows.

    logger.debug(f'Number of candles in state: {len(candles)}')

    # Update the state with the new list of candles
    state.set('candles', candles)

    return candle


def is_same_window(candle_1: Dict[str, Any], candle_2: Dict[str, Any]) -> bool:
    """
    Check if the current candle is in the same window as the last candle.

    Args:
        candle_1 (Dict[str, Any]): The current candle.
        candle_2 (Dict[str, Any]): The last candle.

    Returns:
        bool: True if the two candles are in the same window, False otherwise.
    """
    return (
        candle_1['window_start_ms'] == candle_2['window_start_ms']
        and candle_1['window_end_ms'] == candle_2['window_end_ms']
    )
