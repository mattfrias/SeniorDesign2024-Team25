import argparse
import subprocess
from string import Template


def apply(args):
    filename = args.name
    if args.num != None: # Check if the number of resources is specified
        num_resources = args.num_resources
    else:
        num_resources = 1

    with open(filename) as f: # Read the resource file
        template = Template(f.read())
        
    try:
        for i in range(1, num_resources + 1):
            cmd_args = ["kubectl", "apply"]
            cmd_args.extend(["-f", "-"])
            subprocess.run(cmd_args, input=template.substitute(id=i).encode(), check=True) # Apply the resource
    except subprocess.CalledProcessError:
        print(f"Failed to apply resource from file '{filename}'.")


def cluster(args):
    cluster_action = args.action
    cluster_name = args.name
    if cluster_action == "create":
        try:
            subprocess.run(["kwokctl", "create", "cluster", "--name", cluster_name], check=True) # Create a cluster
            print(f"Cluster '{cluster_name}' created successfully.")
        except subprocess.CalledProcessError:
            print(f"Failed to create cluster '{cluster_name}'.")
    elif cluster_action == "delete":
        try:
            subprocess.run(["kwokctl", "delete", "cluster", "--name", cluster_name], check=True) # Delete a cluster
            print(f"Cluster '{cluster_name}' deleted successfully.")
        except subprocess.CalledProcessError:
            print(f"Failed to delete cluster '{cluster_name}'.") 


def delete(args):
    resource_type = args.type
    resource_name = args.name
    try:
        subprocess.run(["kubectl", "delete", resource_type, resource_name], check=True) # Delete the resource
        print(f"Deleted {resource_type} '{resource_name}' successfully.")
    except subprocess.CalledProcessError:
        print(f"Failed to delete {resource_type} '{resource_name}'.")


def get(args):
    resource_type = args.type
    try:
        subprocess.run(["kubectl", "get", resource_type], check=True) # Get the resource
    except subprocess.CalledProcessError:
        print(f"Failed to execute 'kubectl get {resource_type}'.")


def show(args):
    resource = args.resource
    try:
        if resource == "nodes":
            cmd = "kubectl describe nodes | awk '/Allocated resources:/,/ephemeral-storage/ {print}'"
            subprocess.run(cmd, shell=True) # Show node allocated resources
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
            ) # See what priority classes are assigned to pods
        elif resource == "pods":
            subprocess.run(
                [
                    "kubectl",
                    "get",
                    "pods",
                    "--output=custom-columns=NAMESPACE:.metadata.namespace,NAME:.metadata.name,CPU-REQUEST:.spec.containers[].resources.requests.cpu,CPU-LIMIT:.spec.containers[].resources.limits.cpu,MEMORY-REQUEST:.spec.containers[].resources.requests.memory,MEMORY-LIMIT:.spec.containers[].resources.limits.memory,AGE:.metadata.creationTimestamp",
                ]
            ) # Show pod requests and limits
    except subprocess.CalledProcessError:
        if resource == "nodes":
            print("Failed to show node allocated resources.")
        elif resource == "priority":
            print("Failed to get pod priority classes.")
        elif resource == "pods":
            print("Failed to show pod characteristics.")


def main():
    parser = argparse.ArgumentParser(description="Script to setup resources in Kubernetes WithOut Kubelet (KWOK)") # Initialize the command line tool
    subparsers = parser.add_subparsers(title="Available Commands") # Initialize subparsers for different commands

    apply_parser = subparsers.add_parser("apply", help="Apply specified resource") # Add the apply command
    apply_parser.add_argument("name", help="Filename") # Add the filename argument
    apply_parser.add_argument("--num", type=int, help="Number of resources to deploy (optional)") # Add the optional number of resources argument
    apply_parser.set_defaults(func=apply) # Set the function to apply

    cluster_parser = subparsers.add_parser("cluster", help="Cluster management (create/delete)") # Add the cluster command
    cluster_parser.add_argument("action", choices=["create", "delete"], help="Cluster Action") # Add the action argument
    cluster_parser.add_argument("name", help="Cluster Name") # Add the cluster name argument
    cluster_parser.set_defaults(func=cluster) # Set the function to cluster

    delete_parser = subparsers.add_parser("delete", help="Delete specified resource") # Add the delete command
    delete_parser.add_argument("type", help="Resource Type") # Add the resource type argument
    delete_parser.add_argument("name", help="Resource Name") # Add the resource name argument
    delete_parser.set_defaults(func=delete)  # Set the function to delete

    get_parser = subparsers.add_parser("get", help="Get specified resource") # Add the get command
    get_parser.add_argument("type", help="resource type") # Add the resource type argument
    get_parser.set_defaults(func=get) # Set the function to get

    show_parser = subparsers.add_parser("show", help="Show pod characteristics") # Add the show command
    show_parser.add_argument("resource", choices=["nodes", "priority", "pods"]) # Add the resource argument
    show_parser.set_defaults(func=show) # Set the function to show

    args = parser.parse_args() # Parse the arguments
    if hasattr(args, "func"): # Check if the function is defined
        args.func(args) # Execute the function
    else:
        parser.print_help() # Print the help message if the function is not defined


if __name__ == "__main__":
    main()
