if [ ! -d "myenv" ]; then
    python -m venv myenv
    powershell -Command "$policy = Get-ExecutionPolicy -Scope Process; if ($policy -ne 'Bypass') { Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force }"
    echo "Installing dependencies..."
    myenv/bin/pip install -r requirements.txt

fi

echo "Downloaded necessary dependencies."
echo "Loading..."
myenv/bin/python -m src.file_parser.py