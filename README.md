# Text Battle Simulator

A turn-based battle game where you face off against AI opponents. Battle through increasingly difficult enemies and build up your win streak!

## Features

- Turn-based combat system with 3 strategic moves:
  - Strike (deal your current attack power as damage)
  - Heal (recover HP equal to half your attack power)
  - Power Up (increase attack power by 50%)
- Win streak system that increases your stats
- Dynamic enemy scaling
- Intelligent CPU opponent that adapts to battle conditions

## How to Play

1. Run the game using Python: `python battle.py`
2. Each turn, choose your attack by entering:
   - `1` for Strike
   - `2` for Heal 
   - `3` for Power Up
3. The opponent will choose moves based on battle conditions
4. Win consecutive battles to increase your power
5. Battle continues until either you or your opponent reaches 0 HP

## Stats

- Player starts with 100 HP and 10 Attack
- Stats increase with each win
- Enemy stats scale with your win streak
- Each win increases base HP by 100 and Attack by 10

## Requirements

- Python 3.6 or higher
