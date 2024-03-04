# Coda

Coda is a simple bot for quickly grabbing clips for you Discord soundboard.  Pass it a YouTube link and it will attach the audio to its response. 

## Running Coda
Create a `.env` file and set `DISCORD_KEY=<your-secret-token>`

Build the container: `docker build -t coda:<version> .`

Run the container: `docker run --env-file .env coda:<version>`


