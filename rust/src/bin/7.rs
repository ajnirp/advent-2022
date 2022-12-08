use std::collections::HashMap;
use util::read_lines;

fn update_sizes(size: u32, cwd: &Vec<String>, sizes: &mut HashMap<String, u32>) {
    let path = cwd.join("/");
    sizes.entry(path).and_modify(|s| *s += size).or_insert(size);
    for i in 0..cwd.len() {
        let ancestor = (&cwd[0..i]).join("/");
        sizes.entry(ancestor).and_modify(|s| *s += size).or_insert(size);
    }
}

fn main() {
    if let Ok(lines) = read_lines("7.txt") {
        let mut cwd = Vec::<String>::new();
        let mut sizes = HashMap::<String, u32>::new();
        for line in lines {
            if let Ok(line_str) = line {
                let chars: Vec<char> = line_str.chars().collect();
                // Skip dir lines. Skip ls lines. Store every dir size in a map. When you see a
                // file, update size for its parent dir as well as each ancestor.
                if chars[0] == '$' && chars[2] == 'c' {
                    let dst = line_str.split(' ').last().unwrap();
                    if dst == "/" {
                        cwd.clear();
                    } else if dst == ".." {
                        cwd.pop();
                    } else {
                        cwd.push(dst.to_string());   
                    }
                } else if chars[0].is_numeric() {
                    let size = line_str.split(' ').next().unwrap().parse::<u32>().unwrap();
                    update_sizes(size, &cwd, &mut sizes);
                }
            }
        }
        let cutoff = 100_000u32;
        let total_available = 70_000_000u32;
        let unused_required = 30_000_000u32;

        println!("{}", sizes.values().filter(|&v| v < &cutoff).sum::<u32>());
        let space_to_free = sizes.get("").unwrap() + unused_required - total_available;
        println!("{}", *sizes.values().filter(|&v| v > &space_to_free).min().unwrap());
    }    
}