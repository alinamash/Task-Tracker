#TODO: Task tracker
made by mash

Before using this application move the todo.bat file to your "C:\Windows\" folder

Adding a new task
usage: todo add [-h] [--description DESCRIPTION] [--status {todo, in_progress, done}] title (todo add [-h] shows this massage)
todo add "Buy groceries" --description "Buy: milk, sugar, bread" --status in_progress (default is todo)

Updating a  task
usage: Todo notes update [-h] [--title TITLE] [--description DESCRIPTION] [--status {todo,in_progress,done}] number
todo update --description "Buy: milk, sugar, bread, potato and chicken" 1

Deleting a task
usage: Todo notes remove [-h] number
todo remove 1 (removes a first task in the list)

Marking a task as in progress or done
to mark as in progress: todo update --status in_progress 1
to mark as done: todo done mark-done 1

Listing all tasks
usage: todo show [-h] [--all] [--todo] [--in-progress] [--done]
