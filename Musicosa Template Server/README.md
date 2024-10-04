# Musicosa Template Server
**Author:** Juan Pablo García Plaza Pérez (@pablogpz)

# Overview

This project serves as a Musicosa Template Model editor and renderer for automatic generation purposes

- The editor is available at `/templates/editor`
- The renderer endpoint is available at `/templates/[uuid]`. Alternative endpoint to query templates by 
ranking sequence available at `/templates?q=[rankingSequence]`
- An additional mock data generator endpoint is available at `/api/templates/seed-with-mock-data`

To improve response times it is recommended to run the build step and start the server in production to trigger SSG
of the available templates in Musicosa DB

### Environment
See `.env.example` to provide the mandatory env vars

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

© 2024 pablogpz