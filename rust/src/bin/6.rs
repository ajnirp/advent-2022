use itertools::Itertools;
use std::fs;

fn find_first_index(data: &str, n: usize) -> usize {
    for i in (n - 1)..data.len() {
        let substr = &data[(i - n + 1)..(i + 1)];
        if substr.chars().unique().collect::<Vec<char>>().len() == n {
            return i + 1;
        }
    }
    panic!("Control shouldn't reach here");
}

fn main() {
    if let Ok(data) = fs::read_to_string("./data/6.txt") {
        println!("{}", find_first_index(&data, 4));
        println!("{}", find_first_index(&data, 14));
    }
}
