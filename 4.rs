mod util;

use util::util::read_lines;

type Interval = (u32, u32);

fn parse_range(s: &str) -> Interval {
    let vec: Vec<&str> = s.split('-').collect();
    (
        vec[0].parse::<u32>().unwrap(),
        vec[1].parse::<u32>().unwrap(),
    )
}

// True iff [x1, y1] lies within [x2, y2]
// Overlaps permitted i.e. x1 == x2 and/or y1 == y2
fn strict_subset(r1: &Interval, r2: &Interval) -> bool {
    let (x1, y1) = r1;
    let (x2, y2) = r2;
    x2 <= x1 && y1 <= y2
}

// True iff r1 and r2 overlap
fn overlap(r1: &Interval, r2: &Interval) -> bool {
    let (x1, y1) = r1;
    let (x2, y2) = r2;
    (x2 <= x1 && x1 <= y2) || (x2 <= y1 && y1 <= y2) || strict_subset(r2, r1)
}

fn main() {
    if let Ok(lines) = read_lines("4.txt") {
        let (mut result_1, mut result_2) = (0u32, 0u32);
        for line in lines {
            if let Ok(line_str) = line {
                let vec: Vec<Interval> = line_str.split(',').map(parse_range).collect();
                let (r1, r2) = (&vec[0], &vec[1]);
                if strict_subset(r1, r2) || strict_subset(r2, r1) {
                    result_1 += 1;
                }
                if overlap(r1, r2) {
                    result_2 += 1;
                }
            }
        }
        println!("{} {}", result_1, result_2);
    }
}
