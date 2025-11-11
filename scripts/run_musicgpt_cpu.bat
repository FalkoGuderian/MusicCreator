@echo off
echo Starting MusicGPT Docker container (CPU mode)...
echo Pulling image if not present...
docker pull gabotechs/musicgpt

echo Running MusicGPT in CPU mode (slower but works without GPU)...
echo Access the UI at http://localhost:8642 after startup
docker run -it -p 8642:8642 -v %USERPROFILE%\.musicgpt:/root/.local/share/musicgpt gabotechs/musicgpt --ui-expose

echo MusicGPT container stopped.
pause
