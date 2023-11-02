use actix_web::{get, HttpRequest, HttpResponse, Responder};
use std::option::Option;

use super::types::ServerConfiguration;

pub async fn index(config: Option<&ServerConfiguration>) -> impl Responder {
    HttpResponse::Ok().body("Route working !")
}
