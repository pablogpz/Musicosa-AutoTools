-- TFA 2º EDITION BASE CONTENT

-- AVATARS
INSERT INTO avatars(id, image_filename, image_height, score_box_position_top, score_box_position_left,
                    score_box_font_scale, score_box_font_color)
VALUES (1, 'Caster.png', 805, 32, 78, 0.2,
        'black');
INSERT INTO avatars(id, image_filename, image_height, score_box_position_top, score_box_position_left,
                    score_box_font_scale, score_box_font_color)
VALUES (2, 'Pablo.png', 925, 30, 75, 0.2,
        'red');
INSERT INTO avatars(id, image_filename, image_height, score_box_position_top, score_box_position_left,
                    score_box_font_scale, score_box_font_color)
VALUES (3, 'Sergio.png', 883, 16, 80, 0.175,
        'white');

-- MEMBERS
INSERT INTO members(id, name, avatar)
VALUES ('8e3cf84d72585b7ebf6546e8615e78de', 'Cáster', 1);
INSERT INTO members(id, name, avatar)
VALUES ('309c75a4ebda5e97ba5ce78f8524672b', 'Pablo', 2);
INSERT INTO members(id, name, avatar)
VALUES ('17c6cb4ae2d6554480d0dd7b092aa2c1', 'Sergio', 3);

-- AWARDS
INSERT INTO awards(slug, designation)
VALUES ('silksont', 'Silkson''t');
INSERT INTO awards(slug, designation)
VALUES ('plot-twist-el-videojuego', 'Plot Twist: El Videojuego');
INSERT INTO awards(slug, designation)
VALUES ('ojo-llameante-de-mordor', 'Ojo Llameante de Mordor');
INSERT INTO awards(slug, designation)
VALUES ('threshold-kids', 'Threshold Kids');
INSERT INTO awards(slug, designation)
VALUES ('caught-in-4k', 'Caught in 4K');
INSERT INTO awards(slug, designation)
VALUES ('susto-menor', 'Susto Menor');
INSERT INTO awards(slug, designation)
VALUES ('angers-award', 'Anger''s Award');
INSERT INTO awards(slug, designation)
VALUES ('odisea-virtual', 'Odisea Virtual');
INSERT INTO awards(slug, designation)
VALUES ('what-is-that-melody', 'What is that Melody?');
INSERT INTO awards(slug, designation)
VALUES ('hans-williams', 'Hans Williams');
INSERT INTO awards(slug, designation)
VALUES ('musica-momento', 'Música-Momento');
INSERT INTO awards(slug, designation)
VALUES ('comedy-bender', 'Comedy Bender');
INSERT INTO awards(slug, designation)
VALUES ('im-just-ken', 'I''m Just Ken');
INSERT INTO awards(slug, designation)
VALUES ('mujercalculos', 'Mujercálculos');
INSERT INTO awards(slug, designation)
VALUES ('el-killer-no-tu-abuela', 'El Killer, No tu Abuela');
INSERT INTO awards(slug, designation)
VALUES ('now-that-is-drama', 'Now that is Drama!');
INSERT INTO awards(slug, designation)
VALUES ('oscar', 'Óscar');
INSERT INTO awards(slug, designation)
VALUES ('pixel-perfect', 'Pixel Perfect');
INSERT INTO awards(slug, designation)
VALUES ('the-poet-and-the-muse', 'The Poet and the Muse');
INSERT INTO awards(slug, designation)
VALUES ('mini-lisan-al-gaib-mini-lag', 'Mini Lisan Al Gaib (Mini LAG)');
INSERT INTO awards(slug, designation)
VALUES ('lisan-al-gaib-lag', 'Lisan Al Gaib (LAG)');

