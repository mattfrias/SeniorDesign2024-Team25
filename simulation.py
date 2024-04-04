import argparse
import subprocess
from string import Template


def apply(args):
    filename = args.name
    if args.num_resources != None:
        num_resources = args.num_resources
    else:
        num_resources = 1

    with open(filename) as f:
        template = Template(f.read())
    try:
        for i in range(1, num_resources + 1):
            cmd_args = ["kubectl", "apply"]
            cmd_args.extend(["-f", "-"])
            subprocess.run(
                cmd_args, input=template.substitute(id=i).encode(), check=True
            )
    except subprocess.CalledProcessError:
        print(f"Failed to apply resource from file '{filename}'.")


def cluster(args):
    cluster_action = args.action
    cluster_name = args.name
    if cluster_action == "create":
        try:
            subprocess.run(["kwokctl", "create", "cluster", "--name", cluster_name], check=True)
            print(f"Cluster '{cluster_name}' created successfully.")
        except subprocess.CalledProcessError:
            print(f"Failed to create cluster '{cluster_name}'.")
    elif cluster_action == "delete":
        try:
            subprocess.run(["kwokctl", "delete", "cluster", "--name", cluster_name], check=True)
            print(f"Cluster '{cluster_name}' deleted successfully.")
        except subprocess.CalledProcessError:
            print(f"Failed to delete cluster '{cluster_name}'.")


def delete(args):
    resource_type = args.type
    resource_name = args.name
    try:
        subprocess.run(["kubectl", "delete", resource_type, resource_name], check=True)
        print(f"Deleted {resource_type} '{resource_name}' successfully.")
    except subprocess.CalledProcessError:
        print(f"Failed to delete {resource_type} '{resource_name}'.")


def get(args):
    resource_type = args.type
    try:
        subprocess.run(["kubectl", "get", resource_type], check=True)
    except subprocess.CalledProcessError:
        print(f"Failed to execute 'kubectl get {resource_type}'.")


def show(args):
    resource = args.resource
    try:
        if resource == "nodes":
            cmd = "kubectl describe nodes | awk '/Allocated resources:/,/ephemeral-storage/ {print}'"
            subprocess.run(cmd, shell=True)
        elif resource == "priority":
            subprocess.run(
                [
                    "kubectl",
                    "get",
                    "pods",
                    "-n",
                    "default",
                    "-o",
                    "custom-columns=NAME:.metadata.name,PRIORITY:.spec.priorityClassName",
                ]
            )
        elif resource == "pods":
            subprocess.run(
                [
                    "kubectl",
                    "get",
                    "pods",
                    "--output=custom-columns=NAMESPACE:.metadata.namespace,NAME:.metadata.name,CPU-REQUEST:.spec.containers[].resources.requests.cpu,CPU-LIMIT:.spec.containers[].resources.limits.cpu,MEMORY-REQUEST:.spec.containers[].resources.requests.memory,MEMORY-LIMIT:.spec.containers[].resources.limits.memory,AGE:.metadata.creationTimestamp",
                ]
            )
    except subprocess.CalledProcessError:
        if resource == "nodes":
            print("Failed to show node allocated resources.")
        elif resource == "priority":
            print("Failed to get pod priority classes.")
        elif resource == "pods":
            print("Failed to show pod characteristics.")


def main():
    parser = argparse.ArgumentParser(description="Script to setup resources in Kubernetes WithOut Kubelet (KWOK)")
    subparsers = parser.add_subparsers(title="Available Commands")

    apply_parser = subparsers.add_parser("apply", help="Apply specified resource")
    apply_parser.add_argument("name", help="Filename")
    apply_parser.add_argument("--num", type=int, help="Number of resources to deploy (optional)")
    apply_parser.set_defaults(func=apply)

    cluster_parser = subparsers.add_parser("cluster", help="Cluster management (create/delete)")
    cluster_parser.add_argument("action", choices=["create", "delete"], help="Cluster Action")
    cluster_parser.add_argument("name", help="Cluster Name")
    cluster_parser.set_defaults(func=cluster)

    delete_parser = subparsers.add_parser("delete", help="Delete specified resource")
    delete_parser.add_argument("type", help="Resource Type")
    delete_parser.add_argument("name", help="Resource Name")
    delete_parser.set_defaults(func=delete)

    get_parser = subparsers.add_parser("get", help="Get specified resource")
    get_parser.add_argument("type", help="resource type")
    get_parser.set_defaults(func=get)

    show_parser = subparsers.add_parser("show", help="Show pod characteristics")
    show_parser.add_argument("resource", choices=["nodes", "priority", "pods"])
    show_parser.set_defaults(func=show)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
