PRAGMA foreign_keys = ON;

-- BASE "TFA" DATABASE SCHEMA AND INITIAL VALUES

CREATE TABLE metadata
(
    field TEXT NOT NULL
        CONSTRAINT metadata_pk PRIMARY KEY,
    value TEXT NOT NULL
);

INSERT INTO metadata (field, value)
VALUES ('edition', ''); -- FIXME: TO BE FILLED

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
VALUES ('validation', 'score_min_value', '0.0', 'real');
INSERT INTO settings (group_key, setting, value, type)
VALUES ('validation', 'score_max_value', '10.0', 'real');
INSERT INTO settings (group_key, setting, value, type)
VALUES ('ranking', 'significant_decimal_digits', '10', 'integer');
INSERT INTO settings (group_key, setting, value, type)
VALUES ('frame', 'width_px', '1920', 'integer');
INSERT INTO settings (group_key, setting, value, type)
VALUES ('frame', 'height_px', '1080', 'integer');
INSERT INTO settings (group_key, setting, value, type)
VALUES ('templates', 'display_decimal_digits', '2', 'integer');

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

CREATE TABLE members
(
    -- uuid_v5 (namespace: ISO OID (RFC 4122), name: name)
    id     TEXT(36) NOT NULL
        CONSTRAINT member_pk PRIMARY KEY,
    name   TEXT     NOT NULL UNIQUE,
    avatar INTEGER,

    CONSTRAINT displayed_by_fk FOREIGN KEY (avatar) REFERENCES avatars (id)
        ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE awards
(
    slug        TEXT NOT NULL
        CONSTRAINT award_pk PRIMARY KEY,
    designation TEXT NOT NULL
);

CREATE TABLE nominations
(
    -- uuid_v5 (namespace: ISO OID (RFC 4122), name: game_title + nominee + award)
    id         TEXT(36) NOT NULL
        CONSTRAINT nomination_pk PRIMARY KEY,
    game_title TEXT     NOT NULL,
    nominee    TEXT,
    award      TEXT     NOT NULL,

    CONSTRAINT award_fk FOREIGN KEY (award) REFERENCES awards (slug)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE templates
(
    nomination                 TEXT    NOT NULL
        CONSTRAINT template_pk PRIMARY KEY,
    avatar_scale               REAL    NOT NULL DEFAULT 1.0,
    video_box_width_px         INTEGER NOT NULL
        CONSTRAINT video_box_width_is_positive CHECK ( video_box_width_px > 0 ),
    video_box_height_px        INTEGER NOT NULL
        CONSTRAINT video_box_height_is_positive CHECK ( video_box_height_px > 0 ),
    video_box_position_top_px  INTEGER NOT NULL,
    video_box_position_left_px INTEGER NOT NULL,

    CONSTRAINT nomination_fk FOREIGN KEY (nomination) REFERENCES nominations (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE videoclips
(
    id  INTEGER NOT NULL
        CONSTRAINT videoclip_pk PRIMARY KEY,
    url TEXT    NOT NULL
);

CREATE TABLE video_options
(
    nomination      TEXT    NOT NULL
        CONSTRAINT video_options_pk PRIMARY KEY,
    videoclip       INTEGER NOT NULL,
    timestamp_start TEXT    NOT NULL,
    timestamp_end   TEXT    NOT NULL,

    CONSTRAINT nomination_fk FOREIGN KEY (nomination) REFERENCES nominations (id)
        ON UPDATE CASCADE ON DELETE CASCADE,

    CONSTRAINT videoclip_fk FOREIGN KEY (videoclip) REFERENCES videoclips (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE member_grades_nominations
(
    member     TEXT,
    nomination TEXT NOT NULL,
    score      REAL NOT NULL,

    CONSTRAINT member_fk FOREIGN KEY (member) REFERENCES members (id)
        ON UPDATE CASCADE ON DELETE SET NULL,

    CONSTRAINT nomination_fk FOREIGN KEY (nomination) REFERENCES nominations (id)
        ON UPDATE CASCADE ON DELETE CASCADE,

    CONSTRAINT member_grades_nominations_pk PRIMARY KEY (member, nomination)
);

CREATE TABLE stats_nominations
(
    nomination       TEXT NOT NULL
        CONSTRAINT stats_nominations_pk PRIMARY KEY,
    avg_score        REAL,
    ranking_place    INTEGER
        CONSTRAINT ranking_place_is_1_indexed CHECK ( ranking_place >= 1 ),
    ranking_sequence INTEGER
        CONSTRAINT ranking_sequence_is_1_indexed CHECK ( ranking_sequence >= 1 ),

    CONSTRAINT nomination_fk FOREIGN KEY (nomination) REFERENCES nominations (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);