-- NOMINATIONS
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('8f3466a7364a5240a4780eabae1e0711', 'Assassin''s Creed II', '', 'silksont');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('58633d1221395bbcaa798dcdc831ae3d', 'Deathloop', '', 'silksont');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('0554185d80ff56918d978079b69b9ee3', 'Detroit Become Human', '', 'silksont');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('83676e34031e5647a877a4a171b9a8a2', 'Indivisible', '', 'silksont');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('c36dcf6e9b565ce88669be11f895ccbb', 'Inscryption', '', 'silksont');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('a7023fc67b8c5238a2a69727be98642c', 'Outer Wilds', '', 'silksont');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('f0fa075f738456f48a3ffeec8e57696e', 'Limbo', '', 'silksont');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('4229352d08f8559282bb8ab1ae651c70', 'Ori and the Will of the Wisps', '', 'silksont');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('3cfef1a1b4a255339b0d9e2aff054017', 'Super Meat Boy', '', 'silksont');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('64f54f8e8e1c56fbb61ee8e6576fb1e3', 'Oxenfree', '', 'plot-twist-el-videojuego');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('2d26d972f9335d71b6c0e44cb7390b06', 'South Park: The Stick of Truth', '', 'plot-twist-el-videojuego');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('e371c4fb00405af08845fd34f33a8288', 'Batman: Arkham Knight', '', 'plot-twist-el-videojuego');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('06661f65176c50c289044dc5b02d65ca', 'Animal Well', '', 'plot-twist-el-videojuego');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('680290536ab5572096eef63a3cfb1bd6', 'Battletoads', '', 'plot-twist-el-videojuego');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('f73eb7a81fad5b3bbf488e99eff91611', 'South Park: The Stick of Truth', '', 'ojo-llameante-de-mordor');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('e937b15945f656f28720a8e9b85d0555', 'Battletoads', '', 'ojo-llameante-de-mordor');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('b58d4b0ff59256d8ad1b8627510f0206', 'Batman: Arkham City', '', 'ojo-llameante-de-mordor');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('12643111764d5112a07bf11215930c61', 'The Hex', '', 'ojo-llameante-de-mordor');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('8c4a1fa7d7445ec493f58649ab82f1b8', 'Batman: Arkham Knight', '', 'ojo-llameante-de-mordor');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('7ff3d23585285287acc2fa02f3f73dca', 'Super Mario Odyssey', '', 'threshold-kids');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('6219ab45bfe4520ab50b069d44ede64b', 'Animal Well', '', 'threshold-kids');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('bf108127180e521aa4d32ad7e68e0fdb', 'Batman: Arkham Knight', '', 'threshold-kids');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('ff0224b5f52f537a8a8f79e25ad8cf30', 'Katana Zero', '', 'threshold-kids');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('ae3955c2b5c75cc1a229b76441a19192', 'Battletoads', '', 'threshold-kids');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('77f0df72f19c5e9b82905927b6489453', 'Batman: Arkham Knight', '', 'caught-in-4k');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('26d5ec0795ff521cb35f683b46ea421d', 'Senua''s Saga: Hellblade II', '', 'caught-in-4k');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('2120f8e63199538c9c8271adba8c008d', 'Little Nightmares II', '', 'caught-in-4k');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('aa82e0f8df0a526aaaaf4bd2b56ce569', 'The Plucky Squire', '', 'caught-in-4k');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('92d0d95d9b8d5bb8a732ed84622cac0b', 'Super Mario Odyssey', '', 'caught-in-4k');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('a3a2e78fedec55eda37aa8b76b5ba700', 'Little Nightmares II', '', 'susto-menor');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('218aa9dfaf035d25bb151f772d42d2e3', 'Oxenfree', '', 'susto-menor');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('68c61ee0a54752f2beb59cc4cd0a415f', 'Oxenfree II: Lost Signals', '', 'susto-menor');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('b9b25e24babf5bf6814ba7a0faec4e03', 'Senua''s Saga: Hellblade II', '', 'susto-menor');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('10fecf7a46a251bba76cb82f65f0c809', 'Batman: Arkham Knight', '', 'susto-menor');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('a38a5eb4202f53a29070aa036ab73bfb', 'Dark Souls', '', 'angers-award');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('6588e8e485125af3a4d63cd748159f53', 'Katana Zero', '', 'angers-award');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('0ad799e12d7758cdbac423deed4cf8bd', 'Batman: Arkham Knight', '', 'angers-award');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('9fde21c938145e43abfd3dcf4e9e646f', 'NieR: Automata', '', 'angers-award');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('3c456e39dba75300a54c46313ef9e14b', 'Hi-Fi Rush', '', 'angers-award');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('ba0d69bc42965070bfc6267ca1b892e4', 'NieR: Automata', '', 'odisea-virtual');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('f35d6e0923fe5fcdb9ab42304ab26b83', 'Batman: Arkham Knight', '', 'odisea-virtual');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('b2c80ce5c0b452e8a23b20d527da32e8', 'Super Mario Odyssey', '', 'odisea-virtual');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('f8587ca1b38d52fa88b77a2a1be130b7', 'Animal Well', '', 'odisea-virtual');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('9aa3ebe0233253f59bd77f462fdb9a55', 'Senua''s Saga: Hellblade II', '', 'odisea-virtual');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('49e9004a452257929b37f683128d7898', 'Dark Souls', '', 'what-is-that-melody');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('1e65606fce715123a0ae7e4c2361ef3d', 'Little Nightmares II', '', 'what-is-that-melody');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('b9cada1a72745965b050c9fde1f1e7f8', 'NieR: Automata', '', 'what-is-that-melody');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('2447f89ebedd572c84a7c08d1a76252d', 'Super Mario Odyssey', '', 'what-is-that-melody');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('97910953d1c6503e88cbae6b9b92b980', 'Neva', '', 'what-is-that-melody');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('7a21660733205806a7b4a04d3678c0fa', 'Dark Souls', 'Gwyn, Lord of Cinder', 'hans-williams');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('74724cfcf3b15f53aac3887aee586eda', 'Little Nightmares II', 'Main Theme', 'hans-williams');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('6e447d33408c5e23a4ca03870f5c470c', 'Super Mario Odyssey', 'Break Free (Lead the Way)', 'hans-williams');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('a17ccbd9bef75fb59124303dce13ae5a', 'NieR: Automata', 'Amusement Park', 'hans-williams');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('c9966d54d52d592282ef79100aab40e3', 'Neva', 'Detour', 'hans-williams');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('27f25036e9415978bdd0615bdb3952f5', 'Super Mario Odyssey', 'Jump Up, Super Star!', 'musica-momento');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('0987af11753e55be902e9a4d071f9893', 'I Expect You To Die 2', 'Intro', 'musica-momento');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('a7c2d247062b5c8cb5ef5091609932f8', 'Batman: Arkham Knight', 'Llévame al Manicomio', 'musica-momento');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('16b113cf91c155a8b8f94e424081f75b', 'Senua''s Saga: Hellblade II', 'Pelea con Ingun', 'musica-momento');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('53e66698203557febfa7870262309f84', 'Hi-Fi Rush', 'Rompiendo la Barrera', 'musica-momento');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('155e6e56e891502e83c6944951aeedd0', 'South Park: Stick of Truth', 'Cartman', 'comedy-bender');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('7fdcbeecce2c5d59b9f8d710f868ad84', 'Batman: Arkham Trilogy', 'Joker', 'comedy-bender');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('a621d70c480b5e5885953d0a359a4a73', 'Hi-Fi Rush', 'CNMN', 'comedy-bender');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('8e6f6b1cfb375e479a91edae6b637592', 'Battletoads', 'Rash', 'comedy-bender');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('5866a60e93e95d779515e92ac18378ee', 'South Park: Stick of Truth', 'Randy', 'comedy-bender');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('2bd208461ca35e20a1a127060aba7451', 'Batman: Arkham Trilogy', 'Joker', 'im-just-ken');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('e2b0078e04f056f2bab6a591bd5d0f30', 'Batman: Arkham Trilogy', 'Batman', 'im-just-ken');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('249af8475f375eaab6273d3b01e0c574', 'South Park: The Stick of Truth', 'Cartman', 'im-just-ken');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('be9b4754b26755b4a6f35d6e37df1bdd', 'Little Nightmares II', 'Mono', 'im-just-ken');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('b299e31e1628527ab7dfe06441f215ae', 'NieR: Automata', '9S', 'im-just-ken');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('910683c9d80e5f6d8324c9eefac464ca', 'Batman: Arkham Knight', 'Bárbara Gordon / Oráculo', 'mujercalculos');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('c0474c0e93e459828fbedf5ff281fb88', 'Senua''s Saga: Hellblade II', 'Senua', 'mujercalculos');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('2c6666d7707d512d92482716c99570b7', 'Oxenfree I y II', 'Alex', 'mujercalculos');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('fd9de00c1c94500292f31b177acab45f', 'Little Nightmares II', 'Six', 'mujercalculos');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('0e5e843535c15474b2220a16d022aa1b', 'Batman: Arkham Knight', 'Hiedra Venenosa', 'mujercalculos');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('07f094aedd635435befc715037bc0535', 'Batman: Arkham Trilogy', 'Joker', 'el-killer-no-tu-abuela');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('d0f53e8644085aeba5b3c796c6387bc5', 'Little Nightmares II', 'The Thin Man', 'el-killer-no-tu-abuela');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('c5433620974c585aa12c8b5156b7ff96', 'Batman: Arkham Knight', 'El Espantapájaros', 'el-killer-no-tu-abuela');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('d924c78f006c500b877d4afecb377812', 'Oxenfree I y II', 'Fantasmas', 'el-killer-no-tu-abuela');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('f7bc609fb415546e91c0095a62f6ac14', 'Dark Souls', 'Artorias', 'el-killer-no-tu-abuela');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('3376100fecf357fe88ce6a0203c0df54', 'Batman: Arkham Trilogy', 'José Padilla (Voz de el Joker en español)',
        'now-that-is-drama');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('ecc6ba447176569d9d56a30708bfae83', 'South Park: The Stick of Truth', 'Trey Parket (Voz original de Cartman)',
        'now-that-is-drama');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('f0560dc300355054b42823b5c6ad3c8b', 'Senua''s Saga: Hellblade II', 'Melina Juergens (Actriz de Senua)',
        'now-that-is-drama');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('edc38cb0aadb5632a796d0f0e983ced5', 'Neva', 'Cristina Peña (Voz internacional de Alba)', 'now-that-is-drama');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('f71c2a82c1785c839a949edc2cf2fbef', 'Batman: Arkham Trilogy', 'Claudio Serrano (Voz de Batman en español)',
        'now-that-is-drama');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('f3468c3437e15fe0a8c882abb0847a33', 'NieR: Automata', 'Final E', 'oscar');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('4805d279e86d57008dce2d45cece8f65', 'Batman: Arkham City', 'Muerte de el Joker', 'oscar');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('1f1ff74bb305527fa4a00a4d1995eeef', 'Batman: Arkham Knight', 'El suicidio de Bárbara', 'oscar');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('7188e1a070055c21bba1c652c57856ef', 'Batman: Arkham Knight', 'Flashbacks de Bárbara', 'oscar');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('0a8a7416c11e53d6a8bc6fe300db2e4c', 'Little Nightmares II', 'Mono se convierte en The Thin Man', 'oscar');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('2669cd17aec351b895c02f0a09067ceb', 'Neva', '', 'pixel-perfect');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('22fcfcdc6e2852acb520135e43dd6645', 'Super Mario Odyssey', '', 'pixel-perfect');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('0ef9a6053c3b58a897f63997294c73ad', 'Senua''s Saga: Hellblade II', '', 'pixel-perfect');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('2e56114845b95a19b443f16c07966d5c', 'Little Nightmares II', '', 'pixel-perfect');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('7ab8990e1cc95819b0d10a023399a28b', 'Animal Well', '', 'pixel-perfect');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('2012ffba38475f858e19cc8ad9656f6f', 'Little Nightmares II', '', 'the-poet-and-the-muse');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('ceecebde6a095b06bc5e728528346aea', 'NieR: Automata', '', 'the-poet-and-the-muse');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('ad8efffae5115656bdf413a14f4fe70e', 'Oxenfree II: Lost Signals', '', 'the-poet-and-the-muse');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('abd5b244d9d9592cacd4b2323b9fa400', 'Batman: Arkham Knight', '', 'the-poet-and-the-muse');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('8d72ceed013b521ba72155b9dc251d1c', 'Senua''s Saga: Hellblade II', '', 'the-poet-and-the-muse');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('18a3c06605bb540aac94cc02a68188a3', 'Animal Well', '', 'mini-lisan-al-gaib-mini-lag');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('c7189c091f50510b879dd7e03bc46169', 'Little Nightmares II', '', 'mini-lisan-al-gaib-mini-lag');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('bc0d2b70aa7f5f1c99ea932cafc4ef0e', 'Neva', '', 'mini-lisan-al-gaib-mini-lag');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('bc713486a0c65e9d93c11f25a977fc5a', 'Oxenfree', '', 'mini-lisan-al-gaib-mini-lag');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('aec86a3337235148ae91a7567e938417', 'Oxenfree II: Lost Signals', '', 'mini-lisan-al-gaib-mini-lag');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('a64cb25fca195f6c834168bfc50bccd5', 'The Plucky Squire', '', 'mini-lisan-al-gaib-mini-lag');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('75976961e12b5ba38c3f3f9beba31965', 'Hi-Fi Rush', '', 'mini-lisan-al-gaib-mini-lag');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('e93996b9ee5e57f1bd1a994a44028934', 'Katana Zero', '', 'mini-lisan-al-gaib-mini-lag');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('c5741616eadd5079a06f2092bfd367eb', 'Super Mario Odyssey', '', 'lisan-al-gaib-lag');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('db128ad048755e6b972407aa6a75d98b', 'Animal Well', '', 'lisan-al-gaib-lag');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('ef9ce957d73a541ab96f522a62a8433a', 'Batman: Arkham Knight', '', 'lisan-al-gaib-lag');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('ec46855bbf925d269b17aefa0fd8cd52', 'Little Nightmares II', '', 'lisan-al-gaib-lag');
