use axum::{
    extract::State,
    routing::{get, post},
    Json, Router,
};
use serde::{Deserialize, Serialize};
use shared::protocol::{CheckIn, ServerResponse, Task, TaskResult};

use crate::state::AppState;

pub fn router(state: AppState) -> Router {
    Router::new()
        .route("/beacon", post(post_beacon))
        .route("/result", post(post_result))
        .route("/task", post(post_task))
        .route("/agents", get(get_agents))
        .with_state(state)
}

async fn post_beacon(
    State(state): State<AppState>,
    Json(body): Json<CheckIn>,
) -> Json<ServerResponse> {
    Json(crate::handler::checkin(&state, &body.agent_id))
}

async fn post_result(State(state): State<AppState>, Json(body): Json<TaskResult>) {
    crate::handler::store_result(&state, body);
}

#[derive(Deserialize)]
struct QueueTaskBody {
    id: String,
    task: Task,
}

#[derive(Serialize)]
struct StatusResponse {
    ok: bool,
}

async fn post_task(
    State(state): State<AppState>,
    Json(body): Json<QueueTaskBody>,
) -> Json<StatusResponse> {
    let ok = crate::handler::queue_task(&state, &body.id, body.task);
    Json(StatusResponse { ok })
}

async fn get_agents(State(state): State<AppState>) -> Json<Vec<String>> {
    Json(crate::handler::list_agents(&state))
}
