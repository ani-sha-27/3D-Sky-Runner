# 3D-Sky-Runner
A 3D endless runner flight simulator built with Python and OpenGL. Navigate a procedural urban landscape, collect golden rings for points, and avoid dynamic drones or buildings. Features multiple camera perspectives (1st, 2nd, and 3rd person), a life-based health system, local high-score tracking, and adaptive difficulty.
**Gameplay FeaturesInfinite World Generation:** Skyscrapers, golden rings, and clouds are dynamically spawned and recycled, ensuring the world never ends.Adaptive Difficulty:Speed Boost: Once you reach a score of 150, the plane_speed doubles from 1.0 to 2.0, making the game much harder.Drone Enemies: After hitting a score of 100, moving drones begin to spawn and patrol horizontally ($x = -15$ to $x = 15$) to block your path.Scoring & Health:Collect golden rings for 10 points each.You start with 3 lives. Colliding with buildings, drones, or the ground reduces your health until "Game Over".Dynamic Environments: Toggle the sun's visibility or change the cloud colors between white and stormy gray in real-time.
Key,Action
Arrow Keys,"Move Plane (Up, Down, Left, Right)"
Space,Start / Pause Game
R,Reset Game after Game Over
Z / X,Roll/Rotate the aircraft on the Z-axis
4 / 5,Toggle Gray Clouds / Toggle Sun Visibility
