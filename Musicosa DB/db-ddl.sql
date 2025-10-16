PRAGMA foreign_keys = ON;

-- BASE MUSICOSA DATABASE SCHEMA AND INITIAL VALUES

CREATE TABLE metadata
(
    field TEXT NOT NULL
        CONSTRAINT metadata_pk PRIMARY KEY,
    value TEXT NOT NULL
);

INSERT INTO metadata (field, value)
VALUES ('edition', '8');
INSERT INTO metadata (field, value)
VALUES ('topic', 'Canciones y BSO de Videojuegos');
INSERT INTO metadata (field, value)
VALUES ('organiser', 'Ana');
INSERT INTO metadata (field, value)
VALUES ('start_date', '09/09/2025');

CREATE TABLE settings
(
    group_key TEXT NOT NULL,
    setting   TEXT NOT NULL,
    value     TEXT,
    type      TEXT NOT NULL DEFAULT 'string'
        CONSTRAINT type_is_valid_spec CHECK ( type in ('integer', 'real', 'string', 'boolean') ),

    CONSTRAINT settings_pk PRIMARY KEY (group_key, setting)
);

INSERT INTO settings (group_key, setting, value, type)
VALUES ('global', 'round_count', '10', 'integer');
INSERT INTO settings (group_key, setting, value, type)
VALUES ('validation', 'estrelli_count', '10', 'integer');
INSERT INTO settings (group_key, setting, value, type)
VALUES ('validation', 'score_min_value', '0.0', 'real');
INSERT INTO settings (group_key, setting, value, type)
VALUES ('validation', 'score_max_value', '10.0', 'real');
INSERT INTO settings (group_key, setting, value, type)
VALUES ('validation', 'entry_video_duration_seconds', '30', 'integer');
INSERT INTO settings (group_key, setting, value, type)
VALUES ('ranking', 'significant_decimal_digits', '10', 'integer');
INSERT INTO settings (group_key, setting, value, type)
VALUES ('frame', 'width_px', '1920', 'integer');
INSERT INTO settings (group_key, setting, value, type)
VALUES ('frame', 'height_px', '1080', 'integer');
INSERT INTO settings (group_key, setting, value, type)
VALUES ('templates', 'display_decimal_digits', '2', 'integer');
INSERT INTO settings (group_key, setting, value, type)
VALUES ('generation', 'videoclips_override_top_n_duration', '10', 'integer');
INSERT INTO settings (group_key, setting, value, type)
VALUES ('generation', 'videoclips_override_duration_up_to_x_seconds', '-1', 'integer');

CREATE TABLE avatars
(
    id                      INTEGER NOT NULL
        CONSTRAINT avatar_pk PRIMARY KEY AUTOINCREMENT,
    image_filename          TEXT    NOT NULL,
    image_height            REAL    NOT NULL,
    score_box_position_top  REAL    NOT NULL,
    score_box_position_left REAL    NOT NULL,
    score_box_font_scale    REAL    NOT NULL,
    score_box_font_color    TEXT    NOT NULL DEFAULT 'black'
);

CREATE TABLE contestants
(
    -- uuid_v5 (namespace: ISO OID (RFC 4122), name: name)
    id     TEXT(36) NOT NULL
        CONSTRAINT contestant_pk PRIMARY KEY,
    name   TEXT     NOT NULL UNIQUE,
    avatar INTEGER,

    CONSTRAINT displayed_by_fk FOREIGN KEY (avatar) REFERENCES avatars (id)
        ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE entry_topics
(
    designation TEXT NOT NULL
        CONSTRAINT entry_topics_pk PRIMARY KEY
);

CREATE TABLE entries
(
    -- uuid_v5 (namespace: ISO OID (RFC 4122), name: title)
    id            TEXT(36) NOT NULL
        CONSTRAINT entry_pk PRIMARY KEY,
    title         TEXT     NOT NULL UNIQUE,
    author        TEXT,
    video_url     TEXT     NOT NULL,
    topic TEXT,

    CONSTRAINT authored_by_fk FOREIGN KEY (author) REFERENCES contestants (id)
        ON UPDATE CASCADE ON DELETE SET NULL,

    CONSTRAINT is_of_topic_fk FOREIGN KEY (topic) REFERENCES entry_topics (designation)
        ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE templates
(
    entry                      TEXT    NOT NULL
        CONSTRAINT template_pk PRIMARY KEY,
    avatar_scale               REAL    NOT NULL DEFAULT 1.0,
    author_avatar_scale        REAL    NOT NULL DEFAULT 1.0,
    video_box_width_px         INTEGER NOT NULL
        CONSTRAINT video_box_width_is_positive CHECK ( video_box_width_px > 0 ),
    video_box_height_px        INTEGER NOT NULL
        CONSTRAINT video_box_height_is_positive CHECK ( video_box_height_px > 0 ),
    video_box_position_top_px  INTEGER NOT NULL,
    video_box_position_left_px INTEGER NOT NULL,

    CONSTRAINT entry_fk FOREIGN KEY (entry) REFERENCES entries (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE video_options
(
    entry           TEXT NOT NULL
        CONSTRAINT video_options_pk PRIMARY KEY,
    timestamp_start TEXT NOT NULL DEFAULT '00:00:00',
    timestamp_end   TEXT NOT NULL DEFAULT '00:00:30',

    CONSTRAINT entry_fk FOREIGN KEY (entry) REFERENCES entries (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE contestant_grades_entries
(
    contestant TEXT,
    entry    TEXT    NOT NULL,
    score    REAL    NOT NULL,
    estrelli INTEGER NOT NULL DEFAULT 0
        CONSTRAINT estrelli_is_boolean CHECK (estrelli IN (0, 1)),

    CONSTRAINT contestant_fk FOREIGN KEY (contestant) REFERENCES contestants (id)
        ON UPDATE CASCADE ON DELETE SET NULL,

    CONSTRAINT entry_fk FOREIGN KEY (entry) REFERENCES entries (id)
        ON UPDATE CASCADE ON DELETE CASCADE,

    CONSTRAINT contestant_grades_entries_pk PRIMARY KEY (contestant, entry)
);

CREATE TABLE stats_contestants
(
    contestant         TEXT NOT NULL
        CONSTRAINT contestant_stats_pk PRIMARY KEY,
    avg_given_score    REAL,
    avg_received_score REAL,

    CONSTRAINT contestant_fk FOREIGN KEY (contestant) REFERENCES contestants (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE stats_entries
(
    entry            TEXT NOT NULL
        CONSTRAINT entry_stats_pk PRIMARY KEY,
    avg_score        REAL,
    ranking_place    INTEGER
        CONSTRAINT ranking_place_is_1_indexed CHECK ( ranking_place >= 1 ),
    ranking_sequence INTEGER UNIQUE
        CONSTRAINT ranking_sequence_is_1_indexed CHECK ( ranking_sequence >= 1 ),


    CONSTRAINT entry_fk FOREIGN KEY (entry) REFERENCES entries (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);