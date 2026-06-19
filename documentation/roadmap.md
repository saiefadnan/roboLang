# roboLang Roadmap

You have successfully completed the core engine with a working Virtual Machine and collision detection! Here is the plan for the next evolution of roboLang.

## Phase 8: Control Flow (Loops & Conditionals)
- **Goal**: Allow robots to perform repeating tasks (e.g., patrolling) or reactive tasks.
- **Language**: `repeat(5) { ... }`, `if(collision) { ... }`.
- **VM Changes**: Add `JUMP` and `JUMP_IF_FALSE` opcodes.

## Phase 9: Variables & Math
- **Goal**: Support dynamic values and state management.
- **Language**: `let speed = 10`, `movX(speed + 5)`.
- **VM Changes**: Add a `stack` or `registers` for temporary storage.

## Phase 10: Real-time Sensors
- **Goal**: Moving from static `result()` to interactive `sense()`.
- **Logic**: Robots can "look ahead" before moving and change path based on detected objects.

## Phase 11: Subroutines (Functions)
- **Goal**: Reusable code blocks for common behaviors.
- **Language**: `def patrol() { ... }`.
