// This one compiled with --release is so much faster than the python version,
// of which it is a direct translation!

use std::collections::HashSet;
use util::read_lines;

type Position = (i32, i32);
type State = Vec<Position>;

fn parse_instruction(instruction: &str) -> (char, i32) {
    let num_steps: i32 = instruction.split(' ').last().unwrap().parse().unwrap();
    let direction = instruction.chars().next().unwrap();
    return (direction, num_steps);
}

fn init_state(num_knots: usize) -> State {
    let mut state: State = Vec::with_capacity(num_knots);
    for _ in 0..num_knots {
        state.push((0, 0));
    }
    state
}

fn move_head(direction: char, state: &mut State) {
    let (mut x, mut y) = state[0];
    if direction == 'R' {
        x += 1;
    } else if direction == 'L' {
        x -= 1;
    } else if direction == 'U' {
        y += 1;
    } else if direction == 'D' {
        y -= 1;
    }
    state[0] = (x, y);
}

fn adjacent(a: &Position, b: &Position) -> bool {
    if a.0 == b.0 && (a.1 - b.1).abs() <= 1 {
        true // horizontal
    } else if a.1 == b.1 && (a.0 - b.0).abs() <= 1 {
        true // vertical
    } else {
        (a.0 - b.0).abs() == 1 && (a.1 - b.1).abs() == 1 // diagonal
    }
}

fn manhattan(a: &Position, b: &Position) -> u32 {
    let (x1, y1) = a;
    let (x2, y2) = b;
    let result = (x1 - x2).abs() + (y1 - y2).abs();
    result as u32
}

fn move_knot(state: &mut State, idx: usize) {
    if adjacent(&state[idx], &state[idx - 1]) {
        return;
    }

    let leader = state[idx - 1];
    let follower = &mut state[idx];

    let mut best = (0i32, 0i32);
    let mut best_score = 3u32;
    for dx in -1..2 {
        for dy in -1..2 {
            if dx == 0 && dy == 0 {
                continue;
            }
            let candidate = (follower.0 + dx, follower.1 + dy);
            let score = manhattan(&candidate, &leader);
            if score < best_score {
                best = candidate;
                best_score = score;
            }
        }
    }

    *follower = best;
}

fn do_move(direction: char, state: &mut State) {
    move_head(direction, state);
    let num_knots = state.len();
    for i in 1..num_knots {
        move_knot(state, i);
    }
}

fn do_instruction(
    direction: char,
    num_steps: i32,
    state: &mut State,
    seen: &mut HashSet<Position>,
) {
    for _ in 0..num_steps {
        do_move(direction, state);
        seen.insert(*state.last().unwrap());
    }
}

fn solve(instructions: &[String], num_knots: usize) -> usize {
    let mut state = init_state(num_knots);
    let mut seen: HashSet<Position> = HashSet::new();
    for instruction in instructions {
        let (direction, num_steps) = parse_instruction(&instruction);
        do_instruction(direction, num_steps, &mut state, &mut seen);
    }
    seen.len()
}

fn main() {
    if let Ok(lines) = read_lines("9.txt") {
        let mut instructions: Vec<String> = Vec::new();
        for line in lines {
            if let Ok(move_) = line {
                instructions.push(move_);
            }
        }
        println!("{}", solve(&instructions, 2));
        println!("{}", solve(&instructions, 10));
    }
}