INSERT INTO nominations(id, game_title, nominee, award)
VALUES ('26d9857cd0555d9db517540f6d6dee42', 'NieR: Automata', '', 'lisan-al-gaib-lag');

-- VIDEOCLIPS
INSERT INTO videoclips(id, url)
VALUES (1, 'https://www.youtube.com/watch?v=3wHOhOPHpYE&ab_channel=SaulAntonioGonzalezLopez');
INSERT INTO videoclips(id, url)
VALUES (2, 'https://www.youtube.com/watch?v=FxgwIP4Cqpc&ab_channel=PlayStation');
INSERT INTO videoclips(id, url)
VALUES (3, 'https://www.youtube.com/watch?v=Pz8YkV1YmM0&ab_channel=CINEMATICGAMING');
INSERT INTO videoclips(id, url)
VALUES (4, 'https://www.youtube.com/watch?v=S5846AJ898U&ab_channel=PlayStation');
INSERT INTO videoclips(id, url)
VALUES (5, 'https://www.youtube.com/watch?v=uAn7OxLub9Y&ab_channel=PlayStation');
INSERT INTO videoclips(id, url)
VALUES (6, 'https://www.youtube.com/watch?v=d6LGnVCL1_A&t=26s&ab_channel=GameSpotTrailers');
INSERT INTO videoclips(id, url)
VALUES (7, 'https://www.youtube.com/watch?v=PpcPK2okylM&ab_channel=NintendoofAmerica');
INSERT INTO videoclips(id, url)
VALUES (8, 'https://www.youtube.com/watch?v=2reK8k8nwBc&ab_channel=Xbox');
INSERT INTO videoclips(id, url)
VALUES (9, 'https://www.youtube.com/watch?v=snaionoxjos&ab_channel=IGN');
INSERT INTO videoclips(id, url)
VALUES (10, 'https://www.youtube.com/watch?v=7QWYD9XXSQ8&ab_channel=GamingPicks');
INSERT INTO videoclips(id, url)
VALUES (11, 'https://www.youtube.com/watch?v=5BRBR_KR0Ww&ab_channel=ITSHAWK95games');
INSERT INTO videoclips(id, url)
VALUES (12, 'https://www.youtube.com/watch?v=-VwgNeTyseQ&ab_channel=LegendsForeverStudios');
INSERT INTO videoclips(id, url)
VALUES (13, 'https://www.youtube.com/watch?v=i4YnLI6UpTA&t=44s&ab_channel=FuryForged');
INSERT INTO videoclips(id, url)
VALUES (14, 'https://www.youtube.com/watch?v=pwPB6_g3sq4&ab_channel=Xbox');
INSERT INTO videoclips(id, url)
VALUES (15, 'https://www.youtube.com/watch?v=vWH2EcA2usc&ab_channel=TheGOODKyle');
INSERT INTO videoclips(id, url)
VALUES (16, 'https://www.youtube.com/watch?v=v9q3otAKuaw&ab_channel=Kakuchopurei');
INSERT INTO videoclips(id, url)
VALUES (17, 'https://drive.google.com/file/d/1YmJuHJsBTwC8TjsCVu_ylXAjpPEZIddh/view?usp=sharing');
INSERT INTO videoclips(id, url)
VALUES (18, 'https://youtu.be/vilYcBpUn0s?t=2235');
INSERT INTO videoclips(id, url)
VALUES (19, 'https://www.youtube.com/watch?v=SWXWQ8S4xGQ&ab_channel=trastendo');
INSERT INTO videoclips(id, url)
VALUES (20, 'https://www.youtube.com/watch?v=p0bENYZnH6c');
INSERT INTO videoclips(id, url)
VALUES (21, 'https://www.youtube.com/watch?v=BykX5MZePU4');
INSERT INTO videoclips(id, url)
VALUES (22, 'https://www.youtube.com/watch?v=AKqhThk0msc');
INSERT INTO videoclips(id, url)
VALUES (23, 'https://www.youtube.com/watch?v=BXyl85yH1bo&ab_channel=DoriDoriko');
INSERT INTO videoclips(id, url)
VALUES (24, 'https://www.youtube.com/watch?v=xUgHUuvhK9I');
INSERT INTO videoclips(id, url)
VALUES (25, 'https://www.youtube.com/watch?v=GYAI3C7m7Zs&ab_channel=TheBeautyOf');
INSERT INTO videoclips(id, url)
VALUES (26, 'https://www.youtube.com/watch?v=hRv21LqmpRA&ab_channel=DefendTheHouse');
INSERT INTO videoclips(id, url)
VALUES (27, 'https://www.youtube.com/watch?v=kz_8gBOyZko&ab_channel=OGTeckl');
INSERT INTO videoclips(id, url)
VALUES (28, 'https://www.youtube.com/watch?v=tQtaYB712BY&ab_channel=PlayStationLatinoam%C3%A9rica');
INSERT INTO videoclips(id, url)
VALUES (29, 'https://www.youtube.com/watch?v=eE5ZF3hNKak&ab_channel=NintendoEspa%C3%B1a');
INSERT INTO videoclips(id, url)
VALUES (30, 'https://www.youtube.com/watch?v=ThDr_LKn9xk');
INSERT INTO videoclips(id, url)
VALUES (31, 'https://www.youtube.com/watch?v=qZ1sAPaezpk');
INSERT INTO videoclips(id, url)
VALUES (32, 'https://www.youtube.com/watch?v=19W51CwKoi4');
INSERT INTO videoclips(id, url)
VALUES (33, 'https://www.youtube.com/watch?v=FaybESjwj0Y');
INSERT INTO videoclips(id, url)
VALUES (34, 'https://www.youtube.com/watch?v=mDrfuM7nemQ');
INSERT INTO videoclips(id, url)
VALUES (35, 'https://www.youtube.com/watch?v=NBLXISw6fcc&ab_channel=TheBradgicShow');
INSERT INTO videoclips(id, url)
VALUES (36, 'https://www.youtube.com/watch?v=HVxqr21c54M');
INSERT INTO videoclips(id, url)
VALUES (37, 'https://www.youtube.com/watch?v=bC8-EyZlvKk&ab_channel=MoonArkham');
INSERT INTO videoclips(id, url)
VALUES (38, 'https://www.youtube.com/watch?v=BCzYSMsOMWA&ab_channel=TyrellCorp');
INSERT INTO videoclips(id, url)
VALUES (39, 'https://www.youtube.com/watch?v=twfJU6teQ4w&ab_channel=Anikiz');
INSERT INTO videoclips(id, url)
VALUES (40, 'https://www.youtube.com/watch?v=SyVqjTenLLk&ab_channel=Timinator74');
INSERT INTO videoclips(id, url)
VALUES (41, 'https://www.youtube.com/watch?v=JAv0jk1184g&ab_channel=CodigoJuegos');
INSERT INTO videoclips(id, url)
VALUES (42,
        'https://www.youtube.com/watch?v=_fHtdScD7QY&ab_channel=%E2%84%B0%E2%84%92%E2%84%9B%F0%9D%92%9C%F0%9D%92%AB%F0%9D%92%AF%F0%9D%92%AA%E2%84%9B%F0%9D%92%AE%F0%9D%92%B0%F0%9D%92%AB%E2%84%9B%E2%84%B0%E2%84%B3%F0%9D%92%AA');
