pub mod types;
pub mod website;

use self::types::ServerConfiguration;
use actix_web::{web, App, HttpServer};
use std::option::Option;

pub async fn main_loop(config: &ServerConfiguration) -> std::io::Result<()> {
    let index = || website::index(Option::Some(config));
    HttpServer::new(|| App::new().service(web::resource("/").route(web::get().to(index.clone()))))
        .bind("127.0.0.1:9090")?
        .run()
        .await
}
