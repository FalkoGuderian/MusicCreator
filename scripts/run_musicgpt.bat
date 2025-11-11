@echo off
echo Starting MusicGPT Docker container...
echo Pulling image if not present...
docker pull gabotechs/musicgpt

echo Running MusicGPT with GPU support...
echo Access the UI at http://localhost:8642 after startup
docker run -it --gpus all -p 8642:8642 -v %USERPROFILE%\.musicgpt:/root/.local/share/musicgpt gabotechs/musicgpt --gpu --ui-expose

echo MusicGPT container stopped.
pause
