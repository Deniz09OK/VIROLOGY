use shared::protocol::{Task, TaskResult};
use std::collections::HashMap;
use std::sync::{Arc, Mutex};

#[derive(Clone)]
pub struct AppState(pub Arc<Inner>);

pub struct Inner {
    pub agents: Mutex<HashMap<String, AgentSession>>,
}

pub struct AgentSession {
    pub id: String,
    pub pending_tasks: Vec<Task>,
    pub results: Vec<TaskResult>,
}

impl AppState {
    pub fn new() -> Self {
        Self(Arc::new(Inner {
            agents: Mutex::new(HashMap::new()),
        }))
    }
}

impl Default for AppState {
    fn default() -> Self {
        Self::new()
    }
}
