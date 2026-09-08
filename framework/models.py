from dataclasses import dataclass
from typing import Optional

@dataclass
class NetworkConfig:
    name: str
    rtt_ms: int
    loss_rate: float
    trace_file: Optional[str] = None

@dataclass
class ProfileConfig:
    profile_id: str
    gender: str
    age: int
    state: str
    area_type: str
    category: str

@dataclass
class ExperimentConfig:
    experiment_id: str
    portal: str
    workflow: str
    iterations: int
    network: NetworkConfig
    profile: ProfileConfig