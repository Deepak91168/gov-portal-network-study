import yaml
from pathlib import Path
from .models import NetworkConfig, ProfileConfig, ExperimentConfig

class ConfigLoader:
    def __init__(self, base_dir: str = "config"):
        self.base_dir = Path(base_dir)

    def _load_yaml(self, file_path: Path) -> dict:
        if not file_path.exists():
            raise FileNotFoundError(f"Missing config file: {file_path}")
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)

    def load_experiment(self, experiment_name: str) -> ExperimentConfig:
        exp_path = self.base_dir / "experiments" / f"{experiment_name}.yaml"
        raw_exp = self._load_yaml(exp_path)

        # Load referenced sub-configs
        net_path = self.base_dir / "networks" / f"{raw_exp['network_ref']}.yaml"
        prof_path = self.base_dir / "profiles" / f"{raw_exp['profile_ref']}.yaml"
        
        network = NetworkConfig(**self._load_yaml(net_path))
        profile = ProfileConfig(**self._load_yaml(prof_path))

        return ExperimentConfig(
            experiment_id=raw_exp['experiment_id'],
            portal=raw_exp['portal'],
            workflow=raw_exp['workflow'],
            iterations=raw_exp.get('iterations', 1),
            network=network,
            profile=profile
        )