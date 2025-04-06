// 0次在堆上分配内存的json parser
// 里面大概率有bug, 不过懒得改了, 主要是练习rust语法. 

use std::ops::Range;

enum JsonToken {
    LeftBrace,
    RightBrace,
    LeftBracket,
    RightBracket,
    Colon,
    Comma,
    String,
    Number,
    Null,
}

struct JsonIter<'a> {
    json: &'a str,
    idx: usize,
}

impl<'a> JsonIter<'a> {
    fn new(json: &'a str) -> Self {
        JsonIter { json, idx: 0 }
    }
}

impl<'a> Iterator for JsonIter<'a> {
    type Item = (Range<usize>, JsonToken);
    fn next(&mut self) -> Option<Self::Item> {
        if self.idx >= self.json.len() {
            return None;
        }
        let mut in_string = false;
        let mut in_number = false;
        let mut escape = false;
        let start = self.idx;
        let view = &self.json[self.idx..];
        for (i, chr) in view.char_indices() {
            let backup = self.idx;
            self.idx = start + i + 1;
            match (chr, in_string, in_number, escape) {
                (_, _, _, true) => escape = false,
                ('n', false, false, false) => {
                    // FIXME(moyi): check the value is null
                    self.idx += 4;
                    return Some((start..start + 4, JsonToken::Null));
                }
                ('{', false, false, false) => return Some((start..self.idx, JsonToken::LeftBrace)),
                ('}', false, false, false) => {
                    return Some((start..self.idx, JsonToken::RightBrace));
                }
                ('[', false, false, false) => {
                    return Some((start..self.idx, JsonToken::LeftBracket));
                }
                (':', false, false, false) => return Some((start..self.idx, JsonToken::Colon)),
                (']', false, false, false) => {
                    return Some((start..self.idx, JsonToken::RightBracket));
                }
                (',', false, false, false) => {
                    return Some((start..self.idx, JsonToken::Comma));
                }
                (' ' | '\t' | '\n', false, false, false) => {
                    // 直接跳过空格了
                    return self.next();
                }
                ('"', false, false, false) => in_string = true,
                ('"', true, false, false) => {
                    return Some((start..self.idx, JsonToken::String));
                }
                ('\\', true, false, false) => escape = true,
                (_, true, _, _) => continue,
                ('0'..='9', false, _, false) => in_number = true,
                ('.', false, true, false) => in_number = true,
                (_, false, true, false) => {
                    self.idx = backup;
                    return Some((start..self.idx, JsonToken::Number));
                }
                _ => panic!(),
            };
        }
        None
    }
}

fn to_json(json: &str) -> JsonType {
    JsonType::Map(JsonMap::new(json))
}

enum JsonType<'a> {
    Null,
    Int(i64),
    Float(f64),
    String(&'a str),
    Array(JsonArray<'a>),
    Map(JsonMap<'a>),
}

struct JsonArray<'a> {
    json_slice: &'a str,
    index: usize,
    depth: i32,
}

impl Clone for JsonArray<'_> {
    fn clone(&self) -> Self {
        JsonArray {
            json_slice: self.json_slice,
            index: self.index,
            depth: self.depth,
        }
    }
}

impl<'a> JsonArray<'a> {
    fn new(json_slice: &'a str) -> Self {
        JsonArray {
            json_slice,
            index: 0,
            depth: -1,
        }
    }
}

