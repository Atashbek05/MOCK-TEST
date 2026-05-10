"""
IELTS Content Database — Seed Data
===================================
Auto-seeded on first startup (when ielts_tests table is empty).
Teachers can add more tests via POST /ielts/admin/create-test.

Structure per test:
  Test → Passages (1-3) → QuestionGroups → Questions
  Each group has one question_type and one instruction block.
  Questions are numbered globally 1-40 by the seeder.
"""

from . import models

# ─────────────────────────────────────────────────────────────────────────────
# READING TESTS (3 complete tests, 40 questions each)
# ─────────────────────────────────────────────────────────────────────────────

READING_TESTS = [

    # ═════════════════════════════════════════════════════════════════════════
    # TEST 1  —  Environment · Psychology · Smart Cities
    # ═════════════════════════════════════════════════════════════════════════
    {
        "title":      "IELTS Academic Reading — Set 1",
        "test_type":  "academic",
        "component":  "reading",
        "time_limit": 60,
        "passages": [

            # ── Passage 1: Ocean Acidification (Q1-13) ──────────────────────
            {
                "order": 1,
                "title": "Ocean Acidification: A Silent Threat",
                "body_text": (
                    "The world's oceans have long served as a buffer against climate change, "
                    "absorbing approximately one-third of the carbon dioxide emitted by human "
                    "activity since the Industrial Revolution. While this capacity has helped "
                    "moderate rising global temperatures, it has come at a significant cost: as "
                    "seawater absorbs CO₂, a series of chemical reactions alters ocean "
                    "chemistry in a process scientists call ocean acidification.\n\n"

                    "The chemistry behind this phenomenon is straightforward. When carbon dioxide "
                    "dissolves in seawater, it reacts to form carbonic acid, which subsequently "
                    "breaks down into bicarbonate and hydrogen ions. The increase in hydrogen "
                    "ion concentration is measured as a decrease in pH. Since industrialisation "
                    "began, average ocean surface pH has fallen from 8.2 to 8.1 — a seemingly "
                    "small change that represents a 26 per cent increase in acidity, owing to the "
                    "logarithmic nature of the pH scale.\n\n"

                    "The consequences for marine organisms are severe, particularly for those that "
                    "build shells or skeletons from calcium carbonate. Oysters, mussels, sea urchins, "
                    "and many species of plankton depend on carbonate ions to construct their "
                    "protective structures. As acidity increases, carbonate ions become less "
                    "available, making it energetically costly for these animals to build their "
                    "shells. Laboratory experiments have confirmed that many shellfish produce "
                    "thinner, weaker shells under projected future ocean conditions.\n\n"

                    "Coral reefs face a particularly dire future. These ecosystems support "
                    "approximately 25 per cent of all marine species despite covering less than "
                    "one per cent of the ocean floor. Coral polyps build their skeletons by "
                    "secreting calcium carbonate, and in more acidic water the rate of calcification "
                    "falls sharply. The Great Barrier Reef has already experienced repeated mass "
                    "bleaching events associated with warming and acidification.\n\n"

                    "The economic consequences extend beyond tourism. Global fisheries support "
                    "hundreds of millions of livelihoods and provide essential protein for over "
                    "one billion people. Many commercially significant fish depend at some stage "
                    "of their life cycle on shellfish and plankton — the organisms most affected "
                    "by acidification. Aquaculture operations along the Pacific coast of North "
                    "America have already reported increased mortality in shellfish hatcheries.\n\n"

                    "Scientists are investigating several potential interventions. Adding alkaline "
                    "minerals such as olivine to seawater could neutralise excess acidity. Others "
                    "are exploring whether shellfish strains can be selectively bred to tolerate "
                    "more acidic conditions. However, researchers widely agree that these are "
                    "temporary fixes. The fundamental solution must involve a dramatic reduction "
                    "in global carbon dioxide emissions, though even if emissions stopped tomorrow, "
                    "the effects of acidification would persist for centuries."
                ),
                "question_groups": [
                    {
                        "order": 1,
                        "question_type": "tfng",
                        "instruction": (
                            "Do the following statements agree with the information given in the "
                            "Reading Passage?\n\nWrite:\n"
                            "TRUE    if the statement agrees with the information\n"
                            "FALSE   if the statement contradicts the information\n"
                            "NOT GIVEN  if there is no information on this"
                        ),
                        "questions": [
                            {"local_order": 1, "stem": "The ocean absorbs roughly one-third of all human-made carbon dioxide emissions.", "correct_answer": "TRUE"},
                            {"local_order": 2, "stem": "A pH drop of 0.1 represents a 26 per cent increase in acidity due to the logarithmic pH scale.", "correct_answer": "TRUE"},
                            {"local_order": 3, "stem": "All marine species are equally harmed by ocean acidification.", "correct_answer": "FALSE"},
                            {"local_order": 4, "stem": "Coral reefs cover more than one per cent of the ocean floor.", "correct_answer": "FALSE"},
                            {"local_order": 5, "stem": "Selective breeding of shellfish is currently in commercial use at hatcheries worldwide.", "correct_answer": "NOT GIVEN"},
                        ],
                    },
                    {
                        "order": 2,
                        "question_type": "mcq",
                        "instruction": "Choose the correct letter, A, B, C or D.",
                        "questions": [
                            {
                                "local_order": 1,
                                "stem": "What is the main cause of ocean acidification described in the passage?",
                                "options": [
                                    {"key": "A", "text": "Rising ocean temperatures caused by solar radiation"},
                                    {"key": "B", "text": "The absorption of carbon dioxide by seawater"},
                                    {"key": "C", "text": "Increased mining of minerals on the ocean floor"},
                                    {"key": "D", "text": "The dumping of industrial waste into the ocean"},
                                ],
                                "correct_answer": "B",
                            },
                            {
                                "local_order": 2,
                                "stem": "Which creatures are described as particularly vulnerable to ocean acidification?",
                                "options": [
                                    {"key": "A", "text": "Large predatory fish such as sharks and tuna"},
                                    {"key": "B", "text": "Deep-sea species found below 1,000 metres"},
                                    {"key": "C", "text": "Organisms that build shells or skeletons from calcium carbonate"},
                                    {"key": "D", "text": "Species that migrate between fresh and salt water"},
                                ],
                                "correct_answer": "C",
                            },
                            {
                                "local_order": 3,
                                "stem": "What is significant about coral reefs in terms of marine biodiversity?",
                                "options": [
                                    {"key": "A", "text": "They are found in all the world's major oceans"},
                                    {"key": "B", "text": "They support 25% of marine species while covering less than 1% of the ocean floor"},
                                    {"key": "C", "text": "They are the primary habitat for commercially fished species"},
                                    {"key": "D", "text": "They grow most rapidly in highly acidic conditions"},
                                ],
                                "correct_answer": "B",
                            },
                            {
                                "local_order": 4,
                                "stem": "What do researchers believe is the most effective long-term solution to ocean acidification?",
                                "options": [
                                    {"key": "A", "text": "Adding alkaline minerals to the ocean on a global scale"},
                                    {"key": "B", "text": "Creating protected marine areas around coral reefs"},
                                    {"key": "C", "text": "Significantly reducing global carbon dioxide emissions"},
                                    {"key": "D", "text": "Developing acid-resistant coral through genetic engineering"},
                                ],
                                "correct_answer": "C",
                            },
                        ],
                    },
                    {
                        "order": 3,
                        "question_type": "sentence_completion",
                        "instruction": "Complete the sentences below. Choose NO MORE THAN TWO WORDS from the passage for each answer.",
                        "word_limit": 2,
                        "questions": [
                            {"local_order": 1, "stem": "Since industrialisation, the average ocean surface pH has fallen from 8.2 to _____.", "correct_answer": "8.1"},
                            {"local_order": 2, "stem": "Coral polyps construct their skeletons by secreting _____.", "correct_answer": "calcium carbonate"},
                            {"local_order": 3, "stem": "The process by which corals build their skeletons is called _____.", "correct_answer": "calcification"},
                            {"local_order": 4, "stem": "Scientists are investigating whether adding the mineral _____ to seawater could help counteract acidification.", "correct_answer": "olivine"},
                        ],
                    },
                ],
            },

            # ── Passage 2: Psychology of Decision Making (Q14-26) ───────────
            {
                "order": 2,
                "title": "The Psychology of Decision Making",
                "body_text": (
                    "For centuries, economists assumed that people are fundamentally rational agents "
                    "who weigh costs and benefits and consistently choose the outcome maximising their "
                    "well-being — a model known as rational choice theory. A growing body of "
                    "psychological research has fundamentally challenged this view, revealing that "
                    "human decision-making is far more complex, inconsistent, and susceptible to "
                    "outside influence than once believed.\n\n"

                    "A critical insight came from the work of psychologists Daniel Kahneman and Amos "
                    "Tversky, who demonstrated that people rely on cognitive shortcuts known as "
                    "heuristics when making judgements. While these mental shortcuts often serve us "
                    "well — allowing quick decisions in familiar situations — they can lead to "
                    "systematic errors, or biases. The availability heuristic, for example, leads "
                    "people to overestimate the likelihood of dramatic but rare events, such as plane "
                    "crashes, simply because such events are memorable and widely reported.\n\n"

                    "Emotions also play a significant and often underappreciated role. Neuroscientist "
                    "Antonio Damasio's research with patients who had suffered damage to the emotional "
                    "centres of the brain revealed a striking finding: these individuals were unable "
                    "to make even simple decisions despite retaining full cognitive function. This "
                    "suggests that emotions are not merely a source of distortion — they are an "
                    "essential component of the decision-making process.\n\n"

                    "Framing effects illustrate another layer of complexity. Research shows that "
                    "people respond very differently to the same information depending on how it is "
                    "presented. In a classic experiment, participants chose between two medical "
                    "treatments. When told that a treatment had a '90 per cent survival rate,' most "
                    "chose it; when told it had a '10 per cent mortality rate,' many changed their "
                    "preference — even though both statements convey identical information.\n\n"

                    "These insights gave rise to behavioural economics, a field combining principles "
                    "from psychology and economics to develop more effective interventions. The concept "
                    "of the nudge — making beneficial choices the default option while preserving "
                    "individual freedom — has been applied in areas including organ donation, "
                    "retirement savings, and energy conservation. Countries including the United "
                    "Kingdom and the United States have established dedicated behavioural insights "
                    "teams within government.\n\n"

                    "Understanding the limits of rational decision-making has significant implications "
                    "for individuals seeking to make better choices in their personal and professional "
                    "lives. By recognising the specific biases that affect our thinking in particular "
                    "situations, we can develop strategies to counteract their influence and arrive at "
                    "choices that more accurately reflect our genuine interests and values."
                ),
                "question_groups": [
                    {
                        "order": 1,
                        "question_type": "tfng",
                        "instruction": (
                            "Do the following statements agree with the information given in the "
                            "Reading Passage?\n\nWrite:\n"
                            "TRUE    if the statement agrees with the information\n"
                            "FALSE   if the statement contradicts the information\n"
                            "NOT GIVEN  if there is no information on this"
                        ),
                        "questions": [
                            {"local_order": 1, "stem": "Rational choice theory assumed that people always make decisions that maximise their well-being.", "correct_answer": "TRUE"},
                            {"local_order": 2, "stem": "Kahneman and Tversky showed that cognitive heuristics never help people make good decisions.", "correct_answer": "FALSE"},
                            {"local_order": 3, "stem": "Damasio's patients with emotional brain damage made better decisions than healthy individuals.", "correct_answer": "FALSE"},
                            {"local_order": 4, "stem": "The behavioural insights approach has been formally adopted by governments in more than ten countries.", "correct_answer": "NOT GIVEN"},
                        ],
                    },
                    {
                        "order": 2,
                        "question_type": "matching_headings",
                        "instruction": (
                            "The Reading Passage has six paragraphs, A–F.\n"
                            "Choose the correct heading for paragraphs C–F from the list of headings below."
                        ),
                        "options_pool": {
                            "i":   "How presentation affects our choices",
                            "ii":  "The limits of rational economic models",
                            "iii": "Individual benefits of understanding bias",
                            "iv":  "Emotional processing as a decision tool",
                            "v":   "Government application of behavioural insights",
                            "vi":  "Mental shortcuts and their consequences",
                        },
                        "questions": [
                            {"local_order": 1, "stem": "Paragraph C", "correct_answer": "iv", "answer_variants": ["iv"]},
                            {"local_order": 2, "stem": "Paragraph D", "correct_answer": "i",  "answer_variants": ["i"]},
                            {"local_order": 3, "stem": "Paragraph E", "correct_answer": "v",  "answer_variants": ["v"]},
                            {"local_order": 4, "stem": "Paragraph F", "correct_answer": "iii","answer_variants": ["iii"]},
                        ],
                    },
                    {
                        "order": 3,
                        "question_type": "short_answer",
                        "instruction": "Answer the questions below. Choose NO MORE THAN THREE WORDS from the passage for each answer.",
                        "word_limit": 3,
                        "questions": [
                            {"local_order": 1, "stem": "What term describes the mental shortcuts people use when making quick judgements?", "correct_answer": "heuristics", "answer_variants": ["cognitive shortcuts"]},
                            {"local_order": 2, "stem": "What type of heuristic leads people to misjudge the probability of widely-reported events?", "correct_answer": "availability heuristic"},
                            {"local_order": 3, "stem": "What is the term for a policy intervention that makes the beneficial option the default choice?", "correct_answer": "nudge", "answer_variants": ["nudges"]},
                            {"local_order": 4, "stem": "What field combines psychology and economics to improve policy and individual decision-making?", "correct_answer": "behavioural economics"},
                            {"local_order": 5, "stem": "Name one country mentioned as having a dedicated government behavioural insights team.", "correct_answer": "United Kingdom", "answer_variants": ["UK", "United States", "US"]},
                        ],
                    },
                ],
            },

            # ── Passage 3: Smart Cities (Q27-40) ────────────────────────────
            {
                "order": 3,
                "title": "Smart Cities: Promises and Pitfalls",
                "body_text": (
                    "In the 21st century, cities face an unprecedented convergence of challenges. "
                    "Rapid urbanisation — with more than half the global population now living in "
                    "urban areas and projections suggesting this will rise to two-thirds by 2050 "
                    "— places enormous pressure on infrastructure, services, and the environment. "
                    "In response, planners and technology companies have promoted the concept of the "
                    "'smart city': an urban environment in which digital technology and data "
                    "analytics are used to enhance efficiency, sustainability, and quality of life.\n\n"

                    "Smart city initiatives typically integrate sensors, connected devices, and data "
                    "networks across urban infrastructure. Traffic management systems that adjust "
                    "signal timing in real time to reduce congestion, smart meters that optimise "
                    "energy and water consumption, and public transport networks that respond "
                    "dynamically to passenger demand are among the most widespread applications. "
                    "Barcelona, Singapore, and Amsterdam are frequently cited as leading examples "
                    "of cities that have successfully implemented such systems at scale.\n\n"

                    "A key component of smart city strategies is using data to improve public "
                    "services. Sensors embedded in rubbish bins can signal collection vehicles when "
                    "they are full, reducing unnecessary journeys and lowering emissions. Street "
                    "lighting that dims automatically when streets are empty saves significant "
                    "amounts of energy. In some cities, predictive analytics identify areas at high "
                    "risk of flooding or infrastructure failure before problems occur, enabling "
                    "preventive maintenance rather than costly emergency repairs.\n\n"

                    "Critics raise important concerns. The collection of vast quantities of data "
                    "about citizens' movements and daily routines raises serious questions about "
                    "privacy and civil liberties. Data breaches and unauthorised access have "
                    "highlighted these risks. Furthermore, the high cost of smart city technology "
                    "means its benefits are often concentrated in wealthier urban areas, potentially "
                    "widening the gap between affluent districts and economically disadvantaged "
                    "communities within the same city.\n\n"

                    "Questions of governance are also at stake. When critical urban services are "
                    "managed by private technology companies rather than elected authorities, "
                    "transparency and democratic accountability become problematic. The high-profile "
                    "withdrawal of Sidewalk Labs — a subsidiary of Google's parent company "
                    "Alphabet — from a major smart city project in Toronto in 2020 brought these "
                    "issues to widespread public attention.\n\n"

                    "Despite these challenges, digital technology will play an increasingly central "
                    "role in urban management. The most successful approaches treat technology as a "
                    "means rather than an end: using data and digital tools to address specific, "
                    "identified problems rather than pursuing innovation for its own sake. Inclusive "
                    "governance models that involve citizens in decision-making, alongside robust "
                    "regulatory frameworks to protect privacy and ensure equitable distribution of "
                    "benefits, are widely regarded as prerequisites for smart city projects that "
                    "genuinely serve the public interest."
                ),
                "question_groups": [
                    {
                        "order": 1,
                        "question_type": "mcq",
                        "instruction": "Choose the correct letter, A, B, C or D.",
                        "questions": [
                            {
                                "local_order": 1,
                                "stem": "According to the passage, what proportion of the global population will live in urban areas by 2050?",
                                "options": [
                                    {"key": "A", "text": "About a quarter"},
                                    {"key": "B", "text": "More than half"},
                                    {"key": "C", "text": "Approximately two-thirds"},
                                    {"key": "D", "text": "Nearly all"},
                                ],
                                "correct_answer": "C",
                            },
                            {
                                "local_order": 2,
                                "stem": "What do Barcelona, Singapore, and Amsterdam have in common according to the passage?",
                                "options": [
                                    {"key": "A", "text": "They invented the concept of the smart city"},
                                    {"key": "B", "text": "They have implemented smart city systems at scale"},
                                    {"key": "C", "text": "They are the most densely populated cities in their regions"},
                                    {"key": "D", "text": "They have banned the use of private technology companies"},
                                ],
                                "correct_answer": "B",
                            },
                            {
                                "local_order": 3,
                                "stem": "How do smart rubbish collection systems improve efficiency?",
                                "options": [
                                    {"key": "A", "text": "By automatically sorting recyclable materials"},
                                    {"key": "B", "text": "By compressing rubbish to reduce volume"},
                                    {"key": "C", "text": "By signalling vehicles only when bins are full"},
                                    {"key": "D", "text": "By using robots to collect rubbish at night"},
                                ],
                                "correct_answer": "C",
                            },
                            {
                                "local_order": 4,
                                "stem": "What is the primary concern critics raise about smart city data collection?",
                                "options": [
                                    {"key": "A", "text": "Data infrastructure is too expensive to maintain"},
                                    {"key": "B", "text": "Smart city technology rarely works as intended"},
                                    {"key": "C", "text": "Data collection threatens citizens' privacy and civil liberties"},
                                    {"key": "D", "text": "Smart cities depend too heavily on foreign technology"},
                                ],
                                "correct_answer": "C",
                            },
                            {
                                "local_order": 5,
                                "stem": "What did the Sidewalk Labs withdrawal from Toronto bring to public attention?",
                                "options": [
                                    {"key": "A", "text": "Technical difficulties of implementing smart infrastructure"},
                                    {"key": "B", "text": "The risk of data breaches in connected urban environments"},
                                    {"key": "C", "text": "Questions about governance and accountability in smart city projects"},
                                    {"key": "D", "text": "The financial instability of technology companies in urban sectors"},
                                ],
                                "correct_answer": "C",
                            },
                        ],
                    },
                    {
                        "order": 2,
                        "question_type": "sentence_completion",
                        "instruction": "Complete the sentences below. Choose NO MORE THAN TWO WORDS from the passage for each answer.",
                        "word_limit": 2,
                        "questions": [
                            {"local_order": 1, "stem": "More than half the global population currently lives in _____ areas.", "correct_answer": "urban"},
                            {"local_order": 2, "stem": "Smart city technology that identifies risks before they occur enables _____ maintenance.", "correct_answer": "preventive"},
                            {"local_order": 3, "stem": "Street lighting systems that adjust automatically when areas are empty can save significant amounts of _____.", "correct_answer": "energy"},
                            {"local_order": 4, "stem": "Sidewalk Labs is a subsidiary of Google's parent company _____.", "correct_answer": "Alphabet"},
                            {"local_order": 5, "stem": "Researchers suggest technology should be treated as a _____ rather than an end in urban planning.", "correct_answer": "means"},
                        ],
                    },
                    {
                        "order": 3,
                        "question_type": "short_answer",
                        "instruction": "Answer the questions below. Choose NO MORE THAN THREE WORDS from the passage for each answer.",
                        "word_limit": 3,
                        "questions": [
                            {"local_order": 1, "stem": "What type of analytics enables cities to identify flooding risks before they occur?", "correct_answer": "predictive analytics"},
                            {"local_order": 2, "stem": "Name one city mentioned as a leading example of smart city implementation.", "correct_answer": "Barcelona", "answer_variants": ["Singapore", "Amsterdam"]},
                            {"local_order": 3, "stem": "What must be in place to ensure the equitable distribution of smart city benefits?", "correct_answer": "regulatory frameworks", "answer_variants": ["inclusive governance"]},
                            {"local_order": 4, "stem": "What type of governance model is described as involving citizens in smart city decision-making?", "correct_answer": "inclusive governance"},
                        ],
                    },
                ],
            },
        ],
    },

    # ═════════════════════════════════════════════════════════════════════════
    # TEST 2  —  Remote Work · Biodiversity · Vaccination
    # ═════════════════════════════════════════════════════════════════════════
    {
        "title":      "IELTS Academic Reading — Set 2",
        "test_type":  "academic",
        "component":  "reading",
        "time_limit": 60,
        "passages": [

            # ── Passage 1: Remote Work Revolution (Q1-13) ───────────────────
            {
                "order": 1,
                "title": "The Remote Work Revolution",
                "body_text": (
                    "The COVID-19 pandemic of 2020 precipitated what many consider the largest "
                    "unplanned experiment in remote working in human history. Within weeks, millions "
                    "of office workers found themselves working from home, forcing organisations "
                    "to rapidly adapt their processes, technologies, and management approaches. "
                    "While remote work had existed as a limited option prior to the pandemic, its "
                    "sudden universal adoption provided an unprecedented opportunity to examine "
                    "both its benefits and challenges at scale.\n\n"

                    "Research conducted during and after the pandemic revealed a nuanced picture. "
                    "Surveys of knowledge workers — those whose work primarily involves creating, "
                    "processing, or communicating information — consistently report higher levels "
                    "of satisfaction with remote work than with traditional office employment. "
                    "Benefits cited include elimination of commuting time, greater scheduling "
                    "flexibility, and reduced workplace distractions. However, collaborative and "
                    "creative work may suffer without the spontaneous interactions that office "
                    "environments facilitate.\n\n"

                    "For organisations, the remote work shift delivered mixed results. Costs "
                    "associated with office space, utilities, and urban-centre amenities fell "
                    "significantly for companies that reduced their physical footprints. However, "
                    "maintaining organisational culture, onboarding new employees effectively, "
                    "and preserving institutional knowledge became more challenging in distributed "
                    "environments. Productivity effects vary significantly by role: while software "
                    "developers and data analysts have generally adapted well, roles requiring "
                    "physical presence or access to specialised equipment have struggled.\n\n"

                    "The rapid normalisation of remote work has reshaped the geography of "
                    "employment. Workers freed from commuting requirements have migrated to "
                    "smaller towns and rural areas, seeking larger homes, lower costs, and "
                    "different quality-of-life priorities. This population shift has brought "
                    "economic benefits to some previously declining communities while contributing "
                    "to housing price pressures in previously affordable areas.\n\n"

                    "Questions of equity have also come to the fore. Remote work opportunities "
                    "are heavily concentrated in higher-paying professional and managerial "
                    "occupations. Workers in healthcare, manufacturing, food service, and transport "
                    "— essential industries — generally cannot work from home. This asymmetry "
                    "has reinforced existing socioeconomic inequalities, as those who can work "
                    "remotely have maintained their economic positions while others faced greater "
                    "employment instability.\n\n"

                    "Most organisations are converging on hybrid working models that combine "
                    "remote and in-person work. Rather than a binary choice between full office "
                    "attendance and fully remote arrangements, hybrid models attempt to preserve "
                    "the flexibility many workers value while maintaining the collaborative, "
                    "cultural, and mentoring functions that physical co-presence best provides."
                ),
                "question_groups": [
                    {
                        "order": 1,
                        "question_type": "tfng",
                        "instruction": (
                            "Do the following statements agree with the information given in the "
                            "Reading Passage?\n\nWrite:\n"
                            "TRUE    if the statement agrees with the information\n"
                            "FALSE   if the statement contradicts the information\n"
                            "NOT GIVEN  if there is no information on this"
                        ),
                        "questions": [
                            {"local_order": 1, "stem": "Remote work did not exist in any form before the COVID-19 pandemic.", "correct_answer": "FALSE"},
                            {"local_order": 2, "stem": "Knowledge workers generally report greater satisfaction with remote work than office work.", "correct_answer": "TRUE"},
                            {"local_order": 3, "stem": "All organisations experienced increased productivity when staff moved to remote work.", "correct_answer": "FALSE"},
                            {"local_order": 4, "stem": "Remote work has caused some workers to relocate from major cities to rural areas.", "correct_answer": "TRUE"},
                            {"local_order": 5, "stem": "Hybrid working models are expected to completely replace traditional office environments within a decade.", "correct_answer": "NOT GIVEN"},
                        ],
                    },
                    {
                        "order": 2,
                        "question_type": "mcq",
                        "instruction": "Choose the correct letter, A, B, C or D.",
                        "questions": [
                            {
                                "local_order": 1,
                                "stem": "According to paragraph 2, which types of tasks do remote workers find more difficult?",
                                "options": [
                                    {"key": "A", "text": "Tasks requiring sustained concentration"},
                                    {"key": "B", "text": "Individual data-intensive assignments"},
                                    {"key": "C", "text": "Collaborative and creative work"},
                                    {"key": "D", "text": "Time-sensitive administrative duties"},
                                ],
                                "correct_answer": "C",
                            },
                            {
                                "local_order": 2,
                                "stem": "Which type of worker is described as having generally adapted well to remote work?",
                                "options": [
                                    {"key": "A", "text": "Healthcare professionals"},
                                    {"key": "B", "text": "Food service workers"},
                                    {"key": "C", "text": "Transport operators"},
                                    {"key": "D", "text": "Software developers"},
                                ],
                                "correct_answer": "D",
                            },
                            {
                                "local_order": 3,
                                "stem": "What impact has the growth of remote work had on some smaller communities?",
                                "options": [
                                    {"key": "A", "text": "Population decline as workers moved to cities"},
                                    {"key": "B", "text": "Economic benefits from an influx of new residents"},
                                    {"key": "C", "text": "Increased demand for office space"},
                                    {"key": "D", "text": "Higher levels of local unemployment"},
                                ],
                                "correct_answer": "B",
                            },
                            {
                                "local_order": 4,
                                "stem": "What best characterises the concept of hybrid working described in the passage?",
                                "options": [
                                    {"key": "A", "text": "Choosing either fully remote or fully in-office employment"},
                                    {"key": "B", "text": "Different employees working under different contract types"},
                                    {"key": "C", "text": "A combination of remote and in-person work"},
                                    {"key": "D", "text": "Using technology to recreate the office environment at home"},
                                ],
                                "correct_answer": "C",
                            },
                        ],
                    },
                    {
                        "order": 3,
                        "question_type": "sentence_completion",
                        "instruction": "Complete the sentences below. Choose NO MORE THAN TWO WORDS from the passage for each answer.",
                        "word_limit": 2,
                        "questions": [
                            {"local_order": 1, "stem": "Workers whose jobs primarily involve creating or processing information are called _____ workers.", "correct_answer": "knowledge"},
                            {"local_order": 2, "stem": "A key benefit of remote work cited by workers is the elimination of _____ time.", "correct_answer": "commuting"},
                            {"local_order": 3, "stem": "Costs associated with _____ fell significantly for companies that reduced their physical footprints.", "correct_answer": "office space"},
                            {"local_order": 4, "stem": "The concentration of remote work in higher-paying roles has reinforced existing _____ inequalities.", "correct_answer": "socioeconomic"},
                        ],
                    },
                ],
            },

            # ── Passage 2: Biodiversity Loss (Q14-26) ───────────────────────
            {
                "order": 2,
                "title": "Biodiversity Loss: Causes and Consequences",
                "body_text": (
                    "Biodiversity — the variety of life on Earth across all its forms — is "
                    "declining at a rate scientists describe as the sixth mass extinction event in "
                    "planetary history. Unlike the five previous mass extinctions, caused by natural "
                    "events such as asteroid impacts and volcanic eruptions, the current crisis is "
                    "driven predominantly by human activities. The consequences for ecosystems, "
                    "economies, and human well-being are profound and, in many cases, irreversible.\n\n"

                    "The primary drivers of biodiversity loss are well established. Habitat "
                    "destruction, particularly through conversion of forests, wetlands, and "
                    "grasslands into agricultural land, is widely regarded as the leading cause. "
                    "Agriculture occupies approximately 50 per cent of the world's habitable land, "
                    "a proportion that has doubled over the past century. The fragmentation of "
                    "remaining habitats into isolated patches further compounds the problem by "
                    "reducing population sizes, limiting genetic diversity, and preventing species "
                    "from migrating in response to climate change.\n\n"

                    "Climate change itself is rapidly emerging as a significant threat. Rising "
                    "temperatures are shifting the geographical ranges within which many species "
                    "can survive, forcing populations towards the poles and to higher altitudes. "
                    "Species unable to migrate quickly enough, particularly those with small "
                    "populations or restricted ranges, face local or global extinction. Ocean "
                    "warming and acidification are bleaching coral reefs and disrupting the marine "
                    "food webs that support hundreds of thousands of species.\n\n"

                    "Overexploitation of natural resources — through hunting, fishing, and trade "
                    "in wild species — represents another major driver. Approximately one-third "
                    "of commercial fish populations are harvested at unsustainable levels. The "
                    "illegal wildlife trade, estimated at tens of billions of dollars annually, "
                    "drives the decline of species such as elephants, rhinoceroses, and pangolins. "
                    "Invasive species introduced to new environments have caused the extinction of "
                    "numerous indigenous species on islands and in freshwater systems.\n\n"

                    "Biodiversity underpins ecosystem services on which human societies depend. "
                    "Pollination by wild insects is essential to approximately three-quarters of "
                    "crop species, representing a service with an annual value of hundreds of "
                    "billions of dollars. Coastal wetlands and mangrove forests protect shorelines "
                    "from erosion and storm damage. The genetic diversity of wild species has "
                    "repeatedly yielded compounds with medical applications, from aspirin to "
                    "anti-cancer drugs.\n\n"

                    "Conservation efforts have achieved significant successes in particular cases. "
                    "International agreements such as CITES have helped stabilise some threatened "
                    "animal populations. Protected area networks cover approximately 15 per cent "
                    "of the world's land surface, though their effectiveness depends critically "
                    "on adequate funding and enforcement. Conservationists increasingly emphasise "
                    "integrating biodiversity objectives into mainstream economic and land-use "
                    "decisions, rather than confining conservation to designated protected areas."
                ),
                "question_groups": [
                    {
                        "order": 1,
                        "question_type": "tfng",
                        "instruction": (
                            "Do the following statements agree with the information given in the "
                            "Reading Passage?\n\nWrite:\n"
                            "TRUE    if the statement agrees with the information\n"
                            "FALSE   if the statement contradicts the information\n"
                            "NOT GIVEN  if there is no information on this"
                        ),
                        "questions": [
                            {"local_order": 1, "stem": "The current biodiversity crisis is driven mainly by natural events, as were previous mass extinctions.", "correct_answer": "FALSE"},
                            {"local_order": 2, "stem": "Agricultural land currently covers approximately 50 per cent of the world's habitable land.", "correct_answer": "TRUE"},
                            {"local_order": 3, "stem": "Climate change only affects terrestrial species and has no impact on marine biodiversity.", "correct_answer": "FALSE"},
                            {"local_order": 4, "stem": "The genetic material found in wild species has contributed to the development of medical treatments.", "correct_answer": "TRUE"},
                        ],
                    },
                    {
                        "order": 2,
                        "question_type": "matching_headings",
                        "instruction": (
                            "The Reading Passage has six paragraphs, A–F.\n"
                            "Choose the correct heading for paragraphs B, D, E and F "
                            "from the list of headings below."
                        ),
                        "options_pool": {
                            "i":   "How habitat loss isolates wildlife populations",
                            "ii":  "The economic value of natural ecosystem services",
                            "iii": "Past successes and limitations of conservation efforts",
                            "iv":  "Human exploitation driving species decline",
                            "v":   "The relationship between climate and ocean health",
                            "vi":  "The scale and urgency of the biodiversity crisis",
                        },
                        "questions": [
                            {"local_order": 1, "stem": "Paragraph B", "correct_answer": "i",   "answer_variants": ["i"]},
                            {"local_order": 2, "stem": "Paragraph D", "correct_answer": "iv",  "answer_variants": ["iv"]},
                            {"local_order": 3, "stem": "Paragraph E", "correct_answer": "ii",  "answer_variants": ["ii"]},
                            {"local_order": 4, "stem": "Paragraph F", "correct_answer": "iii", "answer_variants": ["iii"]},
                        ],
                    },
                    {
                        "order": 3,
                        "question_type": "short_answer",
                        "instruction": "Answer the questions below. Choose NO MORE THAN THREE WORDS from the passage for each answer.",
                        "word_limit": 3,
                        "questions": [
                            {"local_order": 1, "stem": "What proportion of the world's habitable land is currently used for agriculture?", "correct_answer": "50 per cent", "answer_variants": ["approximately 50 per cent", "50%"]},
                            {"local_order": 2, "stem": "What fraction of commercial fish populations are being harvested at unsustainable levels?", "correct_answer": "one-third", "answer_variants": ["approximately one-third", "a third"]},
                            {"local_order": 3, "stem": "What proportion of crop species depends on pollination by wild insects?", "correct_answer": "three-quarters", "answer_variants": ["approximately three-quarters"]},
                            {"local_order": 4, "stem": "What percentage of the world's land surface is covered by protected areas?", "correct_answer": "15 per cent", "answer_variants": ["approximately 15 per cent", "15%"]},
                            {"local_order": 5, "stem": "Name one example of an iconic species threatened by the illegal wildlife trade.", "correct_answer": "elephants", "answer_variants": ["rhinoceroses", "pangolins", "elephant", "rhinoceros", "pangolin"]},
                        ],
                    },
                ],
            },

            # ── Passage 3: Vaccination (Q27-40) ─────────────────────────────
            {
                "order": 3,
                "title": "Vaccination: History and Modern Challenges",
                "body_text": (
                    "The development of vaccines represents one of the most significant "
                    "achievements in the history of medicine. By priming the immune system to "
                    "recognise specific pathogens without the risks of actual infection, vaccines "
                    "have dramatically reduced — and in some cases eliminated — diseases that "
                    "once caused widespread disability and death. The eradication of smallpox in "
                    "1980, declared by the World Health Organization after a decade-long global "
                    "campaign, stands as the most complete triumph of vaccination to date.\n\n"

                    "The story begins with Edward Jenner, an English physician who observed that "
                    "milkmaids who contracted cowpox — a mild disease related to smallpox — "
                    "appeared protected against the far more deadly smallpox virus. In 1796, "
                    "Jenner inoculated a young boy with cowpox material and subsequently exposed "
                    "him to smallpox, demonstrating that earlier exposure provided protection. "
                    "Though Jenner did not understand the immunological mechanisms, his work laid "
                    "the foundation for one of medicine's most powerful preventive tools.\n\n"

                    "Vaccination programmes throughout the twentieth century produced dramatic "
                    "reductions in infectious disease. Poliomyelitis, measles, diphtheria, and "
                    "pertussis, which had killed millions annually, became rare in countries with "
                    "high vaccination coverage. The development of oral polio vaccine in the "
                    "1950s, which could be administered without syringes and maintained its "
                    "efficacy in resource-limited settings, was particularly transformative.\n\n"

                    "Modern vaccines are produced through a variety of techniques, from "
                    "conventional approaches using killed or weakened pathogens to newer mRNA "
                    "technology, which instructs cells to produce a protein that triggers an "
                    "immune response. The rapid development of mRNA vaccines against SARS-CoV-2 "
                    "during the COVID-19 pandemic — achieving regulatory approval within less "
                    "than a year of the virus being identified — demonstrated this technology's "
                    "potential to respond rapidly to emerging infectious threats.\n\n"

                    "Despite proven vaccine efficacy, vaccine hesitancy — a reluctance or "
                    "refusal to accept vaccines despite their availability — has become a "
                    "significant public health challenge. Concerns about vaccine safety, fuelled "
                    "partly by misinformation spread through social media, have contributed to "
                    "declining vaccination coverage. The consequences are tangible: outbreaks of "
                    "measles have occurred in countries including the United States and across "
                    "Europe in regions where coverage has fallen below the threshold for herd "
                    "immunity.\n\n"

                    "Global distribution raises distinct equity challenges. While high-income "
                    "countries maintain consistent access to an expanding vaccine portfolio, "
                    "many low-income countries continue to struggle with the costs, cold-chain "
                    "infrastructure requirements, and healthcare workforce capacity needed for "
                    "high coverage. The COVID-19 pandemic exposed these inequities starkly: "
                    "wealthy nations secured early access through advance purchase agreements "
                    "while many developing countries waited months for initial supplies."
                ),
                "question_groups": [
                    {
                        "order": 1,
                        "question_type": "mcq",
                        "instruction": "Choose the correct letter, A, B, C or D.",
                        "questions": [
                            {
                                "local_order": 1,
                                "stem": "According to the passage, smallpox was formally declared eradicated in:",
                                "options": [
                                    {"key": "A", "text": "1796"},
                                    {"key": "B", "text": "The 1950s"},
                                    {"key": "C", "text": "1980"},
                                    {"key": "D", "text": "2020"},
                                ],
                                "correct_answer": "C",
                            },
                            {
                                "local_order": 2,
                                "stem": "What observation led Edward Jenner to investigate vaccination?",
                                "options": [
                                    {"key": "A", "text": "People with certain blood types resisted smallpox"},
                                    {"key": "B", "text": "Milkmaids who had cowpox seemed protected against smallpox"},
                                    {"key": "C", "text": "People living near cattle rarely died from any infection"},
                                    {"key": "D", "text": "Children recovered more quickly from smallpox than adults"},
                                ],
                                "correct_answer": "B",
                            },
                            {
                                "local_order": 3,
                                "stem": "What advantage of oral polio vaccine made it particularly useful in resource-limited settings?",
                                "options": [
                                    {"key": "A", "text": "It was cheaper to manufacture than injectable vaccines"},
                                    {"key": "B", "text": "It could be combined with other vaccines in a single dose"},
                                    {"key": "C", "text": "It could be given without syringes and maintained efficacy in difficult conditions"},
                                    {"key": "D", "text": "It provided lifelong immunity after a single dose"},
                                ],
                                "correct_answer": "C",
                            },
                            {
                                "local_order": 4,
                                "stem": "What does mRNA vaccine technology demonstrate, according to the passage?",
                                "options": [
                                    {"key": "A", "text": "Traditional vaccine methods are no longer reliable"},
                                    {"key": "B", "text": "The technology can respond rapidly to new infectious threats"},
                                    {"key": "C", "text": "Regulatory approval processes have become too slow"},
                                    {"key": "D", "text": "Private companies should control vaccine development"},
                                ],
                                "correct_answer": "B",
                            },
                            {
                                "local_order": 5,
                                "stem": "What has been a demonstrable consequence of declining vaccination rates in some regions?",
                                "options": [
                                    {"key": "A", "text": "The appearance of entirely new infectious diseases"},
                                    {"key": "B", "text": "Outbreaks of previously controlled diseases such as measles"},
                                    {"key": "C", "text": "An increase in antibiotic resistance"},
                                    {"key": "D", "text": "Reduced effectiveness of existing vaccines"},
                                ],
                                "correct_answer": "B",
                            },
                        ],
                    },
                    {
                        "order": 2,
                        "question_type": "sentence_completion",
                        "instruction": "Complete the sentences below. Choose NO MORE THAN TWO WORDS from the passage for each answer.",
                        "word_limit": 2,
                        "questions": [
                            {"local_order": 1, "stem": "Vaccines prime the body's _____ system to recognise specific pathogens without causing actual infection.", "correct_answer": "immune"},
                            {"local_order": 2, "stem": "The first human deliberately given vaccine material was a young _____ by Edward Jenner.", "correct_answer": "boy"},
                            {"local_order": 3, "stem": "The oral polio vaccine was especially valuable because it could be given without medical _____.", "correct_answer": "syringes"},
                            {"local_order": 4, "stem": "mRNA vaccines work by instructing cells to produce a _____ that triggers an immune response.", "correct_answer": "protein"},
                            {"local_order": 5, "stem": "A decline in coverage can cause outbreaks in communities that previously had _____ immunity.", "correct_answer": "herd"},
                        ],
                    },
                    {
                        "order": 3,
                        "question_type": "short_answer",
                        "instruction": "Answer the questions below. Choose NO MORE THAN THREE WORDS from the passage for each answer.",
                        "word_limit": 3,
                        "questions": [
                            {"local_order": 1, "stem": "What disease did Edward Jenner use in his early vaccination experiments?", "correct_answer": "cowpox"},
                            {"local_order": 2, "stem": "What term describes a reluctance or refusal to accept vaccines despite their availability?", "correct_answer": "vaccine hesitancy"},
                            {"local_order": 3, "stem": "What type of infrastructure required in developing countries presents a significant challenge to vaccine distribution?", "correct_answer": "cold-chain", "answer_variants": ["cold chain"]},
                            {"local_order": 4, "stem": "What mechanism allowed wealthy nations to secure early vaccine access during the COVID-19 pandemic?", "correct_answer": "advance purchase agreements"},
                        ],
                    },
                ],
            },
        ],
    },

    # ═════════════════════════════════════════════════════════════════════════
    # TEST 3  —  AI in Healthcare · Silk Road · Science of Memory
    # ═════════════════════════════════════════════════════════════════════════
    {
        "title":      "IELTS Academic Reading — Set 3",
        "test_type":  "academic",
        "component":  "reading",
        "time_limit": 60,
        "passages": [

            # ── Passage 1: AI in Healthcare (Q1-13) ─────────────────────────
            {
                "order": 1,
                "title": "Artificial Intelligence in Healthcare",
                "body_text": (
                    "Artificial intelligence is rapidly transforming medical practice, offering "
                    "faster and more accurate diagnoses, personalised treatment plans, and more "
                    "efficient healthcare delivery. Machine learning algorithms — systems that "
                    "improve their performance through exposure to large datasets rather than "
                    "explicit programming — have demonstrated impressive capabilities in "
                    "analysing medical images, interpreting genomic data, and predicting patient "
                    "outcomes.\n\n"

                    "In radiology, AI systems trained on millions of medical images have achieved "
                    "diagnostic accuracy comparable to, and in some specific tasks exceeding, that "
                    "of experienced radiologists. Research has shown that machine learning models "
                    "can detect certain cancers — including breast cancer in mammograms and lung "
                    "cancer in CT scans — with high sensitivity. At a time when many health "
                    "systems face shortages of specialist physicians, AI tools that rapidly screen "
                    "large volumes of imaging data have the potential to significantly expand "
                    "diagnostic capacity.\n\n"

                    "Beyond imaging, AI is being applied to drug discovery. Traditional drug "
                    "development — from initial compound identification to regulatory approval "
                    "— can take more than a decade and cost billions of dollars, with most "
                    "candidate compounds failing at late stages of testing. AI systems can analyse "
                    "vast chemical libraries to predict which compounds are most likely to be "
                    "effective, substantially reducing the time required. In 2020, AlphaFold — "
                    "an AI system developed by the London-based company DeepMind — solved one "
                    "of biology's grand challenges by accurately predicting the three-dimensional "
                    "structure of proteins from their amino acid sequences.\n\n"

                    "The integration of AI into clinical decision-making raises important questions "
                    "about responsibility. When an AI system contributes to a diagnostic error, "
                    "determining liability becomes complex. The opacity of many machine learning "
                    "models — often described as 'black box' systems because their internal "
                    "reasoning cannot easily be inspected — complicates the identification of "
                    "errors and makes it harder to build the clinical trust required for adoption.\n\n"

                    "Issues of bias represent another significant concern. AI systems learn from "
                    "historical data, which often reflects longstanding inequalities in healthcare "
                    "provision. A model trained predominantly on data from one demographic group "
                    "may perform less accurately for others. Documented cases of AI diagnostic "
                    "tools performing less well for patients with darker skin tones highlight the "
                    "risk of technology reinforcing rather than reducing existing health disparities.\n\n"

                    "Despite these challenges, there is widespread consensus that AI will play an "
                    "increasingly important role in healthcare. The most optimistic visions "
                    "imagine genuinely personalised medicine — treatments tailored to the "
                    "specific genetic, physiological, and lifestyle characteristics of individual "
                    "patients — while freeing clinicians from routine tasks to focus on the "
                    "aspects of care that require empathy, judgement, and human connection."
                ),
                "question_groups": [
                    {
                        "order": 1,
                        "question_type": "tfng",
                        "instruction": (
                            "Do the following statements agree with the information given in the "
                            "Reading Passage?\n\nWrite:\n"
                            "TRUE    if the statement agrees with the information\n"
                            "FALSE   if the statement contradicts the information\n"
                            "NOT GIVEN  if there is no information on this"
                        ),
                        "questions": [
                            {"local_order": 1, "stem": "Machine learning systems improve through exposure to data rather than through specific programming instructions.", "correct_answer": "TRUE"},
                            {"local_order": 2, "stem": "AI systems always outperform experienced radiologists in diagnostic accuracy.", "correct_answer": "FALSE"},
                            {"local_order": 3, "stem": "Most drug candidates fail during the early stages of the testing process.", "correct_answer": "FALSE"},
                            {"local_order": 4, "stem": "The AlphaFold system was developed by a company based in London.", "correct_answer": "TRUE"},
                            {"local_order": 5, "stem": "All machine learning models can clearly explain the reasoning behind their decisions.", "correct_answer": "FALSE"},
                        ],
                    },
                    {
                        "order": 2,
                        "question_type": "mcq",
                        "instruction": "Choose the correct letter, A, B, C or D.",
                        "questions": [
                            {
                                "local_order": 1,
                                "stem": "What advantage do AI radiology tools offer to health systems facing physician shortages?",
                                "options": [
                                    {"key": "A", "text": "They can replace radiologists entirely"},
                                    {"key": "B", "text": "They enable rapid screening of large volumes of imaging data"},
                                    {"key": "C", "text": "They eliminate the risk of diagnostic error"},
                                    {"key": "D", "text": "They allow radiologists to work remotely"},
                                ],
                                "correct_answer": "B",
                            },
                            {
                                "local_order": 2,
                                "stem": "What was the significance of AlphaFold's achievement in 2020?",
                                "options": [
                                    {"key": "A", "text": "It identified a new class of anti-cancer drug compounds"},
                                    {"key": "B", "text": "It was the first AI to surpass all radiologists on a diagnostic task"},
                                    {"key": "C", "text": "It accurately predicted the three-dimensional structure of proteins"},
                                    {"key": "D", "text": "It reduced the cost of drug trials by over 50 per cent"},
                                ],
                                "correct_answer": "C",
                            },
                            {
                                "local_order": 3,
                                "stem": "Why is the 'black box' nature of many AI systems a problem in healthcare?",
                                "options": [
                                    {"key": "A", "text": "It makes AI systems too slow to be clinically useful"},
                                    {"key": "B", "text": "It prevents AI from accessing the full range of patient data"},
                                    {"key": "C", "text": "It makes identifying errors and building clinical trust more difficult"},
                                    {"key": "D", "text": "It means AI systems cannot learn from historical medical data"},
                                ],
                                "correct_answer": "C",
                            },
                            {
                                "local_order": 4,
                                "stem": "What risk associated with biased training data is described in the passage?",
                                "options": [
                                    {"key": "A", "text": "AI becoming too dependent on a single data source"},
                                    {"key": "B", "text": "Technology reinforcing rather than reducing health inequalities"},
                                    {"key": "C", "text": "Patients refusing to use AI-assisted diagnostic tools"},
                                    {"key": "D", "text": "AI performing less well as medical knowledge advances"},
                                ],
                                "correct_answer": "B",
                            },
                        ],
                    },
                    {
                        "order": 3,
                        "question_type": "sentence_completion",
                        "instruction": "Complete the sentences below. Choose NO MORE THAN TWO WORDS from the passage for each answer.",
                        "word_limit": 2,
                        "questions": [
                            {"local_order": 1, "stem": "Machine learning systems improve their performance through exposure to large _____.", "correct_answer": "datasets", "answer_variants": ["data sets"]},
                            {"local_order": 2, "stem": "Traditional drug development from initial compound to approval can take more than a _____.", "correct_answer": "decade"},
                            {"local_order": 3, "stem": "Machine learning models are sometimes called '_____ box' systems because their internal reasoning is opaque.", "correct_answer": "black"},
                            {"local_order": 4, "stem": "The optimistic vision of AI in healthcare imagines genuinely _____ medicine tailored to each patient's characteristics.", "correct_answer": "personalised"},
                        ],
                    },
                ],
            },

            # ── Passage 2: The Silk Road (Q14-26) ───────────────────────────
            {
                "order": 2,
                "title": "The Silk Road: Commerce and Cultural Exchange",
                "body_text": (
                    "The Silk Road — the network of overland and maritime trade routes connecting "
                    "East Asia, Central Asia, the Middle East, and Europe from antiquity through "
                    "the early modern period — was not a single road but a vast, shifting web "
                    "of paths across some of the world's most challenging terrain. Despite its "
                    "name, derived from the high-value Chinese silk that was among the most prized "
                    "commodities, the Silk Road carried an extraordinary variety of goods in both "
                    "directions: spices, glassware, paper, textiles, precious metals, and horses, "
                    "as well as ideas, religions, technologies, and diseases.\n\n"

                    "The origins of Silk Road trade can be traced to the second century BCE, when "
                    "the Han Chinese emperor dispatched the diplomat Zhang Qian westward to forge "
                    "alliances against a nomadic confederation known as the Xiongnu. Though his "
                    "military mission largely failed, Zhang Qian returned with detailed knowledge "
                    "of Central Asian civilisations, resources, and trade possibilities, "
                    "catalysing a dramatic expansion of commercial and diplomatic exchange. Within "
                    "decades, caravans bearing Chinese goods were travelling regularly to Parthia.\n\n"

                    "At its height during the Tang dynasty (618–907 CE), Chang'an — the Chinese "
                    "imperial capital near modern-day Xi'an — was one of the most cosmopolitan "
                    "cities in the world. Buddhist monasteries, Zoroastrian temples, Nestorian "
                    "Christian churches, and Islamic mosques coexisted within the city walls, "
                    "reflecting the remarkable religious and cultural diversity that Silk Road "
                    "exchange had produced. Buddhist art from this period shows a rich fusion of "
                    "Indian, Central Asian, and Chinese artistic traditions.\n\n"

                    "The Silk Road served as the primary channel through which major world "
                    "religions spread across Eurasia. Buddhism travelled from India through "
                    "Central Asia to China along Silk Road routes, eventually becoming one of "
                    "China's most significant religious traditions. Islam spread rapidly across "
                    "Central Asia following the Arab conquests of the seventh century. "
                    "Papermaking technology, originally developed in China, diffused westward "
                    "along Silk Road networks, reaching the Arab world by the eighth century "
                    "and transforming the possibilities of written communication.\n\n"

                    "The gradual decline of overland Silk Road trade from the fifteenth century "
                    "onwards was driven by a combination of political and technological factors. "
                    "The Mongol Empire, which at its height had unified an enormous swath of "
                    "Eurasia under a single administration, fragmented and collapsed, "
                    "destabilising the conditions that had facilitated cross-continental travel. "
                    "Simultaneously, the development of oceanic navigation technology by European "
                    "powers opened new maritime routes between Europe and Asia that were faster "
                    "and capable of carrying far greater volumes of cargo. The Portuguese "
                    "establishment of a maritime route around Africa to India in 1498 "
                    "contributed to a fundamental shift in global trading patterns."
                ),
                "question_groups": [
                    {
                        "order": 1,
                        "question_type": "tfng",
                        "instruction": (
                            "Do the following statements agree with the information given in the "
                            "Reading Passage?\n\nWrite:\n"
                            "TRUE    if the statement agrees with the information\n"
                            "FALSE   if the statement contradicts the information\n"
                            "NOT GIVEN  if there is no information on this"
                        ),
                        "questions": [
                            {"local_order": 1, "stem": "The Silk Road was a single, well-defined route connecting China and Europe.", "correct_answer": "FALSE"},
                            {"local_order": 2, "stem": "Zhang Qian's original diplomatic mission was a complete political and military success.", "correct_answer": "FALSE"},
                            {"local_order": 3, "stem": "Chang'an during the Tang dynasty was home to people and institutions from many different cultures and religions.", "correct_answer": "TRUE"},
                            {"local_order": 4, "stem": "Buddhist art of the Tang period was influenced purely by Chinese artistic traditions.", "correct_answer": "FALSE"},
                        ],
                    },
                    {
                        "order": 2,
                        "question_type": "matching_headings",
                        "instruction": (
                            "The Reading Passage has five paragraphs, A–E.\n"
                            "Choose the correct heading for paragraphs B, C, D and E "
                            "from the list of headings below."
                        ),
                        "options_pool": {
                            "i":   "The origins of Chinese westward exploration",
                            "ii":  "How Silk Road exchange shaped art and culture",
                            "iii": "The transfer of religions and technologies",
                            "iv":  "The maritime challenge to overland trade",
                            "v":   "The variety of commodities on the Silk Road",
                            "vi":  "Political rivalry along the trade routes",
                        },
                        "questions": [
                            {"local_order": 1, "stem": "Paragraph B", "correct_answer": "i",   "answer_variants": ["i"]},
                            {"local_order": 2, "stem": "Paragraph C", "correct_answer": "ii",  "answer_variants": ["ii"]},
                            {"local_order": 3, "stem": "Paragraph D", "correct_answer": "iii", "answer_variants": ["iii"]},
                            {"local_order": 4, "stem": "Paragraph E", "correct_answer": "iv",  "answer_variants": ["iv"]},
                        ],
                    },
                    {
                        "order": 3,
                        "question_type": "short_answer",
                        "instruction": "Answer the questions below. Choose NO MORE THAN THREE WORDS from the passage for each answer.",
                        "word_limit": 3,
                        "questions": [
                            {"local_order": 1, "stem": "What was the name of the Han Chinese diplomat sent westward in the second century BCE?", "correct_answer": "Zhang Qian"},
                            {"local_order": 2, "stem": "What was the name of the Chinese imperial capital during the Tang dynasty?", "correct_answer": "Chang'an", "answer_variants": ["Xi'an"]},
                            {"local_order": 3, "stem": "During which century did papermaking technology reach the Arab world via Silk Road networks?", "correct_answer": "eighth century"},
                            {"local_order": 4, "stem": "Which country established a maritime trade route around Africa to India in 1498?", "correct_answer": "Portuguese", "answer_variants": ["Portugal"]},
                            {"local_order": 5, "stem": "Name one type of religious building found within the walls of Tang dynasty Chang'an.", "correct_answer": "Buddhist monasteries", "answer_variants": ["Zoroastrian temples", "Islamic mosques", "Buddhist monastery", "Nestorian churches"]},
                        ],
                    },
                ],
            },

            # ── Passage 3: Science of Memory (Q27-40) ───────────────────────
            {
                "order": 3,
                "title": "The Science of Memory and Learning",
                "body_text": (
                    "Memory is not a single, unified system but a collection of distinct processes "
                    "involving different brain regions and operating according to different "
                    "principles. This insight emerged partly from careful study of patients with "
                    "memory impairments following brain injury — most famously from a patient "
                    "known for decades only by his initials, H.M., who underwent radical brain "
                    "surgery in 1953 to relieve severe epilepsy. He subsequently lost the ability "
                    "to form new long-term memories while retaining memories from before the "
                    "operation.\n\n"

                    "H.M.'s case clearly illustrated the distinction between short-term, or "
                    "working, memory and long-term memory. Working memory — the cognitive system "
                    "that holds and manipulates information for immediate use — typically retains "
                    "roughly seven items at a time for only seconds to minutes without active "
                    "rehearsal. Long-term memory, by contrast, appears to have essentially "
                    "unlimited capacity and can retain information for a lifetime, though with "
                    "variable fidelity.\n\n"

                    "Within long-term memory, researchers distinguish between declarative and "
                    "non-declarative forms. Declarative memory encompasses the conscious "
                    "recollection of facts and events: knowing that Paris is the capital of "
                    "France, or remembering the details of a specific conversation. "
                    "Non-declarative memory involves skills and learned behaviours operating "
                    "without conscious awareness — riding a bicycle or driving a familiar route. "
                    "H.M. was able to learn new motor skills despite being unable to remember "
                    "the learning sessions, demonstrating that these two systems operate "
                    "independently.\n\n"

                    "Memories are not stored as fixed recordings. Each time a memory is "
                    "retrieved, it enters a temporarily unstable state and must be "
                    "reconsolidated — essentially re-stored — before it can be accessed again. "
                    "This means memories can be subtly altered each time they are recalled: new "
                    "information acquired around the time of retrieval can be integrated into "
                    "the stored memory. This process explains why eyewitness testimony is often "
                    "less reliable than intuition might suggest.\n\n"

                    "Sleep plays a critical role in memory consolidation — the process by which "
                    "newly acquired information is transferred from temporary storage into more "
                    "permanent long-term memory. During slow-wave sleep, the hippocampus — the "
                    "brain region particularly associated with forming new declarative memories "
                    "— appears to replay recently acquired information, facilitating its transfer "
                    "to the cortex. Studies consistently show that sleep deprivation severely "
                    "impairs both the acquisition of new memories and the consolidation of "
                    "memories formed before the period of sleep loss."
                ),
                "question_groups": [
                    {
                        "order": 1,
                        "question_type": "mcq",
                        "instruction": "Choose the correct letter, A, B, C or D.",
                        "questions": [
                            {
                                "local_order": 1,
                                "stem": "What did the study of patient H.M. primarily help scientists understand?",
                                "options": [
                                    {"key": "A", "text": "The relationship between epilepsy and memory loss"},
                                    {"key": "B", "text": "The distinction between short-term and long-term memory systems"},
                                    {"key": "C", "text": "How brain surgery can improve memory function"},
                                    {"key": "D", "text": "The process by which memories deteriorate with age"},
                                ],
                                "correct_answer": "B",
                            },
                            {
                                "local_order": 2,
                                "stem": "According to the passage, roughly how many items can working memory typically retain at one time?",
                                "options": [
                                    {"key": "A", "text": "Three"},
                                    {"key": "B", "text": "Five"},
                                    {"key": "C", "text": "Seven"},
                                    {"key": "D", "text": "Twelve"},
                                ],
                                "correct_answer": "C",
                            },
                            {
                                "local_order": 3,
                                "stem": "What is described as an example of non-declarative memory?",
                                "options": [
                                    {"key": "A", "text": "Knowing the capital city of a country"},
                                    {"key": "B", "text": "Recalling the details of a specific conversation"},
                                    {"key": "C", "text": "Remembering a list of historical dates"},
                                    {"key": "D", "text": "Riding a bicycle without conscious attention"},
                                ],
                                "correct_answer": "D",
                            },
                            {
                                "local_order": 4,
                                "stem": "What does the process of reconsolidation suggest about the nature of memory?",
                                "options": [
                                    {"key": "A", "text": "Memories become more accurate each time they are recalled"},
                                    {"key": "B", "text": "Memories can be altered when retrieved, incorporating new information"},
                                    {"key": "C", "text": "Only long-term memories undergo reconsolidation"},
                                    {"key": "D", "text": "Memory reconsolidation occurs only during sleep"},
                                ],
                                "correct_answer": "B",
                            },
                            {
                                "local_order": 5,
                                "stem": "What role does the hippocampus play in memory, according to the passage?",
                                "options": [
                                    {"key": "A", "text": "It stores all long-term memories permanently"},
                                    {"key": "B", "text": "It controls the capacity of working memory"},
                                    {"key": "C", "text": "It is particularly associated with forming new declarative memories"},
                                    {"key": "D", "text": "It prevents old memories from being altered by new experiences"},
                                ],
                                "correct_answer": "C",
                            },
                        ],
                    },
                    {
                        "order": 2,
                        "question_type": "sentence_completion",
                        "instruction": "Complete the sentences below. Choose NO MORE THAN TWO WORDS from the passage for each answer.",
                        "word_limit": 2,
                        "questions": [
                            {"local_order": 1, "stem": "The brain region particularly associated with forming new declarative memories is called the _____.", "correct_answer": "hippocampus"},
                            {"local_order": 2, "stem": "The process by which newly acquired information is transferred to long-term memory is known as memory _____.", "correct_answer": "consolidation"},
                            {"local_order": 3, "stem": "Each time a memory is retrieved, it must be re-stored through a process called _____.", "correct_answer": "reconsolidation"},
                            {"local_order": 4, "stem": "H.M. could learn new motor skills despite being unable to remember the _____ sessions.", "correct_answer": "learning"},
                            {"local_order": 5, "stem": "Studies show that sleep _____ severely impairs both the acquisition and consolidation of memories.", "correct_answer": "deprivation"},
                        ],
                    },
                    {
                        "order": 3,
                        "question_type": "short_answer",
                        "instruction": "Answer the questions below. Choose NO MORE THAN THREE WORDS from the passage for each answer.",
                        "word_limit": 3,
                        "questions": [
                            {"local_order": 1, "stem": "What term describes memory for conscious recollection of facts and events?", "correct_answer": "declarative memory"},
                            {"local_order": 2, "stem": "Name one example of non-declarative memory given in the passage.", "correct_answer": "riding a bicycle", "answer_variants": ["driving a familiar route", "motor skills"]},
                            {"local_order": 3, "stem": "Why is eyewitness testimony described as often unreliable, according to the passage?", "correct_answer": "reconsolidation", "answer_variants": ["memories can be altered", "new information"]},
                            {"local_order": 4, "stem": "What kind of sleep is specifically mentioned as playing a role in memory consolidation?", "correct_answer": "slow-wave sleep"},
                        ],
                    },
                ],
            },
        ],
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# WRITING PROMPTS (15 prompts — Task 1 Academic + Task 2 Academic)
# ─────────────────────────────────────────────────────────────────────────────

WRITING_PROMPTS = [
    # ── Task 1 (Academic) — describe a chart, graph, diagram, or process ───
    {
        "task": 1, "test_type": "academic", "topic": "environment", "min_words": 150,
        "prompt_text": (
            "The line graph below shows changes in global average surface temperature "
            "between 1900 and 2020.\n\n"
            "Summarise the information by selecting and reporting the main features, "
            "and make comparisons where relevant.\n\nWrite at least 150 words."
        ),
        "image_description": "Line graph: global average temperature anomaly (°C) vs year, 1900–2020. "
                             "Relatively stable from 1900–1950, gradual rise 1950–1980, sharp upward trend 1980–2020.",
    },
    {
        "task": 1, "test_type": "academic", "topic": "technology", "min_words": 150,
        "prompt_text": (
            "The bar chart below compares the percentage of households with internet "
            "access in five countries in 2010 and 2023.\n\n"
            "Summarise the information by selecting and reporting the main features, "
            "and make comparisons where relevant.\n\nWrite at least 150 words."
        ),
        "image_description": "Grouped bar chart: internet access % for UK, US, Brazil, India, Nigeria in 2010 and 2023.",
    },
    {
        "task": 1, "test_type": "academic", "topic": "education", "min_words": 150,
        "prompt_text": (
            "The pie charts below show the proportion of students enrolled in different "
            "subject areas at universities in two countries in 2022.\n\n"
            "Summarise the information by selecting and reporting the main features, "
            "and make comparisons where relevant.\n\nWrite at least 150 words."
        ),
        "image_description": "Two pie charts: Country A and Country B, subjects: STEM, Humanities, Business, Social Sciences, Arts.",
    },
    {
        "task": 1, "test_type": "academic", "topic": "science", "min_words": 150,
        "prompt_text": (
            "The diagram below illustrates the process of water purification in a "
            "modern urban water treatment plant.\n\n"
            "Summarise the information by selecting and reporting the main features "
            "and stages of the process.\n\nWrite at least 150 words."
        ),
        "image_description": "Flow diagram: river water → screening → sedimentation → filtration → chlorination → pH adjustment → distribution.",
    },
    {
        "task": 1, "test_type": "academic", "topic": "business", "min_words": 150,
        "prompt_text": (
            "The line graph below shows changes in the number of tourists visiting "
            "three countries between 2000 and 2022.\n\n"
            "Summarise the information by selecting and reporting the main features, "
            "and make comparisons where relevant.\n\nWrite at least 150 words."
        ),
        "image_description": "Line graph: annual international tourist arrivals (millions) for France, Japan, and Brazil, 2000–2022.",
    },
    {
        "task": 1, "test_type": "academic", "topic": "health", "min_words": 150,
        "prompt_text": (
            "The table below shows data on average life expectancy, obesity rates, "
            "and healthcare spending per capita for six countries in 2020.\n\n"
            "Summarise the information by selecting and reporting the main features, "
            "and make comparisons where relevant.\n\nWrite at least 150 words."
        ),
        "image_description": "Table: Country, Life Expectancy (years), Obesity Rate (%), Healthcare Spend (USD/capita) for 6 countries.",
    },

    # ── Task 2 (Academic) — discursive essay ───────────────────────────────
    {
        "task": 2, "test_type": "academic", "topic": "technology", "min_words": 250,
        "prompt_text": (
            "Some people believe that technology has made our lives more complicated "
            "rather than simpler.\n\n"
            "To what extent do you agree or disagree?\n\n"
            "Give reasons for your answer and include any relevant examples from your "
            "own knowledge or experience.\n\nWrite at least 250 words."
        ),
        "image_description": None,
    },
    {
        "task": 2, "test_type": "academic", "topic": "environment", "min_words": 250,
        "prompt_text": (
            "In many countries, the number of wild animals and plant species is "
            "declining at an alarming rate.\n\n"
            "What do you think are the main causes of this? What solutions can you suggest?\n\n"
            "Give reasons for your answer and include any relevant examples from your "
            "own knowledge or experience.\n\nWrite at least 250 words."
        ),
        "image_description": None,
    },
    {
        "task": 2, "test_type": "academic", "topic": "education", "min_words": 250,
        "prompt_text": (
            "Some people think that universities should focus primarily on providing "
            "theoretical knowledge, while others believe their main purpose should "
            "be to prepare students for future employment.\n\n"
            "Discuss both these views and give your own opinion.\n\nWrite at least 250 words."
        ),
        "image_description": None,
    },
    {
        "task": 2, "test_type": "academic", "topic": "health", "min_words": 250,
        "prompt_text": (
            "The prevention of health problems and illness is more important than "
            "treatment and medicine.\n\n"
            "To what extent do you agree or disagree with this statement?\n\n"
            "Give reasons for your answer and include any relevant examples from your "
            "own knowledge or experience.\n\nWrite at least 250 words."
        ),
        "image_description": None,
    },
    {
        "task": 2, "test_type": "academic", "topic": "society", "min_words": 250,
        "prompt_text": (
            "Many people today spend more time on social media platforms than on direct "
            "social interaction with friends and family.\n\n"
            "What are the advantages and disadvantages of this development?\n\n"
            "Give reasons for your answer and include any relevant examples from your "
            "own knowledge or experience.\n\nWrite at least 250 words."
        ),
        "image_description": None,
    },
    {
        "task": 2, "test_type": "academic", "topic": "education", "min_words": 250,
        "prompt_text": (
            "Some people believe that children should begin learning a foreign language "
            "as soon as they start school. Others think this should be delayed until "
            "secondary school.\n\n"
            "Discuss both views and give your own opinion.\n\nWrite at least 250 words."
        ),
        "image_description": None,
    },
    {
        "task": 2, "test_type": "academic", "topic": "science", "min_words": 250,
        "prompt_text": (
            "Scientific research should be carried out and funded by governments "
            "rather than private companies.\n\n"
            "To what extent do you agree or disagree?\n\n"
            "Give reasons for your answer and include any relevant examples from your "
            "own knowledge or experience.\n\nWrite at least 250 words."
        ),
        "image_description": None,
    },
    {
        "task": 2, "test_type": "academic", "topic": "environment", "min_words": 250,
        "prompt_text": (
            "Some people think the best way to reduce global carbon emissions is to "
            "tax companies and individuals who pollute the environment. Others believe "
            "that alternative measures are more effective.\n\n"
            "Discuss both views and give your own opinion.\n\nWrite at least 250 words."
        ),
        "image_description": None,
    },
    {
        "task": 2, "test_type": "academic", "topic": "society", "min_words": 250,
        "prompt_text": (
            "Some people argue that unpaid community service should be a compulsory "
            "part of school programmes for teenagers.\n\n"
            "To what extent do you agree or disagree?\n\n"
            "Give reasons for your answer and include any relevant examples from your "
            "own knowledge or experience.\n\nWrite at least 250 words."
        ),
        "image_description": None,
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# SEEDER — called from main.py startup
# ─────────────────────────────────────────────────────────────────────────────

def seed(db) -> dict:
    """
    Seeds IELTS reading tests and writing prompts into the database.
    Safe to call repeatedly: skips if content already exists.
    Returns a summary dict for logging.
    """
    result = {"reading_tests_added": 0, "writing_prompts_added": 0}

    # ── Reading tests ──────────────────────────────────────────────────────
    if db.query(models.IELTSTest).count() == 0:
        for test_data in READING_TESTS:
            _create_test(test_data, db)
        result["reading_tests_added"] = len(READING_TESTS)

    # ── Writing prompts ────────────────────────────────────────────────────
    if db.query(models.WritingPrompt).count() == 0:
        for p in WRITING_PROMPTS:
            db.add(models.WritingPrompt(**p))
        db.commit()
        result["writing_prompts_added"] = len(WRITING_PROMPTS)

    return result


def _create_test(data: dict, db) -> None:
    """Creates one complete IELTSTest with all nested passages, groups, and questions."""
    test = models.IELTSTest(
        title=data["title"],
        test_type=data["test_type"],
        component=data["component"],
        time_limit=data["time_limit"],
        created_by=None,
    )
    db.add(test)
    db.flush()

    global_num = 1
    for p_data in data["passages"]:
        passage = models.IELTSPassage(
            test_id=test.id,
            order=p_data["order"],
            title=p_data["title"],
            body_text=p_data["body_text"],
            image_url=p_data.get("image_url"),
        )
        db.add(passage)
        db.flush()

        for g_data in p_data["question_groups"]:
            group = models.IELTSQuestionGroup(
                passage_id=passage.id,
                order=g_data["order"],
                question_type=g_data["question_type"],
                instruction=g_data["instruction"],
                word_limit=g_data.get("word_limit"),
                options_pool=g_data.get("options_pool"),
            )
            db.add(group)
            db.flush()

            for q_data in g_data["questions"]:
                db.add(models.IELTSQuestion(
                    group_id=group.id,
                    global_number=global_num,
                    local_order=q_data["local_order"],
                    stem=q_data["stem"],
                    options=q_data.get("options"),
                    correct_answer=q_data["correct_answer"],
                    answer_variants=q_data.get("answer_variants"),
                ))
                global_num += 1

    db.commit()
