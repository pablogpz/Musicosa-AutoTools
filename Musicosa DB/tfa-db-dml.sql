-- Avatars
INSERT INTO avatars (id, image_filename, image_height, score_box_position_top, score_box_position_left,
                     score_box_font_scale, score_box_font_color)
VALUES (1, 'Caster.png', 1644, 16, 79, 0.175, 'black');
INSERT INTO avatars (id, image_filename, image_height, score_box_position_top, score_box_position_left,
                     score_box_font_scale, score_box_font_color)
VALUES (2, 'Ana.png', 1607, 16, 79.5, 0.175, 'black');
INSERT INTO avatars (id, image_filename, image_height, score_box_position_top, score_box_position_left,
                     score_box_font_scale, score_box_font_color)
VALUES (3, 'Pablo.png', 1646, 16, 78, 0.175, 'black');

-- Members
INSERT INTO members(id, name, avatar)
VALUES ('d60d1905-52bb-547e-811c-fb3264f30f74', 'Cáster', 1);
INSERT INTO members(id, name, avatar)
VALUES ('6603dc0d-c484-5407-baa9-7ef26c6241ee', 'Ana', 2);
INSERT INTO members(id, name, avatar)
VALUES ('309c75a4-ebda-5e97-ba5c-e78f8524672b', 'Pablo', 3);

-- Awards
INSERT INTO awards (slug, designation)
VALUES ('half-lifent-3', 'HALF LIFEN''T 3');
INSERT INTO awards (slug, designation)
VALUES ('plot-twist-el-videojuego', 'PLOT TWIST: EL VIDEOJUEGO');
INSERT INTO awards (slug, designation)
VALUES ('juego-mas-original', 'JUEGO MÁS ORIGINAL');
INSERT INTO awards (slug, designation)
VALUES ('ojo-llameante-de-mordor', 'OJO LLAMEANTE DE MORDOR');
INSERT INTO awards (slug, designation)
VALUES ('threshold-kids', 'THRESHOLD KIDS');
INSERT INTO awards (slug, designation)
VALUES ('mundo-1-1', 'MUNDO 1-1');
INSERT INTO awards (slug, designation)
VALUES ('caught-in-4k', 'CAUGHT IN 4K');
INSERT INTO awards (slug, designation)
VALUES ('el-souls-de-los-premios', 'EL SOULS DE LOS PREMIOS');
INSERT INTO awards (slug, designation)
VALUES ('susto-menor', 'SUSTO MENOR');
INSERT INTO awards (slug, designation)
VALUES ('angers-award', 'ANGER''S AWARD');
INSERT INTO awards (slug, designation)
VALUES ('odisea-virtual', 'ODISEA VIRTUAL');
INSERT INTO awards (slug, designation)
VALUES ('metapremio', 'METAPREMIO');
INSERT INTO awards (slug, designation)
VALUES ('what-is-that-melody', 'WHAT IS THAT MELODY?');
INSERT INTO awards (slug, designation)
VALUES ('hans-williams', 'HANS WILLIAMS');
INSERT INTO awards (slug, designation)
VALUES ('musica-momento', 'MÚSICA-MOMENTO');
INSERT INTO awards (slug, designation)
VALUES ('comedy-bender', 'COMEDY BENDER');
INSERT INTO awards (slug, designation)
VALUES ('im-just-ken', 'I''M JUST KEN');
INSERT INTO awards (slug, designation)
VALUES ('mujercalculos', 'MUJERCÁLCULOS');
INSERT INTO awards (slug, designation)
VALUES ('el-killer-no-tu-abuela', 'EL KILLER, NO TU ABUELA');
INSERT INTO awards (slug, designation)
VALUES ('roster-of-the-obra-dinn', 'ROSTER OF THE OBRA DINN');
INSERT INTO awards (slug, designation)
VALUES ('now-thats-drama', 'NOW THAT''S DRAMA!');
INSERT INTO awards (slug, designation)
VALUES ('oscar', 'ÓSCAR');
INSERT INTO awards (slug, designation)
VALUES ('spawny', 'SPAWNY');
INSERT INTO awards (slug, designation)
VALUES ('atrezzo-rosso', 'ATREZZO ROSSO');
INSERT INTO awards (slug, designation)
VALUES ('pixel-perfect', 'PIXEL PERFECT');
INSERT INTO awards (slug, designation)
VALUES ('the-poet-and-the-muse', 'THE POET AND THE MUSE');
INSERT INTO awards (slug, designation)
VALUES ('lore-per-favore', 'LORE PER FAVORE');
INSERT INTO awards (slug, designation)
VALUES ('mini-lisan-al-gaib', 'MINI LISAN AL GAIB');
INSERT INTO awards (slug, designation)
VALUES ('lisan-al-gaib-lag', 'LISAN AL GAIB (LAG)');

