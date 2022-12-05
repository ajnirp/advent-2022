use std::collections::HashMap;
use util::read_lines;

fn main() {
    let first_col_map = HashMap::from([('A', 'R'), ('B', 'P'), ('C', 'S')]);
    let second_col_map = HashMap::from([('X', 'R'), ('Y', 'P'), ('Z', 'S')]);
    let value = HashMap::from([('R', 1), ('P', 2), ('S', 3)]);
    let defeats = HashMap::from([('R', 'S'), ('P', 'R'), ('S', 'P')]);
    let mut defeated_by = HashMap::<char, char>::new();
    for (k, v) in &defeats {
        defeated_by.insert(*v, *k);
    }

    if let Ok(lines) = read_lines("2.txt") {
        let mut score_1 = 0u32;
        let mut score_2 = 0u32;

        for line in lines {
            if let Ok(line_str) = line {
                let bytes = line_str.as_bytes();

                let first = bytes[0] as char;
                let second = bytes[bytes.len() - 1] as char;

                let them = first_col_map[&first];
                let me = second_col_map[&second];

                score_1 += value[&me];
                if me == them {
                    score_1 += 3
                } else if defeats[&me] == them {
                    score_1 += 6
                }

                if second == 'Y' {
                    score_2 += 3 + value[&them];
                } else if second == 'X' {
                    score_2 += value[&defeats[&them]];
                } else {
                    score_2 += 6 + value[&defeated_by[&them]];
                }
            }
        }

        println!("{} {}", score_1, score_2);
    }
}
