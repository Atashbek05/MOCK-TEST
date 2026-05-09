"""
IELTS Reading Test Seed Data
4 tests × 3 passages × 6 questions = 72 questions total
"""

READING_TESTS = [
    # ─────────────────────────────────────────────────────────────────────────
    # TEST 1 — Technology and Society
    # ─────────────────────────────────────────────────────────────────────────
    {
        "title": "Reading Test 1 — Technology and Society",
        "passages": [
            {
                "order": 1,
                "title": "Artificial Intelligence in Healthcare",
                "text": (
                    "Artificial intelligence (AI) is rapidly transforming the healthcare industry, "
                    "offering solutions that were once considered science fiction. Machine learning "
                    "algorithms can now analyse medical images with an accuracy that rivals, and in "
                    "some cases surpasses, that of experienced physicians. A landmark study published "
                    "in 2019 demonstrated that an AI system could detect breast cancer from mammograms "
                    "with 94.5% accuracy, outperforming a panel of six radiologists.\n\n"
                    "Beyond imaging, AI is making significant strides in drug discovery. Traditional "
                    "pharmaceutical research is a notoriously slow and expensive process, often taking "
                    "over a decade and costing billions of dollars to bring a single drug to market. "
                    "AI platforms can screen millions of chemical compounds in a matter of days, "
                    "predicting which molecules are most likely to be effective against specific "
                    "diseases. During the COVID-19 pandemic, AI tools helped researchers identify "
                    "potential antiviral compounds in record time.\n\n"
                    "Predictive analytics represents another powerful application. By analysing "
                    "patient data — including medical history, lifestyle factors, and genetic "
                    "information — AI systems can forecast an individual's risk of developing "
                    "conditions such as heart disease or diabetes years before symptoms appear. "
                    "This shift from reactive to preventive medicine has the potential to save "
                    "millions of lives and significantly reduce healthcare costs.\n\n"
                    "However, the integration of AI into healthcare is not without challenges. "
                    "Questions of data privacy are paramount; training effective AI models requires "
                    "vast amounts of sensitive patient information, raising serious ethical concerns "
                    "about consent and data security. Moreover, AI systems are only as reliable as "
                    "the data used to train them. Historical healthcare datasets often reflect "
                    "societal biases, and there is a risk that AI tools could inadvertently "
                    "perpetuate unequal treatment if not carefully designed.\n\n"
                    "Healthcare professionals also express concerns about the 'black box' nature of "
                    "many AI systems — the inability to explain how a specific decision or "
                    "recommendation was reached. In medicine, where the rationale behind a diagnosis "
                    "can be just as important as the diagnosis itself, this lack of transparency "
                    "poses a significant obstacle to widespread adoption. Regulatory frameworks are "
                    "still catching up with this rapidly evolving technology, and questions of "
                    "liability remain largely unresolved."
                ),
                "questions": [
                    {
                        "question_text": "According to the passage, how did an AI system perform in detecting breast cancer compared to radiologists?",
                        "option_a": "It performed worse than the panel of radiologists",
                        "option_b": "It matched the performance of the most experienced radiologist",
                        "option_c": "It outperformed a panel of six radiologists with 94.5% accuracy",
                        "option_d": "It was comparable but needed human verification for all results",
                        "correct_answer": "C",
                    },
                    {
                        "question_text": "What is described as a major advantage of AI in drug discovery?",
                        "option_a": "Eliminating the need for clinical trials",
                        "option_b": "Screening millions of compounds quickly to identify promising molecules",
                        "option_c": "Reducing the cost of medical manufacturing",
                        "option_d": "Allowing patients to self-diagnose conditions",
                        "correct_answer": "B",
                    },
                    {
                        "question_text": "What does the passage say about predictive analytics in healthcare?",
                        "option_a": "It can only be used for patients who already have symptoms",
                        "option_b": "It analyses lifestyle and genetic data to forecast disease risk years in advance",
                        "option_c": "It is primarily used to reduce hospital waiting times",
                        "option_d": "It has been fully implemented in hospitals worldwide",
                        "correct_answer": "B",
                    },
                    {
                        "question_text": "Which of the following is identified as a challenge in integrating AI into healthcare?",
                        "option_a": "The high cost of AI hardware",
                        "option_b": "Resistance from patients who prefer human doctors",
                        "option_c": "The risk of AI systems perpetuating biases from historical data",
                        "option_d": "The inability of AI to process large datasets",
                        "correct_answer": "C",
                    },
                    {
                        "question_text": "What does 'black box' refer to in the context of the passage?",
                        "option_a": "A secure data storage system used in hospitals",
                        "option_b": "The inability to explain how an AI system arrives at its decisions",
                        "option_c": "A type of encrypted AI communication protocol",
                        "option_d": "A specialised AI tool used only in emergency medicine",
                        "correct_answer": "B",
                    },
                    {
                        "question_text": "What does the author suggest about regulatory frameworks for AI in healthcare?",
                        "option_a": "They are comprehensive and have resolved most liability issues",
                        "option_b": "They are too strict and are slowing AI development",
                        "option_c": "They are still developing and have not fully addressed liability",
                        "option_d": "They are not needed as the industry is self-regulating",
                        "correct_answer": "C",
                    },
                ],
            },
            {
                "order": 2,
                "title": "The Internet of Things: A Connected World",
                "text": (
                    "The Internet of Things (IoT) describes the vast network of physical devices — "
                    "from household appliances and wearable fitness trackers to industrial sensors "
                    "and autonomous vehicles — that are embedded with software, sensors, and "
                    "connectivity to exchange data over the internet. The concept, first coined in "
                    "the late 1990s, has grown from a theoretical idea into a global technological "
                    "infrastructure that analysts predict will encompass over 75 billion connected "
                    "devices by 2030.\n\n"
                    "At the consumer level, IoT has transformed daily life in subtle but profound "
                    "ways. Smart home systems allow homeowners to control lighting, heating, and "
                    "security cameras remotely through smartphone applications. Refrigerators can "
                    "automatically compile shopping lists based on their contents, and voice-activated "
                    "assistants manage calendars, play music, and provide real-time information on "
                    "demand. These conveniences, while often dismissed as luxury features, represent "
                    "a fundamental shift in the relationship between humans and their physical "
                    "environment.\n\n"
                    "In industrial settings, IoT delivers even more substantial benefits. "
                    "Manufacturing plants deploy networks of sensors to monitor equipment "
                    "performance, predicting mechanical failures before they occur — a practice "
                    "known as predictive maintenance. This approach has been shown to reduce "
                    "equipment downtime by up to 50% and lower maintenance costs by up to 40%. "
                    "Agriculture is also being transformed: smart irrigation systems use weather "
                    "data and soil moisture sensors to optimise water usage, reducing consumption "
                    "by up to 30% while maintaining or improving crop yields.\n\n"
                    "The smart city concept represents perhaps the most ambitious application of "
                    "IoT technology. Cities around the world are deploying sensor networks to manage "
                    "traffic flow in real time, reduce energy consumption in public buildings, "
                    "improve waste collection efficiency, and monitor air quality. Barcelona's smart "
                    "city initiative, for example, reportedly saves the city €75 million annually "
                    "and has created thousands of new jobs.\n\n"
                    "Despite these benefits, IoT raises significant security concerns. The sheer "
                    "volume of connected devices creates an enormous attack surface for "
                    "cybercriminals. Many consumer IoT products are manufactured with minimal "
                    "security features — default passwords that users rarely change, unencrypted "
                    "data transmission, and infrequent software updates. In 2016, the Mirai botnet "
                    "attack demonstrated the scale of this vulnerability, when hackers commandeered "
                    "hundreds of thousands of IoT devices to launch a massive distributed "
                    "denial-of-service attack that temporarily disabled major internet services."
                ),
                "questions": [
                    {
                        "question_text": "How many connected IoT devices do analysts predict will exist by 2030?",
                        "option_a": "Over 7.5 billion",
                        "option_b": "Over 75 billion",
                        "option_c": "Over 750 billion",
                        "option_d": "Over 7.5 trillion",
                        "correct_answer": "B",
                    },
                    {
                        "question_text": "What is 'predictive maintenance' as described in the passage?",
                        "option_a": "Using historical data to plan scheduled maintenance intervals",
                        "option_b": "Monitoring equipment with sensors to predict failures before they happen",
                        "option_c": "A new form of factory management software",
                        "option_d": "Training workers to identify early signs of equipment failure",
                        "correct_answer": "B",
                    },
                    {
                        "question_text": "According to the passage, what financial benefit has Barcelona's smart city initiative achieved?",
                        "option_a": "It has attracted €75 million in foreign investment",
                        "option_b": "It saves the city €75 million annually",
                        "option_c": "It has reduced city debt by €75 million",
                        "option_d": "It generates €75 million in tourism revenue",
                        "correct_answer": "B",
                    },
                    {
                        "question_text": "What security vulnerability was demonstrated by the 2016 Mirai botnet attack?",
                        "option_a": "Government databases could be accessed through IoT devices",
                        "option_b": "Smartphone applications were the weakest point in IoT security",
                        "option_c": "Hundreds of thousands of IoT devices could be used to disrupt major internet services",
                        "option_d": "Smart home devices could be used to conduct physical surveillance",
                        "correct_answer": "C",
                    },
                    {
                        "question_text": "Which of the following is NOT mentioned as a feature creating IoT security risks?",
                        "option_a": "Default passwords that users rarely change",
                        "option_b": "Unencrypted data transmission",
                        "option_c": "Infrequent software updates",
                        "option_d": "Excessive power consumption draining device batteries",
                        "correct_answer": "D",
                    },
                    {
                        "question_text": "How does the author describe the consumer IoT conveniences mentioned in the passage?",
                        "option_a": "As essential tools that most households now rely on",
                        "option_b": "As examples of a fundamental shift in how humans relate to their environment",
                        "option_c": "As overhyped products that deliver limited practical value",
                        "option_d": "As technologies primarily beneficial for elderly users",
                        "correct_answer": "B",
                    },
                ],
            },
            {
                "order": 3,
                "title": "The Gig Economy: Flexibility and Fragility",
                "text": (
                    "The gig economy — a labour market characterised by short-term contracts and "
                    "freelance work rather than permanent employment — has expanded dramatically over "
                    "the past decade. Platforms such as Uber, Deliveroo, Fiverr, and Upwork have "
                    "created a new category of worker: independent contractors who can earn income "
                    "by completing discrete 'gigs' on a flexible schedule. Proponents celebrate this "
                    "model for the autonomy and flexibility it offers workers, while critics argue "
                    "it represents a dangerous erosion of labour protections built up over a century.\n\n"
                    "The statistics paint a complex picture. In the United Kingdom, an estimated "
                    "five million people work in the gig economy, a figure that has grown "
                    "substantially since 2016. In the United States, various studies suggest that "
                    "anywhere between 15 and 34 percent of the workforce participates in some form "
                    "of gig work, either as a primary or supplementary income source. The COVID-19 "
                    "pandemic accelerated this trend as companies sought to reduce fixed costs and "
                    "workers sought more flexible arrangements.\n\n"
                    "For many workers, particularly those with caregiving responsibilities, "
                    "disabilities, or other constraints that make traditional employment difficult, "
                    "gig work offers genuine advantages. The ability to set one's own hours, choose "
                    "preferred tasks, and work from any location provides a degree of autonomy "
                    "unavailable in conventional jobs. Many highly skilled professionals — software "
                    "developers, graphic designers, and consultants — use gig platforms to build "
                    "lucrative independent careers with incomes far exceeding what they might earn "
                    "as employees.\n\n"
                    "However, for the majority of gig workers, the reality is more precarious. "
                    "Without employer-provided benefits such as health insurance, paid sick leave, "
                    "retirement contributions, and unemployment protection, gig workers bear all "
                    "the risks of income volatility themselves. Studies consistently show that most "
                    "gig workers earn below the minimum wage once expenses such as vehicle "
                    "maintenance, fuel, and equipment are deducted. The psychological burden of "
                    "income uncertainty can also be significant, with research linking precarious "
                    "employment to higher rates of anxiety and depression.\n\n"
                    "Legal battles over the classification of gig workers have become a defining "
                    "feature of the modern labour landscape. In 2021, the UK Supreme Court ruled "
                    "that Uber drivers were 'workers' rather than independent contractors, entitling "
                    "them to minimum wage protections, holiday pay, and pension contributions. "
                    "Similar legal challenges are unfolding across Europe and the United States, "
                    "where the fundamental question — whether platforms are employers or merely "
                    "digital marketplaces — remains deeply contested."
                ),
                "questions": [
                    {
                        "question_text": "Approximately how many people work in the gig economy in the United Kingdom?",
                        "option_a": "One million",
                        "option_b": "Three million",
                        "option_c": "Five million",
                        "option_d": "Ten million",
                        "correct_answer": "C",
                    },
                    {
                        "question_text": "According to the passage, what did the UK Supreme Court rule in 2021?",
                        "option_a": "That gig economy platforms must be regulated as traditional employers",
                        "option_b": "That Uber drivers were 'workers' entitled to minimum wage and holiday pay",
                        "option_c": "That gig work contracts were legally invalid",
                        "option_d": "That all gig workers must be reclassified as full-time employees",
                        "correct_answer": "B",
                    },
                    {
                        "question_text": "Which group does the passage suggest benefits most from gig work?",
                        "option_a": "Factory workers seeking overtime pay",
                        "option_b": "Retired individuals looking for extra income",
                        "option_c": "Highly skilled professionals such as developers and designers",
                        "option_d": "Recent graduates with no work experience",
                        "correct_answer": "C",
                    },
                    {
                        "question_text": "What psychological consequence of gig work does the passage identify for many workers?",
                        "option_a": "Increased sense of purpose and professional satisfaction",
                        "option_b": "Higher rates of anxiety and depression linked to income uncertainty",
                        "option_c": "Social isolation from working without colleagues",
                        "option_d": "Loss of professional identity over time",
                        "correct_answer": "B",
                    },
                    {
                        "question_text": "Which factor does the passage NOT mention as contributing to the growth of the gig economy?",
                        "option_a": "Companies reducing fixed costs",
                        "option_b": "Workers seeking more flexible arrangements",
                        "option_c": "The COVID-19 pandemic",
                        "option_d": "Government incentives for platform businesses",
                        "correct_answer": "D",
                    },
                    {
                        "question_text": "What is the fundamental legal question that remains contested regarding gig platforms?",
                        "option_a": "Whether platforms must pay corporate taxes on gig worker earnings",
                        "option_b": "Whether platforms are employers or merely digital marketplaces",
                        "option_c": "Whether gig work contracts must be written or can be verbal",
                        "option_d": "Whether gig workers should be allowed to form trade unions",
                        "correct_answer": "B",
                    },
                ],
            },
        ],
    },

    # ─────────────────────────────────────────────────────────────────────────
    # TEST 2 — Environment and Science
    # ─────────────────────────────────────────────────────────────────────────
    {
        "title": "Reading Test 2 — Environment and Science",
        "passages": [
            {
                "order": 1,
                "title": "Ocean Acidification: The Other CO₂ Problem",
                "text": (
                    "While the warming of Earth's atmosphere has dominated discussions of climate "
                    "change, a parallel and equally alarming process is unfolding in the world's "
                    "oceans. Ocean acidification — the ongoing decrease in the pH of seawater "
                    "caused by the ocean's absorption of atmospheric carbon dioxide — has reduced "
                    "the average pH of surface ocean waters from 8.2 to approximately 8.1 since "
                    "the Industrial Revolution. This change of 0.1 pH units represents a 26% "
                    "increase in acidity, and scientists project that pH could fall a further 0.3 "
                    "to 0.4 units by the end of the century if current emissions continue.\n\n"
                    "The mechanism is straightforward chemistry. When carbon dioxide dissolves in "
                    "seawater, it reacts with water to form carbonic acid. This acid then "
                    "dissociates, releasing hydrogen ions that increase the water's acidity and "
                    "reduce the concentration of carbonate ions. It is this reduction in carbonate "
                    "ions that poses the greatest threat to marine ecosystems, as carbonate is the "
                    "building block that many marine organisms — including corals, oysters, mussels, "
                    "and certain species of plankton — use to construct their shells and skeletons.\n\n"
                    "Research has demonstrated that even the modest acidification already observed "
                    "is affecting marine life in significant ways. Studies of oyster hatcheries on "
                    "the US Pacific Coast have documented sharp declines in larval survival rates "
                    "directly linked to increased water acidity. Experiments on pteropods — tiny "
                    "free-swimming snails that form a critical part of the food web in polar and "
                    "sub-polar oceans — have shown that their shells begin to dissolve within 45 "
                    "days when exposed to ocean pH levels projected for the year 2100.\n\n"
                    "Coral reef ecosystems, which cover less than one percent of the ocean floor "
                    "yet support an estimated 25% of all marine species, face a particularly severe "
                    "threat. Coral bleaching events, already increasing in frequency due to warming "
                    "temperatures, are compounded by acidification's effect on the ability of corals "
                    "to rebuild their calcium carbonate structures. Some scientists now predict that "
                    "if current trends continue, the majority of the world's coral reefs could be "
                    "in a critical state of decline by 2050.\n\n"
                    "The consequences extend beyond marine biodiversity. The fishing industry — "
                    "which provides food and livelihoods for hundreds of millions of people "
                    "worldwide — is directly at risk. Shellfish farming, a particularly vulnerable "
                    "sector, contributes over $1 billion annually to the US economy alone. "
                    "Furthermore, healthy ocean ecosystems play a crucial role in regulating "
                    "Earth's climate by absorbing both carbon dioxide and heat. Their deterioration "
                    "could trigger feedback loops that accelerate the very climate changes that "
                    "caused ocean acidification in the first place."
                ),
                "questions": [
                    {
                        "question_text": "By how much has ocean acidity increased since the Industrial Revolution?",
                        "option_a": "8%",
                        "option_b": "16%",
                        "option_c": "26%",
                        "option_d": "36%",
                        "correct_answer": "C",
                    },
                    {
                        "question_text": "What chemical process causes ocean acidification?",
                        "option_a": "Nitrogen from industrial runoff reacting with ocean salt",
                        "option_b": "Carbon dioxide dissolving in seawater to form carbonic acid",
                        "option_c": "Solar radiation breaking down water molecules into acid compounds",
                        "option_d": "Temperature increases causing chemical reactions in deep sea minerals",
                        "correct_answer": "B",
                    },
                    {
                        "question_text": "What happened to pteropod shells in experiments simulating year 2100 ocean pH?",
                        "option_a": "They grew thicker as a natural adaptation",
                        "option_b": "They changed colour but maintained structural integrity",
                        "option_c": "They began to dissolve within 45 days",
                        "option_d": "They developed microscopic cracks over several months",
                        "correct_answer": "C",
                    },
                    {
                        "question_text": "What percentage of all marine species do coral reefs support?",
                        "option_a": "1%",
                        "option_b": "10%",
                        "option_c": "25%",
                        "option_d": "50%",
                        "correct_answer": "C",
                    },
                    {
                        "question_text": "What financial contribution does shellfish farming make to the US economy annually?",
                        "option_a": "Over $100 million",
                        "option_b": "Over $1 billion",
                        "option_c": "Over $10 billion",
                        "option_d": "Over $100 billion",
                        "correct_answer": "B",
                    },
                    {
                        "question_text": "What does the passage suggest about ocean deterioration and climate change?",
                        "option_a": "Healthy oceans can fully reverse the effects of climate change",
                        "option_b": "Ocean deterioration could trigger feedback loops that accelerate climate change",
                        "option_c": "Oceans are unaffected by climate change but affect the atmosphere",
                        "option_d": "The relationship is too complex to model or predict",
                        "correct_answer": "B",
                    },
                ],
            },
            {
                "order": 2,
                "title": "The Solar Energy Revolution",
                "text": (
                    "Solar energy has undergone one of the most remarkable cost reductions in the "
                    "history of any technology. In 2010, the average cost of generating one "
                    "megawatt-hour of electricity from solar photovoltaic (PV) panels was "
                    "approximately $380. By 2023, this figure had fallen to below $30 — a decline "
                    "of over 90% in just thirteen years. This dramatic reduction has transformed "
                    "solar from a niche alternative into the cheapest source of electricity in "
                    "history in many parts of the world.\n\n"
                    "The physics underlying solar PV technology is based on the photoelectric "
                    "effect, first explained by Albert Einstein in 1905, for which he received the "
                    "Nobel Prize. When photons from sunlight strike a semiconductor material — "
                    "typically silicon — they knock electrons loose, creating a flow of electrical "
                    "current. Modern commercial solar panels convert between 15% and 22% of "
                    "incident sunlight into electricity, while research-grade cells have achieved "
                    "efficiencies exceeding 47% in laboratory conditions.\n\n"
                    "The rapid expansion of solar capacity has been striking. Global installed "
                    "solar capacity reached one terawatt in 2022 and is projected to reach five "
                    "terawatts by 2030. China leads the world in solar installations, accounting "
                    "for roughly 40% of global capacity, while Germany, the United States, Japan, "
                    "and India are also major producers.\n\n"
                    "Despite this progress, significant challenges remain. The intermittent nature "
                    "of solar power — panels only generate electricity when sunlight is available "
                    "— requires effective energy storage solutions or complementary power sources "
                    "to ensure reliable grid supply. Battery storage technology has improved "
                    "significantly, but storing enough energy to supply power through cloudy "
                    "periods or at night remains expensive at grid scale.\n\n"
                    "Land use is another consideration. Utility-scale solar farms require "
                    "substantial areas, which can create conflicts with agriculture, wildlife "
                    "habitats, and local communities. However, emerging approaches such as "
                    "agrivoltaics — the co-location of solar panels and agricultural crops — show "
                    "promise in addressing this tension. Research has demonstrated that certain "
                    "crops actually benefit from partial shading provided by solar panels, while "
                    "panel efficiency can improve in the cooler microclimate created beneath crop "
                    "canopies."
                ),
                "questions": [
                    {
                        "question_text": "By approximately how much did the cost of solar electricity fall between 2010 and 2023?",
                        "option_a": "Over 50%",
                        "option_b": "Over 70%",
                        "option_c": "Over 90%",
                        "option_d": "Over 99%",
                        "correct_answer": "C",
                    },
                    {
                        "question_text": "Who first explained the photoelectric effect that underlies solar PV technology?",
                        "option_a": "Isaac Newton",
                        "option_b": "Marie Curie",
                        "option_c": "Albert Einstein",
                        "option_d": "Nikola Tesla",
                        "correct_answer": "C",
                    },
                    {
                        "question_text": "What efficiency range do modern commercial solar panels achieve?",
                        "option_a": "5–10% of incident sunlight",
                        "option_b": "15–22% of incident sunlight",
                        "option_c": "30–40% of incident sunlight",
                        "option_d": "45–50% of incident sunlight",
                        "correct_answer": "B",
                    },
                    {
                        "question_text": "What is 'agrivoltaics' as described in the passage?",
                        "option_a": "A new type of solar panel made from agricultural materials",
                        "option_b": "The co-location of solar panels and agricultural crops",
                        "option_c": "Using solar energy to power agricultural machinery",
                        "option_d": "Converting agricultural waste into solar fuel",
                        "correct_answer": "B",
                    },
                    {
                        "question_text": "Which country accounts for approximately 40% of global solar capacity?",
                        "option_a": "United States",
                        "option_b": "Germany",
                        "option_c": "India",
                        "option_d": "China",
                        "correct_answer": "D",
                    },
                    {
                        "question_text": "What challenge does the passage identify regarding solar power grid integration?",
                        "option_a": "Solar panels require specialised transmission cables",
                        "option_b": "High solar penetration can cause voltage fluctuations and stability issues",
                        "option_c": "Solar electricity cannot be transmitted over long distances",
                        "option_d": "Grid operators cannot predict solar output accurately enough",
                        "correct_answer": "B",
                    },
                ],
            },
            {
                "order": 3,
                "title": "Deforestation: Causes, Consequences, and Solutions",
                "text": (
                    "Forests cover approximately 31% of Earth's total land area, storing an "
                    "estimated 662 billion tonnes of carbon and harbouring more than 80% of "
                    "terrestrial species. Yet each year, an area roughly equivalent to the size "
                    "of Portugal is lost to deforestation. Since 1990, the world has lost "
                    "approximately 420 million hectares of forest — an area larger than the "
                    "European Union — and despite growing international attention, the pace of "
                    "forest loss has shown little sign of abating in the most vulnerable regions.\n\n"
                    "The drivers of deforestation are complex and interconnected. Agricultural "
                    "expansion — particularly for cattle ranching and soy production — is "
                    "responsible for the majority of tropical forest loss, especially in the "
                    "Amazon basin, which has lost nearly 20% of its original extent. Palm oil "
                    "cultivation has driven devastating deforestation across Southeast Asia, "
                    "particularly in Indonesia and Malaysia, where large areas of biodiverse "
                    "rainforest and carbon-rich peatlands have been cleared.\n\n"
                    "The consequences extend far beyond the loss of individual trees. Forests "
                    "regulate regional and global climate systems by absorbing carbon dioxide, "
                    "releasing water vapour that generates rainfall, and influencing surface "
                    "albedo. When large areas of the Amazon are deforested, the forest's capacity "
                    "to generate its own rainfall is diminished, pushing the ecosystem toward a "
                    "tipping point — sometimes called 'dieback' — at which large sections could "
                    "transition from rainforest to savanna in a self-reinforcing process. Some "
                    "researchers believe this threshold may be reached at a deforestation level "
                    "of 20–25% of the original forest extent.\n\n"
                    "Indigenous communities represent both the most affected and, arguably, the "
                    "most effective guardians of forest ecosystems. Research consistently shows "
                    "that forests legally controlled by indigenous peoples have significantly "
                    "lower deforestation rates than forests under other forms of management. In "
                    "the Brazilian Amazon, indigenous territories have deforestation rates an "
                    "estimated 11 times lower than surrounding areas. Securing and strengthening "
                    "indigenous land rights is therefore increasingly recognised as one of the "
                    "most cost-effective strategies for forest conservation.\n\n"
                    "International policy frameworks, including the REDD+ programme (Reducing "
                    "Emissions from Deforestation and Forest Degradation), seek to compensate "
                    "developing countries financially for preserving forests. However, progress "
                    "has been hampered by funding shortfalls, monitoring challenges, and "
                    "governance failures. More recently, corporate commitments to achieve "
                    "deforestation-free supply chains have gained momentum, driven by regulatory "
                    "pressure in major consumer markets."
                ),
                "questions": [
                    {
                        "question_text": "Approximately how much forest has the world lost since 1990?",
                        "option_a": "42 million hectares",
                        "option_b": "420 million hectares",
                        "option_c": "4,200 million hectares",
                        "option_d": "42,000 million hectares",
                        "correct_answer": "B",
                    },
                    {
                        "question_text": "What is the primary driver of tropical forest loss in the Amazon?",
                        "option_a": "Illegal logging for luxury timber",
                        "option_b": "Infrastructure expansion such as dams and roads",
                        "option_c": "Agricultural expansion, particularly cattle ranching and soy production",
                        "option_d": "Urban expansion and population growth",
                        "correct_answer": "C",
                    },
                    {
                        "question_text": "What does the concept of Amazon 'dieback' refer to?",
                        "option_a": "The death of individual tree species due to disease",
                        "option_b": "A process by which deforested areas transition from rainforest to savanna",
                        "option_c": "The reduction of biodiversity caused by hunting",
                        "option_d": "The decline of indigenous forest communities",
                        "correct_answer": "B",
                    },
                    {
                        "question_text": "How do deforestation rates in indigenous territories compare to surrounding areas in the Brazilian Amazon?",
                        "option_a": "They are roughly the same",
                        "option_b": "They are approximately 3 times lower",
                        "option_c": "They are approximately 11 times lower",
                        "option_d": "They are approximately 20 times lower",
                        "correct_answer": "C",
                    },
                    {
                        "question_text": "What does the REDD+ programme aim to do?",
                        "option_a": "Train local communities to replant deforested areas",
                        "option_b": "Compensate developing countries financially for preserving forests",
                        "option_c": "Impose trade sanctions on countries with high deforestation rates",
                        "option_d": "Fund scientific research into new reforestation techniques",
                        "correct_answer": "B",
                    },
                    {
                        "question_text": "Which of the following best describes recent corporate commitments regarding deforestation?",
                        "option_a": "Most companies have abandoned deforestation commitments due to cost",
                        "option_b": "Corporate commitments to deforestation-free supply chains have gained momentum",
                        "option_c": "Companies are increasing forest clearing to meet rising demand",
                        "option_d": "Corporate pledges have had no measurable impact on forest loss",
                        "correct_answer": "B",
                    },
                ],
            },
        ],
    },

    # ─────────────────────────────────────────────────────────────────────────
    # TEST 3 — Society and Behaviour
    # ─────────────────────────────────────────────────────────────────────────
    {
        "title": "Reading Test 3 — Society and Behaviour",
        "passages": [
            {
                "order": 1,
                "title": "The Science of Habit Formation",
                "text": (
                    "Habits govern a surprising proportion of human behaviour. Research by Duke "
                    "University psychologist Wendy Wood suggests that approximately 43% of daily "
                    "actions are performed habitually — not as the result of conscious deliberate "
                    "choice, but as automatic responses triggered by familiar cues in a given "
                    "environment. Understanding how habits form, persist, and can be changed has "
                    "become one of the most practically significant areas of psychology.\n\n"
                    "The neurological basis of habit formation is now well-established. When a "
                    "behaviour is repeated consistently in response to the same cue, neural "
                    "pathways in the brain are gradually strengthened through a process known as "
                    "long-term potentiation. Over time, the behaviour becomes encoded in the basal "
                    "ganglia — a region of the brain associated with procedural learning and "
                    "automatic behaviour — allowing it to be executed with minimal conscious "
                    "effort. This neural 'chunking' of behaviour is highly efficient: by automating "
                    "routine actions, the brain conserves cognitive resources for novel challenges.\n\n"
                    "MIT researcher Ann Graybiel identified what has become known as the 'habit "
                    "loop' — a three-component cycle consisting of a cue (the trigger that "
                    "initiates the behaviour), a routine (the behaviour itself), and a reward "
                    "(the positive reinforcement that encourages the brain to repeat the cycle). "
                    "This framework has been highly influential, informing both academic research "
                    "and popular accounts of behaviour change.\n\n"
                    "The formation of a new habit takes considerably longer than popular culture "
                    "suggests. Research by Phillippa Lally at University College London found "
                    "that it took participants an average of 66 days — not the frequently cited "
                    "21 days — for a new behaviour to reach automaticity. The time varied "
                    "significantly depending on the complexity of the behaviour and individual "
                    "differences, ranging from 18 to 254 days in the study's sample.\n\n"
                    "Breaking established habits presents its own set of challenges. Contrary to "
                    "what many people assume, old habits are not erased but rather suppressed — "
                    "the neural pathways that underlie them remain intact, making relapse "
                    "particularly likely under conditions of stress or fatigue when conscious "
                    "self-regulation is weakened. Effective strategies for habit change therefore "
                    "focus less on willpower and more on environmental design: modifying the "
                    "physical and social context to remove cues that trigger unwanted behaviours "
                    "and introduce cues that support desired ones."
                ),
                "questions": [
                    {
                        "question_text": "According to Duke University research, what percentage of daily actions are habitual?",
                        "option_a": "About 23%",
                        "option_b": "About 33%",
                        "option_c": "About 43%",
                        "option_d": "About 53%",
                        "correct_answer": "C",
                    },
                    {
                        "question_text": "Which part of the brain stores automatic habitual behaviours?",
                        "option_a": "The prefrontal cortex",
                        "option_b": "The basal ganglia",
                        "option_c": "The hippocampus",
                        "option_d": "The amygdala",
                        "correct_answer": "B",
                    },
                    {
                        "question_text": "What are the three components of the 'habit loop' identified by Ann Graybiel?",
                        "option_a": "Motivation, action, and satisfaction",
                        "option_b": "Cue, routine, and reward",
                        "option_c": "Trigger, response, and reinforcement",
                        "option_d": "Stimulus, behaviour, and consequence",
                        "correct_answer": "B",
                    },
                    {
                        "question_text": "According to Phillippa Lally's research, how long does it take on average for a new behaviour to become automatic?",
                        "option_a": "21 days",
                        "option_b": "30 days",
                        "option_c": "66 days",
                        "option_d": "100 days",
                        "correct_answer": "C",
                    },
                    {
                        "question_text": "What does the passage say happens to old habits when people try to break them?",
                        "option_a": "They are permanently erased from the brain",
                        "option_b": "They are replaced entirely by new habits",
                        "option_c": "They are suppressed but the neural pathways remain intact",
                        "option_d": "They gradually weaken through disuse",
                        "correct_answer": "C",
                    },
                    {
                        "question_text": "What approach does the passage suggest is more effective for habit change than willpower?",
                        "option_a": "Positive thinking and visualisation techniques",
                        "option_b": "Regular self-monitoring and journaling",
                        "option_c": "Environmental design to modify cues and context",
                        "option_d": "Reward systems and incentive programmes",
                        "correct_answer": "C",
                    },
                ],
            },
            {
                "order": 2,
                "title": "Social Media and Adolescent Mental Health",
                "text": (
                    "The relationship between social media use and adolescent mental health has "
                    "become one of the most debated topics in contemporary psychology. As rates "
                    "of anxiety, depression, and self-harm among teenagers have risen in many "
                    "Western countries since the early 2010s — a period that coincides with the "
                    "widespread adoption of smartphones and social media platforms — researchers, "
                    "parents, and policymakers have sought to understand whether a causal link "
                    "exists, and if so, how strong it is.\n\n"
                    "The evidence is more nuanced than much public discourse suggests. While "
                    "numerous studies have found associations between heavy social media use and "
                    "poorer mental health outcomes in adolescents, association does not equal "
                    "causation. A comprehensive review published in Nature Human Behaviour in 2019 "
                    "found that the association between social media use and well-being was 'about "
                    "as large as the effect of wearing glasses or eating potatoes' — statistically "
                    "present but practically minimal in the context of the many factors that "
                    "influence adolescent mental health.\n\n"
                    "However, critics argue that such analyses obscure important distinctions. "
                    "Not all social media use is equivalent: passive consumption of others' "
                    "carefully curated content is associated with higher levels of social "
                    "comparison and lower self-esteem, while active, interactive engagement such "
                    "as messaging friends appears more neutral or even positive. Research also "
                    "suggests that the effects are not uniform across all users: adolescent girls "
                    "appear consistently more vulnerable than boys to the negative effects of "
                    "social media, possibly due to differences in how social comparison and "
                    "appearance-related content affect self-image.\n\n"
                    "The mechanisms by which social media might harm mental health include social "
                    "comparison, sleep disruption caused by late-night device use, exposure to "
                    "cyberbullying, and displacement of face-to-face social interactions. Sleep "
                    "disruption is particularly concerning, as inadequate sleep is strongly "
                    "associated with depression, anxiety, and impaired academic performance.\n\n"
                    "The policy response has evolved rapidly. Several countries have introduced "
                    "or are considering legislation restricting social media access for minors. "
                    "Australia passed laws in 2024 banning social media platforms for children "
                    "under 16 — one of the most restrictive measures in the world. Critics of "
                    "such bans argue that they may push young people toward less regulated corners "
                    "of the internet and that parental supervision and digital literacy education "
                    "would be more effective approaches."
                ),
                "questions": [
                    {
                        "question_text": "What did a 2019 review in Nature Human Behaviour find about social media and adolescent well-being?",
                        "option_a": "The association was strong enough to confirm a causal relationship",
                        "option_b": "The association was statistically present but practically minimal",
                        "option_c": "No significant association was found in the research",
                        "option_d": "Social media was found to have primarily positive effects",
                        "correct_answer": "B",
                    },
                    {
                        "question_text": "What type of social media use is more negatively associated with mental health?",
                        "option_a": "Active engagement such as messaging friends",
                        "option_b": "Creating and sharing original content",
                        "option_c": "Passive consumption of others' curated content",
                        "option_d": "Following news and current affairs accounts",
                        "correct_answer": "C",
                    },
                    {
                        "question_text": "Which group of adolescents appears most vulnerable to the negative effects of social media?",
                        "option_a": "Boys in secondary school",
                        "option_b": "Children under the age of twelve",
                        "option_c": "Students with pre-existing mental health conditions",
                        "option_d": "Adolescent girls",
                        "correct_answer": "D",
                    },
                    {
                        "question_text": "Why is sleep disruption from social media use particularly concerning for adolescents?",
                        "option_a": "It reduces their physical activity levels",
                        "option_b": "It is strongly associated with depression, anxiety, and poor academic performance",
                        "option_c": "It permanently affects brain development",
                        "option_d": "It leads to increased aggression and behavioural problems",
                        "correct_answer": "B",
                    },
                    {
                        "question_text": "What policy did Australia introduce in 2024?",
                        "option_a": "A digital literacy curriculum for all secondary school students",
                        "option_b": "A requirement for parental consent for social media accounts",
                        "option_c": "A ban on social media platforms for children under 16",
                        "option_d": "Compulsory daily limits on social media use for minors",
                        "correct_answer": "C",
                    },
                    {
                        "question_text": "What argument do critics make against social media bans for minors?",
                        "option_a": "Bans are technologically impossible to enforce",
                        "option_b": "Young people may be pushed toward less regulated internet spaces",
                        "option_c": "Bans violate young people's right to freedom of expression",
                        "option_d": "Social media has no proven negative effects that justify a ban",
                        "correct_answer": "B",
                    },
                ],
            },
            {
                "order": 3,
                "title": "Urban Green Spaces and Human Wellbeing",
                "text": (
                    "As cities have grown denser and more sprawling, the provision of green space "
                    "— parks, gardens, street trees, and nature reserves — within urban "
                    "environments has become an increasingly important policy concern. A substantial "
                    "body of research now demonstrates that access to urban green spaces provides "
                    "measurable benefits across multiple dimensions of human health and wellbeing, "
                    "from reduced stress and improved mood to lower rates of cardiovascular disease "
                    "and increased life expectancy.\n\n"
                    "The psychological benefits of exposure to nature have been explored through "
                    "several theoretical frameworks. Attention Restoration Theory, developed by "
                    "psychologists Rachel and Stephen Kaplan, proposes that natural environments "
                    "restore directed attention — the focused, effortful concentration required "
                    "for work and problem-solving — by engaging the involuntary attention that "
                    "humans instinctively direct toward natural stimuli such as running water, "
                    "clouds, and vegetation. This restoration of cognitive resources is claimed "
                    "to improve mood, reduce mental fatigue, and enhance creative thinking.\n\n"
                    "Stress Reduction Theory, proposed by Roger Ulrich, holds that natural "
                    "environments trigger a rapid psychophysiological stress recovery response, "
                    "reducing cortisol levels, heart rate, and blood pressure within minutes of "
                    "exposure. This theory is supported by experimental evidence: studies in "
                    "which participants are shown video footage of natural versus urban "
                    "environments consistently demonstrate faster physiological recovery from "
                    "stress in those exposed to natural scenes.\n\n"
                    "The health benefits extend beyond psychological effects. Research across "
                    "multiple countries has found that residents who live closer to green spaces "
                    "have lower rates of obesity, type 2 diabetes, and cardiovascular disease. "
                    "A study of over 290,000 participants in the UK found that those with good "
                    "access to green space had a 16% lower risk of obesity. Physical activity "
                    "levels are one mediating factor, but the effects persist even after "
                    "controlling for physical activity, suggesting that other mechanisms — "
                    "including air quality, noise reduction, and the facilitation of social "
                    "interactions — also contribute.\n\n"
                    "Despite these well-documented benefits, access to urban green space is "
                    "profoundly unequal. In many cities, wealthier neighbourhoods enjoy more "
                    "green space per capita than lower-income areas. This 'green gap' can "
                    "exacerbate existing health inequalities, as those who may benefit most from "
                    "nature exposure often have the least access. Environmental justice advocates "
                    "argue that equitable distribution of green space should be a central "
                    "priority in urban planning."
                ),
                "questions": [
                    {
                        "question_text": "According to Attention Restoration Theory, why do natural environments benefit cognitive function?",
                        "option_a": "They reduce noise levels that distract from concentrated work",
                        "option_b": "They engage involuntary attention, allowing directed attention to recover",
                        "option_c": "They provide physical exercise that improves brain blood flow",
                        "option_d": "They create positive emotional states that enhance memory formation",
                        "correct_answer": "B",
                    },
                    {
                        "question_text": "What does Stress Reduction Theory propose about natural environments?",
                        "option_a": "Long-term exposure to nature permanently lowers baseline stress levels",
                        "option_b": "Nature triggers a rapid psychophysiological recovery from stress",
                        "option_c": "Natural environments are only beneficial if they contain water features",
                        "option_d": "Green spaces reduce stress primarily by encouraging social interaction",
                        "correct_answer": "B",
                    },
                    {
                        "question_text": "What did a UK study of over 290,000 participants find about green space and obesity?",
                        "option_a": "Green space access eliminated obesity risk entirely",
                        "option_b": "Those with good green space access had a 16% lower risk of obesity",
                        "option_c": "The effect on obesity was only significant for those who exercised regularly",
                        "option_d": "Green space access had no significant effect on obesity once diet was controlled for",
                        "correct_answer": "B",
                    },
                    {
                        "question_text": "What does the passage suggest about green space health benefits beyond physical activity?",
                        "option_a": "Physical activity is the only significant mechanism",
                        "option_b": "The benefits only appear in people who visit green spaces daily",
                        "option_c": "Other mechanisms such as air quality, noise reduction, and social facilitation also contribute",
                        "option_d": "The health benefits are primarily psychological rather than physical",
                        "correct_answer": "C",
                    },
                    {
                        "question_text": "What is the 'green gap' as described in the passage?",
                        "option_a": "The difference in green space quality between public parks and private gardens",
                        "option_b": "The unequal distribution of green space, with wealthier areas having more access",
                        "option_c": "The gap between the amount of green space needed and the amount available in cities",
                        "option_d": "The difference in biodiversity between urban and rural green spaces",
                        "correct_answer": "B",
                    },
                    {
                        "question_text": "What do environmental justice advocates argue regarding urban planning?",
                        "option_a": "Cities should prioritise green spaces over affordable housing",
                        "option_b": "Only national governments can address the green gap",
                        "option_c": "Equitable distribution of green space should be a central planning priority",
                        "option_d": "All urban residents should pay equal taxes to fund green space maintenance",
                        "correct_answer": "C",
                    },
                ],
            },
        ],
    },

    # ─────────────────────────────────────────────────────────────────────────
    # TEST 4 — Health and Medicine
    # ─────────────────────────────────────────────────────────────────────────
    {
        "title": "Reading Test 4 — Health and Medicine",
        "passages": [
            {
                "order": 1,
                "title": "The Science of Sleep",
                "text": (
                    "Sleep is a fundamental biological necessity, yet it remains among the least "
                    "understood aspects of human physiology. For most of recorded history, sleep "
                    "was regarded as a passive state — a mere absence of waking activity. The "
                    "discovery of rapid eye movement (REM) sleep in the 1950s by Nathaniel "
                    "Kleitman and Eugene Aserinsky transformed this view, revealing that the "
                    "sleeping brain is far from dormant. During REM sleep, neural activity is "
                    "comparable to waking levels, and this stage is now understood to be critical "
                    "for memory consolidation, emotional regulation, and cognitive performance.\n\n"
                    "Human sleep architecture follows a cyclical pattern. Each sleep cycle lasts "
                    "approximately 90 minutes and consists of several stages: lighter non-REM "
                    "(NREM) stages, followed by deep slow-wave sleep, and then a period of REM "
                    "sleep. Adults typically experience four to six complete cycles per night, "
                    "with the proportion of deep slow-wave sleep being highest in the early part "
                    "of the night and the proportion of REM sleep increasing toward morning.\n\n"
                    "The consequences of inadequate sleep are extensive and well-documented. Even "
                    "a single night of less than six hours of sleep impairs cognitive function in "
                    "ways comparable to legal intoxication. Chronic sleep deprivation — defined "
                    "as consistently sleeping less than seven to nine hours per night — is "
                    "associated with a significantly elevated risk of obesity, type 2 diabetes, "
                    "cardiovascular disease, and certain cancers. A landmark study published in "
                    "Science in 2013 revealed that during sleep, the brain's glymphatic system "
                    "activates, dramatically increasing the clearance of metabolic waste products "
                    "— including amyloid-beta, a protein associated with Alzheimer's disease — "
                    "from brain tissue.\n\n"
                    "Circadian rhythms — the approximately 24-hour biological cycles that govern "
                    "sleep-wake timing, body temperature, and hormone secretion — are regulated "
                    "by a master clock in the suprachiasmatic nucleus of the hypothalamus. These "
                    "rhythms are entrained primarily by light exposure, particularly in the blue "
                    "wavelength range (480 nm). The proliferation of blue-light-emitting screens "
                    "in the hours before bedtime has raised concerns among sleep researchers, as "
                    "evening light exposure suppresses the secretion of melatonin — the hormone "
                    "that signals the onset of biological night and promotes sleepiness.\n\n"
                    "Despite the robust scientific consensus on sleep's importance, modern "
                    "societies systematically undervalue it. Cultural attitudes that equate "
                    "minimal sleep with productivity and discipline remain pervasive in many "
                    "professional and educational environments. Shift work, which disrupts "
                    "circadian rhythms, affects a substantial proportion of the workforce in "
                    "industrialised countries and is associated with a range of adverse health "
                    "outcomes."
                ),
                "questions": [
                    {
                        "question_text": "What discovery in the 1950s transformed scientific understanding of sleep?",
                        "option_a": "The identification of melatonin as the sleep hormone",
                        "option_b": "The discovery of circadian rhythms regulated by the hypothalamus",
                        "option_c": "The discovery of rapid eye movement (REM) sleep by Kleitman and Aserinsky",
                        "option_d": "The identification of the glymphatic system's role in brain cleaning",
                        "correct_answer": "C",
                    },
                    {
                        "question_text": "How long does a typical adult sleep cycle last?",
                        "option_a": "Approximately 60 minutes",
                        "option_b": "Approximately 90 minutes",
                        "option_c": "Approximately 120 minutes",
                        "option_d": "Approximately 45 minutes",
                        "correct_answer": "B",
                    },
                    {
                        "question_text": "What was the key finding of the 2013 Science study mentioned in the passage?",
                        "option_a": "Sleeping fewer than six hours impairs cognitive function",
                        "option_b": "REM sleep is essential for emotional regulation",
                        "option_c": "The brain's glymphatic system clears metabolic waste including amyloid-beta during sleep",
                        "option_d": "Chronic sleep deprivation increases the risk of type 2 diabetes",
                        "correct_answer": "C",
                    },
                    {
                        "question_text": "Where in the brain is the master circadian clock located?",
                        "option_a": "The prefrontal cortex",
                        "option_b": "The hippocampus",
                        "option_c": "The suprachiasmatic nucleus of the hypothalamus",
                        "option_d": "The pineal gland",
                        "correct_answer": "C",
                    },
                    {
                        "question_text": "Why does evening blue-light exposure from screens concern sleep researchers?",
                        "option_a": "It overstimulates the visual cortex, making it harder to fall asleep",
                        "option_b": "It suppresses melatonin secretion, potentially delaying sleep onset",
                        "option_c": "It increases cortisol levels, raising alertness inappropriately",
                        "option_d": "It disrupts the circadian rhythm by resetting the sleep clock earlier",
                        "correct_answer": "B",
                    },
                    {
                        "question_text": "How does the passage characterise modern societies' attitude toward sleep?",
                        "option_a": "Most societies now recognise sleep as a public health priority",
                        "option_b": "Attitudes are gradually shifting toward valuing sleep more highly",
                        "option_c": "Modern societies systematically undervalue sleep, equating minimal sleep with productivity",
                        "option_d": "Only certain cultures have negative attitudes toward sufficient sleep",
                        "correct_answer": "C",
                    },
                ],
            },
            {
                "order": 2,
                "title": "The Rise of Telemedicine",
                "text": (
                    "Telemedicine — the delivery of healthcare services using telecommunications "
                    "technology — has existed in various forms since the 1960s, when NASA used "
                    "remote physiological monitoring systems to track the health of astronauts. "
                    "However, it remained a niche application for several decades, limited by "
                    "technological constraints and regulatory barriers. The COVID-19 pandemic "
                    "transformed this picture almost overnight: when physical contact between "
                    "patients and clinicians became a public health risk, healthcare systems "
                    "around the world pivoted rapidly to virtual consultations, and the volume "
                    "of telemedicine encounters increased by factors of ten to a hundred in some "
                    "specialties within just a few weeks.\n\n"
                    "This rapid expansion revealed both the enormous potential of telemedicine "
                    "and its significant limitations. On the positive side, telemedicine "
                    "dramatically expands access to specialist care for patients in rural and "
                    "remote areas, where specialist services may be hundreds of kilometres away. "
                    "A patient in a remote rural area can now consult a specialist based in a "
                    "major urban centre without the time, expense, and disruption of travel.\n\n"
                    "The effectiveness of telemedicine varies considerably by specialty and "
                    "condition. For dermatology, psychiatry, follow-up appointments for stable "
                    "chronic conditions, and the management of minor acute illnesses, evidence "
                    "suggests that telemedicine provides outcomes comparable to in-person care. "
                    "However, many conditions require physical examination, and telemedicine "
                    "cannot fully replicate the diagnostic capabilities of an in-person "
                    "consultation. A clinician cannot palpate an abdomen, auscultate a heart, "
                    "or assess a patient's gait through a video screen.\n\n"
                    "Equity concerns complicate the telemedicine picture. While telemedicine "
                    "has the potential to expand access, its benefits are most readily available "
                    "to those with reliable high-speed internet connections, digital literacy, "
                    "and suitable devices. Elderly patients, those in lower socioeconomic groups, "
                    "and residents of areas with poor digital infrastructure may be excluded "
                    "from or disadvantaged by the shift to virtual care.\n\n"
                    "Regulatory frameworks have struggled to keep pace with the technology. "
                    "Reimbursement policies for telemedicine services vary enormously between "
                    "and within countries, creating inconsistencies in what services are available "
                    "and who can access them. Licensing requirements that restrict clinicians to "
                    "providing care only within the jurisdictions where they are licensed create "
                    "barriers to cross-border telemedicine, potentially limiting its benefits "
                    "for patients in areas near administrative boundaries."
                ),
                "questions": [
                    {
                        "question_text": "When did telemedicine first begin, according to the passage?",
                        "option_a": "During the COVID-19 pandemic",
                        "option_b": "In the 1990s with the rise of the internet",
                        "option_c": "In the 1960s, with NASA monitoring astronaut health",
                        "option_d": "In the 1980s with early computer networks",
                        "correct_answer": "C",
                    },
                    {
                        "question_text": "By how much did telemedicine encounters increase in some specialties during COVID-19?",
                        "option_a": "Two to three times",
                        "option_b": "Five to seven times",
                        "option_c": "Ten to a hundred times",
                        "option_d": "More than a thousand times",
                        "correct_answer": "C",
                    },
                    {
                        "question_text": "For which conditions does the passage suggest telemedicine is most effective?",
                        "option_a": "Emergency medical situations requiring rapid intervention",
                        "option_b": "Complex surgical conditions requiring pre-operative assessment",
                        "option_c": "Dermatology, psychiatry, stable chronic condition follow-ups, and minor acute illnesses",
                        "option_d": "Intensive care monitoring of critically ill patients",
                        "correct_answer": "C",
                    },
                    {
                        "question_text": "What limitation does the passage identify for telemedicine's physical examination?",
                        "option_a": "Clinicians cannot prescribe medications through telemedicine",
                        "option_b": "Video quality is too poor for diagnostic purposes in most cases",
                        "option_c": "A clinician cannot palpate, auscultate, or assess physical symptoms through a screen",
                        "option_d": "Patients are less honest about symptoms in virtual consultations",
                        "correct_answer": "C",
                    },
                    {
                        "question_text": "Which groups does the passage identify as potentially disadvantaged by virtual care?",
                        "option_a": "Urban patients who prefer walking to nearby clinics",
                        "option_b": "Elderly patients, lower socioeconomic groups, and those with poor digital infrastructure",
                        "option_c": "Patients with chronic conditions who require frequent monitoring",
                        "option_d": "Healthcare workers who prefer in-person patient interaction",
                        "correct_answer": "B",
                    },
                    {
                        "question_text": "What regulatory barrier to cross-border telemedicine does the passage mention?",
                        "option_a": "Different countries have incompatible telecommunications standards",
                        "option_b": "International ethics codes prohibit remote cross-border consultations",
                        "option_c": "Licensing requirements restrict clinicians to providing care only within their licensed jurisdictions",
                        "option_d": "Data privacy laws prevent transfer of patient records across national borders",
                        "correct_answer": "C",
                    },
                ],
            },
            {
                "order": 3,
                "title": "Advances in Genetic Medicine",
                "text": (
                    "The completion of the Human Genome Project in 2003 — a thirteen-year "
                    "international effort to map the complete sequence of human DNA — marked a "
                    "watershed moment in biomedical science. Researchers anticipated that "
                    "identifying the approximately 20,000 to 25,000 genes in the human genome "
                    "would rapidly translate into a revolution in medicine, with genetic tests "
                    "enabling personalised prevention and treatment strategies. While this "
                    "revolution has been slower and more complex than initially anticipated, the "
                    "past decade has witnessed genuine and significant advances that are beginning "
                    "to reshape clinical medicine.\n\n"
                    "Genome-Wide Association Studies (GWAS) have identified thousands of genetic "
                    "variants associated with susceptibility to common diseases including diabetes, "
                    "heart disease, schizophrenia, and various cancers. These findings have "
                    "deepened scientific understanding of disease mechanisms and identified new "
                    "potential drug targets. Polygenic risk scores — which aggregate the effects "
                    "of thousands of genetic variants to estimate an individual's overall genetic "
                    "predisposition to a condition — are being evaluated for clinical use in "
                    "cardiovascular disease prevention and cancer screening programmes.\n\n"
                    "The development of CRISPR-Cas9 gene editing technology, first described in "
                    "its application to human cells in 2012, has opened new possibilities for "
                    "treating genetic diseases. CRISPR acts as a form of molecular scissors, "
                    "allowing scientists to cut, modify, or replace specific sequences of DNA "
                    "with unprecedented precision. In 2023, the first CRISPR-based therapy — "
                    "Casgevy, developed to treat sickle cell disease and beta thalassaemia — "
                    "received regulatory approval in the United Kingdom and United States, "
                    "marking a milestone in the translation of gene editing from laboratory to "
                    "clinic.\n\n"
                    "Pharmacogenomics — the study of how genetic variation influences individual "
                    "responses to drugs — offers another avenue for personalising medicine. It "
                    "is now understood that genetic variants affecting drug-metabolising enzymes "
                    "can cause the same medication to be highly effective in some patients, toxic "
                    "in others, and entirely ineffective in yet others. Some regulators now "
                    "require pharmacogenomic testing before prescribing certain drugs.\n\n"
                    "Ethical questions accompany these scientific advances. The prospect of "
                    "germline editing — modifications to the DNA of embryos or reproductive cells "
                    "that would be heritable by future generations — raises profound concerns "
                    "about unintended consequences and informed consent, as future generations "
                    "cannot consent to modifications made before their birth. The birth of "
                    "gene-edited babies in China in 2018, announced by scientist He Jiankui, "
                    "provoked international condemnation and highlighted the need for robust "
                    "governance frameworks."
                ),
                "questions": [
                    {
                        "question_text": "When was the Human Genome Project completed?",
                        "option_a": "1990",
                        "option_b": "1997",
                        "option_c": "2003",
                        "option_d": "2010",
                        "correct_answer": "C",
                    },
                    {
                        "question_text": "What are polygenic risk scores designed to estimate?",
                        "option_a": "The likelihood of inheriting a single gene mutation from a parent",
                        "option_b": "An individual's overall genetic predisposition to a condition based on many variants",
                        "option_c": "The effectiveness of a specific drug based on genetic makeup",
                        "option_d": "The number of genes a person carries that are linked to disease",
                        "correct_answer": "B",
                    },
                    {
                        "question_text": "What was significant about Casgevy, approved in 2023?",
                        "option_a": "It was the first drug developed using genome sequencing data",
                        "option_b": "It was the first treatment for COVID-19 using genetic technology",
                        "option_c": "It was the first CRISPR-based therapy approved to treat genetic diseases",
                        "option_d": "It was the first personalised cancer treatment approved globally",
                        "correct_answer": "C",
                    },
                    {
                        "question_text": "What does pharmacogenomics study?",
                        "option_a": "How environmental factors interact with genetic predispositions",
                        "option_b": "How genetic variation influences individual responses to drugs",
                        "option_c": "The genetic basis of drug addiction and substance dependence",
                        "option_d": "How to use genetic information to develop new pharmaceutical compounds",
                        "correct_answer": "B",
                    },
                    {
                        "question_text": "What is 'germline editing' and why does it raise ethical concerns?",
                        "option_a": "Editing bacteria in the human gut; concerns relate to disrupting microbiome balance",
                        "option_b": "Editing cancer cells; concerns relate to the risk of spreading edited cells",
                        "option_c": "Modifying embryo or reproductive cell DNA that would be heritable by future generations",
                        "option_d": "Editing somatic cells; concerns relate to immune system rejection",
                        "correct_answer": "C",
                    },
                    {
                        "question_text": "What international reaction followed He Jiankui's announcement of gene-edited babies in 2018?",
                        "option_a": "Widespread scientific acclaim for the technical achievement",
                        "option_b": "International condemnation and calls for better governance frameworks",
                        "option_c": "Immediate replication of the technique in other countries",
                        "option_d": "Government funding for further research into germline editing",
                        "correct_answer": "B",
                    },
                ],
            },
        ],
    },
]
