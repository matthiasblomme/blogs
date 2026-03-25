---
title: 'Sync Plex watch history to Trakt with PlexTraktSync in Docker'
description: How to run PlexTraktSync in Docker to sync Plex watch history, ratings, and collections to Trakt, including fixes for Google login and Docker networking issues.
date: 2026-03-24
author: Matthias Blomme
tags:
- docker
- plex
- trakt
- self-hosting
---

<!--MD_POST_META:START-->

<!--MD_POST_META:END-->


# Syncing Plex watch history to Trakt with PlexTraktSync in Docker

Want your Plex watch history in Trakt without paying for Plex Pass (I'm already paying for that, thanks, but you don't have to) or Trakt VIP? PlexTraktSync does exactly that, and it runs just fine in Docker.

I started setting this up while building an AI-powered recommendation service (in the form of a locally hosted MCP server) for my Plex library. Trakt integration was the obvious next step: more watch history, ratings, and metadata usually means better recommendations.

The setup looks straightforward until Plex login starts fighting you, especially when your account uses Google and the whole thing runs in containers. I ran into both, so this is the version that actually worked.


## What PlexTraktSync does

PlexTraktSync does a few useful things:
- Syncs watched status from Plex to Trakt
- Syncs ratings and collections
- Pushes Plex media info into your Trakt collection
- Syncs watchlists and liked Trakt lists back to Plex
- Can run in `watch` mode to scrobble (media-tracker jargon) in real time over a websocket

## Prerequisites

