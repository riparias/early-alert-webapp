# Early-alert-webapp
The source code of the LIFE RIPARIAS early alert web application

This website is powered by [GBIF Alert](https://github.com/riparias/gbif-alert), therefore this repository contains
mostly configuration files, specific scripts and documentation for the LIFE RIPARIAS project.

## Websites

* [RIPARIAS early alert production website](https://alert.riparias.be)
* [Development / user-acceptance version](https://dev-alert.riparias.be)

## Configuration

The configuration files are located in the `config` directory. Please note that some configuration (species list),
static texts, ... are stored in the database and edited via the Django admin interface. Those parts are not included
in this repository.

## Area data (archive)

The public areas of the RIPARIAS instance (Belgian municipalities/provinces/regions, Flemish and Walloon river
basins, Natura2000, DVW districts/sectors, RIPARIAS study area) used to live in the GBIF Alert repository under
`source_data/public_areas/`. They are instance-specific, so they were moved here (see
[gbif-alert#364](https://github.com/riparias/gbif-alert/issues/364)). All of them are already loaded in the RIPARIAS
databases.

- `area_data/`: the source files (attribution notes in `area_data/credits.md`).
- `area_data/belgian_municipalities/adminvector_4326.gpkg` (209 MB) is too large for git: it is attached to the
  [`area-data-v1` release](https://github.com/riparias/early-alert-webapp/releases/tag/area-data-v1) instead.
- `area_loaders/`: the custom management commands that imported the files GBIF Alert's generic `load_area`
  could not handle.

**These loaders are archived and probably no longer needed.** GBIF Alert now lets a superuser create shared areas
directly over its API (`POST /api/v2/areas/` with GeoJSON, or `POST /api/v2/areas/from-file/` with a file, both
with `shared` set), and simple files can be loaded with `python manage.py load_area <path> --name-field <field>`
(e.g. `BEKNAAM` for `Riparias_Official_StudyArea.geojson`, `NAME_1` for `belgian_regions.shp`, `NAME_2` for
`belgian_provinces.shp`). Consider the loaders deprecated: they are kept only as a record of how the existing areas
were built (tags, name formats, reprojection).

If you really need to run one: copy the contents of `area_data/` (plus the gpkg from the release) to
`source_data/public_areas/` and the script to `dashboard/management/commands/` in a GBIF Alert checkout, then run
it with `python manage.py <script name without .py>`. The scripts are kept unchanged and use those paths.