INSERT INTO videoclips(id, url)
VALUES (43, 'https://www.youtube.com/watch?v=VvtARsnQERI&ab_channel=ChaosNLD');
INSERT INTO videoclips(id, url)
VALUES (44, 'https://www.youtube.com/watch?v=cB7_S7IKMF4&t=436s&ab_channel=DanAllenGaming');
INSERT INTO videoclips(id, url)
VALUES (45, 'https://www.youtube.com/watch?v=gg626me8mxA&ab_channel=MaestroVirgoreo');
INSERT INTO videoclips(id, url)
VALUES (46, 'https://www.youtube.com/watch?v=VmTQxJjvCps&ab_channel=TobiasLilja-Topic');
INSERT INTO videoclips(id, url)
VALUES (47, 'https://www.youtube.com/watch?v=yW5AnWT1d5E&ab_channel=Skwiddlly');
INSERT INTO videoclips(id, url)
VALUES (48, 'https://www.youtube.com/watch?v=Hqe9CIHO5gw&ab_channel=GamersPrey');
INSERT INTO videoclips(id, url)
VALUES (49, 'https://www.youtube.com/watch?v=mQfK8JIrtlQ&t=1491s&ab_channel=GamersPrey');
INSERT INTO videoclips(id, url)
VALUES (50, 'https://www.youtube.com/watch?v=VIeqxGaZnFo&ab_channel=BossFightDatabase');
INSERT INTO videoclips(id, url)
VALUES (51, 'https://www.youtube.com/watch?v=e3l2WEqLApQ&ab_channel=GamesMusic');
INSERT INTO videoclips(id, url)
VALUES (52, 'https://www.youtube.com/watch?v=t7qQzM_Vs9Y&ab_channel=Sadwich');
INSERT INTO videoclips(id, url)
VALUES (53, 'https://www.youtube.com/watch?v=hNdc9LRH25w&ab_channel=Skwiddlly');
INSERT INTO videoclips(id, url)
VALUES (54, 'https://www.youtube.com/watch?v=dotWGSv2kug&ab_channel=BeatsAndPixels');
INSERT INTO videoclips(id, url)
VALUES (55, 'https://www.youtube.com/watch?v=h1IHvzwUd6w&ab_channel=AFGuidesHD');
INSERT INTO videoclips(id, url)
VALUES (56, 'https://www.youtube.com/watch?v=pQE7jf9LCfk&ab_channel=SchellGames');
INSERT INTO videoclips(id, url)
VALUES (57, 'https://www.youtube.com/watch?v=brue4xDkdgc&ab_channel=Dafits1997');
INSERT INTO videoclips(id, url)
VALUES (58,
        'https://www.youtube.com/watch?v=KClWfvrHL_I&ab_channel=KimchiTekken%28%EA%B9%80%EC%B9%98%E9%89%84%E6%8B%B3%29');
