"""
Extra seed data — 4 additional IELTS Academic Reading tests + 5 Writing prompts.
Called from startup after seed_ielts (which seeds tests 1-3).
"""
from sqlalchemy.orm import Session
from . import models


# ─────────────────────────────────────────────────────────────────────────────
# EXTRA READING TESTS  (Tests 4-7)
# ─────────────────────────────────────────────────────────────────────────────

EXTRA_READING_TESTS = [

    # ═════════════════════════════════════════════════════════════════════════
    # TEST 4 — Genetics · Urban Heat Islands · Ancient Trade Routes
    # ═════════════════════════════════════════════════════════════════════════
    {
        "title": "IELTS Academic Reading — Set 4",
        "test_type": "academic", "component": "reading", "time_limit": 60,
        "passages": [
            {
                "order": 1,
                "title": "CRISPR and the Gene-Editing Revolution",
                "body_text": (
                    "In 2012, biochemists Jennifer Doudna and Emmanuelle Charpentier published a landmark paper "
                    "describing how a bacterial immune mechanism could be repurposed as a precise molecular tool "
                    "for editing DNA. The system, known as CRISPR-Cas9, allows scientists to cut the genome at "
                    "virtually any location and either disable a gene or insert new genetic material. The discovery "
                    "earned the two researchers the 2020 Nobel Prize in Chemistry.\n\n"
                    "CRISPR works by exploiting a natural defence system found in bacteria. When a bacterium "
                    "survives a viral attack, it stores fragments of the virus's genetic material in its own "
                    "genome. If the same virus attacks again, the bacterium produces RNA molecules that match "
                    "those stored fragments. The RNA guides a protein called Cas9 to the matching sequence in "
                    "the invading virus, where Cas9 cuts the DNA strand, disabling the virus. Scientists "
                    "realised they could synthesise custom guide RNAs to direct Cas9 to any gene sequence "
                    "they chose.\n\n"
                    "The therapeutic applications are transformative. Clinical trials are already underway "
                    "for sickle cell disease, a painful inherited condition caused by a single mutation in "
                    "the haemoglobin gene. Early results show that CRISPR editing of patients' own stem cells "
                    "can produce functional haemoglobin, eliminating the need for blood transfusions. "
                    "Researchers are also investigating treatments for certain cancers, HIV, and various "
                    "forms of blindness.\n\n"
                    "However, the technology raises profound ethical questions. In 2018, Chinese scientist "
                    "He Jiankui announced that he had used CRISPR to edit the genomes of human embryos "
                    "that were subsequently implanted and born. The claim triggered international outrage; "
                    "He was later sentenced to prison, and the scientific community called for a global "
                    "moratorium on heritable human genome editing. Critics argue that germline editing — "
                    "changes that can be passed to future generations — crosses a line that should not "
                    "be crossed without far wider societal deliberation.\n\n"
                    "Off-target effects remain a technical concern. Cas9 occasionally cuts at sites other "
                    "than the intended target, potentially disrupting other genes. Newer variants of the "
                    "technology, such as base editing and prime editing, aim to make corrections without "
                    "cutting both DNA strands, reducing off-target damage. Despite its enormous promise, "
                    "researchers caution that the full consequences of widespread genome editing — in "
                    "humans, crops, or wild populations — remain incompletely understood."
                ),
                "question_groups": [
                    {
                        "order": 1,
                        "question_type": "tfng",
                        "instruction": "Do the following statements agree with the information in the passage?\nWrite TRUE, FALSE or NOT GIVEN.",
                        "questions": [
                            {"local_order": 1, "stem": "Doudna and Charpentier won the Nobel Prize for Chemistry in 2020.", "correct_answer": "TRUE"},
                            {"local_order": 2, "stem": "CRISPR-Cas9 was developed specifically as a human medical treatment.", "correct_answer": "FALSE"},
                            {"local_order": 3, "stem": "Sickle cell disease affects more people in Africa than on any other continent.", "correct_answer": "NOT GIVEN"},
                            {"local_order": 4, "stem": "He Jiankui was imprisoned following his germline editing experiments.", "correct_answer": "TRUE"},
                            {"local_order": 5, "stem": "Prime editing eliminates the need to cut both strands of DNA.", "correct_answer": "TRUE"},
                        ],
                    },
                    {
                        "order": 2,
                        "question_type": "mcq",
                        "instruction": "Choose the correct letter, A, B, C or D.",
                        "questions": [
                            {
                                "local_order": 1,
                                "stem": "What enables scientists to target a specific gene using CRISPR-Cas9?",
                                "options": [{"key": "A", "text": "A naturally occurring bacterium"},
                                            {"key": "B", "text": "A synthetic guide RNA"},
                                            {"key": "C", "text": "A protein called haemoglobin"},
                                            {"key": "D", "text": "A viral DNA fragment"}],
                                "correct_answer": "B",
                            },
                            {
                                "local_order": 2,
                                "stem": "Which of the following best describes the main concern about off-target effects?",
                                "options": [{"key": "A", "text": "They cause the patient's immune system to reject treatment"},
                                            {"key": "B", "text": "They result in cuts at unintended locations in the genome"},
                                            {"key": "C", "text": "They make CRISPR too expensive for clinical use"},
                                            {"key": "D", "text": "They prevent guide RNA from locating the target gene"}],
                                "correct_answer": "B",
                            },
                        ],
                    },
                    {
                        "order": 3,
                        "question_type": "sentence_completion",
                        "instruction": "Complete the sentences. Write NO MORE THAN TWO WORDS from the passage.",
                        "word_limit": 2,
                        "questions": [
                            {"local_order": 1, "stem": "Bacteria store fragments of viral DNA in their own genome to mount a defence, a process exploited by the _____ system.", "correct_answer": "CRISPR", "answer_variants": ["crispr"]},
                            {"local_order": 2, "stem": "A global _____ on heritable human genome editing was called for by the scientific community.", "correct_answer": "moratorium", "answer_variants": ["moratorium on"]},
                            {"local_order": 3, "stem": "_____ editing corrects DNA without cutting both strands, reducing off-target damage.", "correct_answer": "Prime", "answer_variants": ["prime", "Base", "base"]},
                        ],
                    },
                ],
            },
            {
                "order": 2,
                "title": "The Urban Heat Island Effect",
                "body_text": (
                    "City dwellers have long noticed that urban areas feel noticeably warmer than the surrounding "
                    "countryside, particularly at night. This phenomenon, first documented systematically by "
                    "meteorologist Luke Howard in early nineteenth-century London, is now known as the urban "
                    "heat island (UHI) effect. In major metropolitan areas, the temperature difference between "
                    "city centre and surrounding rural land can exceed 10 degrees Celsius on calm, clear nights.\n\n"
                    "The primary driver is the replacement of natural surfaces — soil, grass, trees — with "
                    "impervious materials such as asphalt, concrete, and brick. Natural surfaces absorb solar "
                    "radiation during the day and release it through evaporation, a process that consumes "
                    "energy and cools the environment. Urban materials, by contrast, store heat during daylight "
                    "hours and radiate it slowly overnight, preventing the nocturnal cooling that occurs in "
                    "rural areas. Dark road surfaces, which absorb up to 95 per cent of incident solar "
                    "radiation, are especially significant contributors.\n\n"
                    "Additional heat is generated directly by human activity — vehicle engines, air-conditioning "
                    "units, industrial processes, and cooking. Known as anthropogenic heat flux, this source "
                    "can contribute several watts per square metre to city temperatures, a figure that rises "
                    "substantially in dense commercial or industrial districts.\n\n"
                    "The health consequences are serious. During the 2003 European heatwave, excess mortality "
                    "in cities was far higher than in rural areas. Elderly people and those without air "
                    "conditioning face particular risk. Urban heat also degrades air quality, as higher "
                    "temperatures accelerate the formation of ground-level ozone, a respiratory irritant.\n\n"
                    "City planners are deploying several strategies to mitigate UHI. Green roofs — which "
                    "support vegetation on building rooftops — reduce heat absorption and provide "
                    "evaporative cooling. Cool pavements and roofs, coated with highly reflective materials, "
                    "can lower surface temperatures by up to 20°C. Urban forests and parks provide shade "
                    "and enhance evapotranspiration. In Singapore, mandatory green space requirements for "
                    "new developments have successfully moderated urban temperatures. However, researchers "
                    "note that as global temperatures rise, these measures may need to be dramatically "
                    "scaled up to remain effective."
                ),
                "question_groups": [
                    {
                        "order": 1,
                        "question_type": "tfng",
                        "instruction": "Do the following statements agree with the information in the passage?\nWrite TRUE, FALSE or NOT GIVEN.",
                        "questions": [
                            {"local_order": 1, "stem": "Luke Howard was the first person to study urban heat islands in London.", "correct_answer": "TRUE"},
                            {"local_order": 2, "stem": "The UHI temperature difference between cities and countryside is always exactly 10°C.", "correct_answer": "FALSE"},
                            {"local_order": 3, "stem": "Dark road surfaces absorb up to 95 per cent of solar radiation.", "correct_answer": "TRUE"},
                            {"local_order": 4, "stem": "Air-conditioning units are the biggest single source of anthropogenic heat in cities.", "correct_answer": "NOT GIVEN"},
                            {"local_order": 5, "stem": "Singapore has regulations requiring green space in new developments.", "correct_answer": "TRUE"},
                        ],
                    },
                    {
                        "order": 2,
                        "question_type": "mcq",
                        "instruction": "Choose the correct letter, A, B, C or D.",
                        "questions": [
                            {
                                "local_order": 1,
                                "stem": "Why do natural surfaces cool the environment more effectively than urban surfaces?",
                                "options": [{"key": "A", "text": "They absorb less solar radiation during daylight hours"},
                                            {"key": "B", "text": "They release stored heat more quickly after sunset"},
                                            {"key": "C", "text": "They cool through evaporation, which consumes energy"},
                                            {"key": "D", "text": "They reflect more heat back into the atmosphere"}],
                                "correct_answer": "C",
                            },
                            {
                                "local_order": 2,
                                "stem": "What air quality problem is worsened by elevated urban temperatures?",
                                "options": [{"key": "A", "text": "Carbon dioxide accumulation"},
                                            {"key": "B", "text": "Ground-level ozone formation"},
                                            {"key": "C", "text": "Particulate matter from vehicle exhausts"},
                                            {"key": "D", "text": "Acid rain from industrial emissions"}],
                                "correct_answer": "B",
                            },
                            {
                                "local_order": 3,
                                "stem": "What effect can cool pavements and roofs have on surface temperature?",
                                "options": [{"key": "A", "text": "A reduction of up to 10°C"},
                                            {"key": "B", "text": "A reduction of up to 15°C"},
                                            {"key": "C", "text": "A reduction of up to 20°C"},
                                            {"key": "D", "text": "A reduction of up to 25°C"}],
                                "correct_answer": "C",
                            },
                        ],
                    },
                    {
                        "order": 3,
                        "question_type": "sentence_completion",
                        "instruction": "Complete the sentences using NO MORE THAN TWO WORDS from the passage.",
                        "word_limit": 2,
                        "questions": [
                            {"local_order": 1, "stem": "The heat produced by vehicles, factories, and other human sources is called _____ heat flux.", "correct_answer": "anthropogenic", "answer_variants": ["anthropogenic heat"]},
                            {"local_order": 2, "stem": "Rooftop gardens that support plants are known as _____ roofs.", "correct_answer": "green", "answer_variants": ["green roofs"]},
                            {"local_order": 3, "stem": "In cities, higher temperatures speed up the production of ground-level _____, which irritates the respiratory system.", "correct_answer": "ozone", "answer_variants": ["ozone formation"]},
                        ],
                    },
                ],
            },
            {
                "order": 3,
                "title": "The Silk Road: Connecting Ancient Worlds",
                "body_text": (
                    "The term 'Silk Road' was coined by German geographer Ferdinand von Richthofen in 1877 to "
                    "describe the ancient network of trade routes linking China with Central Asia, the Middle "
                    "East, and eventually the Mediterranean world. Despite the name, silk was just one of many "
                    "commodities that moved along these routes; spices, glass, metals, paper, and ideas "
                    "travelled in both directions across thousands of kilometres of desert, mountain, and steppe.\n\n"
                    "The routes did not form a single highway but rather a shifting web of paths that changed "
                    "with political circumstances, seasonal conditions, and the preferences of individual "
                    "merchants. At its height, between roughly the second century BCE and the fifteenth "
                    "century CE, the Silk Road connected the Han and Tang dynasties of China with the "
                    "Parthian and Sassanid empires of Persia, the Kushan Empire of Central Asia, and "
                    "ultimately the Roman Empire.\n\n"
                    "The movement of goods was largely carried out by relay, with merchants rarely "
                    "travelling the entire route themselves. Products changed hands multiple times, passing "
                    "through oasis cities such as Samarkand, Dunhuang, and Merv. These cities grew wealthy "
                    "as commercial and cultural hubs, and their architecture, art, and literature reflected "
                    "the extraordinary diversity of peoples who passed through them.\n\n"
                    "Perhaps the most significant cargo on the Silk Road was not physical goods but "
                    "intangible ones: religions, technologies, and diseases. Buddhism spread from India "
                    "through Central Asia to China along these routes. The technique of paper-making, "
                    "invented in China, reached the Islamic world by the eighth century and Europe by "
                    "the twelfth. Tragically, the bubonic plague that devastated fourteenth-century "
                    "Europe also appears to have travelled westward along the trade networks, carried "
                    "by rodents and fleas on merchant caravans.\n\n"
                    "The discovery of sea routes to Asia in the late fifteenth and early sixteenth "
                    "centuries gradually eclipsed the overland Silk Road. European maritime powers "
                    "found ocean travel faster, cheaper, and capable of carrying larger volumes of "
                    "cargo. The great oasis cities declined, and the routes fell into relative "
                    "disuse, though they were never entirely abandoned. In recent decades, China's "
                    "Belt and Road Initiative has invoked the Silk Road's legacy to describe a vast "
                    "programme of infrastructure investment linking Asia, Africa, and Europe."
                ),
                "question_groups": [
                    {
                        "order": 1,
                        "question_type": "tfng",
                        "instruction": "Do the following statements agree with the information?\nWrite TRUE, FALSE or NOT GIVEN.",
                        "questions": [
                            {"local_order": 1, "stem": "Ferdinand von Richthofen invented the Silk Road in 1877.", "correct_answer": "FALSE"},
                            {"local_order": 2, "stem": "The Silk Road was a single, fixed highway between China and Rome.", "correct_answer": "FALSE"},
                            {"local_order": 3, "stem": "Individual merchants commonly travelled the entire Silk Road from start to finish.", "correct_answer": "FALSE"},
                            {"local_order": 4, "stem": "Paper-making technology reached Europe before the Islamic world.", "correct_answer": "FALSE"},
                            {"local_order": 5, "stem": "The Belt and Road Initiative involves infrastructure investment across multiple continents.", "correct_answer": "TRUE"},
                        ],
                    },
                    {
                        "order": 2,
                        "question_type": "mcq",
                        "instruction": "Choose the correct letter, A, B, C or D.",
                        "questions": [
                            {
                                "local_order": 1,
                                "stem": "What does the passage say about goods transported on the Silk Road?",
                                "options": [{"key": "A", "text": "Silk was by far the most valuable commodity carried"},
                                            {"key": "B", "text": "Only luxury goods such as spices and jewels were traded"},
                                            {"key": "C", "text": "Many different types of goods and ideas travelled the routes"},
                                            {"key": "D", "text": "Most trade was conducted by a small number of powerful merchants"}],
                                "correct_answer": "C",
                            },
                            {
                                "local_order": 2,
                                "stem": "What was the main reason sea routes replaced the overland Silk Road?",
                                "options": [{"key": "A", "text": "Sea routes were safer from bandits and hostile armies"},
                                            {"key": "B", "text": "Ocean travel was faster, cheaper and had greater carrying capacity"},
                                            {"key": "C", "text": "The oasis cities were destroyed by the bubonic plague"},
                                            {"key": "D", "text": "China banned overland trade in the fifteenth century"}],
                                "correct_answer": "B",
                            },
                        ],
                    },
                    {
                        "order": 3,
                        "question_type": "sentence_completion",
                        "instruction": "Complete the sentences using NO MORE THAN TWO WORDS from the passage.",
                        "word_limit": 2,
                        "questions": [
                            {"local_order": 1, "stem": "Cities like Samarkand and Merv thrived as commercial and _____ hubs along the Silk Road.", "correct_answer": "cultural", "answer_variants": ["cultural hubs"]},
                            {"local_order": 2, "stem": "The religion of _____ spread from India through Central Asia to China along the Silk Road.", "correct_answer": "Buddhism", "answer_variants": ["buddhism"]},
                            {"local_order": 3, "stem": "The fourteenth-century bubonic plague is believed to have spread westward via merchant _____.", "correct_answer": "caravans", "answer_variants": ["merchant caravans"]},
                        ],
                    },
                ],
            },
        ],
    },

    # ═════════════════════════════════════════════════════════════════════════
    # TEST 5 — Robotics · Microplastics · Language Extinction
    # ═════════════════════════════════════════════════════════════════════════
    {
        "title": "IELTS Academic Reading — Set 5",
        "test_type": "academic", "component": "reading", "time_limit": 60,
        "passages": [
            {
                "order": 1,
                "title": "The Rise of Collaborative Robots",
                "body_text": (
                    "For most of industrial history, robots and humans worked in strict separation. "
                    "Automated machines were confined to caged areas on factory floors, surrounded "
                    "by physical barriers that kept workers safe from their powerful, unpredictable "
                    "movements. This arrangement was both expensive and inflexible. A new generation "
                    "of machines, known as collaborative robots or 'cobots', is fundamentally "
                    "changing that relationship.\n\n"
                    "Cobots are designed from the outset to operate safely alongside people without "
                    "caging or barriers. They achieve this through a combination of force-sensing "
                    "technology, speed limitations, and sophisticated software that can detect the "
                    "presence of a human and halt operations immediately. Leading manufacturers such "
                    "as Universal Robots, FANUC, and ABB now offer cobot models capable of "
                    "handling components ranging from a few hundred grams to over a kilogram.\n\n"
                    "The applications are diverse. In automotive assembly, cobots assist workers "
                    "by handling heavy components such as engines or door panels, reducing "
                    "ergonomic injuries. In electronics manufacturing, their precision exceeds "
                    "human capability for soldering or placing components on circuit boards. In "
                    "healthcare settings, robotic arms assist surgeons with minimally invasive "
                    "procedures, allowing greater precision than the human hand alone.\n\n"
                    "Small and medium-sized enterprises (SMEs) have been among the greatest "
                    "beneficiaries of the cobot revolution. Traditional industrial robots required "
                    "substantial capital investment, specialised programmers, and significant "
                    "installation space. Cobots, by contrast, can often be programmed by operators "
                    "with no robotics expertise, simply by moving the robot's arm through the "
                    "desired sequence of movements — a technique called lead-through programming. "
                    "Prices have fallen dramatically, with some basic cobot arms now available "
                    "for less than $20,000.\n\n"
                    "Despite widespread concerns about automation displacing workers, research "
                    "suggests a more nuanced picture. Studies from the International Federation "
                    "of Robotics consistently find that the countries with the highest robot "
                    "density — Germany, Japan, and South Korea — also have low unemployment rates. "
                    "Cobots, in particular, tend to complement rather than replace human workers, "
                    "handling repetitive or dangerous tasks while freeing people for those requiring "
                    "creativity, judgement, and interpersonal skills. Nevertheless, the distributional "
                    "effects of automation are uneven, with lower-skilled workers in routine-task "
                    "occupations facing greater displacement risk than those with higher education."
                ),
                "question_groups": [
                    {
                        "order": 1,
                        "question_type": "tfng",
                        "instruction": "Write TRUE, FALSE or NOT GIVEN.",
                        "questions": [
                            {"local_order": 1, "stem": "Traditional industrial robots required physical barriers to separate them from human workers.", "correct_answer": "TRUE"},
                            {"local_order": 2, "stem": "Cobots use only speed limitations to ensure safety around humans.", "correct_answer": "FALSE"},
                            {"local_order": 3, "stem": "Universal Robots is the world's most profitable cobot manufacturer.", "correct_answer": "NOT GIVEN"},
                            {"local_order": 4, "stem": "Lead-through programming allows operators with no robotics expertise to program cobots.", "correct_answer": "TRUE"},
                            {"local_order": 5, "stem": "Germany, Japan, and South Korea have high robot density and low unemployment.", "correct_answer": "TRUE"},
                        ],
                    },
                    {
                        "order": 2,
                        "question_type": "mcq",
                        "instruction": "Choose the correct letter, A, B, C or D.",
                        "questions": [
                            {
                                "local_order": 1,
                                "stem": "Which group has particularly benefited from the lower cost of cobots?",
                                "options": [{"key": "A", "text": "Large multinational corporations"},
                                            {"key": "B", "text": "Government research laboratories"},
                                            {"key": "C", "text": "Small and medium-sized enterprises"},
                                            {"key": "D", "text": "University engineering departments"}],
                                "correct_answer": "C",
                            },
                            {
                                "local_order": 2,
                                "stem": "What does the passage say about cobots and employment?",
                                "options": [{"key": "A", "text": "Cobots are causing unemployment in all sectors equally"},
                                            {"key": "B", "text": "Cobots typically supplement human work rather than replace it entirely"},
                                            {"key": "C", "text": "Higher-skilled workers face greater job displacement than lower-skilled ones"},
                                            {"key": "D", "text": "Automation has no measurable effect on overall employment"}],
                                "correct_answer": "B",
                            },
                        ],
                    },
                    {
                        "order": 3,
                        "question_type": "sentence_completion",
                        "instruction": "Complete the sentences using NO MORE THAN TWO WORDS from the passage.",
                        "word_limit": 2,
                        "questions": [
                            {"local_order": 1, "stem": "Programming a cobot by physically guiding its arm through a task is called _____ programming.", "correct_answer": "lead-through", "answer_variants": ["lead through"]},
                            {"local_order": 2, "stem": "In automotive factories, cobots reduce _____ injuries by lifting heavy components.", "correct_answer": "ergonomic", "answer_variants": ["ergonomic injuries"]},
                            {"local_order": 3, "stem": "In surgery, robotic arms allow greater _____ than the human hand can achieve.", "correct_answer": "precision", "answer_variants": ["greater precision"]},
                        ],
                    },
                ],
            },
            {
                "order": 2,
                "title": "Microplastics: An Invisible Contamination Crisis",
                "body_text": (
                    "Plastic pollution visible to the naked eye — bottles, bags, packaging — represents "
                    "only the most conspicuous fraction of a far larger problem. Scientists have identified "
                    "a class of particles smaller than five millimetres, collectively termed microplastics, "
                    "that have infiltrated virtually every ecosystem on Earth. They have been detected in "
                    "Arctic sea ice, deep ocean sediments, mountain snowfields, and most recently in human "
                    "blood and lung tissue.\n\n"
                    "Microplastics originate from two sources. Primary microplastics are manufactured at "
                    "small sizes deliberately: the microbeads in some cosmetics and exfoliating products, "
                    "and the synthetic fibres shed from polyester and nylon clothing during washing. "
                    "Secondary microplastics form when larger plastic items break down under ultraviolet "
                    "radiation, wave action, and temperature fluctuations. Plastic never truly biodegrades; "
                    "it simply fragments into progressively smaller pieces.\n\n"
                    "Marine ecosystems are particularly affected. Plankton — the microscopic organisms "
                    "at the base of the ocean food web — mistake microplastic particles for food, "
                    "ingesting them and reducing their energy intake. These particles then accumulate "
                    "up the food chain through a process called bioaccumulation, reaching higher "
                    "concentrations in predators at the top of the chain, including tuna, dolphins, "
                    "and humans who consume seafood. Additionally, microplastics act as vectors "
                    "for persistent organic pollutants, concentrating toxic compounds and transporting "
                    "them into organisms.\n\n"
                    "Regulatory responses have been uneven. Several countries, including the United "
                    "States, the United Kingdom, and members of the European Union, have banned "
                    "microbeads in rinse-off cosmetic products. However, synthetic textile fibres "
                    "remain largely unregulated, despite constituting a major share of marine "
                    "microplastic pollution. Washing machine filters capable of capturing fibres "
                    "have been developed but are not yet mandatory in most countries.\n\n"
                    "The long-term health effects of microplastic ingestion in humans are an area "
                    "of active research. Animal studies have demonstrated inflammatory responses, "
                    "disruption to reproductive hormones, and cellular damage at high exposure "
                    "levels. Whether the concentrations currently found in the human body are "
                    "sufficient to cause harm remains debated, but many scientists argue that "
                    "applying the precautionary principle is warranted given the ubiquity of "
                    "exposure and the difficulty of reversing contamination once established."
                ),
                "question_groups": [
                    {
                        "order": 1,
                        "question_type": "tfng",
                        "instruction": "Write TRUE, FALSE or NOT GIVEN.",
                        "questions": [
                            {"local_order": 1, "stem": "Microplastics have been found in human blood and lung tissue.", "correct_answer": "TRUE"},
                            {"local_order": 2, "stem": "Primary microplastics are always formed from the breakdown of larger plastic items.", "correct_answer": "FALSE"},
                            {"local_order": 3, "stem": "Plastic fully biodegrades within 50 years under natural conditions.", "correct_answer": "FALSE"},
                            {"local_order": 4, "stem": "The European Union, the USA and the UK have all banned microbeads in cosmetics.", "correct_answer": "TRUE"},
                            {"local_order": 5, "stem": "Washing machine filters are now compulsory in EU member states.", "correct_answer": "FALSE"},
                        ],
                    },
                    {
                        "order": 2,
                        "question_type": "mcq",
                        "instruction": "Choose the correct letter, A, B, C or D.",
                        "questions": [
                            {
                                "local_order": 1,
                                "stem": "What is bioaccumulation as described in the passage?",
                                "options": [{"key": "A", "text": "The process by which plastic breaks into smaller fragments"},
                                            {"key": "B", "text": "The increasing concentration of pollutants in higher-level predators"},
                                            {"key": "C", "text": "The ability of microplastics to absorb ultraviolet radiation"},
                                            {"key": "D", "text": "The digestion of microplastics by plankton in ocean water"}],
                                "correct_answer": "B",
                            },
                            {
                                "local_order": 2,
                                "stem": "What additional hazard do microplastics create beyond their physical presence?",
                                "options": [{"key": "A", "text": "They block sunlight from reaching deep ocean organisms"},
                                            {"key": "B", "text": "They raise the temperature of surrounding seawater"},
                                            {"key": "C", "text": "They concentrate and transport toxic pollutants into organisms"},
                                            {"key": "D", "text": "They permanently alter the salinity of ocean water"}],
                                "correct_answer": "C",
                            },
                        ],
                    },
                    {
                        "order": 3,
                        "question_type": "sentence_completion",
                        "instruction": "Complete the sentences using NO MORE THAN TWO WORDS from the passage.",
                        "word_limit": 2,
                        "questions": [
                            {"local_order": 1, "stem": "Synthetic fibres released from clothes during washing are a type of _____ microplastic.", "correct_answer": "primary", "answer_variants": ["primary microplastic"]},
                            {"local_order": 2, "stem": "Plankton consume microplastics by mistaking them for _____, reducing their nutritional intake.", "correct_answer": "food", "answer_variants": ["their food"]},
                            {"local_order": 3, "stem": "Many scientists favour the _____ principle, arguing for caution given widespread human exposure.", "correct_answer": "precautionary", "answer_variants": ["precautionary principle"]},
                        ],
                    },
                ],
            },
            {
                "order": 3,
                "title": "Language Extinction and the Race to Document Dying Tongues",
                "body_text": (
                    "Of the approximately 7,000 languages spoken in the world today, linguists estimate "
                    "that between 50 and 90 per cent will have disappeared by the end of the twenty-first "
                    "century. Many languages have already entered a terminal phase: they are spoken by "
                    "a handful of elderly individuals with no younger speakers to inherit them. When the "
                    "last fluent speaker of a language dies, an irreplaceable window onto human cognition, "
                    "culture, and history closes forever.\n\n"
                    "Language loss is not a new phenomenon, but its current pace is unprecedented. The "
                    "forces driving it are largely economic and political. Minority language speakers often "
                    "shift to dominant languages — Mandarin, Spanish, English, Arabic — because doing so "
                    "provides access to education, employment, and social mobility. Government policies "
                    "have historically reinforced this process: many nations ran residential school "
                    "systems in the nineteenth and twentieth centuries that explicitly forbade indigenous "
                    "children from speaking their mother tongues.\n\n"
                    "The consequences of language extinction are profound. Each language encodes unique "
                    "ways of understanding time, space, colour, and kinship. The Aboriginal Australian "
                    "language Guugu Yimithirr uses cardinal directions (north, south, east, west) rather "
                    "than egocentric terms (left, right, in front) to describe spatial relationships, "
                    "giving speakers a dramatically different orientation to the world. Ethnobotanists "
                    "have documented cases where a plant species is known to possess medicinal properties "
                    "only within a specific indigenous language community, knowledge that is lost when "
                    "the language disappears.\n\n"
                    "Linguists have responded with intensive documentation efforts. The Endangered Language "
                    "Fund and the Hans Rausing Endangered Languages Project are among the organisations "
                    "funding fieldwork to record vocabularies, grammars, and oral traditions before "
                    "speakers die. Digital technologies have proven invaluable: inexpensive recording "
                    "equipment and online archives allow materials to be stored and shared globally.\n\n"
                    "Revitalisation — bringing a language back into daily use — is far harder than "
                    "documentation. The most celebrated success is Hebrew, which was revived from a "
                    "primarily liturgical language to a mother tongue spoken by millions. Welsh has "
                    "also achieved considerable success through bilingual education and legal recognition. "
                    "However, these cases are exceptional. Most endangered languages lack the combination "
                    "of community commitment, institutional support, and political will that makes "
                    "revitalisation possible."
                ),
                "question_groups": [
                    {
                        "order": 1,
                        "question_type": "tfng",
                        "instruction": "Write TRUE, FALSE or NOT GIVEN.",
                        "questions": [
                            {"local_order": 1, "stem": "Linguists predict that more than half of today's languages may disappear by 2100.", "correct_answer": "TRUE"},
                            {"local_order": 2, "stem": "Language loss is occurring faster today than at any previous point in history.", "correct_answer": "TRUE"},
                            {"local_order": 3, "stem": "Guugu Yimithirr uses directions like 'left' and 'right' to describe spatial relationships.", "correct_answer": "FALSE"},
                            {"local_order": 4, "stem": "Hebrew is the only language ever to have been successfully revived.", "correct_answer": "NOT GIVEN"},
                            {"local_order": 5, "stem": "Welsh has benefited from bilingual education and legal recognition.", "correct_answer": "TRUE"},
                        ],
                    },
                    {
                        "order": 2,
                        "question_type": "mcq",
                        "instruction": "Choose the correct letter, A, B, C or D.",
                        "questions": [
                            {
                                "local_order": 1,
                                "stem": "Why do minority language speakers often shift to dominant languages?",
                                "options": [{"key": "A", "text": "Because their own languages are difficult to learn"},
                                            {"key": "B", "text": "Because government laws require it in most countries"},
                                            {"key": "C", "text": "Because dominant languages offer better opportunities"},
                                            {"key": "D", "text": "Because their children refuse to learn the minority language"}],
                                "correct_answer": "C",
                            },
                            {
                                "local_order": 2,
                                "stem": "What does the passage say about language revitalisation?",
                                "options": [{"key": "A", "text": "It is straightforward given modern digital technology"},
                                            {"key": "B", "text": "It has been successfully achieved for most endangered languages"},
                                            {"key": "C", "text": "It requires community commitment, institutional support and political will"},
                                            {"key": "D", "text": "It is impossible without a large number of existing speakers"}],
                                "correct_answer": "C",
                            },
                        ],
                    },
                    {
                        "order": 3,
                        "question_type": "sentence_completion",
                        "instruction": "Complete the sentences using NO MORE THAN TWO WORDS from the passage.",
                        "word_limit": 2,
                        "questions": [
                            {"local_order": 1, "stem": "Organisations such as the Endangered Language Fund fund _____ to record languages before speakers die.", "correct_answer": "fieldwork", "answer_variants": ["linguistic fieldwork"]},
                            {"local_order": 2, "stem": "Hebrew is celebrated as the most successful case of language _____, having moved from liturgical use to daily speech.", "correct_answer": "revitalisation", "answer_variants": ["revitalization", "language revitalisation"]},
                            {"local_order": 3, "stem": "Indigenous knowledge of _____ properties of plants can be lost permanently when a language disappears.", "correct_answer": "medicinal", "answer_variants": ["medicinal properties"]},
                        ],
                    },
                ],
            },
        ],
    },

    # ═════════════════════════════════════════════════════════════════════════
    # TEST 6 — Renewable Energy · Sleep Science · Archaeological Dating
    # ═════════════════════════════════════════════════════════════════════════
    {
        "title": "IELTS Academic Reading — Set 6",
        "test_type": "academic", "component": "reading", "time_limit": 60,
        "passages": [
            {
                "order": 1,
                "title": "The Storage Challenge in Renewable Energy",
                "body_text": (
                    "Solar panels and wind turbines have achieved dramatic cost reductions over the past "
                    "decade, making renewable electricity cheaper than coal in most markets. However, "
                    "both technologies share a fundamental limitation: they generate power only when "
                    "the sun shines or the wind blows. Matching this intermittent supply with the "
                    "continuous, variable demand of modern economies is the central challenge facing "
                    "the global energy transition.\n\n"
                    "Lithium-ion batteries, familiar from consumer electronics and electric vehicles, "
                    "are the dominant grid-scale storage technology today. They can charge rapidly, "
                    "discharge efficiently, and respond within milliseconds to grid fluctuations. "
                    "Large battery installations, such as the Hornsdale Power Reserve in South "
                    "Australia, have demonstrated that batteries can replace conventional gas "
                    "turbines for balancing short-term supply and demand imbalances. However, "
                    "lithium-ion storage is expensive at multi-day or seasonal scales and raises "
                    "concerns about lithium and cobalt supply chains.\n\n"
                    "Pumped-storage hydropower — which uses surplus electricity to pump water uphill "
                    "and generates power by releasing it downhill through turbines — currently "
                    "provides approximately 90 per cent of global grid storage capacity. Its "
                    "limitations are geographic: suitable sites must have two reservoirs at "
                    "significantly different elevations, a requirement that restricts expansion "
                    "in many regions.\n\n"
                    "Hydrogen has attracted attention as a long-duration storage medium. Surplus "
                    "renewable electricity can power electrolysers that split water into hydrogen "
                    "and oxygen. The hydrogen can be stored and later converted back to electricity "
                    "via fuel cells or burned in gas turbines. The round-trip efficiency — the "
                    "proportion of original energy recovered — is currently only about 30-40 per "
                    "cent, making it far less efficient than batteries. Proponents argue that for "
                    "seasonal storage and hard-to-decarbonise industrial applications, hydrogen's "
                    "high energy density makes it uniquely suitable despite the efficiency penalty.\n\n"
                    "Emerging alternatives include flow batteries, compressed air energy storage "
                    "in underground caverns, and gravity storage using heavy blocks raised by "
                    "electric motors. The energy transition will likely require a portfolio of "
                    "complementary storage technologies rather than a single dominant solution, "
                    "with the optimal mix varying by geography, grid structure, and the specific "
                    "needs of each energy system."
                ),
                "question_groups": [
                    {
                        "order": 1,
                        "question_type": "tfng",
                        "instruction": "Write TRUE, FALSE or NOT GIVEN.",
                        "questions": [
                            {"local_order": 1, "stem": "Renewable electricity is now cheaper than coal in most markets.", "correct_answer": "TRUE"},
                            {"local_order": 2, "stem": "The Hornsdale Power Reserve proved that batteries can balance short-term grid imbalances.", "correct_answer": "TRUE"},
                            {"local_order": 3, "stem": "Pumped-storage hydropower supplies around 90 per cent of global grid storage.", "correct_answer": "TRUE"},
                            {"local_order": 4, "stem": "Hydrogen storage has a round-trip efficiency of approximately 70-80 per cent.", "correct_answer": "FALSE"},
                            {"local_order": 5, "stem": "Flow batteries are currently the most widely deployed storage technology globally.", "correct_answer": "NOT GIVEN"},
                        ],
                    },
                    {
                        "order": 2,
                        "question_type": "mcq",
                        "instruction": "Choose the correct letter, A, B, C or D.",
                        "questions": [
                            {
                                "local_order": 1,
                                "stem": "What is the main limitation of pumped-storage hydropower?",
                                "options": [{"key": "A", "text": "High costs of lithium and cobalt materials"},
                                            {"key": "B", "text": "Slow response time compared to gas turbines"},
                                            {"key": "C", "text": "Geographic requirements that limit where it can be built"},
                                            {"key": "D", "text": "Low efficiency compared to lithium-ion batteries"}],
                                "correct_answer": "C",
                            },
                            {
                                "local_order": 2,
                                "stem": "Why does the passage say hydrogen may be suitable despite low efficiency?",
                                "options": [{"key": "A", "text": "It is cheaper to produce than lithium-ion batteries"},
                                            {"key": "B", "text": "Its high energy density suits seasonal storage and industrial use"},
                                            {"key": "C", "text": "It can be stored in any existing natural gas infrastructure"},
                                            {"key": "D", "text": "Electrolyser technology has recently improved its round-trip efficiency"}],
                                "correct_answer": "B",
                            },
                        ],
                    },
                    {
                        "order": 3,
                        "question_type": "sentence_completion",
                        "instruction": "Complete the sentences using NO MORE THAN TWO WORDS from the passage.",
                        "word_limit": 2,
                        "questions": [
                            {"local_order": 1, "stem": "The proportion of original energy recovered from a storage system is called its _____ efficiency.", "correct_answer": "round-trip", "answer_variants": ["round trip"]},
                            {"local_order": 2, "stem": "Surplus electricity can be used to power _____ that split water into hydrogen and oxygen.", "correct_answer": "electrolysers", "answer_variants": ["electrolyzers"]},
                            {"local_order": 3, "stem": "Experts suggest the energy transition will need a _____ of complementary storage technologies.", "correct_answer": "portfolio", "answer_variants": ["a portfolio"]},
                        ],
                    },
                ],
            },
            {
                "order": 2,
                "title": "Sleep, Memory and the Science of Rest",
                "body_text": (
                    "For much of the twentieth century, sleep was regarded by scientists as a passive "
                    "state — a period of inactivity during which the brain simply idled. Advances in "
                    "neuroscience have thoroughly overturned that assumption. Sleep is now recognised "
                    "as a period of intense biological activity essential to cognitive function, "
                    "emotional regulation, immune health, and metabolic processes.\n\n"
                    "Sleep is not uniform. It proceeds in cycles of approximately 90 minutes, "
                    "alternating between rapid eye movement (REM) sleep and several stages of "
                    "non-REM sleep. During slow-wave sleep — the deepest stage of non-REM — "
                    "the brain replays and consolidates memories acquired during the day, "
                    "transferring information from the hippocampus to longer-term cortical storage. "
                    "REM sleep, characterised by vivid dreaming, appears particularly important "
                    "for processing emotional memories and creative problem-solving.\n\n"
                    "The glymphatic system, identified only in 2013, has revealed another critical "
                    "function of sleep. During sleep, the brain's interstitial space expands by "
                    "approximately 60 per cent, allowing cerebrospinal fluid to flow more freely "
                    "and flush out metabolic waste products, including amyloid-beta and tau "
                    "proteins associated with Alzheimer's disease. Chronic sleep deprivation "
                    "impairs this clearance process, which researchers believe may accelerate "
                    "neurodegenerative disease.\n\n"
                    "Modern sleep science has also produced clear evidence for the health risks "
                    "of insufficient sleep. Adults sleeping fewer than seven hours per night show "
                    "increased risk of obesity, type 2 diabetes, cardiovascular disease, and "
                    "certain cancers. Immune function is measurably suppressed after a single "
                    "night of inadequate sleep. In a landmark experiment, individuals exposed to "
                    "the rhinovirus — the common cold — were almost three times more likely to "
                    "develop an infection if they had been sleeping fewer than seven hours than "
                    "if they were sleeping eight or more.\n\n"
                    "Despite this evidence, modern societies consistently undervalue sleep. "
                    "Economic pressures, artificial lighting, and the culture of the smartphone "
                    "conspire to shorten sleep duration. Shift work — which affects approximately "
                    "20 per cent of the workforce in industrialised nations — disrupts circadian "
                    "rhythms with consequences for physical and mental health. Sleep researchers "
                    "argue that treating adequate sleep as a public health priority, rather than "
                    "a personal lifestyle choice, is essential to addressing a growing and "
                    "largely preventable burden of chronic disease."
                ),
                "question_groups": [
                    {
                        "order": 1,
                        "question_type": "tfng",
                        "instruction": "Write TRUE, FALSE or NOT GIVEN.",
                        "questions": [
                            {"local_order": 1, "stem": "Early twentieth-century scientists believed the brain was highly active during sleep.", "correct_answer": "FALSE"},
                            {"local_order": 2, "stem": "Memory consolidation mainly occurs during the REM stage of sleep.", "correct_answer": "FALSE"},
                            {"local_order": 3, "stem": "The glymphatic system was first described in a 2013 research publication.", "correct_answer": "TRUE"},
                            {"local_order": 4, "stem": "People sleeping under seven hours a night are at greater risk of obesity and diabetes.", "correct_answer": "TRUE"},
                            {"local_order": 5, "stem": "Shift workers receive financial compensation for the health risks of disrupted sleep.", "correct_answer": "NOT GIVEN"},
                        ],
                    },
                    {
                        "order": 2,
                        "question_type": "mcq",
                        "instruction": "Choose the correct letter, A, B, C or D.",
                        "questions": [
                            {
                                "local_order": 1,
                                "stem": "What does the rhinovirus experiment demonstrate?",
                                "options": [{"key": "A", "text": "REM sleep is more important for immunity than non-REM sleep"},
                                            {"key": "B", "text": "Sleeping eight hours completely eliminates the risk of catching a cold"},
                                            {"key": "C", "text": "Short sleepers were nearly three times more likely to develop infection"},
                                            {"key": "D", "text": "The common cold virus spreads more easily in sleep-deprived populations"}],
                                "correct_answer": "C",
                            },
                            {
                                "local_order": 2,
                                "stem": "What happens to the brain's interstitial space during sleep, according to the passage?",
                                "options": [{"key": "A", "text": "It contracts to improve neural signal transmission"},
                                            {"key": "B", "text": "It expands by about 60 per cent to allow waste clearance"},
                                            {"key": "C", "text": "It fills with amyloid-beta and tau proteins"},
                                            {"key": "D", "text": "It transfers memories from cortical to hippocampal storage"}],
                                "correct_answer": "B",
                            },
                        ],
                    },
                    {
                        "order": 3,
                        "question_type": "sentence_completion",
                        "instruction": "Complete the sentences using NO MORE THAN TWO WORDS from the passage.",
                        "word_limit": 2,
                        "questions": [
                            {"local_order": 1, "stem": "During slow-wave sleep, memories are consolidated from the _____ to longer-term cortical storage.", "correct_answer": "hippocampus", "answer_variants": ["hippocampus to"]},
                            {"local_order": 2, "stem": "REM sleep appears especially important for processing emotional memories and _____ problem-solving.", "correct_answer": "creative", "answer_variants": ["creative problem"]},
                            {"local_order": 3, "stem": "The glymphatic system flushes out waste including amyloid-beta, linked to _____ disease.", "correct_answer": "Alzheimer's", "answer_variants": ["alzheimer's", "Alzheimer"]},
                        ],
                    },
                ],
            },
            {
                "order": 3,
                "title": "Archaeological Dating Methods: From Stratigraphy to DNA",
                "body_text": (
                    "Establishing when events in the human past occurred is one of archaeology's "
                    "fundamental challenges. The discipline has developed a range of dating methods "
                    "spanning from simple relative techniques, which establish sequence but not "
                    "absolute age, to sophisticated scientific methods that can date materials to "
                    "within decades or even years.\n\n"
                    "Stratigraphy — the study of the layers of sediment or debris that accumulate "
                    "over time — is the oldest and most universally applicable relative dating "
                    "method. The principle is straightforward: lower layers are generally older "
                    "than upper ones. Objects found within the same layer are assumed to be "
                    "broadly contemporary. While powerful in its simplicity, stratigraphy can "
                    "be complicated by soil disturbance, animal burrowing, and human activity "
                    "that mixes layers.\n\n"
                    "Radiocarbon dating, developed in the late 1940s by Willard Libby, revolutionised "
                    "archaeology by allowing the absolute dating of any organic material — bone, "
                    "charcoal, seeds, textiles — up to about 50,000 years old. The method exploits "
                    "the predictable decay of radioactive carbon-14, which living organisms "
                    "continuously absorb during their lifetimes. When an organism dies, its "
                    "carbon-14 begins to decay at a known rate, allowing the elapsed time to "
                    "be calculated from the remaining proportion. Advances in accelerator mass "
                    "spectrometry have reduced sample sizes from grams to milligrams, enabling "
                    "the dating of objects too precious to sacrifice significant material.\n\n"
                    "Dendrochronology — the analysis of tree-ring patterns — offers annual "
                    "precision for timbers used in construction, ships, or artworks. Trees "
                    "add one growth ring per year, and the width of each ring reflects growing "
                    "conditions. Regional master chronologies extend back over 10,000 years in "
                    "some areas, allowing wooden objects to be matched and precisely dated.\n\n"
                    "Ancient DNA analysis has opened an entirely new dimension of archaeological "
                    "investigation. By sequencing genetic material preserved in skeletal remains, "
                    "researchers can reconstruct migration patterns, population interactions, "
                    "and even the spread of diseases with a precision impossible from artefacts "
                    "and architecture alone. The analysis of ancient individuals from across "
                    "Eurasia has transformed understanding of the Bronze Age, revealing "
                    "massive population movements previously invisible to archaeologists."
                ),
                "question_groups": [
                    {
                        "order": 1,
                        "question_type": "tfng",
                        "instruction": "Write TRUE, FALSE or NOT GIVEN.",
                        "questions": [
                            {"local_order": 1, "stem": "Stratigraphy can establish the absolute date of an artefact.", "correct_answer": "FALSE"},
                            {"local_order": 2, "stem": "Radiocarbon dating was developed by Willard Libby in the 1940s.", "correct_answer": "TRUE"},
                            {"local_order": 3, "stem": "Carbon-14 can date organic materials up to about 50,000 years old.", "correct_answer": "TRUE"},
                            {"local_order": 4, "stem": "Tree-ring chronologies in some regions extend back more than 10,000 years.", "correct_answer": "TRUE"},
                            {"local_order": 5, "stem": "Ancient DNA analysis has confirmed that Bronze Age populations were largely sedentary.", "correct_answer": "FALSE"},
                        ],
                    },
                    {
                        "order": 2,
                        "question_type": "mcq",
                        "instruction": "Choose the correct letter, A, B, C or D.",
                        "questions": [
                            {
                                "local_order": 1,
                                "stem": "What advance has made radiocarbon dating less destructive to precious objects?",
                                "options": [{"key": "A", "text": "The invention of stratigraphy as a complementary method"},
                                            {"key": "B", "text": "The use of accelerator mass spectrometry requiring only milligrams of material"},
                                            {"key": "C", "text": "The development of tree-ring calibration curves"},
                                            {"key": "D", "text": "The sequencing of ancient DNA from bone"}],
                                "correct_answer": "B",
                            },
                            {
                                "local_order": 2,
                                "stem": "What can dendrochronology establish that other methods cannot?",
                                "options": [{"key": "A", "text": "The genetic origin of timber from different tree species"},
                                            {"key": "B", "text": "The age of any organic material up to 50,000 years old"},
                                            {"key": "C", "text": "The annual precision of dates for wooden objects"},
                                            {"key": "D", "text": "The sequence of archaeological layers at a site"}],
                                "correct_answer": "C",
                            },
                        ],
                    },
                    {
                        "order": 3,
                        "question_type": "sentence_completion",
                        "instruction": "Complete the sentences using NO MORE THAN TWO WORDS from the passage.",
                        "word_limit": 2,
                        "questions": [
                            {"local_order": 1, "stem": "The study of sediment or debris layers to establish chronological sequence is called _____.", "correct_answer": "stratigraphy", "answer_variants": ["Stratigraphy"]},
                            {"local_order": 2, "stem": "Trees produce one _____ each year, the width of which reflects growing conditions.", "correct_answer": "growth ring", "answer_variants": ["ring", "tree ring"]},
                            {"local_order": 3, "stem": "Ancient DNA research revealed large _____ movements during the Bronze Age that were previously unknown.", "correct_answer": "population", "answer_variants": ["population movements"]},
                        ],
                    },
                ],
            },
        ],
    },

    # ═════════════════════════════════════════════════════════════════════════
    # TEST 7 — Behavioural Economics · Coral Triangle · Nanotechnology
    # ═════════════════════════════════════════════════════════════════════════
    {
        "title": "IELTS Academic Reading — Set 7",
        "test_type": "academic", "component": "reading", "time_limit": 60,
        "passages": [
            {
                "order": 1,
                "title": "Nudging Behaviour: The Architecture of Choice",
                "body_text": (
                    "In 2008, American economists Richard Thaler and Cass Sunstein published 'Nudge', "
                    "a book that popularised the idea that small, carefully designed changes to the "
                    "environment in which people make decisions — what they termed the 'choice "
                    "architecture' — could reliably shift behaviour in desirable directions without "
                    "restricting freedom or changing financial incentives. The idea quickly attracted "
                    "governments eager to promote healthier eating, higher pension savings, and "
                    "reduced energy consumption without the political costs of legislation or taxation.\n\n"
                    "The theoretical foundation lies in behavioural economics, which integrates "
                    "insights from psychology to challenge the classical assumption that people "
                    "are rational, self-interested maximisers. Research by Kahneman, Tversky, "
                    "and others demonstrated that human decision-making is frequently driven "
                    "by cognitive shortcuts (heuristics) and systematic biases rather than "
                    "deliberate calculation. Among the most powerful of these biases is the "
                    "tendency to stick with the status quo: people rarely switch away from "
                    "whatever option is presented as the default.\n\n"
                    "The power of defaults was dramatically illustrated in a study of organ "
                    "donation rates across European countries. Nations with opt-out systems — "
                    "where citizens were automatically enrolled as donors unless they "
                    "affirmatively chose not to be — had donation rates of 85-99 per cent. "
                    "Countries with opt-in systems, where individuals had to actively register "
                    "as donors, had rates of 4-28 per cent. Identical populations, with "
                    "fundamentally different outcomes produced by a single administrative decision.\n\n"
                    "Pension saving is another domain where nudges have proven effective. "
                    "Research by Thaler and Shlomo Benartzi found that automatically enrolling "
                    "employees in workplace pension schemes and gradually escalating their "
                    "contribution rates — a programme they called Save More Tomorrow — "
                    "dramatically increased retirement savings without reducing take-home pay "
                    "perceptibly. The UK's auto-enrolment pension reform, which made "
                    "workplace pension saving the default from 2012, increased pension participation "
                    "from 55 per cent to over 85 per cent within a decade.\n\n"
                    "Critics raise legitimate concerns. Some argue that nudging is inherently "
                    "paternalistic, manipulating behaviour without full transparency. Others "
                    "point to the risk that poorly designed nudges can cause harm — for instance, "
                    "making unhealthy foods the most visible option in a canteen. There are "
                    "also questions about cultural transferability: a nudge proven effective in "
                    "the United States may not work in a different social context. Proponents "
                    "counter that all choice architectures nudge in one direction or another; "
                    "the question is whether they do so deliberately and in the public interest."
                ),
                "question_groups": [
                    {
                        "order": 1,
                        "question_type": "tfng",
                        "instruction": "Write TRUE, FALSE or NOT GIVEN.",
                        "questions": [
                            {"local_order": 1, "stem": "Thaler and Sunstein published 'Nudge' in 2008.", "correct_answer": "TRUE"},
                            {"local_order": 2, "stem": "Classical economics assumes that people always make rational, self-interested decisions.", "correct_answer": "TRUE"},
                            {"local_order": 3, "stem": "Opt-out countries achieved higher organ donation rates than opt-in countries.", "correct_answer": "TRUE"},
                            {"local_order": 4, "stem": "The 'Save More Tomorrow' programme required employees to cut their spending significantly.", "correct_answer": "FALSE"},
                            {"local_order": 5, "stem": "Nudges have been proven to be equally effective across all cultures.", "correct_answer": "FALSE"},
                        ],
                    },
                    {
                        "order": 2,
                        "question_type": "mcq",
                        "instruction": "Choose the correct letter, A, B, C or D.",
                        "questions": [
                            {
                                "local_order": 1,
                                "stem": "What does the organ donation study demonstrate?",
                                "options": [{"key": "A", "text": "People in opt-out countries are more altruistic than those in opt-in countries"},
                                            {"key": "B", "text": "The default option powerfully influences outcomes regardless of population characteristics"},
                                            {"key": "C", "text": "Legal requirements are more effective than choice architecture in changing behaviour"},
                                            {"key": "D", "text": "Donation rates depend primarily on national wealth and healthcare quality"}],
                                "correct_answer": "B",
                            },
                            {
                                "local_order": 2,
                                "stem": "What result did the UK's auto-enrolment pension reform achieve?",
                                "options": [{"key": "A", "text": "Pension participation rose from 55% to over 85% within a decade"},
                                            {"key": "B", "text": "Employee take-home pay increased alongside pension contributions"},
                                            {"key": "C", "text": "Participation rates fell as workers chose to opt out"},
                                            {"key": "D", "text": "The government collected more tax revenue from pension savings"}],
                                "correct_answer": "A",
                            },
                        ],
                    },
                    {
                        "order": 3,
                        "question_type": "sentence_completion",
                        "instruction": "Complete the sentences using NO MORE THAN TWO WORDS from the passage.",
                        "word_limit": 2,
                        "questions": [
                            {"local_order": 1, "stem": "Thaler and Sunstein used the term _____ architecture to describe the environment in which people make choices.", "correct_answer": "choice", "answer_variants": ["choice architecture"]},
                            {"local_order": 2, "stem": "Human decision-making is often guided by cognitive shortcuts called _____ rather than deliberate reasoning.", "correct_answer": "heuristics", "answer_variants": ["cognitive heuristics"]},
                            {"local_order": 3, "stem": "The Thaler-Benartzi pension programme was called Save More _____, allowing contributions to rise gradually.", "correct_answer": "Tomorrow", "answer_variants": ["tomorrow"]},
                        ],
                    },
                ],
            },
            {
                "order": 2,
                "title": "The Coral Triangle: Cradle of Marine Biodiversity",
                "body_text": (
                    "The Coral Triangle — a roughly triangular region spanning the tropical waters "
                    "of Indonesia, Malaysia, the Philippines, Papua New Guinea, Timor-Leste, and "
                    "the Solomon Islands — is the global epicentre of marine biodiversity. Covering "
                    "just 1.5 per cent of the world's ocean area, it contains more than 75 per "
                    "cent of all known coral species, over 3,000 species of reef fish, and six "
                    "of the world's seven marine turtle species. For this reason, scientists "
                    "sometimes call it the 'Amazon of the Seas'.\n\n"
                    "This extraordinary biodiversity is thought to result from a combination of "
                    "factors including the region's geological history, warm and stable water "
                    "temperatures, and its position at the confluence of three major ocean "
                    "currents. The region's complex island geography creates an enormous variety "
                    "of microhabitats — deep water trenches, shallow lagoons, mangrove forests, "
                    "and seagrass beds — each supporting distinct ecological communities.\n\n"
                    "The Coral Triangle sustains approximately 120 million people who live on "
                    "its coastlines, the vast majority of whom depend on reef fisheries for their "
                    "daily protein. Total fish catch from the region represents a substantial "
                    "fraction of global seafood supply. The region is also a major source of "
                    "live fish and coral for the global aquarium trade, and a significant "
                    "tourism destination.\n\n"
                    "Despite its resilience, the Coral Triangle faces severe and worsening threats. "
                    "Overfishing has dramatically depleted stocks of reef fish in many areas. "
                    "Destructive fishing practices — dynamite fishing and cyanide fishing — "
                    "physically destroy coral structures. Runoff from agricultural land and "
                    "coastal development introduces excess nutrients that promote algal growth "
                    "smothering corals. Climate change threatens coral bleaching events as water "
                    "temperatures exceed the thermal tolerance of coral-algae symbioses.\n\n"
                    "The Coral Triangle Initiative on Coral Reefs, Fisheries and Food Security, "
                    "launched in 2009 by the six governments of the region, represents a "
                    "significant multilateral response. It has established networks of marine "
                    "protected areas and worked to eliminate illegal fishing. Scientists and "
                    "conservationists have also identified naturally heat-tolerant coral strains "
                    "that may provide refugia for reef ecosystems as temperatures rise, though "
                    "whether such strains can protect the broader ecosystem remains uncertain."
                ),
                "question_groups": [
                    {
                        "order": 1,
                        "question_type": "tfng",
                        "instruction": "Write TRUE, FALSE or NOT GIVEN.",
                        "questions": [
                            {"local_order": 1, "stem": "The Coral Triangle covers 1.5 per cent of the ocean but contains over 75 per cent of coral species.", "correct_answer": "TRUE"},
                            {"local_order": 2, "stem": "The region contains all seven of the world's marine turtle species.", "correct_answer": "FALSE"},
                            {"local_order": 3, "stem": "Approximately 120 million coastal people rely on the Coral Triangle for food.", "correct_answer": "TRUE"},
                            {"local_order": 4, "stem": "Dynamite fishing is the leading cause of coral bleaching in the region.", "correct_answer": "FALSE"},
                            {"local_order": 5, "stem": "Heat-tolerant coral strains have been commercially cultivated in Indonesian waters.", "correct_answer": "NOT GIVEN"},
                        ],
                    },
                    {
                        "order": 2,
                        "question_type": "mcq",
                        "instruction": "Choose the correct letter, A, B, C or D.",
                        "questions": [
                            {
                                "local_order": 1,
                                "stem": "What created the Coral Triangle's extraordinary variety of microhabitats?",
                                "options": [{"key": "A", "text": "Large numbers of coral and fish species"},
                                            {"key": "B", "text": "The influence of three major ocean currents and complex island geography"},
                                            {"key": "C", "text": "The high volume of agricultural runoff into coastal waters"},
                                            {"key": "D", "text": "The consistent management of marine protected areas since 1990"}],
                                "correct_answer": "B",
                            },
                            {
                                "local_order": 2,
                                "stem": "What is the purpose of the Coral Triangle Initiative launched in 2009?",
                                "options": [{"key": "A", "text": "To promote the global aquarium trade in the region"},
                                            {"key": "B", "text": "To attract tourism revenue from reef diving"},
                                            {"key": "C", "text": "To protect reefs and manage fisheries through multilateral cooperation"},
                                            {"key": "D", "text": "To breed heat-tolerant corals for commercial sale"}],
                                "correct_answer": "C",
                            },
                        ],
                    },
                    {
                        "order": 3,
                        "question_type": "sentence_completion",
                        "instruction": "Complete the sentences using NO MORE THAN TWO WORDS from the passage.",
                        "word_limit": 2,
                        "questions": [
                            {"local_order": 1, "stem": "Scientists sometimes call the Coral Triangle the '_____ of the Seas' due to its exceptional biodiversity.", "correct_answer": "Amazon", "answer_variants": ["amazon"]},
                            {"local_order": 2, "stem": "Excess _____ from agricultural land promotes algal growth that smothers corals.", "correct_answer": "nutrients", "answer_variants": ["nutrient runoff", "agricultural runoff"]},
                            {"local_order": 3, "stem": "Naturally heat-tolerant coral strains may serve as _____ for reef ecosystems as ocean temperatures rise.", "correct_answer": "refugia", "answer_variants": ["a refugia"]},
                        ],
                    },
                ],
            },
            {
                "order": 3,
                "title": "Nanotechnology: Engineering at the Scale of Atoms",
                "body_text": (
                    "Nanotechnology involves the manipulation of matter at the scale of one to one hundred "
                    "nanometres — a nanometre being one billionth of a metre, approximately the width of "
                    "ten hydrogen atoms placed side by side. At this scale, materials often behave in "
                    "ways that differ markedly from their bulk properties, because quantum mechanical "
                    "effects and the extremely high ratio of surface area to volume become dominant.\n\n"
                    "Gold provides a striking example of nanoscale property changes. In bulk form, "
                    "gold is yellow, chemically inert, and highly electrically conductive. Gold "
                    "nanoparticles of around 20 nanometres, by contrast, appear red in solution "
                    "because of a phenomenon called surface plasmon resonance, in which electrons "
                    "oscillate collectively in response to incident light. At different sizes, "
                    "gold nanoparticles can appear orange, purple, or blue. These optical properties "
                    "are already exploited in pregnancy tests and lateral flow assays.\n\n"
                    "Medical applications represent the most actively pursued frontier. Cancer "
                    "treatment has long been hampered by the toxicity of chemotherapy drugs, "
                    "which damage healthy tissue throughout the body alongside their intended "
                    "targets. Nanoparticle drug delivery systems can be engineered to accumulate "
                    "preferentially in tumour tissue and release their payload in response to "
                    "specific chemical triggers in the tumour microenvironment, sparing healthy "
                    "cells. Several nanoparticle cancer therapies have already received regulatory "
                    "approval in the United States and Europe.\n\n"
                    "In materials science, carbon nanotubes and graphene have attracted particular "
                    "interest. Carbon nanotubes — cylinders of graphene just nanometres in diameter — "
                    "combine exceptional tensile strength, estimated at 100 times that of steel at "
                    "one-sixth the weight, with excellent electrical conductivity. Graphene, a "
                    "single layer of carbon atoms arranged in a hexagonal lattice, is both the "
                    "thinnest and one of the strongest materials known. Both materials hold "
                    "promise for applications in lightweight aerospace components, high-capacity "
                    "batteries, and flexible electronics.\n\n"
                    "Safety questions remain incompletely answered. Some nanoparticles can penetrate "
                    "biological barriers — the blood-brain barrier, the placenta — that block "
                    "larger particles. The long-term effects of inhaling nanoparticles in "
                    "occupational or environmental settings are not fully characterised. Regulatory "
                    "frameworks have struggled to keep pace with the rapid proliferation of "
                    "nano-enabled products on the market."
                ),
                "question_groups": [
                    {
                        "order": 1,
                        "question_type": "tfng",
                        "instruction": "Write TRUE, FALSE or NOT GIVEN.",
                        "questions": [
                            {"local_order": 1, "stem": "At the nanoscale, materials often display different properties from their bulk form.", "correct_answer": "TRUE"},
                            {"local_order": 2, "stem": "Gold nanoparticles always appear red regardless of their size.", "correct_answer": "FALSE"},
                            {"local_order": 3, "stem": "Nanoparticle cancer therapies have been approved by regulators in the USA and Europe.", "correct_answer": "TRUE"},
                            {"local_order": 4, "stem": "Carbon nanotubes are approximately 100 times stronger than steel by weight.", "correct_answer": "FALSE"},
                            {"local_order": 5, "stem": "Graphene is currently the world's most electrically conductive material.", "correct_answer": "NOT GIVEN"},
                        ],
                    },
                    {
                        "order": 2,
                        "question_type": "mcq",
                        "instruction": "Choose the correct letter, A, B, C or D.",
                        "questions": [
                            {
                                "local_order": 1,
                                "stem": "How do nanoparticle drug delivery systems improve cancer treatment?",
                                "options": [{"key": "A", "text": "By making drugs cheaper and easier to manufacture"},
                                            {"key": "B", "text": "By accumulating in tumours and releasing drugs precisely, sparing healthy tissue"},
                                            {"key": "C", "text": "By crossing the blood-brain barrier to treat brain tumours"},
                                            {"key": "D", "text": "By combining chemotherapy with radiation in a single nanoparticle"}],
                                "correct_answer": "B",
                            },
                            {
                                "local_order": 2,
                                "stem": "What property makes gold nanoparticles useful in pregnancy tests?",
                                "options": [{"key": "A", "text": "Their chemical inertness and yellow colour"},
                                            {"key": "B", "text": "Their electrical conductivity at the nanoscale"},
                                            {"key": "C", "text": "Their optical properties arising from surface plasmon resonance"},
                                            {"key": "D", "text": "Their ability to penetrate the blood-brain barrier"}],
                                "correct_answer": "C",
                            },
                        ],
                    },
                    {
                        "order": 3,
                        "question_type": "sentence_completion",
                        "instruction": "Complete the sentences using NO MORE THAN TWO WORDS from the passage.",
                        "word_limit": 2,
                        "questions": [
                            {"local_order": 1, "stem": "The optical colour change in gold nanoparticles is caused by a phenomenon called surface _____ resonance.", "correct_answer": "plasmon", "answer_variants": ["plasmon resonance"]},
                            {"local_order": 2, "stem": "Carbon nanotubes are cylinders of _____ with exceptional tensile strength and electrical conductivity.", "correct_answer": "graphene", "answer_variants": ["carbon graphene"]},
                            {"local_order": 3, "stem": "Regulators have struggled to keep pace with the rapid growth of _____ products entering the market.", "correct_answer": "nano-enabled", "answer_variants": ["nano enabled", "nanotechnology"]},
                        ],
                    },
                ],
            },
        ],
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# EXTRA WRITING PROMPTS (5 more, topics: environment, technology, society)
# ─────────────────────────────────────────────────────────────────────────────

EXTRA_WRITING_PROMPTS = [
    {
        "task_type": "task2",
        "topic": "Technology",
        "prompt": (
            "Artificial intelligence is increasingly being used to make decisions that affect "
            "people's lives, such as in hiring, loan applications, and criminal sentencing.\n\n"
            "To what extent is this a positive or negative development?\n\n"
            "Give reasons for your answer and include any relevant examples from your own "
            "knowledge or experience."
        ),
        "band_descriptors": "Task Achievement, Coherence and Cohesion, Lexical Resource, Grammatical Range",
        "image_description": None,
    },
    {
        "task_type": "task2",
        "topic": "Environment",
        "prompt": (
            "Some people believe that individuals should be responsible for reducing plastic "
            "waste, while others argue that governments and corporations must take the lead.\n\n"
            "Discuss both views and give your own opinion.\n\n"
            "Give reasons for your answer and include any relevant examples from your own "
            "knowledge or experience."
        ),
        "band_descriptors": "Task Achievement, Coherence and Cohesion, Lexical Resource, Grammatical Range",
        "image_description": None,
    },
    {
        "task_type": "task2",
        "topic": "Education",
        "prompt": (
            "University education has become increasingly expensive in many countries. "
            "Some people argue that governments should fund university education fully, "
            "while others believe students should pay for their own degrees.\n\n"
            "Discuss both views and give your own opinion.\n\n"
            "Give reasons for your answer and include any relevant examples from your own "
            "knowledge or experience."
        ),
        "band_descriptors": "Task Achievement, Coherence and Cohesion, Lexical Resource, Grammatical Range",
        "image_description": None,
    },
    {
        "task_type": "task2",
        "topic": "Society",
        "prompt": (
            "In many countries, people are working longer hours and spending less time with "
            "their families. What are the causes of this problem, and what measures could "
            "be taken to address it?\n\n"
            "Give reasons for your answer and include any relevant examples from your own "
            "knowledge or experience."
        ),
        "band_descriptors": "Task Achievement, Coherence and Cohesion, Lexical Resource, Grammatical Range",
        "image_description": None,
    },
    {
        "task_type": "task2",
        "topic": "Health",
        "prompt": (
            "Rising rates of obesity represent a serious global health problem. "
            "Some people say that individual lifestyle choices are responsible, while others "
            "argue that the food industry and government policies are to blame.\n\n"
            "Discuss both views and give your own opinion.\n\n"
            "Give reasons for your answer and include any relevant examples from your own "
            "knowledge or experience."
        ),
        "band_descriptors": "Task Achievement, Coherence and Cohesion, Lexical Resource, Grammatical Range",
        "image_description": None,
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# SEEDER
# ─────────────────────────────────────────────────────────────────────────────

def seed(db: Session) -> dict:
    """Adds extra reading tests and writing prompts if not already present."""
    from .seed_ielts import _create_test

    added_tests = 0
    existing_titles = {t.title for t in db.query(models.IELTSTest.title).all()}
    for test_data in EXTRA_READING_TESTS:
        if test_data["title"] not in existing_titles:
            _create_test(test_data, db)
            added_tests += 1

    added_prompts = 0
    existing_prompts = {p.prompt for p in db.query(models.WritingPrompt.prompt).all()}
    for p in EXTRA_WRITING_PROMPTS:
        if p["prompt"] not in existing_prompts:
            db.add(models.WritingPrompt(**p))
            added_prompts += 1
    if added_prompts:
        db.commit()

    return {"extra_reading_tests_added": added_tests, "extra_writing_prompts_added": added_prompts}
