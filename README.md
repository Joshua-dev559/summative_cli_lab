# Project Management CLI Tool

A python command-line interface for managing users, projects and tasks.

## Setup

```bash
git clone <your-repo-url>
```
## CLI Commands 

All commands run using `python main.py <command>`

### Users

`add-user <name> <email>` Create a new user

### Projects

`add-project <user_id> <title> [-d desc] [-D due_date]` Add a project to a user 
`list-projects [--user-id <id>]` List all projects
`search-projects <keyword>` Search projects by title

### Tasks

`add-task <project_id> <title> [-a assignee]` Add a task to a project 
`list-tasks [--project-id <id>]` List all tasks
`completed-task <task_id>` Mark a task as completed
`update-task <task_id> <status>` Set status: pending, in-progress, completed

## Running Tests

```bash
pytest tests/ -v
```
## Features

- Object Oriented Programming with inheritance, properties, and encapsulation
- One-to-many relationships
- Rich pretty-printed tables with color-coded task statuses
- Search projects by title
- Input validation





