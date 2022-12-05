// Util fns for Advent of Code 2022 in Rust
use std::fs::File;
use std::io::{self, BufRead};

// https://doc.rust-lang.org/rust-by-example/std_misc/file/read_lines.html
pub fn read_lines(filename: &str) -> io::Result<io::Lines<io::BufReader<File>>>
{
    let mut relative_path: String = "./data/".to_owned();
    relative_path.push_str(filename);
    let file = File::open(relative_path)?;
    Ok(io::BufReader::new(file).lines())
}