INSERT INTO videoclips(id, url)
VALUES (59, 'https://www.youtube.com/watch?v=vWH2EcA2usc&t=52s&ab_channel=TheGOODKyle');
INSERT INTO videoclips(id, url)
VALUES (60, 'https://www.youtube.com/watch?v=ENKAPRTtCLg&ab_channel=DarkPlayerGamingTV');
INSERT INTO videoclips(id, url)
VALUES (61, 'https://www.youtube.com/watch?v=PyCC1ZIJXzo&ab_channel=RaRa');
INSERT INTO videoclips(id, url)
VALUES (62, 'https://www.youtube.com/watch?v=IHwYyHt1XAk&ab_channel=Strike-Games');
INSERT INTO videoclips(id, url)
VALUES (63, 'https://www.youtube.com/watch?v=pA1D61jKnjs&ab_channel=Chelone');
INSERT INTO videoclips(id, url)
VALUES (64, 'https://www.youtube.com/watch?v=BnS2r_guf3Y&ab_channel=RockDevil');
INSERT INTO videoclips(id, url)
VALUES (65, 'https://www.youtube.com/watch?v=exPN3-80hJE&ab_channel=DarkPlayerGamingTV');
INSERT INTO videoclips(id, url)
VALUES (66, 'https://www.youtube.com/watch?v=LqcHuW9DSlM&ab_channel=RAMBROplays');
INSERT INTO videoclips(id, url)
VALUES (67, 'https://www.youtube.com/watch?v=-fTEXaA6Y1s&ab_channel=SantaHavelyn');
INSERT INTO videoclips(id, url)
VALUES (68, 'https://www.youtube.com/watch?v=F2mtxwRwA5o&t=877s&ab_channel=mykado33');
INSERT INTO videoclips(id, url)
VALUES (69, 'https://www.youtube.com/watch?v=FaybESjwj0Y&t=52s&ab_channel=VGS-VideoGameSophistry');
INSERT INTO videoclips(id, url)
VALUES (70, 'https://www.youtube.com/watch?v=SIIIdemMmAw&ab_channel=Duck360Gaming');
INSERT INTO videoclips(id, url)
VALUES (71, 'https://www.youtube.com/watch?v=Y3ZpeeqcPeI&t=1255s&ab_channel=GameClips');
INSERT INTO videoclips(id, url)
VALUES (72, 'https://www.youtube.com/watch?v=phXstMZCro8&ab_channel=CodigoJuegos');
INSERT INTO videoclips(id, url)
VALUES (73, 'https://www.youtube.com/watch?v=ocZwsrcQD2A&ab_channel=M.Silva23');
INSERT INTO videoclips(id, url)
VALUES (74, 'https://www.youtube.com/watch?v=6joAqIFEF_Y&ab_channel=Trophygamers');
INSERT INTO videoclips(id, url)
VALUES (75, 'https://www.youtube.com/watch?v=ajzlx4NuLqY&ab_channel=PoopyFungus');
INSERT INTO videoclips(id, url)
VALUES (76, 'https://www.youtube.com/watch?v=rgy1TV12LDc&ab_channel=BossFightDatabase');
INSERT INTO videoclips(id, url)
VALUES (77, 'https://www.youtube.com/watch?v=zfsbwhJvDAA&ab_channel=trastendo');
INSERT INTO videoclips(id, url)
VALUES (78, 'https://www.youtube.com/watch?v=De5C_p9LQt0&ab_channel=TARFUGAMING');
INSERT INTO videoclips(id, url)
VALUES (79, 'https://www.youtube.com/watch?v=K1qG8pREfkA&ab_channel=NinjaTheory');
INSERT INTO videoclips(id, url)
VALUES (80, 'https://www.youtube.com/watch?v=UWIDTJXtq_o&t=4121s&ab_channel=EGLikeDislike');
INSERT INTO videoclips(id, url)
VALUES (81, 'https://www.youtube.com/watch?v=DAsN4fRJa0s&ab_channel=iCRec');
INSERT INTO videoclips(id, url)
VALUES (82, 'https://www.youtube.com/watch?v=jO4v_oMJV3A&ab_channel=PCFriends');
INSERT INTO videoclips(id, url)
VALUES (83, 'https://www.youtube.com/watch?v=mnrDlYWf0Io&t=671s&ab_channel=SEIJASYT');
INSERT INTO videoclips(id, url)
VALUES (84, 'https://www.youtube.com/watch?v=FbjnBi0d7xo&ab_channel=PipeVildosoCastillo');
INSERT INTO videoclips(id, url)
VALUES (85, 'https://www.youtube.com/watch?v=UF01VAvGbV4&ab_channel=Seccussion');
INSERT INTO videoclips(id, url)
VALUES (86, 'https://www.youtube.com/watch?v=uBGvGpeRp1E&ab_channel=PlayStationAsia');
INSERT INTO videoclips(id, url)
VALUES (87, 'https://www.youtube.com/watch?v=Re1JVXOVeWs&ab_channel=Game_track');
INSERT INTO videoclips(id, url)
VALUES (88, 'https://www.youtube.com/watch?v=vbZBmxwQBTI&ab_channel=WendellJ.Silva');
INSERT INTO videoclips(id, url)
VALUES (89, 'https://www.youtube.com/watch?v=IFaYrge3N3M');
INSERT INTO videoclips(id, url)
VALUES (90,
        'https://www.youtube.com/watch?v=4dQ4wGHuCNg&list=PLSQoPnd2HxhIk87_Qj9rX373v1TqA14jk&ab_channel=ValbuenaGames');