- A Plex server (duh)
- A [Trakt](https://trakt.tv) account (free)
- Docker and Docker Compose (a pretty basic requirement, if you follow my blogs)

## Step 1: Create a Trakt API app

1. Go to [https://trakt.tv/oauth/applications/new](https://trakt.tv/oauth/applications/new)
2. Give it a name, for example `PlexTraktSync`
3. Set the redirect URL to `urn:ietf:wg:oauth:2.0:oob`
4. Leave Javascript origins and Permissions blank
5. Save the app, then copy the **Client ID** and **Client Secret**

## Step 2: Create the Docker Compose file

Create a directory for PlexTraktSync and add a `docker-compose.yml` file:

```yaml
version: "2"
services:
  plextraktsync:
    image: ghcr.io/taxel/plextraktsync
    container_name: plextraktsync
    command: watch
    restart: unless-stopped
    volumes:
      - ./config:/app/config
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Amsterdam
```

The `watch` command keeps the container running, listens for Plex events, and scrobbles them to Trakt in real time. `restart: unless-stopped` makes sure it comes back after a reboot unless you stopped it yourself.
This setup keeps your Trakt watch state in sync with Plex, but it does not import your existing history yet. That part comes later. Let's first talk about the setup.

## Step 3: Authenticate with Trakt

Trakt uses device-based authentication, so this step needs to be interactive, meaning you have to enter some credentials:

```bash
docker compose run -it --rm plextraktsync trakt-login
```

It will ask for the Client ID and Client Secret from step 1, and will then provide you with an authentication URL and device code to confirm in your browser.

Use `trakt-login`, not `login`, unless you want to get dumped into the Plex login flow for no reason. I'm going through this in a specific order for a reason, so stay with me here.

## Step 4: Configure Plex (the Google OAuth workaround)

This is where things got a bit annoying.

The interactive `login` command expects a Plex username and password. That breaks when your Plex account uses Google, Apple, or another OAuth provider. Instead of logging in, it just loops with a `401 User could not be authenticated` error, making you doubt your email, username and password. Well, I say NO MORE!

The workaround is simple enough: grab your Plex token manually and write the config files yourself. Which, in my opinion, should be the default authentication anyway.

### Getting your Plex token

1. Open [Plex Web](https://app.plex.tv) and sign in with Google
2. Open any media item
3. Click the **...** menu, then **Get Info**, then **View XML**
4. Check the URL bar for `X-Plex-Token=xxxxxxxxxxxx` (it will be at the end of the URL)

Another option: open browser dev tools (`F12`) on `app.plex.tv`, go to the Network tab, and look for `X-Plex-Token` in a request header or URL parameter.

### Getting your server details

Once you have the token, query the Plex API to get your server URL, machine identifier, and related details:

```bash
curl -s \
  -H "X-Plex-Token: YOUR_TOKEN" \
  -H "X-Plex-Client-Identifier: plextraktsync" \
  -H "Accept: application/json" \
  "https://plex.tv/api/v2/resources?includeHttps=1" | python -m json.tool
```

This returns all available servers with their connection URLs, machine identifiers, and access tokens.

### Writing the config files

Create `config/servers.yml` with your server details:

```yaml
servers:
  default:
    token: YOUR_PLEX_TOKEN
    urls:
    - http://host.docker.internal:32400
    id: your-server-machine-identifier
    config: null
```

If you're wondering what host.docker.internal is doing there, good, that matters in the next step.

Update the `config/.env` with the retrieved data:

```env
# This is .env file for PlexTraktSync
PLEX_USERNAME=your_plex_username
TRAKT_USERNAME=your_trakt_username
PLEX_SERVER=default
PLEX_OWNER_TOKEN=
PLEX_ACCOUNT_TOKEN=YOUR_PLEX_TOKEN
```

## Step 5: Docker networking: use host.docker.internal

This one can take a while to figure out. Luckily, or not, I had already run into the exact same issue earlier when I switched some of my Docker containers from Dockerfiles to Compose, so I recognized the problem pretty quickly.

My Plex server was running on the same machine, but the container still couldn't reach it through the LAN IP (`192.168.1.x`). It also couldn't resolve the `plex.direct` hostnames Plex uses for its SSL setup, those lovely things like `192-168-1-50.xxxx.plex.direct`. And no, those `-` signs are not a mistake.

The fix was to use `host.docker.internal` instead of the host IP. Docker Desktop on Windows and macOS maps that hostname back to the host machine automatically. Depending on your machine and Docker networking setup, the direct IP _might_ work, but host.docker.internal is the safer bet.

```yaml
urls:
  - http://host.docker.internal:32400
```

Got a public Plex URL as well? Add it as a fallback:

```yaml
urls:
  - http://host.docker.internal:32400
  - https://your-public-plex-url:port
```

## Step 6: Run the initial sync and start watching

Remember when I mentioned the container would keep your watch status synced while you use Plex? This is the missing step to get your historic data into Trakt. 

First, run a one-time sync to push your existing Plex history into Trakt:

```bash
docker compose run --rm plextraktsync sync
```

If you'd rather sync a specific library instead of everything, use the `--library` flag:

```bash
docker compose run --rm plextraktsync sync --library "TV Shows"
```

You can also target a specific show or movie:

```bash
docker compose run --rm plextraktsync sync --show "Breaking Bad"
docker compose run --rm plextraktsync sync --movie "Inception"
```

Once the sync is done, the container exits and cleans itself up. The perfect crime. On a big library, this can take a while, think hours. Once that's done, start the long-running watcher we created before:

```bash
docker compose up -d
```

From there, the `watch` command sends new plays, ratings, and collection changes to Trakt as they happen. PlexTraktSync calls this "scrobbling", which is just tracker jargon for automatically sending what you're watching to a service like Trakt.

## Verifying it works

Check the container logs:

```bash
docker logs plextraktsync --tail 20
```

You should see something like this:

```text
INFO     Listening for events!
INFO     Server connected: Plex (version)
INFO     Websocket connected
```

That means PlexTraktSync is connected to your Plex server over websocket and is actively listening for playback events. If you see connection or timeout issues, check that the configured IP and service URLs are correct.

Now play something in Plex and check Trakt. If everything is working, it should show up there without you having to poke it any further.

## Wrapping this up

Once that works, you're done. PlexTraktSync keeps Plex and Trakt in sync. The container starts automatically after a reboot, and you no longer have to babysit the whole thing manually, which is exactly how this should have worked from the start.


## References

- [Trakt API applications](https://trakt.tv/oauth/applications/new)
- [Trakt](https://trakt.tv)
- [Plex Web](https://app.plex.tv)
- [Plex API resources endpoint](https://plex.tv/api/v2/resources?includeHttps=1)
- [PlexTraktSync](https://github.com/Taxel/PlexTraktSync)