-- Nominations
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('037de4fe1e805741a8c9f49473aa1db0', 'DOOM: The Dark Ages', '', 'half-lifent-3');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('e14549bcd7765526bb0223845566471d', 'Blasphemous', '', 'half-lifent-3');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('755b875c59985d03bcb4eaf4b762c813', 'Cuphead', '', 'half-lifent-3');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('a4b557529cd2562ca07a44d0b7d620ab', 'Deathloop', '', 'half-lifent-3');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('07e899df5f0558e18572eb64f69fe715', 'The Last Clockwinder', '', 'half-lifent-3');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('0a77f70e99665461b42bb2eff8cfd126', 'Tomb Raider (2013)', '', 'half-lifent-3');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('60291a77ecfc56139ad0998252b13b75', 'Dispatch', '', 'half-lifent-3');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('39f96defdae85d358eeed0c74741965d', 'Lil Guardsman', '', 'half-lifent-3');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('3172db2ca8dc5beebad36b03ccb2406a', 'The Alters', '', 'half-lifent-3');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('e01b51b203e35fb38d1a621ab10a574a', 'A Plague Tale: Innocence', '', 'half-lifent-3');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('f5df72a50fe051e4a8dcf8591db565e6', 'The Last of Us Parte I', '', 'half-lifent-3');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('c9999208c2ae5913a4401ba88a6e2d37', 'Tunic', '', 'half-lifent-3');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('3d56c30f4124557698c839e6bf16b877', 'Nobody Saves the World', '', 'half-lifent-3');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('939b70cd0dd957f5beb9a776da508bde', 'Lego Batman: The Videogame', '', 'half-lifent-3');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('9ac92802ee3e5693854e3ea02dcd6817', 'Hitman', '', 'half-lifent-3');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('cc9a78c35c9f500f9b8a79c188dee2ae', 'Lorelei and the Laser Eyes', '', 'plot-twist-el-videojuego');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('b9a1a13b14e550cb8e815ca9343fa224', 'Outer Wilds', '', 'plot-twist-el-videojuego');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('88e4a10c13825dd3b76e92b0512fec99', 'Inscryption', '', 'plot-twist-el-videojuego');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('4acb3dbfdc805b508abf04f0d2cabe72', 'Chants of Sennaar', '', 'plot-twist-el-videojuego');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('0bf70ba0b73c53d49047b49b73396f67', 'Forgotton Anne', '', 'plot-twist-el-videojuego');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('dde5d77fc1e45191938a7f76921fd5bb', 'Inscryption', '', 'juego-mas-original');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('edf6d0e122cc589482faab244d4c3e3b', 'Chants of Sennaar', '', 'juego-mas-original');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('283b9fa547615f3686264bde37b8dd64', 'Return of the Obra Dinn', '', 'juego-mas-original');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('257045428e375da9809aca5e48c0e5d7', 'Lorelei and the Laser Eyes', '', 'juego-mas-original');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('bfe46a2344615f8cab9454b1e9edb8ae', 'Viewfinder', '', 'juego-mas-original');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('054950cfb6b55e569718358fdd9fb570', 'En Garde!', '', 'ojo-llameante-de-mordor');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('07cc90832e755a239f11c985b3425319', 'WHAT THE BAT?', '', 'ojo-llameante-de-mordor');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('cc8906d308d4538088887bf152e4185d', 'I Expect You to Die 3', '', 'ojo-llameante-de-mordor');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('2609ae67366657e68794d3f2307f141a', 'Rayman Legends', '', 'ojo-llameante-de-mordor');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('521ac0ffb6d7508a815c2a5837eae48b', 'Mario + Rabbids: Kingdom Battle', '', 'ojo-llameante-de-mordor');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('5afdf93457885cfdb263451bc81f8f87', 'Hollow Knight', '', 'threshold-kids');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('bed06fc37d4651ea94775ed8cd12c4a6', 'WHAT THE BAT?', '', 'threshold-kids');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('84efa98435a45b10875fd1b6d3e90946', 'Super Mario Galaxy 2', '', 'threshold-kids');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('851e99779d3e562f9fa325e4d12e18f1', 'Assassin''s Creed Revelations', '', 'threshold-kids');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('1c12de6ee66a5fc89ed472820ba0ea44', 'Super Meat Boy', '', 'threshold-kids');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('f2e401d38acf51ed8803415ebe667c31', 'Super Meat Boy', '', 'mundo-1-1');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('cc7f348a126550079b167f16cda4284a', 'Super Mario Galaxy 2', '', 'mundo-1-1');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('bb268d3a7e6b528ab1032eea36471036', 'Rayman Legends', '', 'mundo-1-1');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('4114cde02ceb531db1febfcd4df7ee61', 'Mario + Rabbids: Kingdom Battle', '', 'mundo-1-1');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('84ab98adba2d5c8e854cebe90a162591', 'Viewfinder', '', 'mundo-1-1');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('a98f497dfba150f5889e059cfebe07eb', 'Dead Space Remake', '', 'caught-in-4k');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('1bb7158d713d582ca1f6ccc49fb7a87d', 'Assassin''s Creed 3', '', 'caught-in-4k');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('7c9a7e4b492a55c28d76648d3468b061', 'Mario + Rabbids: Kingdom Battle', '', 'caught-in-4k');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('2458533b09085fd5ae44c3d35485f16a', 'Assassin''s Creed', '', 'caught-in-4k');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('88681a16778f5fd0a08a3429978f2db4', 'Ori and the Will of the Wisps', '', 'caught-in-4k');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('9338328a088e523ea51245792891259f', 'Super Meat Boy', '', 'el-souls-de-los-premios');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('609bd6a3acfa5ed9a01788a850944799', 'Mario + Rabbids: Kingdom Battle', '', 'el-souls-de-los-premios');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('03a087320c895d73b1e9a20bec67ce10', 'Hollow Knight', '', 'el-souls-de-los-premios');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('72962ff08530507a9970c9c653766bac', 'En Garde!', '', 'el-souls-de-los-premios');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('2a578d7dbc0a549a8a1851ba1e2d5743', 'Rayman Legends', '', 'el-souls-de-los-premios');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('0c51f4fc43405c9fbd29997d6ab808de', 'Outer Wilds', '', 'susto-menor');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('44a4578f8bfe5c29bc342fccbaa0ac40', 'Lorelei and the Laser Eyes', '', 'susto-menor');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('c4684f094b9658c693ffe400eacf2e35', 'Dead Space Remake', '', 'susto-menor');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('f148eec75f365b94b1a59ff1bbb7e203', 'Inscryption', '', 'susto-menor');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('eb48303c78a35ccfacf97840ce6e6ebb', 'As Dusk Falls', '', 'susto-menor');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('42e3659621cd5f56b7b2964dcb512036', 'Dead Space Remake', '', 'angers-award');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('9d6c0ddf941250d18f155055bfd6c0cf', 'Assassin''s Creed Brotherhood', '', 'angers-award');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('ef0a8fce7e7c5aafbd43972f70d5c9db', 'Assassin''s Creed 2', '', 'angers-award');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('56cb68d76be55bd991a439a93ada01c7', 'En Garde!', '', 'angers-award');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('54e11e825f41515eb954532fbcc2c7ce', 'Tomb Raider: Underworld', '', 'angers-award');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('da47538a6b5d55328aadf422a4609809', 'Tomb Raider: Legend', '', 'odisea-virtual');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('60fc549d6fd3517fa49a206b6147891e', 'Assassin''s Creed 2', '', 'odisea-virtual');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('e026984571cc5c0296822e7714a4b350', 'Outer Wilds', '', 'odisea-virtual');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('cc51fda91f3557cf936c69d8edaf7f49', 'Forgotton Anne', '', 'odisea-virtual');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('e807c46bdade53c6aa19c445a2fa2808', 'Ori and the Blind Forest', '', 'odisea-virtual');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('66ccedfcc052562dbdc51d7888647055', 'Dead Space Remake', '', 'metapremio');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('1606a8fb6bcc506f977dc3bb600f2cd0', 'Inscryption', '', 'metapremio');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('af1272e126065dee9075ed1c087701c5', 'I Expect You to Die 3', '', 'metapremio');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('fd23078334215aa18d697657a72c8bab', 'Chants of Sennaar', '', 'metapremio');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('6629b2ffd8bd5c32b5b4c864b66b3238', 'Assassin''s Creed Brotherhood', '', 'metapremio');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('0a28713d4d0e5c3aae7ab9dfe7e47f19', 'Hollow Knight', '', 'what-is-that-melody');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('5bebe31dcb8c5e369ab9fed42851dc55', 'Super Mario Galaxy', '', 'what-is-that-melody');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('ce111edfddcd54a8b002591e1592a5d1', 'Lorelei and the Laser Eyes', '', 'what-is-that-melody');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('27406279ce6f59b6b801d17d90c55759', 'Outer Wilds', '', 'what-is-that-melody');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('0f75a512353c598f98a71f600bf02653', 'Chants of Sennaar', '', 'what-is-that-melody');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('d4ae1633ef9f5d028ff65294773ae54e', 'Assassin''s Creed 2', 'Ezio''s Family', 'hans-williams');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('fe9e86e8015651f489e2074ee4cf37bb', 'Tomb Raider: Legend', 'Tema principal', 'hans-williams');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('c8a8953882b65e8e8df040c943880554', 'Hollow Knight', 'Mantis Lords', 'hans-williams');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('1642ca9f949e5b4187693ad15af68b0d', 'Super Mario Galaxy', 'Comet Observatory', 'hans-williams');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('b53d2276bd705dd180e5c9fc387e13c1', 'Return of the Obra Dinn', 'Tema principal', 'hans-williams');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('3779efa71b7f558b8806e384646701ae', 'Outer Wilds', 'Travelers', 'musica-momento');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('1e150f7bb028501fb16d55c65f076afc', 'Rayman Legends', 'Castle Rock', 'musica-momento');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('c3e857c5dc435c9495a88a8a318e1074', 'Lorelei and the Laser Eyes', 'Laser Eyes', 'musica-momento');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('f0a456e929245471b55e7e399b88e29d', 'Mario + Rabbids: Kingdom Battle', 'El Fantasma de Bwahpera',
        'musica-momento');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('4df87edc42d053e5ad5e02321815d41c', 'I Expect You to Die 3', 'Cog in the Machine', 'musica-momento');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('de65a57d3d5858698adf33a884e96053', 'Super Mario Galaxy', 'La Mecachacha Andaluza', 'comedy-bender');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('167f6baeea8e5e7c8bdf20a4d4d3a402', 'Mario + Rabbids: Kingdom Battle', 'Rabbid Peach', 'comedy-bender');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('aaa3838c6ec0539896c90dc45b27d950', 'Assassin''s Creed 2, Assassin''s Creed Brotherhood', 'Bartolomeo',
        'comedy-bender');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('9bc13e34c1b752ee89c0c6571ad349bd', 'Rayman Legends', 'Los Diminutos', 'comedy-bender');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('2b265f1831b95417a3a6361b112d8a8c', 'Hollow Knight', 'Príncipe Gris Zote', 'comedy-bender');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('c689642af27257c19501add39715caaf',
        'Assassin''s Creed 2, Assassin''s Creed Brotherhood, Assassin''s Creed Revelations', 'Ezio Auditore Da Firenze',
        'im-just-ken');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('745a6b57c469553f8dbce9c971e340a1', 'Assassin''s Creed, Assassin''s Creed Revelations', 'Altair Ibn-La''Ahad',
        'im-just-ken');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('d3b906790db352cf89bcd7903bc73e88', 'Assassin''s Creed 2, Assassin''s Creed Brotherhood', 'Leonardo Da Vinci',
        'im-just-ken');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('6cdd65c27c36527a81087c3e0d850ab3', 'Lorelei and the Laser Eyes', 'Renzo Nero', 'im-just-ken');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('67d28ae1d92758fbb08a885f05182e00', 'Forgotton Anne', 'Mr. Fig', 'im-just-ken');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('24ea7c614cff59e4a6b99b234342608a', 'Tomb Raider: Legend, Tomb Raider: Anniversary, Tomb Raider: Underworld',
        'Lara Croft', 'mujercalculos');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('979a52bd98a25c2ebc6b4a62764d5fd6', 'En Garde!', 'Adalia de Volador', 'mujercalculos');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('f6fdfcb1bba456ceaaa484f68e0deda8', 'Forgotton Anne', 'Anne', 'mujercalculos');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('fca5f3637f0c538ca3913b4cdf22be36', 'Firewatch', 'Delilah', 'mujercalculos');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('1e72e3adc7855957b12a40654b6e1525', 'Lorelei and the Laser Eyes', 'Lorelei Weiss', 'mujercalculos');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('9a411df83a875541a148ea3b4b87852c', 'Assassin''s Creed 2, Assassin''s Creed Brotherhood', 'Rodrigo Borgia',
        'el-killer-no-tu-abuela');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('e497b322292254c2ad46ad46efbf5fad', 'Assassin''s Creed 3', 'Haytham Kenway', 'el-killer-no-tu-abuela');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('a6fe948048c65d9687498c90c5e29f3f', 'I Expect You to Die 3', 'Doctora Roxana Prism', 'el-killer-no-tu-abuela');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('bcb549ab71b754c68e56ad991edbf1eb', 'Assassin''s Creed Brotherhood', 'César Borgia', 'el-killer-no-tu-abuela');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('77414d92a8485e4fb31d87865e792130', 'Lorelei and the Laser Eyes', 'Renzo Nero', 'el-killer-no-tu-abuela');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('8c097226170e5e6eae806ede481c0511', 'As Dusk Falls', '', 'roster-of-the-obra-dinn');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('54e2279dfed85a9496534ad1b7d75e56', 'Lorelei and the Laser Eyes', '', 'roster-of-the-obra-dinn');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('d1d89e48fbcc5d1ab1e7071bad6d1420', 'Assassin''s Creed Brotherhood', '', 'roster-of-the-obra-dinn');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('ec46dc342de05048b9047f13c1028e16', 'Hollow Knight', '', 'roster-of-the-obra-dinn');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('f0a6bf2df2515a0d8a905ca863470b11', 'Mario + Rabbids: Kingdom Battle', '', 'roster-of-the-obra-dinn');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('528eaad58b8e56b587ab50130dcab792',
        'Assassin''s Creed 2, Assassin''s Creed Brotherhood, Assassin''s Creed Revelations',
        'Luis Reina (Ezio Auditore)', 'now-thats-drama');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('18d3776e6ebd5d7e9f39e650122c3538', 'En Garde!', 'Clara Cantos (Adalia de Volador)', 'now-thats-drama');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('c70010b468655914b09dfe151931e034', 'Assassin''s Creed, Assassin''s Creed Revelations',
        'Claudio Serrano (Altair)', 'now-thats-drama');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('42e0b1a2e33c52668a91b666ad013030', 'As Dusk Falls', 'José Javier Serrano (Vince Walker)', 'now-thats-drama');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('d55302b3b78e53eab846901bd88c6476', 'Firewatch', 'Cissy Jones (Delilah)', 'now-thats-drama');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('0b283b31f1c45cca850b696dd21f77cd', 'Assassin''s Creed Revelations',
        'Los maestros dejan su legado a los que están por venir', 'oscar');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('13b43a512cf35184a58ea519d745c0bd', 'Tomb Raider: Legend', 'Con una espada Lara sella su destino', 'oscar');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('1fb9deefd19e5f74bb813da1b8452cec', 'Assassin''s Creed Brotherhood',
        'Ezio es nombrado Maestro Asesino y Claudia Asesina', 'oscar');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('698805ab2d2b57f78d8c6afc43976261', 'Inscryption', 'La despedida de los escribas', 'oscar');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('d58f23f615d157c4815d3c93742ec0c0', 'Assassin''s Creed Brotherhood', 'La muerte de César Borgia', 'oscar');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('ece1347924e45ab28ac971bff5299516', 'Assassin''s Creed 2',
        'La Primera Civilización contacta a Desmond a través de Ezio', 'oscar');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('52440e46ca605b5a978a4edc580f2caa', 'Forgotton Anne', '', 'spawny');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('2121d7aefdb1561bb3459abbc63e6285', 'En Garde!', '', 'spawny');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('8eb16889cfff59f7b30fe8f2142eed99', 'Rayman Legends', '', 'spawny');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('4ee0f8ba5ff953a6b67062a75db4b49b', 'Mario + Rabbids: Kingdom Battle', '', 'spawny');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('e7445e963d5e558e829452fe8836cbe4', 'Hollow Knight', '', 'spawny');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('a9c9c110c27552b2bdda8fd65a41dc2b', 'Assassin''s Creed 2', '', 'atrezzo-rosso');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('d8794acee7295ce4a534418d9625fd9c', 'Assassin''s Creed Brotherhood', '', 'atrezzo-rosso');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('92dcfa8638425e5b824c435495aeb389', 'Jusant', '', 'atrezzo-rosso');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('3db598f934d855a49ec4882b3cad9cae', 'Ori and the Will of the Wisps', '', 'atrezzo-rosso');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('bb57f393ef18510cb5f00af433fc986a', 'Lorelei and the Laser Eyes', '', 'atrezzo-rosso');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('5df17e6cbe215b13b929e9b7486132f3', 'Chants of Sennaar', '', 'pixel-perfect');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('5e2877efe5f55d72ba7a014d06742776', 'Hollow Knight', '', 'pixel-perfect');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('2e35c3b4f7fe5dffb07eaee763d225ac', 'Jusant', '', 'pixel-perfect');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('a457cbc04c8b5b4e893313c9ccc13f86', 'Forgotton Anne', '', 'pixel-perfect');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('27f05395e42a527b841d0b94c9a1c451', 'Ori and the Will of the Wisps', '', 'pixel-perfect');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('8eb83ea73ab3589f8d7a3e627b80a45a', 'Outer Wilds', '', 'the-poet-and-the-muse');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('06ddd39640275e3db50409f381bb66c4', 'Assassin''s Creed Revelations', '', 'the-poet-and-the-muse');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('5dfc2fe0a21e5676961365669a4b5176', 'Return of the Obra Dinn', '', 'the-poet-and-the-muse');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('d852ba0a23325bffbee98cfd17308ef7', 'Chants of Sennaar', '', 'the-poet-and-the-muse');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('dfc8636866e95575a888d4f0639c9a03', 'Lorelei and the Laser Eyes', '', 'the-poet-and-the-muse');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('091c419048915b249254545426d9c0b7', 'Assassin''s Creed Brotherhood', '', 'lore-per-favore');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('16eae6489af4548cbd7ef4cf14b55679', 'Forgotton Anne', '', 'lore-per-favore');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('530c3cecf5ea5ab994d035cfc1625016', 'As Dusk Falls', '', 'lore-per-favore');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('a2208df3ca07592b8607bae6c4237a15', 'Tomb Raider: Legend', '', 'lore-per-favore');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('6ebe96fb934e5285a598e985250f5ff9', 'Assassin''s Creed 2', '', 'lore-per-favore');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('dbc376b4bb805223912711eab8a25205', 'Hollow Knight', '', 'mini-lisan-al-gaib');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('0e62fe20cc4e5ef6892f7b3963aeaf82', 'Lorelei and the Laser Eyes', '', 'mini-lisan-al-gaib');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('dffc28ca8b9159b58abfa6764dee7497', 'Chants of Sennaar', '', 'mini-lisan-al-gaib');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('b130cf317088597990368b641e70f679', 'Viewfinder', '', 'mini-lisan-al-gaib');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('20cc4737594c5f9c99bb11c1db9ed17f', 'As Dusk Falls', '', 'mini-lisan-al-gaib');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('a8a04b64645958b1b5e88af7114e2227', 'Outer Wilds', '', 'mini-lisan-al-gaib');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('3b6c1f76561959449dc87076f708c089', 'Inscryption', '', 'mini-lisan-al-gaib');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('07fcc5e9d87559e492297a35c67819c2', 'Chants of Sennaar', '', 'lisan-al-gaib-lag');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('0b90571d9abe5934900086b32282f3e7', 'Lorelei and the Laser Eyes', '', 'lisan-al-gaib-lag');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('62488340cc145cad86b1838bda0b41d8', 'Hollow Knight', '', 'lisan-al-gaib-lag');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('bd92c306fa525cc3b9ce369c07f27069', 'Outer Wilds', '', 'lisan-al-gaib-lag');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('8e92a10c37f359fa954c91a36ab913ea', 'Assassin''s Creed 2', '', 'lisan-al-gaib-lag');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('df0875c7f5ed59eca03037d690dfa35c', 'Super Mario Galaxy 2', '', 'lisan-al-gaib-lag');
