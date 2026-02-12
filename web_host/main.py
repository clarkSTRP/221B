from tools.container_controller import ContainerController

def main():
    cfg = {
        "image_name": "sherlock_image",
        "container_name": "sherlock_container",
        "dockerfile_dir": "tools/sherlock",
        "dockerfile_name": "Dockerfile",
    }

    username = "lumaleen"
    # Define the command to be executed inside the container.
    # For many command-line tools, options come before positional arguments.
    # The output file path must be inside the mounted volume, which is at '/data'.
    command_to_run = ["--output", f"/data/{username}.json", username]

    controller = ContainerController()

    controller.build_image(
        cfg["dockerfile_dir"],
        cfg["image_name"],
        cfg["dockerfile_name"]
    )

    container = controller.run_container(
        cfg["image_name"],
        cfg["container_name"],
        command_to_run
    )

    container.wait()
    print(container.logs().decode(errors="replace"))

if __name__ == "__main__":
    main()
