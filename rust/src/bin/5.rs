use lazy_static::lazy_static;
use regex::Regex;
use util::read_lines;

type Config = Vec<Vec<char>>;

// I could've hardcoded this to 9 and 8, but I wanted to write a more generic solution
struct ConfigParams {
    // number of stacks
    num_stacks: u32,

    // for the initial config, maximum length across all stacks
    initial_max_stack_length: usize,
}

// figure out how many stacks we have, and how many items the longest stack has
fn parse_data(data: &[String]) -> ConfigParams {
    let mut max_stack_length = 0usize;
    for line in data {
        if line.as_bytes()[0] == '[' as u8 {
            max_stack_length += 1;
        } else {
            let num_stacks = line
                .split_whitespace()
                .last()
                .unwrap()
                .parse::<u32>()
                .unwrap();
            return ConfigParams {
                num_stacks: num_stacks,
                initial_max_stack_length: max_stack_length,
            };
        }
    }
    panic!("Control shouldn't reach here")
}

// parse the config file data into a list of stacks
fn parse_config(data: &[String], params: &ConfigParams) -> Config {
    let num_stacks = params.num_stacks as usize;
    let mut result: Config = Vec::with_capacity(num_stacks);
    for _ in 0..num_stacks {
        result.push(vec![]);
    }
    for line in data {
        let mut i = 0usize;
        // I trim because I don't assume that the first stack has the most elements
        let bytes = line.trim().as_bytes();
        while i < bytes.len() {
            if bytes[i] == '[' as u8 {
                result[i / 4].push(bytes[i + 1] as char);
            }
            i += 4;
        }
    }
    for stack in &mut result {
        stack.reverse();
    }
    result
}

fn apply_instructions(instructions: &[String], config1: &mut Config, config2: &mut Config) {
    lazy_static! {
        static ref RE: Regex = Regex::new(r"\d+").unwrap();
    }

    for instruction in instructions {
        // parse the instruction
        let nums: Vec<u32> = RE
            .find_iter(instruction)
            .map(|d| d.as_str().parse::<u32>().unwrap())
            .collect();
        let (to_move, src, dst) = (nums[0], (nums[1] - 1) as usize, (nums[2] - 1) as usize);

        for _ in 0..to_move {
            let val = config1[src].pop().unwrap();
            config1[dst].push(val);
        }

        let mut temp_storage = Vec::<char>::new();
        for _ in 0..to_move {
            temp_storage.push(config2[src].pop().unwrap());
        }
        for _ in 0..to_move {
            config2[dst].push(temp_storage.pop().unwrap());
        }
    }
}

fn result(config: &Config) -> String {
    config.iter().map(|v| v.last().unwrap()).collect::<String>()
}

fn main() {
    let mut data = Vec::<String>::new();
    if let Ok(lines) = read_lines("5.txt") {
        for line in lines {
            if let Ok(line_str) = line {
                data.push(line_str);
            }
        }
    }

    let params = parse_data(&data);
    let num_lines_in_config = params.initial_max_stack_length;
    let mut config1 = parse_config(&data[..num_lines_in_config], &params);
    let mut config2 = parse_config(&data[..num_lines_in_config], &params);

    apply_instructions(
        &data[(num_lines_in_config + 2)..],
        &mut config1,
        &mut config2,
    );
    println!("{}", result(&config1));
    println!("{}", result(&config2));
}
