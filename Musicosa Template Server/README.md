# Musicosa Template Server

**Author:** Juan Pablo García Plaza Pérez (@pablogpz)

# Description

This web server is a template editor and renderer for generating template images to be used by the Musicosa processing
pipeline.

- The web editors are available at:
    - Entry templates -> `/templates/editor`
    - Presentation templates -> `/presentations/editor`
- The endpoint for rendering templates is available at `/[templates|presentations]/[uuid]`.
    - Instead of using UUIDs, templates can be queried by ranking sequence at
      `/[templates|presentations]?q=[rankingSequence]`
    -

### Setup

See `.env.example` to provide the mandatory environment variables.

## License

This project is licensed under the MIT License. See the root `LICENSE` file for details.
