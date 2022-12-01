use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn main() {
    if let Ok(lines) = read_lines("1.txt") {
        let mut elves: Vec<u32> = vec![];
        let mut current_elf = 0u32;
        for line in lines {
            if let Ok(val_str) = line {
                if val_str.is_empty() {
                    elves.push(current_elf);
                    current_elf = 0;
                } else {
                    current_elf += val_str.parse::<u32>().unwrap();
                }
            }
        }

        elves.sort();

        let part_1 = elves.last().unwrap();
        let mut part_2 = 0u32;
        for i in 1..4 {
            part_2 += elves[elves.len() - i];
        }
        println!("{} {}", part_1, part_2);
    }
}

// https://doc.rust-lang.org/rust-by-example/std_misc/file/read_lines.html
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
