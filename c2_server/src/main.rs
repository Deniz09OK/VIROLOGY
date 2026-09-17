mod handler;
mod routes;
mod state;

#[tokio::main]
async fn main() {
    let state = state::AppState::new();
    let app = routes::router(state);
    let listener = tokio::net::TcpListener::bind("0.0.0.0:8443").await.unwrap();
    println!("[c2_server] listening on 0.0.0.0:8443");
    axum::serve(listener, app).await.unwrap();
}