INSERT INTO videoclips(id, url)
VALUES (91, 'https://www.youtube.com/watch?v=idC50yINioU&ab_channel=GameClips');
INSERT INTO videoclips(id, url)
VALUES (92, 'https://www.youtube.com/watch?v=4xEEwZsO_H8&ab_channel=MannyMaxo');
INSERT INTO videoclips(id, url)
VALUES (93, 'https://www.youtube.com/watch?v=OKZyTpiHDUA&ab_channel=FPGoodGame');
INSERT INTO videoclips(id, url)
VALUES (94, 'https://www.youtube.com/watch?v=DNsWRPDh0Lg&ab_channel=ConiferousRobot');
INSERT INTO videoclips(id, url)
VALUES (95, 'https://www.youtube.com/watch?v=oUp7w8g6QZA&ab_channel=YOGSCASTKim');
INSERT INTO videoclips(id, url)
VALUES (96, 'https://www.youtube.com/watch?v=_fZ8IVSU5UY&ab_channel=EnigMind');
INSERT INTO videoclips(id, url)
VALUES (97, 'https://www.youtube.com/watch?v=5geFbB4vt_c&ab_channel=IntroGameOver');
INSERT INTO videoclips(id, url)
VALUES (98, 'https://www.youtube.com/watch?v=qcEWLizh6gQ&ab_channel=Levas');
INSERT INTO videoclips(id, url)
VALUES (99, 'https://www.youtube.com/watch?v=etta-lXMLe0&ab_channel=8rgk');
INSERT INTO videoclips(id, url)
VALUES (100, 'https://www.youtube.com/watch?v=Jb1hY8-9aO8&ab_channel=ProsafiaGaming');
INSERT INTO videoclips(id, url)
VALUES (101, 'https://www.youtube.com/watch?v=wWGtVJUtgjQ&ab_channel=Str1d3r08000');
INSERT INTO videoclips(id, url)
VALUES (102, 'https://www.youtube.com/watch?v=x5C6OpKe8w4&ab_channel=Kratosworld');
INSERT INTO videoclips(id, url)
VALUES (103, 'https://www.youtube.com/watch?v=gKCvphbCpPE&ab_channel=GameplayOnly');
INSERT INTO videoclips(id, url)
VALUES (104, 'https://www.youtube.com/watch?v=_v9Ivu4KHso&ab_channel=BossFightDatabase');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('8f3466a7364a5240a4780eabae1e0711', 1, '00:00:00', '00:00:30');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('58633d1221395bbcaa798dcdc831ae3d', 2, '00:00:30', '00:01:00');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('0554185d80ff56918d978079b69b9ee3', 3, '00:03:54', '00:04:24');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('83676e34031e5647a877a4a171b9a8a2', 4, '00:00:26', '00:00:56');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('c36dcf6e9b565ce88669be11f895ccbb', 5, '00:00:22', '00:00:52');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('a7023fc67b8c5238a2a69727be98642c', 6, '00:00:04', '00:00:34');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('f0fa075f738456f48a3ffeec8e57696e', 7, '00:00:06', '00:00:36');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('4229352d08f8559282bb8ab1ae651c70', 8, '00:00:50', '00:01:20');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('3cfef1a1b4a255339b0d9e2aff054017', 9, '00:00:00', '00:00:30');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('64f54f8e8e1c56fbb61ee8e6576fb1e3', 10, '00:00:58', '00:01:28');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('2d26d972f9335d71b6c0e44cb7390b06', 11, '00:00:30', '00:01:00');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('e371c4fb00405af08845fd34f33a8288', 12, '00:00:00', '00:00:30');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('06661f65176c50c289044dc5b02d65ca', 13, '00:17:02', '00:17:32');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('680290536ab5572096eef63a3cfb1bd6', 14, '00:00:57', '00:01:27');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('f73eb7a81fad5b3bbf488e99eff91611', 15, '00:00:52', '00:01:18');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('e937b15945f656f28720a8e9b85d0555', 16, '00:00:20', '00:00:50');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('b58d4b0ff59256d8ad1b8627510f0206', 17, '00:00:00', '00:00:28');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('12643111764d5112a07bf11215930c61', 18, '00:37:21', '00:37:51');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('8c4a1fa7d7445ec493f58649ab82f1b8', 19, '00:00:10', '00:00:29');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('7ff3d23585285287acc2fa02f3f73dca', 20, '00:00:34', '00:00:57');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('6219ab45bfe4520ab50b069d44ede64b', 21, '00:00:00', '00:00:21');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('bf108127180e521aa4d32ad7e68e0fdb', 22, '00:00:00', '00:00:30');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('ff0224b5f52f537a8a8f79e25ad8cf30', 23, '00:00:00', '00:00:40');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('ae3955c2b5c75cc1a229b76441a19192', 24, '00:16:03', '00:16:33');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('77f0df72f19c5e9b82905927b6489453', 25, '00:00:16', '00:00:56');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('26d5ec0795ff521cb35f683b46ea421d', 26, '00:02:37', '00:03:07');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('2120f8e63199538c9c8271adba8c008d', 27, '00:01:00', '00:01:32');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('aa82e0f8df0a526aaaaf4bd2b56ce569', 28, '00:00:20', '00:00:50');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('92d0d95d9b8d5bb8a732ed84622cac0b', 29, '00:00:40', '00:01:10');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('a3a2e78fedec55eda37aa8b76b5ba700', 30, '00:02:10', '00:02:40');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('218aa9dfaf035d25bb151f772d42d2e3', 31, '00:02:38', '00:03:08');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('68c61ee0a54752f2beb59cc4cd0a415f', 32, '00:02:07', '00:02:37');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('b9b25e24babf5bf6814ba7a0faec4e03', 33, '00:00:25', '00:00:59');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('10fecf7a46a251bba76cb82f65f0c809', 34, '00:04:35', '00:05:14');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('a38a5eb4202f53a29070aa036ab73bfb', 35, '00:00:07', '00:00:47');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('6588e8e485125af3a4d63cd748159f53', 36, '00:12:33', '00:13:03');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('0ad799e12d7758cdbac423deed4cf8bd', 37, '00:00:00', '00:00:30');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('9fde21c938145e43abfd3dcf4e9e646f', 38, '00:00:00', '00:00:30');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('3c456e39dba75300a54c46313ef9e14b', 39, '00:00:00', '00:00:27');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('ba0d69bc42965070bfc6267ca1b892e4', 40, '00:00:24', '00:00:54');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('f35d6e0923fe5fcdb9ab42304ab26b83', 41, '00:03:13', '00:03:43');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('b2c80ce5c0b452e8a23b20d527da32e8', 42, '00:00:00', '00:00:30');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('f8587ca1b38d52fa88b77a2a1be130b7', 43, '00:01:34', '00:02:04');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('9aa3ebe0233253f59bd77f462fdb9a55', 44, '00:00:55', '00:01:25');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('49e9004a452257929b37f683128d7898', 45, '00:00:00', '00:00:30');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('1e65606fce715123a0ae7e4c2361ef3d', 46, '00:00:38', '00:01:08');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('b9cada1a72745965b050c9fde1f1e7f8', 47, '00:00:00', '00:00:30');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('2447f89ebedd572c84a7c08d1a76252d', 48, '00:03:08', '00:03:40');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('97910953d1c6503e88cbae6b9b92b980', 49, '00:56:47', '00:57:17');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('7a21660733205806a7b4a04d3678c0fa', 50, '00:00:00', '00:00:30');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('74724cfcf3b15f53aac3887aee586eda', 51, '00:01:00', '00:01:30');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('6e447d33408c5e23a4ca03870f5c470c', 52, '00:00:00', '00:00:30');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('a17ccbd9bef75fb59124303dce13ae5a', 53, '00:00:00', '00:00:32');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('c9966d54d52d592282ef79100aab40e3', 54, '00:01:33', '00:02:03');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('27f25036e9415978bdd0615bdb3952f5', 55, '00:04:40', '00:05:11');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('0987af11753e55be902e9a4d071f9893', 56, '00:01:40', '00:02:10');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('a7c2d247062b5c8cb5ef5091609932f8', 57, '00:00:00', '00:00:30');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('16b113cf91c155a8b8f94e424081f75b', 44, '00:06:10', '00:06:40');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('53e66698203557febfa7870262309f84', 58, '00:03:09', '00:03:45');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('155e6e56e891502e83c6944951aeedd0', 59, '00:00:06', '00:00:34');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('7fdcbeecce2c5d59b9f8d710f868ad84', 60, '00:27:00', '00:27:40');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('a621d70c480b5e5885953d0a359a4a73', 61, '00:00:20', '00:00:43');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('8e6f6b1cfb375e479a91edae6b637592', 62, '00:17:53', '00:18:29');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('5866a60e93e95d779515e92ac18378ee', 63, '00:00:00', '00:00:30');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('2bd208461ca35e20a1a127060aba7451', 64, '00:54:45', '00:55:17');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('e2b0078e04f056f2bab6a591bd5d0f30', 65, '00:24:41', '00:25:13');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('249af8475f375eaab6273d3b01e0c574', 59, '00:08:52', '00:09:18');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('be9b4754b26755b4a6f35d6e37df1bdd', 66, '00:05:25', '00:05:55');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('b299e31e1628527ab7dfe06441f215ae', 67, '00:02:57', '00:03:27');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('910683c9d80e5f6d8324c9eefac464ca', 68, '00:02:10', '00:02:45');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('c0474c0e93e459828fbedf5ff281fb88', 69, '00:02:26', '00:02:56');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('2c6666d7707d512d92482716c99570b7', 70, '00:05:11', '00:05:47');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('fd9de00c1c94500292f31b177acab45f', 71, '00:17:59', '00:18:38');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('0e5e843535c15474b2220a16d022aa1b', 72, '00:00:10', '00:00:47');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('07f094aedd635435befc715037bc0535', 73, '00:00:05', '00:00:35');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('d0f53e8644085aeba5b3c796c6387bc5', 74, '00:01:05', '00:01:35');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('c5433620974c585aa12c8b5156b7ff96', 65, '00:10:01', '00:10:45');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('d924c78f006c500b877d4afecb377812', 75, '00:00:00', '00:00:28');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('f7bc609fb415546e91c0095a62f6ac14', 76, '00:00:00', '00:00:39');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('3376100fecf357fe88ce6a0203c0df54', 77, '00:00:00', '00:00:31');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('ecc6ba447176569d9d56a30708bfae83', 78, '00:00:00', '00:00:37');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('f0560dc300355054b42823b5c6ad3c8b', 79, '00:00:25', '00:00:59');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('edc38cb0aadb5632a796d0f0e983ced5', 80, '00:24:49', '00:25:08');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('f71c2a82c1785c839a949edc2cf2fbef', 81, '00:01:57', '00:02:41');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('f3468c3437e15fe0a8c882abb0847a33', 82, '00:24:01', '00:24:31');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('4805d279e86d57008dce2d45cece8f65', 83, '00:10:20', '00:11:16');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('1f1ff74bb305527fa4a00a4d1995eeef', 84, '00:00:49', '00:01:38');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('7188e1a070055c21bba1c652c57856ef', 41, '00:00:02', '00:01:00');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('0a8a7416c11e53d6a8bc6fe300db2e4c', 71, '00:20:35', '00:21:37');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('2669cd17aec351b895c02f0a09067ceb', 85, '00:02:00', '00:02:30');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('22fcfcdc6e2852acb520135e43dd6645', 29, '00:01:17', '00:02:47');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('0ef9a6053c3b58a897f63997294c73ad', 26, '00:00:00', '00:00:30');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('2e56114845b95a19b443f16c07966d5c', 27, '00:00:00', '00:00:30');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('7ab8990e1cc95819b0d10a023399a28b', 86, '00:00:01', '00:00:24');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('2012ffba38475f858e19cc8ad9656f6f', 87, '00:42:26', '00:42:56');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('ceecebde6a095b06bc5e728528346aea', 88, '00:00:00', '00:00:30');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('ad8efffae5115656bdf413a14f4fe70e', 89, '00:10:37', '00:11:07');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('abd5b244d9d9592cacd4b2323b9fa400', 90, '00:03:50', '00:04:20');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('8d72ceed013b521ba72155b9dc251d1c', 91, '03:01:15', '03:01:59');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('18a3c06605bb540aac94cc02a68188a3', 92, '00:00:22', '00:01:10');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('c7189c091f50510b879dd7e03bc46169', 93, '00:00:00', '00:00:39');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('bc0d2b70aa7f5f1c99ea932cafc4ef0e', 94, '00:01:00', '00:01:45');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('bc713486a0c65e9d93c11f25a977fc5a', 95, '00:02:15', '00:03:04');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('aec86a3337235148ae91a7567e938417', 96, '00:30:25', '00:31:24');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('a64cb25fca195f6c834168bfc50bccd5', 97, '00:22:27', '00:23:15');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('75976961e12b5ba38c3f3f9beba31965', 98, '00:05:48', '00:06:38');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('e93996b9ee5e57f1bd1a994a44028934', 99, '00:00:50', '00:01:40');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('c5741616eadd5079a06f2092bfd367eb', 100, '00:02:49', '00:03:37');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('db128ad048755e6b972407aa6a75d98b', 101, '00:05:11', '00:05:45');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('ef9ce957d73a541ab96f522a62a8433a', 102, '03:56:52', '03:57:59');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('ec46855bbf925d269b17aefa0fd8cd52', 103, '00:00:37', '00:01:25');
INSERT INTO video_options(nomination, videoclip, timestamp_start, timestamp_end)
VALUES ('26d9857cd0555d9db517540f6d6dee42', 104, '00:01:30', '00:02:25');
