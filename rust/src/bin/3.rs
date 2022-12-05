use util::read_lines;

fn priority(c: char) -> u8 {
    let byte = c as u8;
    if ('a' as u8) <= byte && byte <= ('z' as u8) {
        return byte - ('a' as u8) + 1;
    }
    byte - ('A' as u8) + 27
}

fn common2(s1: &str, s2: &str) -> Option<char> {
    s1.chars().find(|&c| s2.contains(c))
}

fn common3(s1: &str, s2: &str, s3: &str) -> Option<char> {
    s1.chars().find(|&c| s2.contains(c) && s3.contains(c))
}

fn part_1(data: &Vec<String>) -> u32 {
    let mut result = 0u32;
    for line in data {
        let mid = line.len() / 2;
        if let Some(c) = common2(&line[..mid], &line[mid..]) {
            result += priority(c) as u32;
        }
    }
    result
}

fn part_2(data: &Vec<String>) -> u32 {
    let mut result = 0u32;
    let mut i = 0usize;
    while i < data.len() {
        if let Some(c) = common3(&data[i], &data[i + 1], &data[i + 2]) {
            result += priority(c) as u32;
        }
        i += 3;
    }
    result
}

fn main() {
    let mut data = Vec::<String>::new();
    if let Ok(lines) = read_lines("3.txt") {
        for line in lines {
            if let Ok(line_str) = line {
                data.push(line_str);
            }
        }
    }

    println!("{}", part_1(&data));
    println!("{}", part_2(&data));
}
