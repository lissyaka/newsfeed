# News Feed

## How to run
  1. Install and setup docker
  2. Run `docker-compose build prepare_elastic ; docker-compose run prepare_elastic` to be sure that elastic is running, configured and seeded with data before starting application;
  3. Run `docker-compose up --build` to run application;
  4. Go to `{docker-machine-ip}:8888`
