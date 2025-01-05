🟡Snake Game with Menu:-

A classic Snake Game implemented using Python and Pygame, enhanced with a menu system, sound effects, and smooth gameplay mechanics. This game features options to start a new game, resume a paused game, and quit.


🟡Features:-

Menu System: Start a new game, resume, or quit.

Dynamic Snake Movement: Smooth movement with speed increments as you score.

Animated Food: Food has a pulsating effect to grab your attention.

Sound Effects: Sounds for eating, game-over, button hover, and click events.

Pause Functionality: Pause and resume your game anytime.

High-Quality Graphics: Grid background, animated buttons, and snake details like eyes.


🟡Requirements:-

Python 3.8 or higher

Pygame library (```pip install pygame```)



🛠️ Installation and Setup Prerequisites:-

1)Clone the repository:

(```git clone https://github.com/your-username/snake-game.git
cd snake-game```)

2)Install dependencies:


```pip install pygame```

3)Place the required sound files in the sounds/ directory:

```eat.wav```
```game_over.wav```
```hover.wav```
```click.wav```


🟡How to Play:-

1)Run the game:

```python snake_game.py```

2)Menu Options:

Click New Game to start.

Click Resume Game to continue from where you paused.

Click Quit Game to exit.

3)In-Game Controls:

Arrow keys (```↑, ↓, ←, →```) to move.

Press ```ESC``` to pause.

4)Goal:

Navigate the snake to eat the red food and grow longer.

Avoid colliding with the snake's body or the edges of the game window.

🟡Screenshots:-
1)Main Menu

![Screenshot 2025-01-05 224416](https://github.com/user-attachments/assets/eba16c4f-cead-492e-8eee-43f0c6969335)


2)Gameplay

![running](https://github.com/user-attachments/assets/d35cd3d1-5a2e-4a64-b8c9-3ee2b6766483)


3)Game Paused

![Screenshot 2025-01-05 224705](https://github.com/user-attachments/assets/d032095a-dbd0-46cd-aa57-0bf4c5a4eaab)



🟡Customization:-

Background Grid: Modify the ```create_background``` method for different styles.

Snake Speed: Adjust ```INITIAL_SPEED``` and ```SPEED_INCREMENT``` in the ```SnakeGame``` class.

Food Animation: Customize the pulsating effect in the update method.


🟡Known Issues:-

None at the moment. Open an issue if you find any!

🟡Contributing:-

Contributions are welcome! Feel free to submit a pull request or create an issue for suggestions or bug reports.

🟡License:-

This project is licensed under the MIT License. See the LICENSE file for details.

