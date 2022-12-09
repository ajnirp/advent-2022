use std::cmp::max;
use std::collections::HashSet;
use util::read_lines;

fn process_line(s: &str) -> Vec<u32> {
    s.chars().map(|c| c.to_digit(10).unwrap()).collect()
}

fn update_seen(coords: &(usize, usize), count: &mut u32, seen: &mut HashSet<(usize, usize)>) {
    if !seen.contains(coords) {
        *count += 1;
        seen.insert(*coords);
    }
}

fn count_visible(grid: &Vec<Vec<u32>>) -> u32 {
    let (r, c) = (grid.len(), grid[0].len());
    let mut result = 2*(r + c - 2) as u32;
    let mut seen: HashSet<(usize, usize)> = HashSet::new();

    for ri in 1..(r-1) {
        // go right
        let mut max_so_far = grid[ri][0];
        for cj in 1..(c-1) {
            if grid[ri][cj] > max_so_far {
                update_seen(&(ri, cj), &mut result, &mut seen);
                max_so_far = grid[ri][cj];
            }
        }

        // go left
        max_so_far = grid[ri][c-1];
        for cj in (1..(c-1)).rev() {
            if grid[ri][cj] > max_so_far {
                update_seen(&(ri, cj), &mut result, &mut seen);
                max_so_far = grid[ri][cj];
            }
        }
    }

    for cj in 1..(c-1) {
        // go down
        let mut max_so_far = grid[0][cj];
        for ri in 1..(r-1) {
            if grid[ri][cj] > max_so_far {
                update_seen(&(ri, cj), &mut result, &mut seen);
                max_so_far = grid[ri][cj];
            }
        }

        // go up
        let mut max_so_far = grid[r-1][cj];
        for ri in (1..(r-1)).rev() {
            if grid[ri][cj] > max_so_far {
                update_seen(&(ri, cj), &mut result, &mut seen);
                max_so_far = grid[ri][cj];
            }
        }
    }

    result
}

fn best_score(grid: &Vec<Vec<u32>>) -> u32 {
    let (r, c) = (grid.len(), grid[0].len());
    let mut result = 1u32;

    for ri in 1..(r-1) {
        for cj in 1..(c-1) {
            // go up
            let mut up = 0u32;
            for rk in (0..ri).rev() {
                up += 1;
                if grid[rk][cj] >= grid[ri][cj] {
                    break;
                }
            }

            // go down
            let mut down = 0u32;
            for rk in (ri+1)..r {
                down += 1;
                if grid[rk][cj] >= grid[ri][cj] {
                    break;
                }
            }

            // go left
            let mut left = 0u32;
            for ck in (0..cj).rev() {
                left += 1;
                if grid[ri][ck] >= grid[ri][cj] {
                    break;
                }
            }

            // go right
            let mut right = 0u32;
            for ck in (cj+1)..c {
                right += 1;
                if grid[ri][ck] >= grid[ri][cj] {
                    break;
                }
            }

            let score = up * down * left * right;
            result = max(result, score);
        }
    }

    result
}

fn main() {
    if let Ok(lines) = read_lines("8.txt") {
        let mut grid: Vec<Vec<u32>> = vec![];
        for line in lines {
            if let Ok(line_str) = line {
                grid.push(process_line(&line_str));
            }
        }
        println!("{}", count_visible(&grid));
        println!("{}", best_score(&grid));
    }
}