INSERT INTO nominations (id, game_title, nominee, award)
VALUES ('62898baaa4d35a14884dc3f48d06fff7', 'Tomb Raider: Legend', '', 'lisan-al-gaib-lag');

-- Videoclips
INSERT INTO videoclips (id, url)
VALUES (1, 'https://www.youtube.com/watch?v=fpqara4Lz7s');
INSERT INTO videoclips (id, url)
VALUES (2, 'https://www.youtube.com/watch?v=MhFBOSM3jfI');
INSERT INTO videoclips (id, url)
VALUES (3, 'https://www.youtube.com/watch?v=NN-9SQXoi50');
INSERT INTO videoclips (id, url)
VALUES (4, 'https://www.youtube.com/watch?v=pmd3y6AZdWo');
INSERT INTO videoclips (id, url)
VALUES (5, 'https://www.youtube.com/watch?v=ZGYJ6Y9ZXtQ');
INSERT INTO videoclips (id, url)
VALUES (6, 'https://www.youtube.com/watch?v=nFBrgeSjj-0');
INSERT INTO videoclips (id, url)
VALUES (7, 'https://www.youtube.com/watch?v=ZbERWU5bc50');
INSERT INTO videoclips (id, url)
VALUES (8, 'https://www.youtube.com/watch?v=eKXVIqQyrJI');
INSERT INTO videoclips (id, url)
VALUES (9, 'https://www.youtube.com/watch?v=6qFhWQ-BJq0');
INSERT INTO videoclips (id, url)
VALUES (10, 'https://www.youtube.com/watch?v=H4FOb16Nenk');
INSERT INTO videoclips (id, url)
VALUES (11, 'https://www.youtube.com/watch?v=VjKKfoy0J30');
INSERT INTO videoclips (id, url)
VALUES (12, 'https://www.youtube.com/watch?v=Q5XpgTO7YN0');
INSERT INTO videoclips (id, url)
VALUES (13, 'https://www.youtube.com/watch?v=AiV0D1FXX_s');
INSERT INTO videoclips (id, url)
VALUES (14, 'https://www.youtube.com/watch?v=cEVoc3FXCpI');
INSERT INTO videoclips (id, url)
VALUES (15, 'https://www.youtube.com/watch?v=sM9j0xTG1Fw');
INSERT INTO videoclips (id, url)
VALUES (16, 'https://www.youtube.com/watch?v=p2DYhQU2oiE');
INSERT INTO videoclips (id, url)
VALUES (17, 'https://www.youtube.com/watch?v=d6LGnVCL1_A');
INSERT INTO videoclips (id, url)
VALUES (18, 'https://www.youtube.com/watch?v=E-zxjhz_TN8');
INSERT INTO videoclips (id, url)
VALUES (19, 'https://www.youtube.com/watch?v=2zNOrRY7HgY');
INSERT INTO videoclips (id, url)
VALUES (20, 'https://www.youtube.com/watch?v=dF6eYVEjIiI');
INSERT INTO videoclips (id, url)
VALUES (21, 'https://www.youtube.com/watch?v=s4J3c68lOWU');
INSERT INTO videoclips (id, url)
VALUES (22, 'https://www.youtube.com/watch?v=tSN6KhscgiE');
INSERT INTO videoclips (id, url)
VALUES (23, 'https://www.youtube.com/watch?v=ILolesm8kFY');
INSERT INTO videoclips (id, url)
VALUES (24, 'https://www.youtube.com/watch?v=rPZpKKhlL_g');
INSERT INTO videoclips (id, url)
VALUES (25, 'https://www.youtube.com/watch?v=G1QgXaXhEvs');
INSERT INTO videoclips (id, url)
VALUES (26, 'https://www.youtube.com/watch?v=Onebc8AfJi8');
INSERT INTO videoclips (id, url)
VALUES (27, 'https://www.youtube.com/watch?v=wyLuiF_ovaw');
INSERT INTO videoclips (id, url)
VALUES (28, 'https://www.youtube.com/watch?v=_pJfvBF2Opk');
INSERT INTO videoclips (id, url)
VALUES (29, 'https://www.youtube.com/watch?v=E7TRB8gka-4');
INSERT INTO videoclips (id, url)
VALUES (30, 'https://www.youtube.com/watch?v=MAoXy9iBTIU');
INSERT INTO videoclips (id, url)
VALUES (31, 'https://www.youtube.com/watch?v=0QnLG-JEzzU');
INSERT INTO videoclips (id, url)
VALUES (32, 'https://www.youtube.com/watch?v=4uwjfoMuElw');
INSERT INTO videoclips (id, url)
VALUES (33, 'https://www.youtube.com/watch?v=TtAEt2VyZx0');
INSERT INTO videoclips (id, url)
VALUES (34, 'https://www.youtube.com/watch?v=XO8NE87HpNA');
INSERT INTO videoclips (id, url)
VALUES (35, 'https://www.youtube.com/watch?v=BJCDoH-eNsQ');
INSERT INTO videoclips (id, url)
VALUES (36, 'https://www.youtube.com/watch?v=1NkR_Gnwv7A');
INSERT INTO videoclips (id, url)
VALUES (37, 'https://www.youtube.com/watch?v=Ngzfk2tg9UI');
INSERT INTO videoclips (id, url)
VALUES (38, 'https://www.youtube.com/watch?v=GB7kriVEQkU');
INSERT INTO videoclips (id, url)
VALUES (39, 'https://www.youtube.com/watch?v=8S2xZwoAJjY');
INSERT INTO videoclips (id, url)
VALUES (40, 'https://www.youtube.com/watch?v=2dblNpwLbYU');
INSERT INTO videoclips (id, url)
VALUES (41, 'https://www.youtube.com/watch?v=rTKaOkCvQr0');
INSERT INTO videoclips (id, url)
VALUES (42, 'https://www.youtube.com/watch?v=EOnZKbl0dg8');
INSERT INTO videoclips (id, url)
VALUES (43, 'https://www.youtube.com/watch?v=TGL-LHKSWTA');
INSERT INTO videoclips (id, url)
VALUES (44, 'https://www.youtube.com/watch?v=5cLXRo0IkoY');
INSERT INTO videoclips (id, url)
VALUES (45, 'https://www.youtube.com/watch?v=DHan1iksato');
INSERT INTO videoclips (id, url)
VALUES (46, 'https://www.youtube.com/watch?v=Ep2X8iNMvI4');
INSERT INTO videoclips (id, url)
VALUES (47, 'https://www.youtube.com/watch?v=Cb7kgrpuOPw');
INSERT INTO videoclips (id, url)
VALUES (48, 'https://www.youtube.com/watch?v=9rg8UBKtt1o');
INSERT INTO videoclips (id, url)
VALUES (49, 'https://www.youtube.com/watch?v=vddOlrEDkSQ');
INSERT INTO videoclips (id, url)
VALUES (50, 'https://www.youtube.com/watch?v=Wgt6e5J5A9o');
INSERT INTO videoclips (id, url)
VALUES (51, 'https://www.youtube.com/watch?v=6yWGO6nPzUo');
INSERT INTO videoclips (id, url)
VALUES (52, 'https://www.youtube.com/watch?v=YRKzeFKbo-o');
INSERT INTO videoclips (id, url)
VALUES (53, 'https://www.youtube.com/watch?v=KWBGTbZESk4');
INSERT INTO videoclips (id, url)
VALUES (54, 'https://www.youtube.com/watch?v=G1piYuxh4Eg&list=PLSQoPnd2HxhIdGQd_76DVRBm8SBUbSWNW&index=6');
INSERT INTO videoclips (id, url)
VALUES (55, 'https://www.youtube.com/watch?v=v8tjM6XvGhM');
INSERT INTO videoclips (id, url)
VALUES (56, 'https://www.youtube.com/watch?v=BJYlAu-hJng');
INSERT INTO videoclips (id, url)
VALUES (57, 'https://www.youtube.com/watch?v=Hfih6l452ng');
INSERT INTO videoclips (id, url)
VALUES (58, 'https://www.youtube.com/watch?v=w7SgVrQBmVk');
INSERT INTO videoclips (id, url)
VALUES (59, 'https://www.youtube.com/watch?v=gjRXfooNXkw&list=PLgv8tls6d-QCjJpO8OLjaGp6JRddFNM9a&index=7');
INSERT INTO videoclips (id, url)
VALUES (60, 'https://drive.google.com/file/d/1Brl0Ey4YPrOpVokQq_WSlMayrKR_Gmi_/view');
INSERT INTO videoclips (id, url)
VALUES (61, 'https://www.youtube.com/watch?v=X2SwF9gipNs');
INSERT INTO videoclips (id, url)
VALUES (62, 'https://www.youtube.com/watch?v=A9C5pRp6Thg&list=PLGKJJhcJXlNziWVNslj6zSraldRiVOmOf&index=10');
INSERT INTO videoclips (id, url)
VALUES (63, 'https://www.youtube.com/watch?v=cklw-Yu3moE');
INSERT INTO videoclips (id, url)
VALUES (64, 'https://www.youtube.com/watch?v=H-33KnYkbYM');
INSERT INTO videoclips (id, url)
VALUES (65, 'https://www.youtube.com/watch?v=yAncIwz77Ps');
INSERT INTO videoclips (id, url)
VALUES (66, 'https://www.youtube.com/watch?v=LzU80W9xxi4');
INSERT INTO videoclips (id, url)
VALUES (67, 'https://www.youtube.com/watch?v=c7Wkd1BSfMM');
INSERT INTO videoclips (id, url)
VALUES (68, 'https://www.youtube.com/watch?v=Htz7ZSyiovU');
INSERT INTO videoclips (id, url)
VALUES (69, 'https://www.youtube.com/watch?v=P8xvLvCQAO4');
INSERT INTO videoclips (id, url)
VALUES (70, 'https://www.youtube.com/watch?v=1p8ADoTqggY');
INSERT INTO videoclips (id, url)
VALUES (71, 'https://www.youtube.com/watch?v=2_tWzAn1xD8');
INSERT INTO videoclips (id, url)
VALUES (72, 'https://www.youtube.com/watch?v=BC_2Rfw1QZo');
INSERT INTO videoclips (id, url)
VALUES (73, 'https://www.youtube.com/watch?v=rdtsL5nRBnQ');
INSERT INTO videoclips (id, url)
VALUES (74, 'https://www.youtube.com/watch?v=Egsz3TciHLU');
INSERT INTO videoclips (id, url)
VALUES (75, 'https://www.youtube.com/watch?v=0asI8EoYy-E');
INSERT INTO videoclips (id, url)
VALUES (76, 'https://www.youtube.com/watch?v=z34enKCqRGk');
INSERT INTO videoclips (id, url)
VALUES (77, 'https://www.youtube.com/watch?v=wV-w6crl3-c');
INSERT INTO videoclips (id, url)
VALUES (78, 'https://www.youtube.com/watch?v=89qoIKiu0mU');
INSERT INTO videoclips (id, url)
VALUES (79, 'https://www.youtube.com/watch?v=PH-cpqE-efw');
INSERT INTO videoclips (id, url)
VALUES (80, 'https://www.youtube.com/watch?v=J4KgdaWF03E');
INSERT INTO videoclips (id, url)
VALUES (81, 'https://www.youtube.com/watch?v=VF_721qe9P4');
INSERT INTO videoclips (id, url)
VALUES (82, 'https://www.youtube.com/watch?v=5a8V65mQh4w');
INSERT INTO videoclips (id, url)
VALUES (83, 'https://www.youtube.com/watch?v=V94z2xJxuks');
INSERT INTO videoclips (id, url)
VALUES (84, 'https://www.youtube.com/watch?v=sSiK-AfINSc');
INSERT INTO videoclips (id, url)
VALUES (85, 'https://www.youtube.com/watch?v=mGrtmDt_Y_4');
INSERT INTO videoclips (id, url)
VALUES (86, 'https://www.youtube.com/watch?v=Fn0_g7GBayw');
INSERT INTO videoclips (id, url)
VALUES (87, 'https://www.youtube.com/watch?v=KhlIYPls6Vw');
INSERT INTO videoclips (id, url)
VALUES (88, 'https://www.youtube.com/watch?v=yVgoS1AaKYM');
INSERT INTO videoclips (id, url)
VALUES (89, 'https://www.youtube.com/watch?v=ZruMyF9ohAM');
INSERT INTO videoclips (id, url)
VALUES (90, 'https://www.youtube.com/watch?v=zCuPt9JoMuc');
INSERT INTO videoclips (id, url)
VALUES (91, 'https://www.youtube.com/watch?v=8Dy7Ct2RzmQ');
INSERT INTO videoclips (id, url)
VALUES (92, 'https://www.youtube.com/watch?v=bOv0aGVSErQ');
INSERT INTO videoclips (id, url)
VALUES (93, 'https://www.youtube.com/watch?v=61szo3OXIgc');
INSERT INTO videoclips (id, url)
VALUES (94, 'https://www.youtube.com/watch?v=8U4Jpk6NYjg');
INSERT INTO videoclips (id, url)
VALUES (95, 'https://www.youtube.com/watch?v=RDoYLPLLqWc');
INSERT INTO videoclips (id, url)
VALUES (96, 'https://www.youtube.com/watch?v=5xbm6ILMoZ8');
INSERT INTO videoclips (id, url)
VALUES (97, 'https://www.youtube.com/watch?v=OTaxW5HDobA');
INSERT INTO videoclips (id, url)
VALUES (98, 'https://www.youtube.com/watch?v=Ss-_JdoplyM&list=PLSQoPnd2HxhIdGQd_76DVRBm8SBUbSWNW&index=3');
INSERT INTO videoclips (id, url)
VALUES (99, 'https://www.youtube.com/watch?v=G6xMUhj2bDo');
INSERT INTO videoclips (id, url)
VALUES (100, 'https://www.youtube.com/watch?v=q1JFHI1Qpkw');
INSERT INTO videoclips (id, url)
VALUES (101, 'https://www.youtube.com/watch?v=lF-vwRamNY4');
INSERT INTO videoclips (id, url)
VALUES (102, 'https://www.youtube.com/watch?v=5WedGZZkpIo');
INSERT INTO videoclips (id, url)
VALUES (103, 'https://www.youtube.com/watch?v=n1YqPEU6Cjs');
INSERT INTO videoclips (id, url)
VALUES (104, 'https://www.youtube.com/watch?v=HS8cooegfN8');
INSERT INTO videoclips (id, url)
VALUES (105, 'https://www.youtube.com/watch?v=WtcDRr4FYCI');
INSERT INTO videoclips (id, url)
VALUES (106, 'https://www.youtube.com/watch?v=QsegHcsc2-Q&list=PLSQoPnd2HxhIdGQd_76DVRBm8SBUbSWNW&index=1');
INSERT INTO videoclips (id, url)
VALUES (107, 'https://www.youtube.com/watch?v=1tV2MHL8xGU');
INSERT INTO videoclips (id, url)
VALUES (108, 'https://www.youtube.com/watch?v=pKxgXt6KQAk');
INSERT INTO videoclips (id, url)
VALUES (109, 'https://www.youtube.com/watch?v=OviGqEQJcfE');
INSERT INTO videoclips (id, url)
VALUES (110, 'https://www.youtube.com/watch?v=UdxsjN5RfPk');
INSERT INTO videoclips (id, url)
VALUES (111, 'https://www.youtube.com/watch?v=cQ3peEOenfI');
INSERT INTO videoclips (id, url)
VALUES (112, 'https://www.youtube.com/watch?v=AdCLgeSi9-w');
INSERT INTO videoclips (id, url)
VALUES (113, 'https://www.youtube.com/watch?v=WykUf507LFA');
INSERT INTO videoclips (id, url)
VALUES (114, 'https://www.youtube.com/watch?v=qWvyPVJxAu8');
INSERT INTO videoclips (id, url)
VALUES (115, 'https://www.youtube.com/watch?v=9f8Yn3T5aBQ');
INSERT INTO videoclips (id, url)
VALUES (116, 'https://www.youtube.com/watch?v=nGBjvsPB50w');
INSERT INTO videoclips (id, url)
VALUES (117, 'https://www.youtube.com/watch?v=plqPQPIiILw');
INSERT INTO videoclips (id, url)
VALUES (118, 'https://www.youtube.com/watch?v=2m_j6Ziz3vQ');
INSERT INTO videoclips (id, url)
VALUES (119, 'https://www.youtube.com/watch?v=Si7RYQwXqOk');
INSERT INTO videoclips (id, url)
VALUES (120, 'https://www.youtube.com/watch?v=gkHTYydSPks');
INSERT INTO videoclips (id, url)
VALUES (121, 'https://www.youtube.com/watch?v=uRAMoaEp-08');
INSERT INTO videoclips (id, url)
VALUES (122, 'https://www.youtube.com/watch?v=cHk7t5cNxK4');
INSERT INTO videoclips (id, url)
VALUES (123, 'https://www.youtube.com/watch?v=ZAluiUarPzw');
INSERT INTO videoclips (id, url)
VALUES (124, 'https://www.youtube.com/watch?v=gFJtqywIqcU');
INSERT INTO videoclips (id, url)
VALUES (125, 'https://www.youtube.com/watch?v=-RFpGSvjyfY');
INSERT INTO videoclips (id, url)
VALUES (126, 'https://www.youtube.com/watch?v=5Zp2msLH368');
INSERT INTO videoclips (id, url)
VALUES (127, 'https://www.youtube.com/watch?v=VhHYr2Izd1Y');
INSERT INTO videoclips (id, url)
VALUES (128, 'https://www.youtube.com/watch?v=dmCAtJs3BlI&t=80s');
INSERT INTO videoclips (id, url)
VALUES (129, 'https://www.youtube.com/watch?v=XNIBcYA5dMo');
INSERT INTO videoclips (id, url)
VALUES (130, 'https://www.youtube.com/watch?v=MCl5TwywpOc&list=PLSQoPnd2HxhIdGQd_76DVRBm8SBUbSWNW&index=5');
INSERT INTO videoclips (id, url)
VALUES (131, 'https://www.youtube.com/watch?v=s4BLgdQLQrg');
INSERT INTO videoclips (id, url)
VALUES (132, 'https://www.youtube.com/watch?v=SnBU0UOqq88');
INSERT INTO videoclips (id, url)
VALUES (133, 'https://www.youtube.com/watch?v=A2snVijCkgY');
INSERT INTO videoclips (id, url)
VALUES (134, 'https://www.youtube.com/watch?v=EajRGJbZ-A0');
INSERT INTO videoclips (id, url)
VALUES (135, 'https://www.youtube.com/watch?v=OjNhyslC2hA');
INSERT INTO videoclips (id, url)
VALUES (136, 'https://www.youtube.com/watch?v=zpvfdEdZvww');
INSERT INTO videoclips (id, url)
VALUES (137, 'https://www.youtube.com/watch?v=MpveJMwnghY');
INSERT INTO videoclips (id, url)
VALUES (138, 'https://www.youtube.com/watch?v=2rPQWBxTRSM');
INSERT INTO videoclips (id, url)
VALUES (139, 'https://www.youtube.com/watch?v=gyAUiqJOa4A');

