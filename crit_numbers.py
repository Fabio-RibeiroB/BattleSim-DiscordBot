import random
from typing import List
import json
import re

def critical_hit_numbers(n: int) -> List:
    """Generate n critical hit numbers at random"""
    if n == 1: return random.randint(1,10)
    else: return [random.randint(1,10) for i in range(n)]

def training(Player: str) -> None:
    """Increase crit hit number score by random amount"""
    boost = critical_hit_numbers(1)

    with open('battle_data.json', 'r') as f:
        stats = json.load(f)
    
    stats[Player]['CritNumber']+=boost
    
    with open('battle_data.json', 'w') as f:
            json.dump(stats, f)


def find_victor(text: str) -> bool:
    pattern = r':\s*([^\s]+)'
    match = re.search(pattern, text)
    if match:
        return match.group(1).rstrip('.')
    else:
        return None