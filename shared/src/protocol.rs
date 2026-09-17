// C2 wire protocol — JSON over HTTPS — T1071.001

use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct CheckIn {
    pub agent_id: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Task {
    pub id: String,
    pub cmd: String,
    pub args: Vec<String>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct TaskResult {
    pub agent_id: String,
    pub task_id: String,
    pub output: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ServerResponse {
    pub tasks: Vec<Task>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct KeyExchange {
    pub agent_id: String,
    /// RSA-4096 public key PEM (agent → server on first contact)
    pub public_key_pem: String,
}