-- Video Options
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('037de4fe1e805741a8c9f49473aa1db0', 1, '00:00:12', '00:00:39');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('e14549bcd7765526bb0223845566471d', 2, '00:00:06', '00:00:36');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('755b875c59985d03bcb4eaf4b762c813', 3, '00:00:06', '00:00:36');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('a4b557529cd2562ca07a44d0b7d620ab', 4, '00:00:10', '00:00:40');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('07e899df5f0558e18572eb64f69fe715', 5, '00:00:45', '00:01:15');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('0a77f70e99665461b42bb2eff8cfd126', 6, '00:01:12', '00:01:42');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('60291a77ecfc56139ad0998252b13b75', 7, '00:00:50', '00:01:20');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('39f96defdae85d358eeed0c74741965d', 8, '00:00:10', '00:00:40');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('3172db2ca8dc5beebad36b03ccb2406a', 9, '00:01:15', '00:01:45');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('e01b51b203e35fb38d1a621ab10a574a', 10, '00:00:00', '00:00:30');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('f5df72a50fe051e4a8dcf8591db565e6', 11, '00:19:34', '00:20:08');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('c9999208c2ae5913a4401ba88a6e2d37', 12, '00:00:36', '00:01:06');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('3d56c30f4124557698c839e6bf16b877', 13, '00:00:15', '00:00:45');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('939b70cd0dd957f5beb9a776da508bde', 14, '00:00:10', '00:00:40');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('9ac92802ee3e5693854e3ea02dcd6817', 15, '00:01:50', '00:02:20');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('cc9a78c35c9f500f9b8a79c188dee2ae', 16, '00:01:37', '00:02:04');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('b9a1a13b14e550cb8e815ca9343fa224', 17, '00:00:05', '00:00:35');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('88e4a10c13825dd3b76e92b0512fec99', 18, '00:00:00', '00:00:30');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('4acb3dbfdc805b508abf04f0d2cabe72', 19, '00:00:14', '00:00:44');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('0bf70ba0b73c53d49047b49b73396f67', 20, '00:01:00', '00:01:30');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('dde5d77fc1e45191938a7f76921fd5bb', 21, '00:00:00', '00:00:30');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('edf6d0e122cc589482faab244d4c3e3b', 22, '00:01:05', '00:01:35');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('283b9fa547615f3686264bde37b8dd64', 23, '00:01:20', '00:01:50');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('257045428e375da9809aca5e48c0e5d7', 24, '00:00:00', '00:00:26');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('bfe46a2344615f8cab9454b1e9edb8ae', 25, '00:00:33', '00:01:03');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('054950cfb6b55e569718358fdd9fb570', 26, '00:00:40', '00:01:10');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('07cc90832e755a239f11c985b3425319', 27, '00:05:03', '00:05:33');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('cc8906d308d4538088887bf152e4185d', 28, '00:20:40', '00:21:25');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('2609ae67366657e68794d3f2307f141a', 29, '00:00:58', '00:01:28');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('521ac0ffb6d7508a815c2a5837eae48b', 30, '00:03:18', '00:03:31');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('5afdf93457885cfdb263451bc81f8f87', 31, '00:00:00', '00:00:30');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('bed06fc37d4651ea94775ed8cd12c4a6', 32, '00:00:02', '00:00:33');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('84efa98435a45b10875fd1b6d3e90946', 33, '00:01:00', '00:01:30');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('851e99779d3e562f9fa325e4d12e18f1', 34, '00:00:18', '00:00:59');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('1c12de6ee66a5fc89ed472820ba0ea44', 35, '00:01:38', '00:02:06');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('f2e401d38acf51ed8803415ebe667c31', 36, '00:00:00', '00:00:30');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('cc7f348a126550079b167f16cda4284a', 37, '00:04:00', '00:04:35');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('bb268d3a7e6b528ab1032eea36471036', 38, '00:00:00', '00:00:30');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('4114cde02ceb531db1febfcd4df7ee61', 39, '00:00:12', '00:00:42');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('84ab98adba2d5c8e854cebe90a162591', 40, '00:00:16', '00:00:38');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('a98f497dfba150f5889e059cfebe07eb', 41, '00:01:30', '00:02:00');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('1bb7158d713d582ca1f6ccc49fb7a87d', 42, '00:00:22', '00:00:54');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('7c9a7e4b492a55c28d76648d3468b061', 43, '00:01:28', '00:01:58');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('2458533b09085fd5ae44c3d35485f16a', 44, '00:00:23', '00:00:53');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('88681a16778f5fd0a08a3429978f2db4', 45, '00:01:27', '00:01:57');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('9338328a088e523ea51245792891259f', 46, '00:01:02', '00:01:32');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('609bd6a3acfa5ed9a01788a850944799', 47, '00:00:03', '00:01:37');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('03a087320c895d73b1e9a20bec67ce10', 48, '00:00:23', '00:00:57');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('72962ff08530507a9970c9c653766bac', 49, '00:00:25', '00:00:55');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('2a578d7dbc0a549a8a1851ba1e2d5743', 50, '00:00:01', '00:00:54');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('0c51f4fc43405c9fbd29997d6ab808de', 51, '00:00:00', '00:00:30');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('44a4578f8bfe5c29bc342fccbaa0ac40', 16, '00:24:47', '00:25:18');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('c4684f094b9658c693ffe400eacf2e35', 52, '00:00:52', '00:01:22');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('f148eec75f365b94b1a59ff1bbb7e203', 53, '00:03:28', '00:04:05');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('eb48303c78a35ccfacf97840ce6e6ebb', 54, '00:13:50', '00:14:20');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('42e3659621cd5f56b7b2964dcb512036', 55, '00:00:00', '00:00:41');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('9d6c0ddf941250d18f155055bfd6c0cf', 56, '00:24:46', '00:25:21');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('ef0a8fce7e7c5aafbd43972f70d5c9db', 57, '00:00:00', '00:00:25');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('56cb68d76be55bd991a439a93ada01c7', 58, '00:01:48', '00:02:18');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('54e11e825f41515eb954532fbcc2c7ce', 59, '00:00:45', '00:01:15');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('da47538a6b5d55328aadf422a4609809', 60, '00:00:05', '00:00:35');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('60fc549d6fd3517fa49a206b6147891e', 61, '00:00:00', '00:00:35');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('e026984571cc5c0296822e7714a4b350', 17, '00:00:59', '00:01:29');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('cc51fda91f3557cf936c69d8edaf7f49', 62, '00:11:20', '00:11:50');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('e807c46bdade53c6aa19c445a2fa2808', 63, '00:00:51', '00:01:29');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('66ccedfcc052562dbdc51d7888647055', 64, '00:01:42', '00:02:12');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('1606a8fb6bcc506f977dc3bb600f2cd0', 65, '00:00:03', '00:00:50');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('af1272e126065dee9075ed1c087701c5', 66, '00:20:28', '00:20:58');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('fd23078334215aa18d697657a72c8bab', 22, '00:02:30', '00:03:00');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('6629b2ffd8bd5c32b5b4c864b66b3238', 67, '00:06:30', '00:07:00');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('0a28713d4d0e5c3aae7ab9dfe7e47f19', 68, '00:00:20', '00:00:50');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('5bebe31dcb8c5e369ab9fed42851dc55', 69, '00:11:36', '00:12:14');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('ce111edfddcd54a8b002591e1592a5d1', 24, '00:15:10', '00:15:40');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('27406279ce6f59b6b801d17d90c55759', 70, '00:01:05', '00:01:35');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('0f75a512353c598f98a71f600bf02653', 71, '00:00:20', '00:00:50');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('d4ae1633ef9f5d028ff65294773ae54e', 72, '00:01:35', '00:02:21');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('fe9e86e8015651f489e2074ee4cf37bb', 60, '00:00:25', '00:00:55');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('c8a8953882b65e8e8df040c943880554', 73, '00:00:02', '00:00:36');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('1642ca9f949e5b4187693ad15af68b0d', 74, '00:04:18', '00:04:59');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('b53d2276bd705dd180e5c9fc387e13c1', 75, '00:01:35', '00:02:05');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('3779efa71b7f558b8806e384646701ae', 76, '00:01:15', '00:01:45');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('1e150f7bb028501fb16d55c65f076afc', 77, '00:00:40', '00:01:10');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('c3e857c5dc435c9495a88a8a318e1074', 78, '00:00:44', '00:01:18');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('f0a456e929245471b55e7e399b88e29d', 79, '00:00:19', '00:00:53');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('4df87edc42d053e5ad5e02321815d41c', 80, '00:02:15', '00:02:45');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('de65a57d3d5858698adf33a884e96053', 81, '00:00:00', '00:00:30');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('167f6baeea8e5e7c8bdf20a4d4d3a402', 30, '00:01:30', '00:02:00');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('aaa3838c6ec0539896c90dc45b27d950', 82, '00:00:25', '00:00:58');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('9bc13e34c1b752ee89c0c6571ad349bd', 83, '00:08:17', '00:08:44');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('2b265f1831b95417a3a6361b112d8a8c', 84, '00:00:06', '00:00:36');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('c689642af27257c19501add39715caaf', 85, '00:00:00', '00:00:38');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('745a6b57c469553f8dbce9c971e340a1', 86, '00:01:06', '00:01:40');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('d3b906790db352cf89bcd7903bc73e88', 87, '00:01:17', '00:01:54');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('6cdd65c27c36527a81087c3e0d850ab3', 88, '00:13:20', '00:13:50');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('67d28ae1d92758fbb08a885f05182e00', 89, '00:01:00', '00:01:30');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('24ea7c614cff59e4a6b99b234342608a', 90, '00:02:00', '00:02:30');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('979a52bd98a25c2ebc6b4a62764d5fd6', 91, '00:00:10', '00:00:40');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('f6fdfcb1bba456ceaaa484f68e0deda8', 92, '00:01:02', '00:01:32');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('fca5f3637f0c538ca3913b4cdf22be36', 93, '00:00:49', '00:01:22');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('1e72e3adc7855957b12a40654b6e1525', 24, '00:00:47', '00:01:20');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('9a411df83a875541a148ea3b4b87852c', 94, '00:05:38', '00:06:32');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('e497b322292254c2ad46ad46efbf5fad', 95, '00:01:43', '00:02:13');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('a6fe948048c65d9687498c90c5e29f3f', 96, '00:06:40', '00:07:25');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('bcb549ab71b754c68e56ad991edbf1eb', 97, '00:01:34', '00:02:28');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('77414d92a8485e4fb31d87865e792130', 88, '00:13:50', '00:14:20');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('8c097226170e5e6eae806ede481c0511', 98, '00:20:40', '00:21:10');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('54e2279dfed85a9496534ad1b7d75e56', 99, '00:00:00', '00:00:57');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('d1d89e48fbcc5d1ab1e7071bad6d1420', 100, '00:00:20', '00:01:00');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('ec46dc342de05048b9047f13c1028e16', 101, '00:00:00', '00:00:24');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('f0a6bf2df2515a0d8a905ca863470b11', 102, '00:00:48', '00:01:20');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('528eaad58b8e56b587ab50130dcab792', 103, '00:00:37', '00:01:13');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('18d3776e6ebd5d7e9f39e650122c3538', 104, '00:00:10', '00:00:40');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('c70010b468655914b09dfe151931e034', 105, '00:13:45', '00:14:26');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('42e0b1a2e33c52668a91b666ad013030', 106, '00:24:25', '00:24:55');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('d55302b3b78e53eab846901bd88c6476', 107, '00:00:30', '00:01:02');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('0b283b31f1c45cca850b696dd21f77cd', 108, '00:00:25', '00:00:55');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('13b43a512cf35184a58ea519d745c0bd', 109, '00:02:00', '00:02:30');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('1fb9deefd19e5f74bb813da1b8452cec', 110, '00:00:57', '00:01:48');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('698805ab2d2b57f78d8c6afc43976261', 111, '00:19:20', '00:20:00');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('d58f23f615d157c4815d3c93742ec0c0', 112, '00:03:39', '00:04:21');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('ece1347924e45ab28ac971bff5299516', 113, '00:01:25', '00:01:55');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('52440e46ca605b5a978a4edc580f2caa', 114, '00:10:20', '00:10:50');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('2121d7aefdb1561bb3459abbc63e6285', 115, '00:00:00', '00:00:30');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('8eb16889cfff59f7b30fe8f2142eed99', 116, '00:00:15', '00:00:45');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('4ee0f8ba5ff953a6b67062a75db4b49b', 117, '00:00:00', '00:00:30');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('e7445e963d5e558e829452fe8836cbe4', 118, '00:00:02', '00:00:32');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('a9c9c110c27552b2bdda8fd65a41dc2b', 119, '00:01:11', '00:01:41');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('d8794acee7295ce4a534418d9625fd9c', 120, '00:02:27', '00:02:57');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('92dcfa8638425e5b824c435495aeb389', 121, '00:00:30', '00:01:00');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('3db598f934d855a49ec4882b3cad9cae', 122, '00:00:26', '00:00:55');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('bb57f393ef18510cb5f00af433fc986a', 16, '00:45:40', '00:46:10');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('5df17e6cbe215b13b929e9b7486132f3', 123, '00:00:10', '00:00:40');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('5e2877efe5f55d72ba7a014d06742776', 124, '00:00:00', '00:00:35');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('2e35c3b4f7fe5dffb07eaee763d225ac', 121, '00:01:00', '00:01:30');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('a457cbc04c8b5b4e893313c9ccc13f86', 125, '00:00:40', '00:01:10');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('27f05395e42a527b841d0b94c9a1c451', 122, '00:00:58', '00:01:32');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('8eb83ea73ab3589f8d7a3e627b80a45a', 126, '00:01:09', '00:01:39');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('06ddd39640275e3db50409f381bb66c4', 108, '00:04:00', '00:04:48');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('5dfc2fe0a21e5676961365669a4b5176', 127, '00:00:25', '00:00:55');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('d852ba0a23325bffbee98cfd17308ef7', 128, '00:01:17', '00:01:37');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('dfc8636866e95575a888d4f0639c9a03', 16, '00:26:24', '00:26:55');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('091c419048915b249254545426d9c0b7', 129, '00:10:15', '00:11:03');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('16eae6489af4548cbd7ef4cf14b55679', 20, '00:00:16', '00:00:46');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('530c3cecf5ea5ab994d035cfc1625016', 130, '00:27:50', '00:28:20');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('a2208df3ca07592b8607bae6c4237a15', 131, '00:08:42', '00:09:12');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('6ebe96fb934e5285a598e985250f5ff9', 94, '00:10:14', '00:10:52');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('dbc376b4bb805223912711eab8a25205', 132, '00:00:20', '00:00:50');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('0e62fe20cc4e5ef6892f7b3963aeaf82', 16, '00:30:12', '00:30:45');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('dffc28ca8b9159b58abfa6764dee7497', 133, '00:00:12', '00:00:42');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('b130cf317088597990368b641e70f679', 134, '00:01:08', '00:02:02');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('20cc4737594c5f9c99bb11c1db9ed17f', 135, '00:00:15', '00:00:45');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('a8a04b64645958b1b5e88af7114e2227', 136, '00:03:50', '00:04:20');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('3b6c1f76561959449dc87076f708c089', 137, '00:00:00', '00:00:35');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('07fcc5e9d87559e492297a35c67819c2', 133, '00:00:42', '00:01:12');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('0b90571d9abe5934900086b32282f3e7', 24, '00:18:46', '00:19:36');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('62488340cc145cad86b1838bda0b41d8', 68, '00:05:00', '00:05:32');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('bd92c306fa525cc3b9ce369c07f27069', 136, '00:09:00', '00:09:30');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('8e92a10c37f359fa954c91a36ab913ea', 138, '00:00:20', '00:00:50');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('df0875c7f5ed59eca03037d690dfa35c', 139, '00:06:43', '00:07:17');
INSERT INTO video_options (nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('62898baaa4d35a14884dc3f48d06fff7', 60, '00:01:26', '00:01:56');
