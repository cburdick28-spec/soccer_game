NEW_BLOCK = '''    if position_group == "Forward":
        return [
            # 0 \u2013 Youth Academy (16-18)
            [
                (
                    "{name} arrived at the academy as a pacy {style}, terrorising defenders in reserve fixtures. "
                    "The first-team manager kept a close eye on this emerging talent.",
                    ("Push for a first-team debut this season",                  {"goals": 4,  "assists": 2,  "trophies": 0, "caps": 0}),
                    ("Accept a loan to a lower-league club for more minutes",    {"goals": 9,  "assists": 3,  "trophies": 0, "caps": 0}),
                    ("Seek a trial abroad at a European club for a fresh challenge", {"goals": 6,  "assists": 4,  "trophies": 0, "caps": 0}),
                ),
                (
                    "Even in youth football, {name}\'s {style} instincts were impossible to ignore \u2014 "
                    "scouts from three countries watched a hat-trick that left coaches speechless.",
                    ("Dominate the reserve league and force the manager\'s hand for a senior call-up", {"goals": 7,  "assists": 2,  "trophies": 0, "caps": 0}),
                    ("Commit to a specialised finishing bootcamp to sharpen the goal threat",          {"goals": 5,  "assists": 3,  "trophies": 0, "caps": 0}),
                    ("Accept a short-term loan to gain senior minutes in a competitive lower division", {"goals": 8,  "assists": 4,  "trophies": 0, "caps": 0}),
                ),
                (
                    "The academy director described {name} as \'once in a decade\' \u2014 a {style} with hunger in the eyes "
                    "and thunder in the boots. The only question was which path to take first.",
                    ("Immerse in an elite youth tournament abroad and announce {name} to the world",   {"goals": 6,  "assists": 5,  "trophies": 0, "caps": 0}),
                    ("Stay close to home and build chemistry with fellow academy graduates",            {"goals": 5,  "assists": 3,  "trophies": 0, "caps": 0}),
                    ("Push the coaching staff hard for a professional contract a year early",           {"goals": 8,  "assists": 2,  "trophies": 0, "caps": 0}),
                ),
            ],
            # 1 \u2013 Professional Debut (18-21)
            [
                (
                    "Turning professional, {name}\'s sharp movement and instinctive finishing attracted interest from across Europe. "
                    "Two very different paths lay ahead.",
                    ("Sign for a top-flight giant and fight for a squad role",   {"goals": 14, "assists": 8,  "trophies": 1, "caps": 5}),
                    ("Choose a mid-table club for guaranteed first-team minutes", {"goals": 22, "assists": 10, "trophies": 0, "caps": 8}),
                    ("Move abroad to a foreign league as a young starter",        {"goals": 18, "assists": 6,  "trophies": 0, "caps": 12}),
                ),
                (
                    "The professional world is fierce, but {name}\'s {style} gave opponents nightmares from the first whistle. "
                    "A breakout debut season demanded a bold next step.",
                    ("Join a promotion-chasing Championship club as the main striker",               {"goals": 20, "assists": 7,  "trophies": 0, "caps": 6}),
                    ("Sign a multi-year deal with a top-flight club and earn minutes off the bench", {"goals": 15, "assists": 9,  "trophies": 1, "caps": 4}),
                    ("Pursue a high-profile loan to a Serie A side known for developing forwards",   {"goals": 17, "assists": 8,  "trophies": 0, "caps": 10}),
                ),
                (
                    "Scouts had been whispering {name}\'s name for months \u2014 and the debut season silenced all doubters. "
                    "A {style} with 20 goals in a debut campaign had the world at their feet.",
                    ("Accept a starting berth at a Bundesliga club with a renowned attacking system", {"goals": 19, "assists": 7,  "trophies": 0, "caps": 9}),
                    ("Stay in the domestic league and target a top-six finish with an ambitious club", {"goals": 16, "assists": 10, "trophies": 1, "caps": 7}),
                    ("Gamble on a rising La Liga side where the style of play suits perfectly",        {"goals": 21, "assists": 6,  "trophies": 0, "caps": 11}),
                ),
            ],
            # 2 \u2013 Rising Star (21-24)
            [
                (
                    "A prolific season has made {name} one of the hottest properties in world football. "
                    "Champions League clubs are circling and the phone hasn\'t stopped ringing.",
                    ("Join a Champions League contender",                        {"goals": 30, "assists": 15, "trophies": 2, "caps": 15}),
                    ("Become the undisputed main man at an ambitious club",      {"goals": 45, "assists": 18, "trophies": 1, "caps": 20}),
                    ("Accept the captain\'s armband and rebuild a fallen giant",  {"goals": 38, "assists": 22, "trophies": 2, "caps": 18}),
                ),
                (
                    "The numbers are staggering \u2014 {name}\'s {style} has produced 30 goals and the world wants more. "
                    "Two heavyweight clubs have lodged rival bids in the same week.",
                    ("Sign for the reigning European champions and compete at the highest level immediately", {"goals": 32, "assists": 14, "trophies": 2, "caps": 16}),
                    ("Lead a mid-table giant\'s attacking line and shatter the club scoring record",           {"goals": 42, "assists": 17, "trophies": 1, "caps": 19}),
                    ("Accept a dream move to a storied South American club and inspire their continental run", {"goals": 36, "assists": 20, "trophies": 2, "caps": 17}),
                ),
                (
                    "Three hat-tricks in a month. Nine away goals in Europe. {name} is a phenomenon \u2014 and every elite club "
                    "in the world now knows the name.",
                    ("Join an elite Spanish club and thrive in the world\'s most watched league",   {"goals": 35, "assists": 16, "trophies": 2, "caps": 14}),
                    ("Commit to the current club on a record-breaking new contract and dominate domestically", {"goals": 44, "assists": 19, "trophies": 1, "caps": 21}),
                    ("Make a stunning move to a Premier League contender and light up English football",       {"goals": 39, "assists": 21, "trophies": 2, "caps": 17}),
                ),
            ],
            # 3 \u2013 Breakout Season (24-26)
            [
                (
                    "The footballing world is watching {name}. A spectacular individual campaign has produced record-breaking numbers "
                    "and sparked a transfer frenzy. Two life-changing paths have emerged.",
                    ("Stay and break the club scoring record before moving on",  {"goals": 38, "assists": 14, "trophies": 1, "caps": 12}),
                    ("Accept a marquee transfer and prove brilliance in a new top flight", {"goals": 30, "assists": 16, "trophies": 2, "caps": 10}),
                    ("Join a rival league abroad to prove world-class status globally", {"goals": 34, "assists": 20, "trophies": 2, "caps": 14}),
                ),
                (
                    "They are calling {name} the most lethal {style} of a generation. The goals, the drama, the audacity \u2014 "
                    "and now a choice that will define the next decade.",
                    ("Extend the contract and chase the league title with an electrifying current squad", {"goals": 36, "assists": 15, "trophies": 2, "caps": 11}),
                    ("Shock the football world with a move to a rival domestic club to deliver a title",  {"goals": 32, "assists": 17, "trophies": 1, "caps": 13}),
                    ("Make history with a record-fee transfer abroad and become an icon in a new country", {"goals": 33, "assists": 19, "trophies": 2, "caps": 15}),
                ),
                (
                    "Golden boots. Player of the Year. {name}\'s {style} brilliance is impossible to contain \u2014 "
                    "and the summer promises the most dramatic transfer saga in years.",
                    ("Stay for one final defining season before a free-transfer mega-move",            {"goals": 40, "assists": 13, "trophies": 1, "caps": 10}),
                    ("Accept a world-record fee and lead an ambitious club\'s title charge",             {"goals": 31, "assists": 18, "trophies": 2, "caps": 12}),
                    ("Orchestrate a shock Ligue 1 or Eredivisie move to dominate a new country",       {"goals": 35, "assists": 21, "trophies": 2, "caps": 14}),
                ),
            ],
            # 4 \u2013 Peak Years (26-29)
            [
                (
                    "At 26, {name} is feared by every defence. A world-record offer arrives \u2014 "
                    "but so does the chance to cement legendary status at a beloved club.",
                    ("Accept the mega-money move to the wealthiest club",        {"goals": 42, "assists": 22, "trophies": 3, "caps": 20}),
                    ("Stay loyal and chase the title with a beloved club",       {"goals": 55, "assists": 28, "trophies": 4, "caps": 25}),
                    ("Take an unprecedented player-captain role and drive a title from within", {"goals": 48, "assists": 25, "trophies": 3, "caps": 22}),
                ),
                (
                    "There is no stopping {name} \u2014 a {style} in irresistible form, terrorising defenders across every competition. "
                    "The sport\'s biggest clubs are locked in a bidding war.",
                    ("Sign for the richest club in world football and collect every trophy available",  {"goals": 44, "assists": 21, "trophies": 3, "caps": 21}),
                    ("Reject all offers and become an all-time great at the club that raised {name}",   {"goals": 52, "assists": 27, "trophies": 4, "caps": 24}),
                    ("Lead a historic underdog club to an unthinkable league championship",             {"goals": 50, "assists": 23, "trophies": 3, "caps": 19}),
                ),
                (
                    "At the absolute zenith of powers, {name}\'s {style} blend of pace, movement and clinical finishing "
                    "is unmatched on the planet. The next decision must be perfect.",
                    ("Make a sensational switch to a rival who desperately need a talisman to finally win the title", {"goals": 46, "assists": 24, "trophies": 3, "caps": 23}),
                    ("Remain as the undisputed star and break every domestic scoring record imaginable",               {"goals": 53, "assists": 26, "trophies": 4, "caps": 26}),
                    ("Accept a Champions League powerhouse\'s offer to spearhead their European conquest",             {"goals": 43, "assists": 22, "trophies": 3, "caps": 20}),
                ),
            ],
            # 5 \u2013 Prime Dominance (29-32)
            [
                (
                    "At 29, {name} stands at the very pinnacle of the sport. Every metric confirms what fans already know \u2014 "
                    "a generational talent defying gravity. Two epic challenges remain.",
                    ("Lead the national team on an international mission \u2014 a World Cup or continental title", {"goals": 22, "assists": 18, "trophies": 2, "caps": 28}),
                    ("Cement club immortality with back-to-back domestic and European crowns", {"goals": 38, "assists": 24, "trophies": 4, "caps": 14}),
                    ("Accept a shock move to a rival club in the same league for a final title tilt", {"goals": 30, "assists": 20, "trophies": 3, "caps": 18}),
                ),
                (
                    "Gravity does not apply to {name}. Every stadium falls silent when the ball arrives \u2014 "
                    "the greatest {style} of a generation is at full power.",
                    ("Become the cornerstone of a historic Champions League treble campaign",         {"goals": 36, "assists": 22, "trophies": 4, "caps": 15}),
                    ("Lead a glorious international campaign to bring a first major trophy to the nation", {"goals": 20, "assists": 17, "trophies": 2, "caps": 30}),
                    ("Move to the Saudi Pro League early to maximise earnings while still at peak power",  {"goals": 34, "assists": 19, "trophies": 3, "caps": 10}),
                ),
                (
                    "Every record is within range. {name} is a living legend \u2014 and the next three years will determine "
                    "whether the name sits above every other in history.",
                    ("Chase the all-time international goals record with a swashbuckling national campaign", {"goals": 24, "assists": 16, "trophies": 2, "caps": 26}),
                    ("Anchor a club dynasty \u2014 three consecutive domestic titles and two European finals",    {"goals": 40, "assists": 25, "trophies": 4, "caps": 12}),
                    ("Sign a barnstorming short-term deal at a new club and win the league in year one",     {"goals": 31, "assists": 21, "trophies": 3, "caps": 20}),
                ),
            ],
            # 6 \u2013 Veteran Phase (32-36)
            [
                (
                    "32 and still dangerous, {name} has accumulated silverware many players only dream of. "
                    "One final chapter in the top flight remains to be written.",
                    ("Embrace a new challenge in MLS or the Saudi Pro League",   {"goals": 30, "assists": 12, "trophies": 1, "caps": 5}),
                    ("Stay in the top flight and mentor the next generation",    {"goals": 28, "assists": 18, "trophies": 2, "caps": 10}),
                    ("Return to a former club as a free agent and complete unfinished business", {"goals": 22, "assists": 15, "trophies": 2, "caps": 8}),
                ),
                (
                    "Time may have dulled the sprint but the movement and cunning of {name} remain peerless. "
                    "The {style} legend has one final statement to make.",
                    ("Sign for a glamour club in a marquee league and prove age is just a number",     {"goals": 26, "assists": 13, "trophies": 1, "caps": 6}),
                    ("Accept the captaincy at a mid-table club and guide young forwards to stardom",   {"goals": 24, "assists": 17, "trophies": 2, "caps": 9}),
                    ("Make a high-profile move to the Japanese J-League and ignite football fever",    {"goals": 28, "assists": 11, "trophies": 1, "caps": 4}),
                ),
                (
                    "Every goal from {name} now draws a standing ovation \u2014 the crowd knows each one is precious. "
                    "The veteran {style} is a living piece of football history.",
                    ("Lead a newly promoted top-flight club and defy the odds to stay up in style",    {"goals": 20, "assists": 16, "trophies": 1, "caps": 7}),
                    ("Accept a short-term contract at a Champions League contender as an impact player", {"goals": 25, "assists": 14, "trophies": 2, "caps": 9}),
                    ("Take the armband at a storied foreign club and deliver a fairytale league title",  {"goals": 29, "assists": 12, "trophies": 2, "caps": 5}),
                ),
            ],
            # 7 \u2013 Final Chapter (36-40)
            [
                (
                    "The curtain is drawing close on an extraordinary career. {name}\'s name is already written in football\'s golden book. "
                    "One final decision will shape the farewell.",
                    ("Return to the boyhood club for an emotional homecoming season", {"goals": 10, "assists": 8,  "trophies": 1, "caps": 0}),
                    ("Push on for one last trophy as a talismanic figure at a new club", {"goals": 14, "assists": 10, "trophies": 2, "caps": 0}),
                    ("Move to an emerging league to grow the sport and end the journey in style", {"goals": 12, "assists": 9,  "trophies": 1, "caps": 0}),
                ),
                (
                    "They said it couldn\'t last, but {name}\'s {style} never dimmed. The stadium roars every time "
                    "the veteran steps onto the pitch \u2014 but the final chapter must now be written.",
                    ("Accept a farewell tour across a continent, playing one season for a beloved foreign club", {"goals": 11, "assists": 7,  "trophies": 1, "caps": 0}),
                    ("Stay at the current club and break the all-time appearances record in a blaze of glory",   {"goals": 13, "assists": 10, "trophies": 2, "caps": 0}),
                    ("Return home to manage the boyhood club while still lacing up the boots as player-coach",  {"goals": 8,  "assists": 9,  "trophies": 1, "caps": 0}),
                ),
                (
                    "Forty and still lighting up pitches. {name} is defying nature \u2014 every touch is a masterclass "
                    "and every goal a gift to the sport.",
                    ("Sign off with a legendary performance in a cup final to end the story perfectly", {"goals": 9,  "assists": 8,  "trophies": 2, "caps": 0}),
                    ("Move to an MLS expansion side and inspire an entire new generation of fans",      {"goals": 14, "assists": 9,  "trophies": 1, "caps": 0}),
                    ("Accept a charity match world tour and donate goals and memories to the game",     {"goals": 10, "assists": 11, "trophies": 1, "caps": 0}),
                ),
            ],
        ]
    elif position_group == "Midfielder":
        return [
            # 0 \u2013 Youth Academy (16-18)
            [
                (
                    "{name} quickly stood out in the academy with a {style} game that made the coaches compare the youngster "
                    "to midfield legends of the past.",
                    ("Train extra hours on shooting and scoring",                {"goals": 5,  "assists": 6,  "trophies": 0, "caps": 0}),
                    ("Focus on passing range, vision, and game management",      {"goals": 2,  "assists": 12, "trophies": 0, "caps": 0}),
                    ("Join an elite European academy abroad to broaden horizons", {"goals": 3,  "assists": 9,  "trophies": 0, "caps": 0}),
                ),
                (
                    "At 16, the coaches could barely contain their excitement \u2014 {name}\'s {style} ability to read the game "
                    "three moves ahead was simply not normal for this age.",
                    ("Master the art of the key pass and become the academy\'s creative heartbeat",  {"goals": 2,  "assists": 11, "trophies": 0, "caps": 0}),
                    ("Build physical strength and dominate the midfield battle like a seasoned pro", {"goals": 4,  "assists": 7,  "trophies": 0, "caps": 0}),
                    ("Travel abroad on a youth exchange programme and absorb a new football culture", {"goals": 3,  "assists": 10, "trophies": 0, "caps": 0}),
                ),
                (
                    "The youth tournament scouts were unanimous: {name} was the most complete {style} they had seen "
                    "at this age. Now the young star had to choose the right environment to flourish.",
                    ("Push hard for reserve-team appearances and test skills against adults",           {"goals": 5,  "assists": 8,  "trophies": 0, "caps": 0}),
                    ("Concentrate on developing a signature set-piece delivery to stand out",           {"goals": 3,  "assists": 13, "trophies": 0, "caps": 0}),
                    ("Accept a prestigious youth scholarship at a continental footballing powerhouse",  {"goals": 2,  "assists": 10, "trophies": 0, "caps": 0}),
                ),
            ],
            # 1 \u2013 Professional Debut (18-21)
            [
                (
                    "Two clubs made compelling offers. {name}\'s ability to control the tempo of matches was already evident \u2014 "
                    "but where to develop that talent best?",
                    ("Sign for a glamour club as a squad midfielder",            {"goals": 8,  "assists": 14, "trophies": 1, "caps": 4}),
                    ("Choose a team where {name} will be the heartbeat",         {"goals": 12, "assists": 20, "trophies": 0, "caps": 9}),
                    ("Move abroad to a Bundesliga or La Liga side for regular minutes", {"goals": 10, "assists": 16, "trophies": 0, "caps": 10}),
                ),
                (
                    "The professional debut was a statement \u2014 {name}\'s {style} vision slicing through defences as if "
                    "the game were played in slow motion. Every manager in the league took notice.",
                    ("Fight for a spot in a top-six club\'s midfield and embrace the intensity",   {"goals": 9,  "assists": 15, "trophies": 1, "caps": 5}),
                    ("Accept a starting role at an ambitious Championship side targeting promotion", {"goals": 13, "assists": 18, "trophies": 0, "caps": 8}),
                    ("Take a bold loan to a Portuguese or Dutch club renowned for nurturing midfielders", {"goals": 11, "assists": 17, "trophies": 0, "caps": 11}),
                ),
                (
                    "When {name} stepped into professional football, it felt less like a debut and more like an arrival. "
                    "A {style} prodigy with 15 assists before Christmas had changed the conversation.",
                    ("Commit to a storied Premier League club and earn valuable medal experience",    {"goals": 7,  "assists": 16, "trophies": 1, "caps": 4}),
                    ("Lead the midfield at a rebuilding club who make {name} the centre of everything", {"goals": 11, "assists": 21, "trophies": 0, "caps": 10}),
                    ("Seek a move to a renowned technical league \u2014 Serie A or Ligue 1 \u2014 for holistic development", {"goals": 9,  "assists": 17, "trophies": 0, "caps": 9}),
                ),
            ],
            # 2 \u2013 Rising Star (21-24)
            [
                (
                    "21 and flourishing, {name}\'s range of passing and box-to-box energy are drawing national headlines. "
                    "A pivotal transfer window opens.",
                    ("Move to a top-four side fighting for the title",           {"goals": 18, "assists": 35, "trophies": 2, "caps": 18}),
                    ("Lead the midfield at an ambitious club building for glory", {"goals": 25, "assists": 40, "trophies": 1, "caps": 22}),
                    ("Accept a player-captain role at a rising club with ambitious owners", {"goals": 20, "assists": 38, "trophies": 2, "caps": 20}),
                ),
                (
                    "{name}\'s {style} midfield mastery is the talk of every pundit panel \u2014 "
                    "a perfect blend of industry and artistry that clubs are paying a premium to acquire.",
                    ("Join a title-winning club and deliver the final piece in their midfield puzzle",      {"goals": 19, "assists": 36, "trophies": 2, "caps": 17}),
                    ("Become the engine of a mid-table giant on a mission to break into the European elite", {"goals": 23, "assists": 39, "trophies": 1, "caps": 21}),
                    ("Take the biggest offer on the table and prove worth in the Champions League immediately", {"goals": 17, "assists": 37, "trophies": 2, "caps": 19}),
                ),
                (
                    "Europe\'s finest technical directors are queueing at the door. {name} \u2014 the embodiment of {style} \u2014 "
                    "is 21 years old and already essential to every team selection.",
                    ("Accept a dream transfer to a Spanish giant and absorb a master-class tactical education", {"goals": 21, "assists": 37, "trophies": 2, "caps": 19}),
                    ("Become the heartbeat of an exciting young team with a visionary new head coach",         {"goals": 24, "assists": 41, "trophies": 1, "caps": 23}),
                    ("Make a surprise move to the Bundesliga and flourish in a high-press attacking system",   {"goals": 18, "assists": 36, "trophies": 2, "caps": 18}),
                ),
            ],
            # 3 \u2013 Breakout Season (24-26)
            [
                (
                    "{name}\'s vision and technique have made the back pages every week. A defining breakout campaign has earned rave reviews, "
                    "and two compelling opportunities have arrived simultaneously.",
                    ("Win Player of the Season and sign a bumper new deal",      {"goals": 18, "assists": 28, "trophies": 1, "caps": 14}),
                    ("Accept a high-profile move to a title contender",          {"goals": 14, "assists": 32, "trophies": 2, "caps": 10}),
                    ("Make a shock move to a continental rival to test the style in a new league", {"goals": 16, "assists": 30, "trophies": 1, "caps": 12}),
                ),
                (
                    "The season has been a masterpiece. {name}\'s {style} brilliance \u2014 30 assists, "
                    "every ball perfectly weighted \u2014 has ignited a bidding war between continent\'s finest clubs.",
                    ("Stay and lead the current club to their first league title in a generation",          {"goals": 17, "assists": 29, "trophies": 2, "caps": 13}),
                    ("Join a rival city club and ignite a fierce local derby rivalry as the marquee signing", {"goals": 15, "assists": 31, "trophies": 1, "caps": 11}),
                    ("Accept a record fee to dominate Ligue 1 or Serie A with an elite European outfit",      {"goals": 16, "assists": 33, "trophies": 2, "caps": 15}),
                ),
                (
                    "There is no bigger name in midfield right now. {name}\'s {style} ability to win a match "
                    "single-handedly is the talk of football \u2014 and the agents are working overtime.",
                    ("Extend the contract and deliver a historic treble for the beloved club",              {"goals": 19, "assists": 27, "trophies": 2, "caps": 12}),
                    ("Accept an irresistible offer to join a Spanish giant and compete in La Liga",         {"goals": 13, "assists": 33, "trophies": 1, "caps": 10}),
                    ("Pursue a bold move to the Premier League and prove the quality on the grandest stage", {"goals": 17, "assists": 31, "trophies": 2, "caps": 14}),
                ),
            ],
            # 4 \u2013 Peak Years (26-29)
            [
                (
                    "At 26, {name} is arguably the best midfielder in the league. A historic club wants their new midfield general "
                    "and they\'re willing to pay.",
                    ("Join the historic giant and chase the Champions League",   {"goals": 22, "assists": 42, "trophies": 3, "caps": 22}),
                    ("Stay and break the all-time appearances record",           {"goals": 28, "assists": 50, "trophies": 3, "caps": 28}),
                    ("Sign for an emerging project club and help build something historic from scratch", {"goals": 24, "assists": 45, "trophies": 2, "caps": 24}),
                ),
                (
                    "The {style} elegance that made {name} famous has evolved into something even more devastating. "
                    "At 26, the complete midfielder commands any dressing room and dictates any match.",
                    ("Lead a club dynasty \u2014 three consecutive titles anchored by {name}\'s midfield authority",    {"goals": 26, "assists": 48, "trophies": 3, "caps": 26}),
                    ("Accept a world-record midfield fee and become the cornerstone of a continental powerhouse", {"goals": 21, "assists": 44, "trophies": 3, "caps": 21}),
                    ("Commit to the national team\'s golden generation and orchestrate a World Cup charge",        {"goals": 20, "assists": 43, "trophies": 2, "caps": 30}),
                ),
                (
                    "Coaches describe {name} as the general they always dreamed of \u2014 a {style} commanding "
                    "the midfield with the authority of a chess grandmaster on a football pitch.",
                    ("Sign for a Champions League dark horse and steer them to an unforgettable final",            {"goals": 23, "assists": 46, "trophies": 3, "caps": 23}),
                    ("Stay loyal and transform a beloved club into a dominant force across every competition",     {"goals": 27, "assists": 51, "trophies": 3, "caps": 27}),
                    ("Make a bold transfer to Italy\'s most storied club and add Serie A glory to the r\u00e9sum\u00e9",      {"goals": 25, "assists": 44, "trophies": 2, "caps": 25}),
                ),
            ],
            # 5 \u2013 Prime Dominance (29-32)
            [
                (
                    "At 29, {name} is the fulcrum around which everything revolves. Captaincy beckons and legacy is being built game by game.",
                    ("Captain your club to a historic league and cup double",    {"goals": 20, "assists": 44, "trophies": 3, "caps": 20}),
                    ("Become the driving force behind your nation\'s deepest tournament run in decades", {"goals": 14, "assists": 38, "trophies": 2, "caps": 32}),
                    ("Take on a dual player-ambassador role for a new expansion club, combining play and growth", {"goals": 12, "assists": 32, "trophies": 1, "caps": 22}),
                ),
                (
                    "They call {name} the conductor \u2014 a {style} who orchestrates beautiful football "
                    "and makes every team-mate perform at their absolute ceiling.",
                    ("Lead the club to an unprecedented four-trophy season as the undisputed captain",           {"goals": 18, "assists": 42, "trophies": 4, "caps": 18}),
                    ("Spearhead a stunning international run and carry the nation to a first ever tournament win", {"goals": 12, "assists": 36, "trophies": 2, "caps": 34}),
                    ("Champion a move to a continental rival and deliver the title they have craved for decades",  {"goals": 16, "assists": 40, "trophies": 3, "caps": 24}),
                ),
                (
                    "Every pass {name} plays is a lesson. At 29, this {style} midfield maestro has become "
                    "the reference point against which all others are measured.",
                    ("Become the architect of a historic Champions League campaign that breaks all records",   {"goals": 15, "assists": 46, "trophies": 3, "caps": 16}),
                    ("Dedicate the prime years to the national cause and chase a once-in-a-generation title",  {"goals": 13, "assists": 37, "trophies": 2, "caps": 33}),
                    ("Accept the captaincy of a fallen giant and restore them to their former glorious peak",  {"goals": 19, "assists": 41, "trophies": 3, "caps": 21}),
                ),
            ],
            # 6 \u2013 Veteran Phase (32-36)
            [
                (
                    "32 and still covering every blade of grass, {name}\'s experience compensates for whatever edge of pace "
                    "time has taken. The question now is legacy.",
                    ("Move abroad to a new league for one last challenge",       {"goals": 12, "assists": 25, "trophies": 1, "caps": 8}),
                    ("Stay in domestic football until the very last whistle",    {"goals": 15, "assists": 30, "trophies": 2, "caps": 12}),
                    ("Relocate to a new continent \u2014 MLS or J-League \u2014 to leave a global imprint", {"goals": 10, "assists": 22, "trophies": 1, "caps": 6}),
                ),
                (
                    "The legs may be a tick slower but {name}\'s {style} intelligence is sharper than ever \u2014 "
                    "the game\'s greatest teacher giving a masterclass every weekend.",
                    ("Sign for a Ligue 1 or Liga Portugal side hungry for an experienced creative leader",  {"goals": 11, "assists": 26, "trophies": 1, "caps": 7}),
                    ("Stay in the top division and captain the club to one final piece of unexpected silverware", {"goals": 14, "assists": 29, "trophies": 2, "caps": 11}),
                    ("Accept an inviting Saudi Pro League contract and mentor the next generation of stars",      {"goals": 13, "assists": 24, "trophies": 1, "caps": 5}),
                ),
                (
                    "Football slows for no one \u2014 but {name}\'s {style} game makes time irrelevant. "
                    "The veteran is still the smartest player on the pitch and clubs still fight for that signature.",
                    ("Join a club with a famous youth academy and blend playing with unofficial coaching",     {"goals": 9,  "assists": 28, "trophies": 1, "caps": 8}),
                    ("Accept a one-year deal at a promotion-chasing club and be the difference maker",        {"goals": 14, "assists": 27, "trophies": 2, "caps": 10}),
                    ("Relocate to the Australian A-League and inspire a brand new fanbase",                   {"goals": 11, "assists": 23, "trophies": 1, "caps": 5}),
                ),
            ],
            # 7 \u2013 Final Chapter (36-40)
            [
                (
                    "A storied midfield career is entering its final act. {name} reads the game as well as ever, even if the legs have slowed. "
                    "Where does the last chapter unfold?",
                    ("Return to the club where it all began for one last emotional season", {"goals": 8,  "assists": 20, "trophies": 1, "caps": 0}),
                    ("Accept a player-coach role to pass on a lifetime of football wisdom", {"goals": 5,  "assists": 16, "trophies": 2, "caps": 0}),
                    ("Join the coaching staff in a hybrid player-coach capacity at a beloved club", {"goals": 4,  "assists": 14, "trophies": 1, "caps": 0}),
                ),
                (
                    "There is beauty in the way {name} still plays the game \u2014 each pass a signature, "
                    "each movement a lesson. The {style} legend is approaching the final whistle.",
                    ("Accept a farewell season at a passionate lower-league club who adore the legend",      {"goals": 6,  "assists": 18, "trophies": 1, "caps": 0}),
                    ("Stay at a top club as a half-time substitute hero, providing spark when it matters most", {"goals": 5,  "assists": 15, "trophies": 2, "caps": 0}),
                    ("Commit to a full final season in a new country to add one last chapter to the story",   {"goals": 7,  "assists": 19, "trophies": 1, "caps": 0}),
                ),
                (
                    "The standing ovation lasts longer every time {name} walks off the pitch. "
                    "The game knows it is witnessing its final glimpses of a masterful {style}.",
                    ("End the career at a World Cup, captaining the national team one last glorious time",    {"goals": 4,  "assists": 17, "trophies": 1, "caps": 0}),
                    ("Sign off with a cup winner\'s medal as the wise head in a young trophy-chasing squad",   {"goals": 6,  "assists": 15, "trophies": 2, "caps": 0}),
                    ("Retire after leading a community club to their greatest ever achievement",               {"goals": 5,  "assists": 13, "trophies": 1, "caps": 0}),
                ),
            ],
        ]
    elif position_group == "Defender":
        return [
            # 0 \u2013 Youth Academy (16-18)
            [
                (
                    "{name} was a commanding {style} from day one of the academy, throwing themselves into every training "
                    "session with fearless determination.",
                    ("Develop as a ball-playing sweeper with attacking instincts", {"goals": 3, "assists": 5,  "trophies": 0, "caps": 0}),
                    ("Master the fundamentals \u2014 positioning, heading, tackling",  {"goals": 1, "assists": 3,  "trophies": 1, "caps": 0}),
                    ("Trial at a foreign club and return with a new perspective on the game", {"goals": 2, "assists": 4,  "trophies": 0, "caps": 0}),
                ),
                (
                    "No attacker in the academy could get past {name} \u2014 a {style} who played every tackle "
                    "as if the championship depended on it.",
                    ("Push to captain the youth team and develop leadership from an early age",       {"goals": 2, "assists": 4,  "trophies": 1, "caps": 0}),
                    ("Focus on reading the game \u2014 studying footage of the world\'s best defenders",   {"goals": 1, "assists": 5,  "trophies": 0, "caps": 0}),
                    ("Request a loan to a grassroots senior side for physical development",          {"goals": 2, "assists": 3,  "trophies": 0, "caps": 0}),
                ),
                (
                    "The scouts described {name} as a {style} with the instincts of a natural leader \u2014 "
                    "vocal, brave, and utterly uncompromising in the defensive third.",
                    ("Hone aerial ability and set-piece threat to become a complete defender",        {"goals": 3, "assists": 3,  "trophies": 0, "caps": 0}),
                    ("Travel to a continental academy to learn a new defensive philosophy",           {"goals": 1, "assists": 5,  "trophies": 0, "caps": 0}),
                    ("Dedicate the academy season to becoming the most technically refined defender", {"goals": 2, "assists": 4,  "trophies": 1, "caps": 0}),
                ),
            ],
            # 1 \u2013 Professional Debut (18-21)
            [
                (
                    "Defenders mature late, but {name} was ahead of schedule. Two clubs wanted to sign the young stopper \u2014 "
                    "one a title contender, one desperate for defensive solidarity.",
                    ("Join the title contender as a squad defender",              {"goals": 2, "assists": 8,  "trophies": 2, "caps": 4}),
                    ("Anchor the defence at a mid-table club as undisputed no. 1", {"goals": 3, "assists": 10, "trophies": 0, "caps": 9}),
                    ("Move abroad to a league known for developing young defenders", {"goals": 2, "assists": 9,  "trophies": 1, "caps": 6}),
                ),
                (
                    "{name}\'s {style} debut season shook the football world \u2014 not a single league goal conceded "
                    "in the final eight games. Three clubs made formal approaches before the ink had dried.",
                    ("Sign for a Premier League club and compete for a first-team berth from day one",  {"goals": 2, "assists": 7,  "trophies": 1, "caps": 5}),
                    ("Become the undisputed leader of a Championship club\'s defence with full authority", {"goals": 3, "assists": 9,  "trophies": 0, "caps": 8}),
                    ("Move to a Bundesliga club renowned for their defensive structure and learn the system", {"goals": 1, "assists": 10, "trophies": 1, "caps": 7}),
                ),
                (
                    "Nobody got past {name} without paying a heavy price. The {style} prodigy at 18 had the "
                    "presence of a ten-year veteran \u2014 and the transfer market had taken notice.",
                    ("Accept a two-year deal at a Europa League contender and deliver immediately",     {"goals": 2, "assists": 8,  "trophies": 1, "caps": 5}),
                    ("Secure first-team football at a newly promoted top-flight club desperate for leadership", {"goals": 3, "assists": 11, "trophies": 0, "caps": 10}),
                    ("Take a loan move to a competitive foreign league to gain broad experience",        {"goals": 2, "assists": 9,  "trophies": 1, "caps": 6}),
                ),
            ],
            # 2 \u2013 Rising Star (21-24)
            [
                (
                    "21 and reliable as a rock, {name} is now one of the most sought-after defenders on the continent. "
                    "A powerhouse club wants to build their entire backline around this talent.",
                    ("Sign for the powerhouse \u2014 elite level, intense competition", {"goals": 5, "assists": 15, "trophies": 3, "caps": 16}),
                    ("Become the captain of a title-chasing side",                {"goals": 8, "assists": 20, "trophies": 2, "caps": 22}),
                    ("Take the captain\'s armband at a mid-table club with huge potential", {"goals": 6, "assists": 18, "trophies": 1, "caps": 18}),
                ),
                (
                    "Analysts are unanimous: {name}\'s {style} defensive numbers are the best in the league "
                    "for a player under 23. The offers flooding in are impossible to ignore.",
                    ("Join a continental powerhouse fighting on four fronts and play every cup game",  {"goals": 4, "assists": 16, "trophies": 3, "caps": 15}),
                    ("Take the captain\'s armband at an ambitious club who have targeted the title",     {"goals": 7, "assists": 19, "trophies": 2, "caps": 20}),
                    ("Accept a world-class coach\'s vision and join a tactical masterclass of a squad", {"goals": 5, "assists": 17, "trophies": 2, "caps": 17}),
                ),
                (
                    "Clean sheets follow {name} everywhere \u2014 and now the biggest clubs in Europe are competing "
                    "to pair this {style} titan with their own defensive stars.",
                    ("Accept a record defensive fee and move to the reigning European champions",             {"goals": 6, "assists": 14, "trophies": 3, "caps": 17}),
                    ("Stay loyal to the current club and lead them to the most successful season in their history", {"goals": 8, "assists": 21, "trophies": 2, "caps": 23}),
                    ("Move to a sleeping giant in dire need of defensive leadership and rebuild them from the back", {"goals": 5, "assists": 18, "trophies": 1, "caps": 19}),
                ),
            ],
            # 3 \u2013 Breakout Season (24-26)
            [
                (
                    "{name} has become the most talked-about defender on the continent after a near-impenetrable season. "
                    "Europe\'s elite are queuing up with proposals.",
                    ("Lead a charge deep into the Champions League as the defensive cornerstone", {"goals": 6, "assists": 16, "trophies": 2, "caps": 14}),
                    ("Sign for a rebuilding powerhouse who promise to build around {name}",       {"goals": 8, "assists": 20, "trophies": 1, "caps": 10}),
                    ("Move to a rival domestic club to prove elite-level status closer to home", {"goals": 7, "assists": 18, "trophies": 2, "caps": 12}),
                ),
                (
                    "The numbers are extraordinary: {name} has conceded fewer goals than any defender in the league. "
                    "The {style} colossus is fielding calls from all of world football\'s elite.",
                    ("Accept a record transfer and anchor the Champions League campaign of the ages",           {"goals": 5, "assists": 17, "trophies": 2, "caps": 13}),
                    ("Commit to the current club with a franchise deal and lead them to unprecedented heights",  {"goals": 9, "assists": 21, "trophies": 1, "caps": 11}),
                    ("Make a bold switch to a historic rival and become the icon their fans have been craving",  {"goals": 7, "assists": 19, "trophies": 2, "caps": 13}),
                ),
                (
                    "Strikers dread facing {name}. The {style} defender has become the heartbeat of one of "
                    "Europe\'s meanest defences \u2014 and the phone rings daily with irresistible offers.",
                    ("Join the defending champions as the defensive linchpin of their title retention",          {"goals": 6, "assists": 15, "trophies": 2, "caps": 14}),
                    ("Accept the captaincy at a passionate club rising fast through the European football ranks", {"goals": 8, "assists": 20, "trophies": 1, "caps": 11}),
                    ("Move to a rival league abroad for a Champions League winner\'s medal",                      {"goals": 7, "assists": 17, "trophies": 2, "caps": 13}),
                ),
            ],
            # 4 \u2013 Peak Years (26-29)
            [
                (
                    "At 26, {name} is at the peak of defensive powers. Clean sheets are a regular occurrence and "
                    "a huge club arrives with a lavish offer.",
                    ("Join the mega-club and play in the biggest matches",       {"goals": 5, "assists": 18, "trophies": 3, "caps": 22}),
                    ("Become a club legend \u2014 captain them to an unlikely title", {"goals": 8, "assists": 22, "trophies": 4, "caps": 28}),
                    ("Spearhead a European push at an ambitious club not among the traditional elite", {"goals": 6, "assists": 20, "trophies": 3, "caps": 24}),
                ),
                (
                    "At 26, {name}\'s {style} read of the game is peerless. Not a single attacker in world football "
                    "relishes the prospect of facing this immovable force at the back.",
                    ("Accept a transfer to football\'s greatest stage and add a Champions League title",            {"goals": 4, "assists": 19, "trophies": 3, "caps": 21}),
                    ("Become the captain who leads a beloved club to their first league title in twenty years",    {"goals": 7, "assists": 23, "trophies": 4, "caps": 27}),
                    ("Join a serial European winner and claim back-to-back continental crowns as their stalwart",  {"goals": 5, "assists": 21, "trophies": 3, "caps": 25}),
                ),
                (
                    "The {style} authority of {name} at 26 is breathtaking \u2014 a defender who commands "
                    "the penalty area like a king and distributes the ball like a midfielder.",
                    ("Sign for a historic club and help them end a long wait for the biggest prize in football",   {"goals": 6, "assists": 17, "trophies": 3, "caps": 23}),
                    ("Stay at the current club and lead an assault on every domestic and European competition",    {"goals": 9, "assists": 24, "trophies": 4, "caps": 29}),
                    ("Move to a new league and become the dominant defensive force in a new country",              {"goals": 5, "assists": 20, "trophies": 3, "caps": 22}),
                ),
            ],
            # 5 \u2013 Prime Dominance (29-32)
            [
                (
                    "29 and utterly dominant. {name} is captaining teams to silverware, marshalling defences with telepathic leadership. "
                    "Two landmark opportunities have emerged.",
                    ("Skipper the national team to World Cup glory",              {"goals": 4, "assists": 14, "trophies": 3, "caps": 30}),
                    ("Lead your club to an unprecedented clean-sheet record and title glory", {"goals": 7, "assists": 20, "trophies": 4, "caps": 16}),
                    ("Make a bold move abroad to a top continental league and raise the defensive bar", {"goals": 5, "assists": 16, "trophies": 3, "caps": 22}),
                ),
                (
                    "There is not a forward alive who relishes the challenge of facing {name}. "
                    "The {style} captain has become the defensive blueprint every coach studies.",
                    ("Lead the national team on a World Cup run that captures the imagination of a nation",  {"goals": 3, "assists": 13, "trophies": 3, "caps": 32}),
                    ("Deliver a historic back-to-back title campaign as the irreplaceable club captain",     {"goals": 6, "assists": 21, "trophies": 4, "caps": 14}),
                    ("Accept a final big-money transfer and win the Champions League for the first time",    {"goals": 5, "assists": 15, "trophies": 3, "caps": 20}),
                ),
                (
                    "{name}\'s {style} leadership from the back has transformed every club captained. "
                    "At 29, a once-in-a-generation defender is entering the defining years.",
                    ("Commit to the national side through a golden World Cup campaign as the defensive lynchpin", {"goals": 4, "assists": 12, "trophies": 3, "caps": 31}),
                    ("Anchor a club that breaks the all-time clean-sheet record en route to the title",           {"goals": 6, "assists": 19, "trophies": 4, "caps": 17}),
                    ("Make a shock move abroad and become the most dominant defender in a new continental league", {"goals": 5, "assists": 17, "trophies": 3, "caps": 23}),
                ),
            ],
            # 6 \u2013 Veteran Phase (32-36)
            [
                (
                    "32 and still a rock. Experience makes {name} even more dangerous \u2014 anticipation and positioning "
                    "compensate for any reduction in pace.",
                    ("Accept a final challenge in a top foreign league",         {"goals": 3, "assists": 10, "trophies": 1, "caps": 6}),
                    ("See out the career in the domestic top flight",            {"goals": 4, "assists": 12, "trophies": 2, "caps": 10}),
                    ("Join a young squad needing leadership and guide them to unexpected success", {"goals": 3, "assists": 11, "trophies": 2, "caps": 8}),
                ),
                (
                    "Pace may have peaked, but {name}\'s {style} positioning is still a masterclass in the art "
                    "of defending. Experienced clubs recognise the immense value on offer.",
                    ("Accept a farewell Champions League campaign at an elite European club",             {"goals": 2, "assists": 11, "trophies": 1, "caps": 5}),
                    ("Stay in the domestic top flight and captain the club to a surprise cup triumph",   {"goals": 4, "assists": 13, "trophies": 2, "caps": 9}),
                    ("Move to the Middle East or America and use the experience to elevate a new league", {"goals": 3, "assists": 9,  "trophies": 1, "caps": 4}),
                ),
                (
                    "Every header cleared, every tackle timed perfectly \u2014 {name}\'s {style} precision "
                    "is undimmed at 32, and the defensive intelligence remains priceless.",
                    ("Sign for a promoted club and lead them to a stunning top-flight survival campaign",   {"goals": 3, "assists": 10, "trophies": 1, "caps": 7}),
                    ("Commit to a storied club for two more years and deliver a final trophy as captain",   {"goals": 4, "assists": 12, "trophies": 2, "caps": 10}),
                    ("Accept an overseas posting in a new league to end the career as a global legend",    {"goals": 2, "assists": 11, "trophies": 1, "caps": 5}),
                ),
            ],
            # 7 \u2013 Final Chapter (36-40)
            [
                (
                    "36 and still imposing. {name} has one final gift to give the game before hanging up the boots. "
                    "How does the legend\'s story end?",
                    ("Return to the community club roots for a poignant farewell season", {"goals": 2, "assists": 6,  "trophies": 1, "caps": 0}),
                    ("Carry an emerging young club into a trophy final as the experienced guardian", {"goals": 3, "assists": 8,  "trophies": 2, "caps": 0}),
                    ("Move into a player-coach hybrid role to shape the next generation of defenders", {"goals": 2, "assists": 7,  "trophies": 1, "caps": 0}),
                ),
                (
                    "The legend does not fade \u2014 {name}\'s {style} presence commands respect "
                    "from every forward in the land, even now. One final season beckons.",
                    ("Return to the boyhood club and deliver one last memorable performance in a cup final", {"goals": 2, "assists": 7,  "trophies": 2, "caps": 0}),
                    ("Take a short-term deal at a third-division club and guide them to a fairytale trophy",  {"goals": 3, "assists": 6,  "trophies": 1, "caps": 0}),
                    ("Accept a coaching role at an international academy while still lacing up the boots",   {"goals": 1, "assists": 8,  "trophies": 1, "caps": 0}),
                ),
                (
                    "Strikers half {name}\'s age still lose sleep before a match. "
                    "The {style} icon is 36, still priceless \u2014 and the football world refuses to let go.",
                    ("Sign for a beloved club abroad and write a final poetic chapter in a foreign land",   {"goals": 2, "assists": 6,  "trophies": 1, "caps": 0}),
                    ("Stay in the top flight one last season and cap it with a Wembley cup final clean sheet", {"goals": 3, "assists": 9,  "trophies": 2, "caps": 0}),
                    ("Commit to a lower-league club as player-manager and begin the next chapter of the story", {"goals": 1, "assists": 7,  "trophies": 1, "caps": 0}),
                ),
            ],
        ]
    else:  # Goalkeeper
        return [
            # 0 \u2013 Youth Academy (16-18)
            [
                (
                    "At 16, {name} had the reflexes of a cat and the presence of a {style}. "
                    "The goalkeeping coach predicted an international career from the very first training session.",
                    ("Work obsessively on shot-stopping, reflexes and positioning", {"goals": 0, "assists": 0, "trophies": 1, "caps": 0}),
                    ("Develop sweeper-keeper skills and precise distribution",      {"goals": 0, "assists": 2, "trophies": 0, "caps": 0}),
                    ("Spend a season on exchange at a foreign club\'s academy to broaden skills", {"goals": 0, "assists": 1, "trophies": 0, "caps": 0}),
                ),
                (
                    "The goalkeeping coach had coached hundreds of youngsters \u2014 but {name}\'s {style} composure "
                    "under pressure at 16 was something genuinely different.",
                    ("Dedicate the academy season to mastering the aerial game and commanding the box",  {"goals": 0, "assists": 1, "trophies": 1, "caps": 0}),
                    ("Focus entirely on footwork and becoming the definitive sweeper-keeper of the era", {"goals": 0, "assists": 2, "trophies": 0, "caps": 0}),
                    ("Request a loan to a lower-tier club to start accumulating senior minutes early",   {"goals": 0, "assists": 1, "trophies": 0, "caps": 0}),
                ),
                (
                    "Opponents who saw {name} between the sticks in youth football left with a grudging respect \u2014 "
                    "a {style} presence that made the goal seem impossibly small.",
                    ("Push for an early professional contract based on outstanding academy performances", {"goals": 0, "assists": 0, "trophies": 1, "caps": 0}),
                    ("Travel to a renowned goalkeeping school in Europe to absorb expert coaching",      {"goals": 0, "assists": 2, "trophies": 0, "caps": 0}),
                    ("Develop a reputation for penalty saving \u2014 a specialist skill to stand out immediately", {"goals": 0, "assists": 1, "trophies": 0, "caps": 0}),
                ),
            ],
            # 1 \u2013 Professional Debut (18-21)
            [
                (
                    "{name} is 18 and ready for the professional stage. Goalkeepers need experience \u2014 "
                    "but two very different paths are available.",
                    ("Fight for a spot at a top-flight club\'s first team",              {"goals": 0, "assists": 2, "trophies": 1, "caps": 3}),
                    ("Take a loan to a lower-league club for 200 games in two seasons", {"goals": 0, "assists": 4, "trophies": 0, "caps": 6}),
                    ("Move abroad early to a league known for developing young goalkeepers", {"goals": 0, "assists": 3, "trophies": 0, "caps": 8}),
                ),
                (
                    "The coaches knew that a {style} talent like {name} needed matches \u2014 real matches, high pressure, "
                    "the kind that forge a goalkeeper into something special.",
                    ("Accept a season-long loan at a Championship club fighting for promotion",             {"goals": 0, "assists": 3, "trophies": 0, "caps": 5}),
                    ("Battle for a first-team place at a Premier League club with established competition", {"goals": 0, "assists": 2, "trophies": 1, "caps": 4}),
                    ("Move to a La Liga second-division club where the technical demands are already elite", {"goals": 0, "assists": 3, "trophies": 0, "caps": 7}),
                ),
                (
                    "Every save {name} made turned heads \u2014 the {style} instincts were unmistakable. "
                    "Now the question was where to transform those instincts into a professional career.",
                    ("Join a top-flight club\'s squad and compete for cup and rotation appearances",   {"goals": 0, "assists": 2, "trophies": 1, "caps": 3}),
                    ("Take a decisive loan to a Ligue 2 or Liga Portugal club for back-to-back seasons", {"goals": 0, "assists": 4, "trophies": 0, "caps": 7}),
                    ("Accept a Bundesliga second-division starting spot renowned for nurturing keepers", {"goals": 0, "assists": 3, "trophies": 0, "caps": 9}),
                ),
            ],
            # 2 \u2013 Rising Star (21-24)
            [
                (
                    "A string of brilliant performances has made {name} one of the most coveted keepers in Europe. "
                    "Two clubs are desperate to sign them.",
                    ("Join a Champions League regular at a premium price",         {"goals": 0, "assists": 5, "trophies": 3, "caps": 16}),
                    ("Become the undisputed no. 1 at a passionate mid-table club", {"goals": 0, "assists": 8, "trophies": 2, "caps": 22}),
                    ("Take the no. 1 shirt at a newly promoted side with a passionate fanbase", {"goals": 0, "assists": 6, "trophies": 1, "caps": 18}),
                ),
                (
                    "Goalkeepers of the Year are rare \u2014 {name} is already being discussed in those terms at 21. "
                    "The {style} shot-stopper is a phenomenon, and everyone wants a piece.",
                    ("Accept a move to a historic English club fighting for Champions League qualification",  {"goals": 0, "assists": 6, "trophies": 2, "caps": 17}),
                    ("Become the undroppable no. 1 at a club on a genuine title challenge",                  {"goals": 0, "assists": 7, "trophies": 2, "caps": 21}),
                    ("Make a bold transfer to a Spanish club and prove worth in the world\'s best league",    {"goals": 0, "assists": 5, "trophies": 3, "caps": 15}),
                ),
                (
                    "Clean sheet after clean sheet \u2014 {name}\'s {style} dominance between the sticks has "
                    "made the position look effortless. The big clubs are circling.",
                    ("Sign for the club with the most ambitious project and safeguard their European run", {"goals": 0, "assists": 4, "trophies": 3, "caps": 16}),
                    ("Stay loyal to the current club who took the gamble first \u2014 and repay their faith",  {"goals": 0, "assists": 8, "trophies": 2, "caps": 23}),
                    ("Accept an irresistible offer from a Serie A giant with elite defensive structure",  {"goals": 0, "assists": 6, "trophies": 2, "caps": 19}),
                ),
            ],
            # 3 \u2013 Breakout Season (24-26)
            [
                (
                    "{name}\'s shot-stopping brilliance has drawn comparisons to the all-time greats. After a season of jaw-dropping saves, "
                    "two landmark offers have materialised.",
                    ("Win the Golden Glove and sign a bumper new deal at your current club", {"goals": 0, "assists": 4, "trophies": 2, "caps": 14}),
                    ("Accept a transfer to a club where the Champions League is a guaranteed stage", {"goals": 0, "assists": 3, "trophies": 1, "caps": 10}),
                    ("Move to a continental rival on a short-term deal to gain Champions League experience", {"goals": 0, "assists": 3, "trophies": 2, "caps": 12}),
                ),
                (
                    "There was that save \u2014 the one replayed a million times online. {name}\'s {style} reflexes "
                    "have turned the keeper into a global superstar, and the world wants to know what happens next.",
                    ("Commit to the current club with a record-breaking new deal and target the title",        {"goals": 0, "assists": 5, "trophies": 2, "caps": 13}),
                    ("Accept an elite Champions League club\'s offer and play on the greatest European stage",   {"goals": 0, "assists": 3, "trophies": 2, "caps": 11}),
                    ("Join a Bundesliga powerhouse known for building their game plan around the goalkeeper",   {"goals": 0, "assists": 4, "trophies": 1, "caps": 13}),
                ),
                (
                    "Six consecutive clean sheets in Europe. A penalty shootout hero in the cup. {name}\'s "
                    "{style} season has been nothing short of sensational.",
                    ("Re-sign with the current club and lead them to a historic domestic double",                  {"goals": 0, "assists": 4, "trophies": 2, "caps": 15}),
                    ("Take the move to the most prestigious club in Europe and chase the ultimate prize",          {"goals": 0, "assists": 2, "trophies": 1, "caps": 10}),
                    ("Join a title-contending side where the entire defensive system is built to {name}\'s strengths", {"goals": 0, "assists": 3, "trophies": 2, "caps": 12}),
                ),
            ],
            # 4 \u2013 Peak Years (26-29)
            [
                (
                    "26 and at the absolute peak of their powers, {name} is being talked about as the best goalkeeper "
                    "in the world. A historic contract offer arrives.",
                    ("Sign for the wealthiest club and target every trophy",       {"goals": 0, "assists": 6, "trophies": 4, "caps": 20}),
                    ("Remain loyal and carry the beloved club to an unlikely title", {"goals": 0, "assists": 8, "trophies": 3, "caps": 26}),
                    ("Join an ambitious project club and build a dynasty from the back", {"goals": 0, "assists": 7, "trophies": 3, "caps": 22}),
                ),
                (
                    "The world has chosen its best goalkeeper \u2014 and it is {name}. The {style} custodian "
                    "is redefining the position and commanding a price tag to match.",
                    ("Accept the offer from the richest club in the game and collect every trophy available", {"goals": 0, "assists": 5, "trophies": 4, "caps": 21}),
                    ("Stay at the beloved club and become the greatest keeper in their entire history",        {"goals": 0, "assists": 9, "trophies": 3, "caps": 25}),
                    ("Make a shock transfer to a new league and immediately transform the title race",         {"goals": 0, "assists": 7, "trophies": 3, "caps": 23}),
                ),
                (
                    "From wonder-save to wonder-save \u2014 {name}\'s {style} command of the goal is the kind "
                    "that makes entire squads believe they are unbeatable.",
                    ("Commit to the club that built the career and deliver them to European glory",             {"goals": 0, "assists": 8, "trophies": 3, "caps": 27}),
                    ("Accept a mega-money move to a continental superclub and challenge for everything",        {"goals": 0, "assists": 6, "trophies": 4, "caps": 19}),
                    ("Join a South American club on a pioneering contract to become a global ambassador",       {"goals": 0, "assists": 7, "trophies": 3, "caps": 22}),
                ),
            ],
            # 5 \u2013 Prime Dominance (29-32)
            [
                (
                    "29 and unquestionably the best goalkeeper in the world. {name} is as commanding in the dressing room as in the goal. "
                    "Two monumental challenges beckon.",
                    ("Lead the national team to the World Cup final as the last line of defence", {"goals": 0, "assists": 4, "trophies": 2, "caps": 30}),
                    ("Mastermind a historic treble \u2014 league, cup, and Champions League in one season", {"goals": 0, "assists": 5, "trophies": 3, "caps": 14}),
                    ("Take a shock move to a different top league to test skills in a new environment", {"goals": 0, "assists": 4, "trophies": 2, "caps": 22}),
                ),
                (
                    "There is simply no better goalkeeper on the planet. {name}\'s {style} authority "
                    "behind the defence has become the foundation upon which championships are built.",
                    ("Lead the club to a four-trophy season as the irreplaceable last line of defence",         {"goals": 0, "assists": 6, "trophies": 4, "caps": 16}),
                    ("Spearhead a legendary World Cup campaign that ends in a golden trophy for the nation",    {"goals": 0, "assists": 3, "trophies": 2, "caps": 32}),
                    ("Make a barnstorming transfer to an overseas league and raise the global profile of the sport", {"goals": 0, "assists": 5, "trophies": 2, "caps": 20}),
                ),
                (
                    "Commentators have run out of superlatives for {name}. The {style} keeper is an immovable "
                    "force \u2014 a wall behind which entire squads play with total freedom.",
                    ("Secure a historic Champions League treble with back-to-back seasons of flawless goalkeeping", {"goals": 0, "assists": 5, "trophies": 3, "caps": 13}),
                    ("Captain the national team as goalkeeper-captain to an unprecedented continental triumph",     {"goals": 0, "assists": 3, "trophies": 2, "caps": 31}),
                    ("Join a league rival on a dramatic deadline-day transfer and deliver the title immediately",   {"goals": 0, "assists": 4, "trophies": 3, "caps": 23}),
                ),
            ],
            # 6 \u2013 Veteran Phase (32-36)
            [
                (
                    "32 is still young for a goalkeeper. {name} can realistically play at the top level for several more years \u2014 "
                    "but where?",
                    ("Move to a glamour league abroad for a new adventure",     {"goals": 0, "assists": 5, "trophies": 1, "caps": 5}),
                    ("Stay as the evergreen no. 1 in the domestic top flight",  {"goals": 0, "assists": 6, "trophies": 2, "caps": 10}),
                    ("Join a lower-league club fighting for promotion and be the difference maker", {"goals": 0, "assists": 4, "trophies": 1, "caps": 4}),
                ),
                (
                    "Goalkeepers mature like fine wine \u2014 and {name}\'s {style} game is richer and wiser "
                    "than it has ever been. The veteran is still priceless.",
                    ("Accept a Serie A or Ligue 1 challenge and add a new chapter to an iconic career",    {"goals": 0, "assists": 5, "trophies": 1, "caps": 6}),
                    ("Commit to the domestic league and mentor a young understudy in the traditions of the position", {"goals": 0, "assists": 7, "trophies": 2, "caps": 9}),
                    ("Accept an MLS opportunity and ignite football enthusiasm in a new city",              {"goals": 0, "assists": 4, "trophies": 1, "caps": 3}),
                ),
                (
                    "Experience has elevated {name}\'s game beyond pure athleticism \u2014 the {style} "
                    "reading of play is a masterclass that younger keepers study in awe.",
                    ("Take a dramatic short-term deal at a club in a relegation battle and save them single-handedly", {"goals": 0, "assists": 4, "trophies": 1, "caps": 5}),
                    ("Stay at the top club and equal the club record for most appearances in goal",                    {"goals": 0, "assists": 6, "trophies": 2, "caps": 10}),
                    ("Move to the J-League or Saudi Pro League and leave a lasting global footballing legacy",         {"goals": 0, "assists": 5, "trophies": 1, "caps": 4}),
                ),
            ],
            # 7 \u2013 Final Chapter (36-40)
            [
                (
                    "Goalkeepers age like fine wine, and at 36 {name} is still proving the point. "
                    "But the day of retirement is on the horizon. How does the final chapter read?",
                    ("Return to the club where the story began \u2014 the prodigal no. 1 comes home", {"goals": 0, "assists": 3, "trophies": 1, "caps": 0}),
                    ("Stay at the top as a shot-stopper-mentor hybrid, inspiring the next generation", {"goals": 0, "assists": 4, "trophies": 2, "caps": 0}),
                    ("Accept a player-development role at a national football centre alongside playing", {"goals": 0, "assists": 2, "trophies": 1, "caps": 0}),
                ),
                (
                    "The save percentage is still elite. The command of the box still unrivalled. "
                    "{name}\'s {style} presence at 36 is a miracle of preparation and dedication.",
                    ("Accept one final season at a club in a prestigious European league as a farewell gift",   {"goals": 0, "assists": 3, "trophies": 1, "caps": 0}),
                    ("Stay on as a squad goalkeeper-coach hybrid, playing cup games and nurturing a successor",  {"goals": 0, "assists": 4, "trophies": 2, "caps": 0}),
                    ("Sign for a historic continental club and end the career with an unexpected trophy",        {"goals": 0, "assists": 3, "trophies": 2, "caps": 0}),
                ),
                (
                    "They said the reflexes would go \u2014 {name} proved them wrong. The {style} legend at 38 "
                    "is still making saves that leave crowds breathless.",
                    ("Commit to one final season at the boyhood club and retire as a beloved one-club legend",     {"goals": 0, "assists": 2, "trophies": 1, "caps": 0}),
                    ("Join a lower-league club as player-manager and combine final games with a new coaching role", {"goals": 0, "assists": 3, "trophies": 1, "caps": 0}),
                    ("Accept a dream farewell in an all-star charity match and bow out in front of the world",     {"goals": 0, "assists": 4, "trophies": 2, "caps": 0}),
                ),
            ],
        ]'''

content = open('/home/runner/work/soccer_game/soccer_game/app.py').read()
lines = content.split('\n')

# Lines 875-1141 are indices 874-1140 (0-based)
before = '\n'.join(lines[:874])
after = '\n'.join(lines[1141:])

new_content = before + '\n' + NEW_BLOCK + '\n' + after

open('/home/runner/work/soccer_game/soccer_game/app.py', 'w').write(new_content)
print("Done")
