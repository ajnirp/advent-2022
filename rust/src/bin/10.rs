use util::read_lines;

fn part1(data: &Vec<i32>) -> i32 {
    let checkpoint: [u32; 6] = [20, 60, 100, 140, 180, 220];
    let (mut result, mut idx, mut cycle, mut x) = (0i32, 0usize, 1u32, 1i32);
    for val in data {
        if idx == checkpoint.len() {
            return result;
        }
        if cycle == checkpoint[idx] {
            result += (checkpoint[idx] as i32) * x;
            idx += 1;
        }

        if *val == 0 {
            cycle += 1;
            continue;
        } else {
            if idx == checkpoint.len() {
                return result;
            }
            if cycle + 2 > checkpoint[idx] {
                result += (checkpoint[idx] as i32) * x;
                idx += 1;
            }
            cycle += 2;
            x += val;
        }
    }
    result
}

fn part2(data: &Vec<i32>) {
    fn update(cycle: u32, x: i32, crt: &mut [[char; 40]; 6]) {
        let pos = cycle - 1;
        let row = pos / 40u32;
        let col = pos % 40u32;
        if ((col as i32) - x).abs() <= 1 {
            crt[row as usize][col as usize] = '#';
        }
    }
    let (mut cycle, mut x) = (1u32, 1i32);
    let mut crt: [[char; 40]; 6] = [['.'; 40]; 6];
    for val in data {
        if *val == 0 {
            update(cycle, x, &mut crt);
            cycle += 1;
        } else {
            for _ in 0..2 {
                update(cycle, x, &mut crt);
                cycle += 1;
            }
            x += val;
        }
    }
    for r in 0..6 {
        for c in 0..40 {
            print!("{}", crt[r][c]);
        }
        println!("");
    }
}

fn main() {
    if let Ok(lines) = read_lines("10.txt") {
        let mut data: Vec<i32> = Vec::new(); // use 0 to represent noop
        for line in lines {
            if let Ok(line_str) = line {
                if line_str.chars().next() == Some('n') {
                    data.push(0);
                } else {
                    let val: i32 = line_str.split(' ').last().unwrap().parse().unwrap();
                    data.push(val);
                }
            }
        }
        println!("{}", part1(&data));
        part2(&data);
    }
}
