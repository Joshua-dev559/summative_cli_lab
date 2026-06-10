from rich.console import Console
from rich.table import Table

console = Console()

def print_users(users):
    if not users:
        console.print("[bold red]No users found.[/bold red]")
        return
    table = Table(title="Users")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Email", style="green")
    table.add_column("Projects", style="yellow")

    for user in users:
        table.add_row(
            str(user.id),
            user.name,
            user.email,
            str(len(user.projects))
        )

    console.print(table)
    
def print_projects(
projects):
    if not projects:
        console.print("[bold red]No projects found.[/bold red]")
        return
    table = Table(title="Projects")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Description", style="green")
    table.add_column("Owner ID", style="yellow")
    table.add_column("Tasks", style="blue")

    for project in projects:
        table.add_row(
            str(project.id),
            project.title,
            project.description,
            str(project.owner_id),
            str(len(project.tasks)) if project.tasks else "0"
        )

    console.print(table)
    
def print_tasks(
tasks):
    if not tasks:
        console.print("[bold red]No tasks found.[/bold red]")
        return
    
    table = Table(title="Tasks")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Description", style="green")
    table.add_column("Project ID", style="yellow")
    table.add_column("Status", style="blue")

    for task in tasks:
        table.add_row(
            str(task.id),
            task.title,
            task.description,
            str(task.project_id) if task.project_id else "None",
            task.status
        )

    console.print(table)
    
def error(message):
    console.print(f"[bold red]Error:[/bold red] {message}")
    
def success(message):
    console.print(f"[bold green]Success:[/bold green] {message}")
