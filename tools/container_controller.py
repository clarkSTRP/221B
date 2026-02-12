import docker
from pathlib import Path
from typing import List, Optional

class ContainerController:
    def __init__(self):
        self.client = docker.from_env()
        self.output_dir = Path("results")
        self._ensure_output_dir()

    def _ensure_output_dir(self):
        if not self.output_dir.exists():
            print("[*] Creating results directory...")
            self.output_dir.mkdir(parents=True)
        else:
            print("[*] Results directory exists.")

    def build_image(self, dockerfile_dir, image_name, dockerfile_name="Dockerfile"):
        self.client.images.build(
            path=dockerfile_dir,
            dockerfile=dockerfile_name,
            tag=image_name,
            rm=True
        )

    def run_container(self, image_name: str, container_name: str, command: Optional[List[str]] = None):
        # Ensure no container with the same name is already running or stopped.
        try:
            existing_container = self.client.containers.get(container_name)
            print(f"[*] Found and removing existing container '{container_name}'...")
            existing_container.remove(force=True)
        except docker.errors.NotFound:
            pass  # This is the expected case, no container found.

        return self.client.containers.run(
            image=image_name,
            name=container_name,
            detach=True,
            remove=True,
            command=command,
            volumes={
                str(self.output_dir.resolve()): {
                    "bind": "/data",
                    "mode": "rw"
                }
            }
        )
