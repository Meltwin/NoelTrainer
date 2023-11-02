mod api;
use api::types::ServerConfiguration;
use std::env;
use std::option::Option;

const WEBSITE_ARG: &str = "--website";

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let args: Vec<String> = env::args().collect();

    // Extract Informations
    let configuration = get_configuration(&args);

    api::main_loop(&configuration).await
}

// ----------------------------------------------------------------------------
// Server configurations loader
// ----------------------------------------------------------------------------

fn get_configuration(args: &Vec<String>) -> ServerConfiguration {
    return ServerConfiguration {
        website_location: get_argument(args, WEBSITE_ARG),
    };
}

fn get_argument(args: &Vec<String>, tag: &str) -> Option<String> {
    let mut next = false;
    for s in args {
        next = next || (s == tag);
        if next {
            return Option::Some(s.clone());
        }
    }
    return Option::None;
}
