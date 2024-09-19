import subprocess
import os


def run_tailwind_watch():
    """
    Runs TailwindCSS in watch mode for automatic recompilation.
    """
    # Get the absolute path to the tailwindcss.exe
    tailwind_path = os.path.abspath('../tailwindcss.exe')

    input_file = os.path.abspath('static/css/input.css')
    output_file = os.path.abspath('static/css/output.css')

    command = [
        tailwind_path,
        '-i', input_file,
        '-o', output_file,
        '--watch'
    ]
    print('\nTailwindCSS watcher started :)')
    subprocess.Popen(command, cwd=os.path.abspath('../'))

# ./tailwindcss.exe -i project/static/css/input.css -o project/static/css/output.css --watch