impl<'a> Iterator for JsonArray<'a> {
    type Item = JsonType<'a>;
    fn next(&mut self) -> Option<Self::Item> {
        let backup = self.index;
        let view = &self.json_slice[self.index..];
        let mut start = self.index;
        for (rg, token) in JsonIter::new(view) {
            self.index = backup + rg.end;
            match (self.depth, token) {
                (0, JsonToken::Null) => {
                    return Some(JsonType::Null);
                }
                (0, JsonToken::String) => {
                    let token_view = &view[rg];
                    return Some(JsonType::String(token_view));
                }
                (0, JsonToken::Number) => {
                    let token_view = &view[rg];
                    if let Ok(val) = token_view.parse::<i64>() {
                        return Some(JsonType::Int(val));
                    }
                    if let Ok(val) = token_view.parse::<f64>() {
                        return Some(JsonType::Float(val));
                    }
                }
                (0, JsonToken::RightBrace) => {
                    return None;
                }
                (1, JsonToken::RightBrace) => {
                    self.depth -= 1;
                    let token_view = &view[start..rg.end];
                    return Some(JsonType::Array(JsonArray::new(token_view)));
                }
                (1, JsonToken::RightBracket) => {
                    self.depth -= 1;
                    let token_view = &view[start..rg.end];
                    return Some(JsonType::Map(JsonMap::new(token_view)));
                }
                (0, JsonToken::LeftBracket | JsonToken::LeftBrace) => {
                    start = rg.start;
                    self.depth += 1;
                }
                (_, JsonToken::LeftBracket | JsonToken::LeftBrace) => {
                    self.depth += 1;
                }
                _ => continue,
            }
        }
        None
    }
}

struct JsonMap<'a> {
    json_slice: &'a str,
    index: usize,
    depth: i32,
}

impl Clone for JsonMap<'_> {
    fn clone(&self) -> Self {
        JsonMap {
            json_slice: self.json_slice,
            index: self.index,
            depth: self.depth,
        }
    }
}

impl<'a> JsonMap<'a> {
    fn new(json_slice: &'a str) -> Self {
        JsonMap {
            json_slice,
            index: 0,
            depth: -1,
        }
    }

    fn next_item(&mut self) -> Option<JsonType<'a>> {
        let backup = self.index;
        let view = &self.json_slice[self.index..];
        let mut start = self.index;
        for (rg, token) in JsonIter::new(view) {
            self.index = backup + rg.end;
            match (self.depth, token) {
                (0, JsonToken::String) => {
                    let token_view = &view[rg];
                    return Some(JsonType::String(token_view));
                }
                (0, JsonToken::Null) => {
                    return Some(JsonType::Null);
                }
                (0, JsonToken::Number) => {
                    let token_view = &view[rg];
                    if let Ok(val) = token_view.parse::<i64>() {
                        return Some(JsonType::Int(val));
                    }
                    if let Ok(val) = token_view.parse::<f64>() {
                        return Some(JsonType::Float(val));
                    }
                }
                (0, JsonToken::RightBrace) => {
                    return None;
                }
                (1, JsonToken::RightBrace) => {
                    self.depth -= 1;
                    let token_view = &view[start..rg.end];
                    return Some(JsonType::Array(JsonArray::new(token_view)));
                }
                (1, JsonToken::RightBracket) => {
                    self.depth -= 1;
                    let token_view = &view[start..rg.end];
                    return Some(JsonType::Map(JsonMap::new(token_view)));
                }
                (0, JsonToken::LeftBracket | JsonToken::LeftBrace) => {
                    start = rg.start;
                    self.depth += 1;
                }
                (_, JsonToken::LeftBracket | JsonToken::LeftBrace) => {
                    self.depth += 1;
                }
                _ => continue,
            }
        }
        None
    }
}

impl<'a> Iterator for JsonMap<'a> {
    type Item = (JsonType<'a>, JsonType<'a>); // key-value
    fn next(&mut self) -> Option<Self::Item> {
        let key = self.next_item()?;
        let value = self.next_item()?;
        Option::from((key, value))
    }
}

fn print_tree(json: &JsonType) {
    match json {
        JsonType::Null => {
            print!("null");
        }
        JsonType::Int(val) => {
            print!("{}", val);
        }
        JsonType::Float(val) => {
            print!("{}", val);
        }
        JsonType::String(val) => {
            print!("{}", val);
        }
        JsonType::Array(arr) => {
            print!("[");
            for ele in arr.clone() {
                print_tree(&ele);
                print!(",");
            }
            print!("]");
        }
        JsonType::Map(map) => {
            print!("{{");
            for (k, v) in map.clone() {
                print_tree(&k);
                print!(":");
                print_tree(&v);
                print!(",");
            }
            print!("}}");
        }
    }
}

fn main() {
    let json = r#"{"name":"John Doe","age":43,"phones":[null,"+44 2345678"]}"#;
    let map = to_json(json);
    print_tree(&map);
}
