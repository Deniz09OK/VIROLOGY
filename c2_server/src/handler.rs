use crate::state::AppState;
use shared::protocol::{ServerResponse, Task, TaskResult};

pub fn checkin(state: &AppState, agent_id: &str) -> ServerResponse {
    let mut agents = state.0.agents.lock().unwrap();
    let session = agents.entry(agent_id.to_string()).or_insert_with(|| {
        crate::state::AgentSession {
            id: agent_id.to_string(),
            pending_tasks: Vec::new(),
            results: Vec::new(),
        }
    });
    let tasks: Vec<Task> = session.pending_tasks.drain(..).collect();
    ServerResponse { tasks }
}

pub fn store_result(state: &AppState, result: TaskResult) {
    let mut agents = state.0.agents.lock().unwrap();
    if let Some(session) = agents.get_mut(&result.agent_id) {
        session.results.push(result);
    }
}

pub fn queue_task(state: &AppState, agent_id: &str, task: Task) -> bool {
    let mut agents = state.0.agents.lock().unwrap();
    if let Some(session) = agents.get_mut(agent_id) {
        session.pending_tasks.push(task);
        true
    } else {
        false
    }
}

pub fn list_agents(state: &AppState) -> Vec<String> {
    state.0.agents.lock().unwrap().keys().cloned().collect()
}
