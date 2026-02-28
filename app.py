"""
TEACHER PEHPEH - AI-Powered Support for Every Classroom
Institute of Basic Technology (IBT)
Built by Rodney L. Bollie, PhD
"""
import streamlit as st
import time, os, base64, json, random, zlib

# === API KEYS ===
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "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")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "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")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "gen-lang-client-0632330468")
LOGO_FILENAME = "logo.png"

try:
    import openai; OAI = True
except ImportError: OAI = False
try:
    import anthropic; ANT = True
except ImportError: ANT = False
try:
    import google.generativeai as genai; GEM = True
except ImportError: GEM = False

# === IBT COLORS (from website) ===
C_NAVY = "#0F2247"
C_NAVY_L = "#1A2744"
C_BLUE = "#2B7DE9"
C_BLUE_D = "#1D5CBF"
C_RED = "#8B1A1A"
C_RED_L = "#B22234"
C_GOLD = "#D4A843"
C_GOLD_L = "#F5D98E"

# === KNOWLEDGE BASE (assembled at runtime only) ===
@st.cache_data
def _kb():
    return ("IBT RESEARCH (183 students, 6 Liberian schools, 4 STEM subjects):\n"
        "Overall avg 0.433(C-). Chem 0.494(C), Physics 0.399(C-), Math 0.391(C-), Bio 0.447(C). "
        "Scale: 1.0=A,0.75=B+,0.625=B,0.50=B-,0.44=C,0.375=C-,0.25=D.\n"
        "MOTHER'S EDUCATION: Mom HS Grad avg 0.449 vs No HS 0.418 (p=0.031). Physics gap: HS 0.438 vs NoHS 0.363 (p=0.0075). Significant across ALL subgroups.\n"
        "SINGLE MOTHERS (22%): SM HS 0.457 vs SM NoHS 0.399 (14.7% gap). Physics: 0.461 vs 0.310=48.8% gap (p=0.006). SM+NoHS+4kids: Physics 0.283(D). 29% work after school.\n"
        "DIGITAL: 58.5% never used computer. SM NoHS: 81% never. 100% of SM NoHS users study only. +0.041 boost.\n"
        "SCHOOL: #1 predictor (F=8.60 p<0.001). Best 0.512(B-), worst 0.354(D+). 16x parent edu effect.\n"
        "INTERVENTION: Gap widens +0.055/2yr without. Narrows to 0.024 with. Physics most sensitive +0.09/yr.")

# === CONNECTIVITY ===
def check_conn():
    import urllib.request
    r = {"online":False,"quality":"none","latency_ms":None,"label":"No Internet","emoji":"🔴"}
    lats = []
    for u in ["https://api.anthropic.com","https://api.openai.com","https://www.google.com"]:
        try:
            t=time.time(); req=urllib.request.Request(u,method="HEAD"); req.add_header("User-Agent","TP/1.0")
            urllib.request.urlopen(req,timeout=5); lats.append((time.time()-t)*1000)
        except: pass
    if not lats: return r
    a=sum(lats)/len(lats); r.update(online=True,latency_ms=round(a))
    if a<300: r.update(quality="high",label="Strong (WiFi/5G)",emoji="🟢")
    elif a<800: r.update(quality="medium",label="Moderate (4G/3G)",emoji="🟡")
    elif a<2000: r.update(quality="low",label="Slow (2G/Edge)",emoji="🟠")
    else: r.update(quality="very_low",label="Very Slow",emoji="🟠")
    return r

# === IMAGE GENERATION ===
def gen_image(prompt):
    if not OAI or not OPENAI_API_KEY: return None
    try:
        c=openai.OpenAI(api_key=OPENAI_API_KEY)
        r=c.images.generate(model="dall-e-3",prompt=f"Educational illustration for African classroom: {prompt}. Clear, colorful, culturally relevant to West Africa/Liberia.",size="1024x1024",quality="standard",n=1)
        return r.data[0].url
    except: return None

# === QUIZ BANK ===
QUIZ = {
 "Mathematics":{"easy":[
  {"q":"Simplify: 3(2x - 4) + 5x","o":["11x - 12","11x - 4","6x - 12","x - 12"],"a":0,"e":"Expand: 6x - 12 + 5x = 11x - 12.","t":"WASSCE Paper 1 style. Teach: distribute first, then collect like terms. Write each step clearly."},
  {"q":"If log₁₀ 2 = 0.301, find log₁₀ 8.","o":["0.903","2.408","0.602","0.301"],"a":0,"e":"8 = 2³, so log 8 = 3 × log 2 = 3 × 0.301 = 0.903.","t":"WASSCE loves log questions. Teach index form first: 8=2³. Then the log law: log(aⁿ) = n log a."},
  {"q":"Solve: 2x² - 5x - 3 = 0","o":["x = 3 or -½","x = 3 or ½","x = -3 or ½","x = -3 or -½"],"a":0,"e":"Factor: (2x + 1)(x - 3) = 0. So x = -½ or x = 3.","t":"WASSCE always has quadratics. Teach factoring AND formula method. Students should check by substituting back."},
  {"q":"Find the gradient of the line 3y = 6x - 9.","o":["2","-3","6","3"],"a":0,"e":"Rearrange to y = mx + c: y = 2x - 3. Gradient m = 2.","t":"Standard WASSCE. Always rearrange to y = mx + c form first. Gradient = coefficient of x."},
  {"q":"The 5th term of an AP is 17, common difference is 3. Find the first term.","o":["5","8","2","14"],"a":0,"e":"aₙ = a + (n-1)d → 17 = a + 4(3) → a = 17 - 12 = 5.","t":"AP formula appears every year. Drill: a, a+d, a+2d... Students write out terms to verify."},
 ],"medium":[
  {"q":"If P = {1,2,3,4,5} and Q = {3,4,5,6,7}, find n(P ∪ Q).","o":["7","10","5","3"],"a":0,"e":"P ∪ Q = {1,2,3,4,5,6,7}. Count = 7.","t":"Venn diagram on board. Students place each element. WASSCE tests union, intersection, complement."},
  {"q":"In triangle ABC, a=7, b=8, C=60°. Find c using cosine rule.","o":["√57","√113","7.55","8.06"],"a":0,"e":"c² = 7² + 8² - 2(7)(8)cos60° = 49 + 64 - 56 = 57. c = √57.","t":"Cosine rule is a WASSCE favourite. Students must memorize: c² = a² + b² - 2ab·cosC."},
  {"q":"Differentiate y = 3x⁴ - 2x² + 5x - 1.","o":["12x³ - 4x + 5","12x³ - 4x + 5x","3x³ - 2x + 5","12x⁴ - 4x²"],"a":0,"e":"dy/dx = 12x³ - 4x + 5. Rule: bring power down, reduce by 1. Constants vanish.","t":"Differentiation appears in WASSCE Paper 2. Drill the power rule until it's automatic. Use mnemonic: 'Multiply by power, subtract one.'"},
  {"q":"A fair die is thrown twice. P(sum = 7)?","o":["1/6","1/12","5/36","7/36"],"a":0,"e":"Outcomes summing to 7: (1,6)(2,5)(3,4)(4,3)(5,2)(6,1) = 6 out of 36. P = 6/36 = 1/6.","t":"Draw the 6×6 grid. Students count all sums. Probability questions need systematic listing."},
  {"q":"Convert 101101₂ to base 10.","o":["45","37","53","29"],"a":0,"e":"1(32) + 0(16) + 1(8) + 1(4) + 0(2) + 1(1) = 32+8+4+1 = 45.","t":"Number bases: WASSCE staple. Write place values (32,16,8,4,2,1) above the digits. Multiply and add."},
 ],"hard":[
  {"q":"Evaluate ∫(3x² + 2x - 1)dx from 0 to 2.","o":["10","8","12","14"],"a":0,"e":"[x³ + x² - x] from 0 to 2 = (8+4-2) - 0 = 10.","t":"Integration: reverse of differentiation. Add 1 to power, divide by new power. Then substitute limits."},
  {"q":"The 3rd and 6th terms of a GP are 18 and 486. Find the common ratio.","o":["3","9","6","2"],"a":0,"e":"ar² = 18, ar⁵ = 486. Divide: r³ = 27, r = 3.","t":"GP: divide consecutive term equations to eliminate 'a'. This technique appears in WASSCE Theory."},
  {"q":"Two fair coins and a die are tossed. P(2 heads and even number)?","o":["1/4","1/8","1/12","1/6"],"a":0,"e":"P(2 heads) = ¼. P(even) = ½. Independent: ¼ × ½ = ⅛.","t":"Compound probability: independent events multiply. Tree diagrams help visual learners."},
 ]},
 "Physics":{"easy":[
  {"q":"A car accelerates from 10 m/s to 30 m/s in 5s. Acceleration?","o":["4 m/s²","6 m/s²","8 m/s²","2 m/s²"],"a":0,"e":"a = (v-u)/t = (30-10)/5 = 20/5 = 4 m/s².","t":"WASSCE kinematics: always identify u, v, a, s, t first. Write them down before calculating."},
  {"q":"A 2kg mass falls from 10m height. What is its PE at the top? (g=10)","o":["200 J","20 J","100 J","2000 J"],"a":0,"e":"PE = mgh = 2 × 10 × 10 = 200 J.","t":"Energy conservation is key WASSCE topic. PE at top converts to KE at bottom. Ask: where does energy go?"},
  {"q":"Resistance of two 6Ω resistors in parallel?","o":["3 Ω","12 Ω","6 Ω","9 Ω"],"a":0,"e":"1/R = 1/6 + 1/6 = 2/6. R = 3 Ω.","t":"Parallel: 'product over sum' shortcut for two resistors: (6×6)/(6+6) = 36/12 = 3Ω."},
  {"q":"A wave has frequency 50 Hz and wavelength 4m. Speed?","o":["200 m/s","12.5 m/s","54 m/s","46 m/s"],"a":0,"e":"v = fλ = 50 × 4 = 200 m/s.","t":"v = fλ is the wave equation. WASSCE applies it to sound, light, and water waves. Students must know it cold."},
  {"q":"An object on a spring has period 0.5s. Frequency?","o":["2 Hz","0.5 Hz","5 Hz","0.2 Hz"],"a":0,"e":"f = 1/T = 1/0.5 = 2 Hz.","t":"Period and frequency are inverses. This is basic but students often confuse them on WASSCE."},
 ],"medium":[
  {"q":"A 5kg block is pushed with 30N on a frictionless surface. Acceleration?","o":["6 m/s²","150 m/s²","25 m/s²","35 m/s²"],"a":0,"e":"F = ma → a = F/m = 30/5 = 6 m/s².","t":"Newton's 2nd Law: WASSCE asks both calculation and conceptual understanding. What if friction = 10N?"},
  {"q":"A ray enters glass (n=1.5) at 30° to the normal. Angle of refraction?","o":["19.5°","45°","20°","30°"],"a":0,"e":"Snell's law: sin30°/sinr = 1.5 → sinr = 0.5/1.5 = 0.333 → r ≈ 19.5°.","t":"Snell's law is examined every WASSCE. Students must use sine tables or know key sin values."},
  {"q":"EMF of cell = 12V, internal resistance = 2Ω, external R = 4Ω. Current?","o":["2 A","3 A","6 A","4 A"],"a":0,"e":"I = EMF/(R+r) = 12/(4+2) = 2 A.","t":"Internal resistance: WASSCE Theory favourite. Draw the circuit. EMF = V + Ir. Students confuse EMF with terminal p.d."},
  {"q":"Half-life of a substance is 4 days. After 12 days, what fraction remains?","o":["1/8","1/4","1/16","1/6"],"a":0,"e":"12 days = 3 half-lives. Fraction = (½)³ = 1/8.","t":"Half-life: count how many half-lives fit. Each one halves the amount. WASSCE asks both fraction and mass."},
 ],"hard":[
  {"q":"A projectile is launched at 30 m/s at 60° to horizontal. Max height? (g=10)","o":["33.75 m","45 m","22.5 m","15 m"],"a":0,"e":"Vy = 30sin60° = 25.98. H = Vy²/2g = 675/20 = 33.75 m.","t":"Projectile: resolve into components. Vertical determines height, horizontal determines range. WASSCE Paper 2 staple."},
  {"q":"A transformer has 200 primary turns, 50 secondary turns, input 240V. Output voltage?","o":["60 V","960 V","48 V","12 V"],"a":0,"e":"Vs/Vp = Ns/Np → Vs = 240 × 50/200 = 60 V. Step-down transformer.","t":"Transformer equation: Vs/Vp = Ns/Np = Ip/Is. WASSCE tests both step-up and step-down."},
  {"q":"A 0.5kg ball moving at 4 m/s hits a wall and bounces back at 3 m/s. Impulse?","o":["3.5 Ns","0.5 Ns","7 Ns","1.5 Ns"],"a":0,"e":"Impulse = m(v-u) = 0.5(3-(-4)) = 0.5 × 7 = 3.5 Ns. (Direction change: -4 becomes +3.)","t":"Impulse = change in momentum. KEY: when direction reverses, ADD the speeds. Common WASSCE trap."},
 ]},
 "Biology":{"easy":[
  {"q":"Which organelle is the site of aerobic respiration?","o":["Mitochondria","Ribosome","Nucleus","Golgi body"],"a":0,"e":"Mitochondria: the 'powerhouse' where glucose + O₂ → CO₂ + H₂O + ATP.","t":"WASSCE cell biology: students must name organelle AND function. Use the 'factory analogy' — each organelle has a job."},
  {"q":"In humans, the diploid number is 46. How many chromosomes in a gamete?","o":["23","46","92","12"],"a":0,"e":"Gametes are haploid (n). 46/2 = 23 chromosomes.","t":"Meiosis halves the chromosome number. WASSCE tests: diploid vs haploid, mitosis vs meiosis differences."},
  {"q":"Which blood vessel carries oxygenated blood FROM the heart to the body?","o":["Aorta","Pulmonary artery","Vena cava","Pulmonary vein"],"a":0,"e":"The aorta carries oxygenated blood from the left ventricle to the body.","t":"Blood vessel quiz is WASSCE standard. Trick: pulmonary artery carries DE-oxygenated blood (only exception)."},
  {"q":"Sickle cell trait (HbAS) provides resistance to which disease?","o":["Malaria","Typhoid","Cholera","HIV"],"a":0,"e":"HbAS heterozygotes have partial protection against Plasmodium falciparum malaria.","t":"Sickle cell and malaria: a key WASSCE genetics topic. Discuss why the gene persists in malaria-endemic West Africa."},
  {"q":"Which hormone controls blood sugar level?","o":["Insulin","Adrenaline","Thyroxine","Oestrogen"],"a":0,"e":"Insulin (from pancreas) lowers blood glucose by promoting uptake into cells.","t":"Endocrine system: WASSCE asks hormone name, gland, and function. Make a table: gland → hormone → effect."},
 ],"medium":[
  {"q":"In a cross between Tt × Tt, what fraction of offspring are tall (T dominant)?","o":["3/4","1/4","1/2","1"],"a":0,"e":"TT:Tt:tt = 1:2:1. Tall (TT+Tt) = 3/4.","t":"Punnett square every time. WASSCE asks ratios AND probabilities. Practice with different crosses."},
  {"q":"Which nitrogenous base is found in RNA but NOT DNA?","o":["Uracil","Thymine","Adenine","Cytosine"],"a":0,"e":"RNA has Uracil instead of Thymine. Both have A, G, C.","t":"DNA vs RNA: sugar, bases, structure. Mnemonic for RNA bases: 'GACU' sounds like 'gecko.'"},
  {"q":"Oxygen debt occurs after vigorous exercise because:","o":["Lactic acid must be broken down","Glucose runs out","Lungs stop working","Blood pressure drops"],"a":0,"e":"During intense exercise, anaerobic respiration produces lactic acid. Extra O₂ is needed to oxidize it.","t":"Link to students' experience: why do you breathe hard AFTER stopping running? Oxygen debt!"},
  {"q":"Which structure prevents food from entering the windpipe?","o":["Epiglottis","Larynx","Pharynx","Uvula"],"a":0,"e":"The epiglottis closes over the trachea during swallowing.","t":"Digestion system: WASSCE tests the pathway. Students act out swallowing — what moves, what closes?"},
 ],"hard":[
  {"q":"In ecological succession, the first organisms to colonize bare rock are:","o":["Lichens","Grasses","Trees","Ferns"],"a":0,"e":"Lichens are pioneer species — they break down rock into soil, enabling other plants to grow.","t":"Succession: pioneer → grass → shrub → tree. WASSCE Theory asks for full description of stages."},
  {"q":"A man with blood group AB marries a woman with group O. Possible children?","o":["A and B only","AB only","O only","A, B, AB, and O"],"a":0,"e":"Father: IᴬIᴮ × Mother: ii → children are Iᴬi (A) or Iᴮi (B). No AB, no O.","t":"Blood group genetics: multiple alleles + codominance. WASSCE loves this. Always write the genotypes first."},
  {"q":"Which process releases CO₂ back into the atmosphere in the carbon cycle?","o":["Respiration and combustion","Photosynthesis","Nitrogen fixation","Transpiration"],"a":0,"e":"Respiration (by all living things) and combustion (burning fuels) release CO₂.","t":"Carbon cycle: WASSCE asks arrows and processes. Draw the cycle on board with students labeling each arrow."},
 ]},
 "Chemistry":{"easy":[
  {"q":"What is the oxidation state of Mn in KMnO₄?","o":["+7","+4","+2","+6"],"a":0,"e":"K(+1) + Mn(x) + 4O(-2) = 0 → 1 + x - 8 = 0 → x = +7.","t":"Oxidation states: WASSCE standard. Rules: O is -2, alkali metals +1. Solve for the unknown."},
  {"q":"Which gas is collected over water in the lab?","o":["Oxygen","HCl","NH₃","SO₂"],"a":0,"e":"O₂ is insoluble in water, so it's collected by downward displacement of water.","t":"Gas collection methods depend on solubility and density. WASSCE tests all three methods."},
  {"q":"The IUPAC name of CH₃CH₂OH is:","o":["Ethanol","Methanol","Propanol","Ethanal"],"a":0,"e":"2 carbons = eth-. -OH group = -anol. Ethanol.","t":"IUPAC naming: count carbons, identify functional group. WASSCE organic chemistry requires this."},
  {"q":"How many moles are in 44g of CO₂? (C=12, O=16)","o":["1","2","0.5","44"],"a":0,"e":"Molar mass of CO₂ = 12 + 32 = 44 g/mol. Moles = 44/44 = 1.","t":"Mole calculations appear every WASSCE. Formula: n = mass/molar mass. Practice with different substances."},
  {"q":"Which of these is an alkali?","o":["NaOH","HCl","NaCl","H₂SO₄"],"a":0,"e":"NaOH (sodium hydroxide) is a strong alkali/base. It produces OH⁻ in solution.","t":"Acids produce H⁺, alkalis produce OH⁻. WASSCE tests indicators, neutralization, and salt formation."},
 ],"medium":[
  {"q":"What volume of H₂ at STP is produced when 2 moles of Zn react with excess HCl?","o":["44.8 L","22.4 L","11.2 L","67.2 L"],"a":0,"e":"Zn + 2HCl → ZnCl₂ + H₂. 1 mol Zn gives 1 mol H₂. 2 mol Zn → 2 mol H₂ = 2 × 22.4 = 44.8 L.","t":"Stoichiometry + molar volume (22.4L at STP). Write balanced equation first. WASSCE Paper 2 calculation."},
  {"q":"Which type of reaction is: CuO + H₂SO₄ → CuSO₄ + H₂O?","o":["Neutralization","Decomposition","Displacement","Combustion"],"a":0,"e":"Base (CuO) + Acid (H₂SO₄) → Salt + Water = Neutralization.","t":"Reaction types: WASSCE tests naming AND identifying from equations. Make a chart of types with examples."},
  {"q":"In electrolysis of brine, what is produced at the cathode?","o":["Hydrogen","Chlorine","Sodium","Oxygen"],"a":0,"e":"At cathode (negative), H⁺ ions are reduced: 2H⁺ + 2e⁻ → H₂.","t":"Electrolysis: cathode = reduction (CATions go to CAThode). WASSCE tests products at each electrode."},
  {"q":"An element has electronic configuration 2,8,7. Its likely ion is:","o":["X⁻","X⁷⁺","X⁺","X²⁻"],"a":0,"e":"7 outer electrons — needs 1 more for stable octet. Gains 1 electron → X⁻ (like chlorine).","t":"Electronic configuration → group → valency → ion charge. This chain of reasoning is WASSCE standard."},
 ],"hard":[
  {"q":"Calculate the enthalpy change: C + O₂ → CO₂, given C + ½O₂ → CO (ΔH=-110kJ) and CO + ½O₂ → CO₂ (ΔH=-283kJ).","o":["-393 kJ","-173 kJ","+393 kJ","-110 kJ"],"a":0,"e":"Hess's Law: add the two equations. ΔH = -110 + (-283) = -393 kJ.","t":"Hess's Law: WASSCE Theory. Energy is a state function — path doesn't matter. Add equations like algebra."},
  {"q":"0.1M NaOH is titrated against 0.05M H₂SO₄. What volume of acid neutralizes 25ml of NaOH?","o":["25 ml","50 ml","12.5 ml","100 ml"],"a":0,"e":"2NaOH + H₂SO₄. Moles NaOH = 0.1×25 = 2.5mmol. Moles acid = 2.5/2 = 1.25mmol. Vol = 1.25/0.05 = 25ml.","t":"Titration: write balanced equation, find mole ratio, use C₁V₁/n₁ = C₂V₂/n₂. WASSCE practical and theory."},
  {"q":"Which compound shows geometric (cis-trans) isomerism?","o":["But-2-ene","Ethene","Propane","Ethanol"],"a":0,"e":"But-2-ene: C=C with different groups on each carbon allows cis/trans forms.","t":"Isomerism: structural vs geometric vs optical. WASSCE asks students to draw both forms. C=C restricts rotation."},
 ]},
 "Reading Comprehension":{"easy":[
  {"q":"'The government's education budget was slashed by 30%, leading to school closures across rural communities.' — What caused the school closures?","o":["Budget cuts","Natural disaster","Teacher strike","Student protests"],"a":0,"e":"The passage states the budget was 'slashed by 30%' which led to closures.","t":"WASSCE comprehension: identify cause and effect. Teach students to look for linking words: 'leading to', 'because', 'therefore'."},
  {"q":"'Despite the drought, the farmers of Bong County managed to harvest enough rice to sustain their families through the dry season.' — What is the tone?","o":["Resilient / hopeful","Angry","Sad","Humorous"],"a":0,"e":"'Despite' shows challenge overcome. 'Managed to' shows resilience. Tone is hopeful.","t":"Tone questions: look at word choice. 'Despite' + 'managed' = overcoming. WASSCE tests tone, mood, attitude."},
  {"q":"'Deforestation in the tropics has accelerated at an alarming rate.' — What does 'accelerated' mean here?","o":["Increased in speed","Slowed down","Stopped completely","Remained constant"],"a":0,"e":"'Accelerated' means sped up / increased. 'Alarming rate' confirms it's getting worse.","t":"Vocabulary in context: WASSCE gives unfamiliar words. Teach: look at surrounding words for clues. 'Alarming' = bad = getting worse."},
 ],"medium":[
  {"q":"'The author argues that technology alone cannot solve Africa's education crisis; rather, it must be coupled with trained teachers and culturally relevant curricula.' — What is the author's main argument?","o":["Technology needs teachers and relevant curricula to work","Technology is useless","Africa doesn't need technology","Curricula are already good"],"a":0,"e":"Key phrase: 'cannot solve alone... must be coupled with.' Author wants technology PLUS human/cultural elements.","t":"Argumentative comprehension: find the claim AND the qualifier. WASSCE asks 'What is the writer's view?' Look for 'rather', 'however', 'must'."},
  {"q":"'She was the proverbial candle burning at both ends — teaching by day, farming by evening, and studying by lamplight.' — What figure of speech?","o":["Metaphor","Simile","Personification","Hyperbole"],"a":0,"e":"'Was the candle' (not 'like a candle') = metaphor. Describes exhausting double life.","t":"Simile uses 'like/as'. Metaphor says IS. WASSCE English Paper 1 tests these. Students collect examples from their own speech."},
 ],"hard":[
  {"q":"Read: 'The policy, while well-intentioned, failed to account for the socioeconomic realities of the communities it aimed to serve.' — The author's attitude is:","o":["Critically sympathetic","Fully supportive","Hostile","Indifferent"],"a":0,"e":"'Well-intentioned' = sympathetic. 'Failed to account' = critical. Both together = critically sympathetic.","t":"Advanced comprehension: authors can hold MIXED views. WASSCE rewards nuanced answers over simple ones."},
  {"q":"'The minister's assertion that unemployment had decreased was contradicted by data showing a 15% rise in joblessness among youth.' — This is an example of:","o":["Irony","Metaphor","Alliteration","Flashback"],"a":0,"e":"The minister's claim is the OPPOSITE of reality — this is verbal/situational irony.","t":"WASSCE literary devices: irony = opposite of what's expected/stated. Teach with local examples: 'The fire station burned down.'"},
 ]},
}

PRAISE = ["🌶️ Excellent! Teacher Pehpeh is proud!","🌶️ You're on FIRE!","🌶️ That's the pepper spirit!","🌶️ Outstanding! Getting stronger!","🌶️ Sharp like pepper!","🌶️ Brilliant! Hard work pays off!","🌶️ You nailed it!","🌶️ The village would be proud!"]
ENCOURAGE = ["🌶️ Not quite — every mistake teaches!","🌶️ Close! Read explanation, try next one!","🌶️ Even the tallest palm started as seed. Keep growing!","🌶️ No worry! Let's learn together."]

WASSCE_TIPS = """📝 WASSCE EXAM STRATEGY:\n\n1. ANSWER SHEET: HB pencil only. Shade completely. Erase cleanly. Check numbers match.\n2. ELIMINATION: Read ALL options. Cross out wrong ones. 'Always'/'never' usually wrong.\n3. TIME: Paper 1: ~1 min/question. Paper 2: start easiest. Leave 10 min to check.\n4. NIGHT BEFORE: Review only. Eat well, sleep early. Rested brain > tired cramming."""

# === DROPDOWNS ===
REGIONS={"Urban":"urban","Peri-Urban":"peri-urban","Rural":"rural","Remote / Island":"remote"}
# Sub-Saharan African countries only
COUNTRIES=["Liberia","Sierra Leone","Ghana","Nigeria","Kenya","Uganda","Tanzania","Ethiopia","Senegal","Cameroon","Gambia","Guinea","Côte d'Ivoire","Mali","Burkina Faso","Rwanda","Malawi","Zambia","Zimbabwe","Mozambique","South Africa","Botswana","Namibia","DRC","Angola","Togo","Benin","Niger","Chad","Somalia","Eritrea","Djibouti","South Sudan","Sudan","Central African Republic","Republic of Congo","Gabon","Equatorial Guinea","São Tomé and Príncipe","Cape Verde","Comoros","Madagascar","Mauritius","Seychelles","Eswatini","Lesotho","Burundi","Guinea-Bissau"]
FLAGS={"Liberia":"🇱🇷","Sierra Leone":"🇸🇱","Ghana":"🇬🇭","Nigeria":"🇳🇬","Kenya":"🇰🇪","Uganda":"🇺🇬","Tanzania":"🇹🇿","Ethiopia":"🇪🇹","Senegal":"🇸🇳","Cameroon":"🇨🇲","Gambia":"🇬🇲","Guinea":"🇬🇳","Côte d'Ivoire":"🇨🇮","Mali":"🇲🇱","Burkina Faso":"🇧🇫","Rwanda":"🇷🇼","Malawi":"🇲🇼","Zambia":"🇿🇲","Zimbabwe":"🇿🇼","Mozambique":"🇲🇿","South Africa":"🇿🇦","Botswana":"🇧🇼","Namibia":"🇳🇦","DRC":"🇨🇩","Angola":"🇦🇴","Togo":"🇹🇬","Benin":"🇧🇯","Niger":"🇳🇪","Chad":"🇹🇩","Somalia":"🇸🇴","Eritrea":"🇪🇷","Djibouti":"🇩🇯","South Sudan":"🇸🇸","Sudan":"🇸🇩","Central African Republic":"🇨🇫","Republic of Congo":"🇨🇬","Gabon":"🇬🇦","Equatorial Guinea":"🇬🇶","São Tomé and Príncipe":"🇸🇹","Cape Verde":"🇨🇻","Comoros":"🇰🇲","Madagascar":"🇲🇬","Mauritius":"🇲🇺","Seychelles":"🇸🇨","Eswatini":"🇸🇿","Lesotho":"🇱🇸","Burundi":"🇧🇮","Guinea-Bissau":"🇬🇼"}
GRADES=["9th Grade","10th Grade","11th Grade","12th Grade (WASSCE)"]
SUBJECTS=["Mathematics","English Language","Integrated Science","Social Studies","Physics","Chemistry","Biology","Economics","Government / Civics","Literature in English","History","Geography","Agriculture","French","Religious Studies","Business Management","Accounting","Computer Studies / ICT","Technical Drawing","Home Economics","Physical Education","Art / Creative Arts","Music"]
TOPICS={"Mathematics":["Number and Numeration","Fractions and Decimals","Percentages","Ratio and Proportion","Algebraic Expressions","Linear Equations","Quadratic Equations","Simultaneous Equations","Sets and Venn Diagrams","Trigonometry","Mensuration","Geometry","Statistics","Probability","Vectors","Logarithms","Indices and Surds"],
"English Language":["Comprehension","Summary Writing","Essay (Narrative)","Essay (Argumentative)","Letter Writing (Formal)","Parts of Speech","Tenses","Active/Passive Voice","Punctuation","Vocabulary","Idioms"],
"Physics":["Measurement","Motion","Newton's Laws","Work Energy Power","Simple Machines","Pressure","Heat Transfer","Gas Laws","Waves","Sound","Light","Electricity","Ohm's Law"],
"Chemistry":["States of Matter","Atomic Structure","Periodic Table","Chemical Bonding","Reactions","Acids Bases Salts","Electrolysis","Organic Chemistry","Mole Concept"],
"Biology":["Cell Structure","Cell Division","Photosynthesis","Human Body Systems","Reproduction","Genetics","Evolution","Ecology","Diseases and Immunity"],
"Integrated Science":["Scientific Method","Cells","Photosynthesis","Respiration","Human Body","Ecology","Matter","Energy","Electricity"],
}
DEF_TOPICS=["Core Concepts","Key Terms","Applications","Review","Exam Practice"]
TASKS={"Lesson Plan":"detailed lesson plan","Quiz (10 Q)":"10-question quiz with answer key","Quiz (20 Q)":"20-question quiz","WASSCE MCQ (50)":"50 WASSCE-style MCQs","WASSCE Theory":"WASSCE theory questions","BECE Exam":"BECE-style exam","Homework":"homework with minimal resources","Group Activity":"group activity","Reading Comprehension":"reading passage with questions","No-Lab Practical":"hands-on zero-cost activity","Rubric":"grading rubric","Strategy Guide":"teaching strategies","Parent Letter":"parent communication","Weekly Scheme":"5-day scheme of work","Term Scheme":"term plan","Remedial Material":"catch-up material","Study Notes":"revision guide","Educational Game":"zero-cost teaching game","Illustrated Lesson (AI image)":"lesson with AI-generated visual"}
SIZES={"Small (<25)":"<25 students","Medium (25-40)":"25-40","Large (40-60)":"40-60","Very Large (60+)":"60+"}
RESOURCES={"Chalkboard only":"chalkboard/chalk only","+ shared textbooks":"chalkboard + shared textbooks","+ handouts":"+ printable handouts","Computer/projector":"occasional tech","Phones/tablets":"student devices","Well-equipped":"regular tech"}
LANGS={"English only":"English","English + local":"English + local language","French only":"French","French + local":"French + local"}
ABILITY={"Mixed":"mixed-ability","Struggling":"below grade level","On level":"at expected level","Advanced":"needs challenge","Inclusive":"includes learning differences"}
TIMES=["Single period (30-40 min)","Double (60-80 min)","Half day","Full day","Weekly","N/A"]
EXTRAS=["Differentiation","Formative assessment","Take-home activity","WASSCE alignment","Local examples","Literacy integration","Large-class strategies","Cross-curricular","AI visual aid"]

# === LOGO ===
def get_b64():
    d=os.path.dirname(os.path.abspath(__file__))
    for n in [LOGO_FILENAME,"logo.png"]:
        p=os.path.join(d,n)
        if os.path.exists(p):
            with open(p,"rb") as f: return base64.b64encode(f.read()).decode()
    return None

def show_logo(country=None):
    b=get_b64()
    flag=FLAGS.get(country,"") if country else ""
    if b: st.markdown(f'<div style="text-align:center;padding:.8rem 0 .2rem;display:flex;align-items:center;justify-content:center;gap:16px"><span style="font-size:3rem">{flag}</span><img src="data:image/png;base64,{b}" style="max-height:170px;filter:drop-shadow(0 4px 12px rgba(212,168,67,.3))"><span style="font-size:3rem">{flag}</span></div>',unsafe_allow_html=True)
    else: st.markdown(f'<div style="text-align:center"><h1 style="color:{C_GOLD}">{flag} 🌶️ Teacher Pehpeh {flag}</h1></div>',unsafe_allow_html=True)

def ico(s=20):
    b=get_b64()
    return f'<img src="data:image/png;base64,{b}" style="height:{s}px;width:{s}px;vertical-align:middle;border-radius:50%">' if b else "🌶️"

def pprog(stg,tot,msg):
    b=get_b64(); lit=min(stg,tot); pct=int(lit/tot*100)
    if not b: return f'<div style="background:{C_NAVY_L};border:1px solid #333;border-radius:10px;padding:12px;margin:8px 0"><div style="background:#2d3748;border-radius:6px;height:8px;overflow:hidden"><div style="background:linear-gradient(90deg,{C_BLUE},{C_BLUE_D});height:100%;width:{pct}%;border-radius:6px"></div></div><p style="text-align:center;color:#9CA3AF;font-size:.85rem;margin:6px 0 0">{msg}</p></div>'
    peps="".join(f'<img src="data:image/png;base64,{b}" style="height:26px;width:26px;margin:0 3px;opacity:{"1" if i<lit else ".12"};{"" if i<lit else "filter:grayscale(100%);"}border-radius:50%">' for i in range(tot))
    corner="".join(f'<img src="data:image/png;base64,{b}" style="height:{14+i*3}px;width:{14+i*3}px;margin:0 1px;opacity:{"1" if i<lit else ".15"};{"" if i<lit else "filter:grayscale(100%);"}border-radius:50%">' for i in range(tot))
    return f'<div style="position:fixed;top:12px;right:70px;z-index:9999;display:flex;align-items:flex-end;gap:2px;background:rgba(15,34,71,.95);padding:6px 10px;border-radius:20px;border:1px solid {C_BLUE}">{corner}</div><div style="background:{C_NAVY_L};border:1px solid #333;border-radius:10px;padding:12px 16px;margin:8px 0"><div style="display:flex;justify-content:center;margin-bottom:8px">{peps}</div><div style="background:#2d3748;border-radius:6px;height:8px;overflow:hidden"><div style="background:linear-gradient(90deg,{C_BLUE},{C_BLUE_D});height:100%;width:{pct}%;border-radius:6px;transition:width .5s"></div></div><p style="text-align:center;color:#9CA3AF;font-size:.85rem;margin:6px 0 0">{msg}</p></div>'

# === PROMPTS ===
def _p():
    return "You are Teacher Pehpeh — AI teaching assistant by IBT. Warm, wise, practical. Speak like a trusted teacher/village elder. African idioms, proverbs, analogies (fetching water, clearing farm, cassava). Liberian terms. Cheerful, encouraging."
def _g():
    return "Groups: 1(0-4 siblings,most time), 2(5-8,limited), 3(8+,very little). Consider socioeconomic, computer access, parents' ed."
def _r():
    return "Rules: stated resources only, max 3 problems/group, self-contained tips, WAEC format for exams, African context, Socratic method, print/chalkboard-ready."

def build_sys(reg,cty,grd,subj,task,cls,res,lng,abl,tm,top):
    return f"{_p()}\nCLASS: {cty},{reg},{grd},{subj},{task},{cls},{res},{lng},{abl},Time:{tm},Topic:{top}\n{_g()}\n{_kb()}\nPhysics=extra scaffolding. Group 3=SHORT. 58% no computer=paper first.\n{_r()}"

def build_chat(reg,cty,grd,subj,cls,res,lng,abl):
    return f"{_p()}\nWhen greeted: 'Hello, how can Teacher Pehpeh help you today!'\nCLASS: {cty},{reg},{grd},{subj},{cls},{res},{lng},{abl}\n{_g()}\n{_kb()}\nIntervention WORKS. Teacher's work matters.\n{_r()}"

def build_stu(reg,cty,grd,subj,cls,res,lng,abl,info):
    return f"{_p()}\nCLASS: {cty},{reg},{grd},{subj},{cls},{res},{lng},{abl}\nSTUDENT: {info}\n{_kb()}\nTargeted advice. Compare to data. Risk factors. Interventions.\n{_r()}"

# === AI ===
def ask_gpt(sp,q,h=None):
    if not OAI or not OPENAI_API_KEY: return None
    try:
        m=[{"role":"system","content":sp}]+(h or [])+[{"role":"user","content":q}]
        return openai.OpenAI(api_key=OPENAI_API_KEY).chat.completions.create(model="gpt-4o-mini",messages=m,max_tokens=3000,temperature=.7).choices[0].message.content
    except Exception as e: return f"⚠️ {e}"

def ask_cl(sp,q,h=None):
    if not ANT or not ANTHROPIC_API_KEY: return None
    try:
        m=list(h or [])+[{"role":"user","content":q}]
        return anthropic.Anthropic(api_key=ANTHROPIC_API_KEY).messages.create(model="claude-haiku-4-5-20251001",max_tokens=3000,system=sp,messages=m).content[0].text
    except Exception as e: return f"⚠️ {e}"

def ask_gem(sp,q):
    if not GEM or not GOOGLE_API_KEY: return None
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        return genai.GenerativeModel("gemini-1.5-flash",system_instruction=sp).generate_content(q).text
    except Exception as e: return f"⚠️ {e}"

def best(sp,q,h=None):
    for fn,nm in [(ask_cl,"Claude"),(ask_gpt,"ChatGPT")]:
        r=fn(sp,q,h)
        if r and not str(r).startswith("⚠️"): return r,nm
    r=ask_gem(sp,q)
    if r and not str(r).startswith("⚠️"): return r,"Gemini"
    return "⚠️ No models responded.",None

def synth(sp,q,resps):
    v={k:v for k,v in resps.items() if v and not str(v).startswith("⚠️")}
    if not v: return "⚠️ No models responded."
    if len(v)==1: return list(v.values())[0]
    p=f"Combine into ONE print-ready document:\n{sp}\n{q}\n\n"+"".join(f"=== {k} ===\n{r}\n\n" for k,r in v.items())
    for fn in [ask_cl,ask_gpt]:
        r=fn("Expert editor.",p)
        if r and not str(r).startswith("⚠️"): return r
    return max(v.values(),key=len)

# === MAIN ===
def main():
    st.set_page_config(page_title="Teacher Pehpeh",page_icon="🌶️",layout="wide")
    for k in ["chat_messages","students","conn_checked","conn_info"]:
        if k not in st.session_state: st.session_state[k]=[] if k in ("chat_messages","students") else (False if k=="conn_checked" else None)
    for sk in QUIZ: 
        k=f"qz_{sk}"
        if k not in st.session_state: st.session_state[k]={"lv":"easy","qi":0,"sc":0,"tot":0,"stk":0,"done":False,"sel":None,"hist":[]}

    if not st.session_state.conn_checked:
        with st.spinner("🌶️ Checking connection..."):
            st.session_state.conn_info=check_conn(); st.session_state.conn_checked=True
    conn=st.session_state.conn_info; online=conn["online"] if conn else False

    # CSS
    st.markdown(f"""<style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700&family=Playfair+Display:wght@600;700&display=swap');
    .stApp {{font-family:'Source Sans Pro',sans-serif;background:{C_NAVY}}}
    section[data-testid="stSidebar"] {{background:linear-gradient(180deg,#4A0E0E 0%,{C_RED} 40%,#7B2020 100%) !important}}
    section[data-testid="stSidebar"] .stMarkdown h2 {{color:{C_GOLD_L} !important;font-family:'Playfair Display',serif}}
    section[data-testid="stSidebar"] .stMarkdown p,section[data-testid="stSidebar"] .stMarkdown li {{color:#F0D5D5}}
    section[data-testid="stSidebar"] label {{color:#F0D5D5 !important}}
    section[data-testid="stSidebar"] .stSelectbox > div > div {{background:#3D0C0C !important;color:#F0D5D5 !important;border-color:#8B3030 !important}}
    section[data-testid="stSidebar"] hr {{border-color:#8B3030 !important}}
    .stStatusWidget {{display:none !important}}
    .stTabs [data-baseweb="tab-list"] {{background:{C_NAVY_L};border-radius:8px;padding:4px}}
    .stTabs [aria-selected="true"] {{color:white !important;background:{C_BLUE} !important;border-radius:6px}}
    .stButton > button[kind="primary"] {{background:linear-gradient(135deg,{C_BLUE_D},{C_BLUE}) !important;color:white !important;font-weight:700 !important;border:none !important;border-radius:8px !important}}
    .stButton > button[kind="primary"]:hover {{box-shadow:0 4px 16px rgba(43,125,233,.4) !important}}
    .rh {{background:linear-gradient(135deg,{C_RED},{C_RED_L});color:white;padding:1rem;border-radius:10px 10px 0 0;margin-top:1rem}}
    .rh h3 {{margin:0;color:white;font-family:'Playfair Display',serif;font-size:1.15rem}}
    .rb {{border:1px solid #2a3a5a;border-top:none;border-radius:0 0 10px 10px;padding:1.2rem;background:{C_NAVY_L};color:#D0D8E8;line-height:1.7}}
    .ct {{background:rgba(43,125,233,.08);border:1px solid rgba(43,125,233,.3);border-radius:12px;padding:12px 16px;margin:6px 0;color:#D0D8E8}}
    .cp {{background:rgba(139,26,26,.1);border:1px solid rgba(178,34,52,.3);border-radius:12px;padding:12px 16px;margin:6px 0;color:#D0D8E8}}
    .qbox {{background:{C_NAVY_L};border:2px solid {C_BLUE};border-radius:14px;padding:18px;margin:10px 0}}
    .qok {{background:rgba(76,175,80,.12);border:2px solid #4CAF50;border-radius:12px;padding:14px;margin:8px 0;color:#A5D6A7}}
    .qno {{background:rgba(239,83,80,.1);border:2px solid #EF5350;border-radius:12px;padding:14px;margin:8px 0;color:#EF9A9A}}
    .qsc {{background:rgba(212,168,67,.1);border:1px solid {C_GOLD};border-radius:10px;padding:10px 16px;display:inline-block;color:{C_GOLD}}}
    .qtip {{background:rgba(43,125,233,.08);border-left:4px solid {C_BLUE};border-radius:0 8px 8px 0;padding:10px 14px;margin:8px 0;font-size:.88rem;color:#93BBEA}}
    .sc {{background:{C_NAVY_L};border:1px solid #2a3a5a;border-radius:10px;padding:12px 16px;margin:6px 0}}
    .ft {{text-align:center;color:#556677;font-size:.8rem;padding:1.5rem 0 1rem;border-top:1px solid #1a2a44;margin-top:2rem}}
    .ft a {{color:{C_GOLD};text-decoration:none}}
    </style>""",unsafe_allow_html=True)

    # Sidebar (defined first so country is available for logo flag)
    with st.sidebar:
        st.markdown("## 🌶️ My Classroom"); st.caption("Set once — shapes every response"); st.markdown("---")
        country=st.selectbox("Country",COUNTRIES); region=st.selectbox("Setting",list(REGIONS.keys()))
        grade=st.selectbox("Grade",GRADES,index=1); subject=st.selectbox("Subject",SUBJECTS)
        clsz=st.selectbox("Class Size",list(SIZES.keys()),index=2); res=st.selectbox("Resources",list(RESOURCES.keys()),index=1)
        lang=st.selectbox("Language",list(LANGS.keys())); abl=st.selectbox("Student Level",list(ABILITY.keys()))
        st.markdown("---"); st.caption("© 2026 Institute of Basic Technology")
        st.markdown("[🌐 Visit our website](https://www.institutebasictechnology.org/index.php)")

    show_logo(country)
    st.markdown('<p style="text-align:center;color:#8899BB;font-size:.95rem;margin-bottom:.6rem">Curating Personalized Content to Support Underresourced Teachers<br>ChatGPT &bull; Claude &bull; Gemini</p>',unsafe_allow_html=True)

    # Connection
    if conn:
        if conn["quality"]=="none": st.markdown(f'<div style="padding:.5rem 1rem;border-radius:6px;background:rgba(239,83,80,.15);border-left:4px solid #EF5350;color:#EF9A9A;margin-bottom:.6rem">{conn["emoji"]} <strong>OFFLINE</strong> — Practice Quiz available!</div>',unsafe_allow_html=True)
        else:
            c="rgba(76,175,80,.1);border-left:4px solid #4CAF50;color:#81C784" if conn["quality"] in ("high","medium") else "rgba(255,167,38,.1);border-left:4px solid #FFA726;color:#FFB74D"
            st.markdown(f'<div style="padding:.5rem 1rem;border-radius:6px;background:{c};margin-bottom:.6rem">{conn["emoji"]} <strong>{conn["label"]}</strong> ({conn["latency_ms"]}ms)</div>',unsafe_allow_html=True)
    if st.sidebar.button("🔄 Re-check"): st.session_state.conn_checked=False; st.rerun()

    keys=sum([bool(OPENAI_API_KEY),bool(ANTHROPIC_API_KEY),bool(GOOGLE_API_KEY)])
    act=[n for k,n in [(OPENAI_API_KEY,"ChatGPT"),(ANTHROPIC_API_KEY,"Claude"),(GOOGLE_API_KEY,"Gemini")] if k]
    if online and keys:
        st.markdown(f'<div style="background:rgba(43,125,233,.1);border-left:4px solid {C_BLUE};padding:.5rem 1rem;border-radius:6px;font-size:.85rem;color:#7BB8F5;margin-bottom:.6rem">{ico(16)} <strong>{len(act)}</strong>: {" · ".join(act)}{"  · 🎨 DALL-E" if OPENAI_API_KEY else ""}</div>',unsafe_allow_html=True)

    # Tabs
    if online and keys:
        t1,t2,t3,t4=st.tabs(["📋 Generate","🧑‍🎓 Students","💬 Chat","🌶️ Quiz"])
    else: t1=t2=t3=None; t4=st.container()

    # TAB 1: GENERATE
    if t1:
     with t1:
        c1,c2=st.columns(2)
        with c1: task=st.selectbox("Task",list(TASKS.keys()))
        with c2: tm=st.selectbox("Time",TIMES)
        topic=st.selectbox("Topic",TOPICS.get(subject,DEF_TOPICS))
        with st.expander("Options"):
            exs=[o for i,o in enumerate(EXTRAS) if st.checkbox(o,key=f"x{i}")]
        if st.button("🌶️ Generate",type="primary",use_container_width=True,key="gen"):
            sp=build_sys(REGIONS[region],country,grade,subject,task,SIZES[clsz],RESOURCES[res],LANGS[lang],ABILITY[abl],tm,topic)
            q=f"Create {TASKS[task]}.\nSubject:{subject}\nGrade:{grade}\nTopic:{topic}\nIMMEDIATELY USABLE."
            if exs: q+="\n"+"; ".join(exs)
            rs={}; ph=st.empty(); s=0; tot=keys+1
            ph.markdown(pprog(0,tot,"Preparing..."),unsafe_allow_html=True)
            for k,fn,nm in [(OPENAI_API_KEY,ask_gpt,"ChatGPT"),(ANTHROPIC_API_KEY,ask_cl,"Claude"),(GOOGLE_API_KEY,ask_gem,"Gemini")]:
                if k:
                    s+=1; ph.markdown(pprog(s,tot,f"{nm}..."),unsafe_allow_html=True)
                    rs[nm]=fn(sp,q) if nm!="Gemini" else fn(sp,q)
            s+=1; ph.markdown(pprog(s,tot,"Combining..."),unsafe_allow_html=True)
            result=synth(sp,q,rs); ph.markdown(pprog(tot,tot,"✅ Done!"),unsafe_allow_html=True); time.sleep(.3); ph.empty()
            img=None
            if "image" in task.lower() or "AI visual" in str(exs):
                with st.spinner("🎨 Generating visual..."): img=gen_image(f"{subject}: {topic} for {grade} in {country}")
            st.markdown(f'<div class="rh"><h3>{ico(20)} {task} — {topic}</h3></div>',unsafe_allow_html=True)
            if img: st.image(img,caption=topic,use_container_width=True)
            st.markdown(f'<div class="rb">',unsafe_allow_html=True); st.markdown(result); st.markdown('</div>',unsafe_allow_html=True)
            st.download_button("📥 Download",data=result,file_name=f"{task}_{topic}.txt".replace(" ","_")[:60])

    # TAB 2: STUDENTS
    if t2:
     with t2:
        st.markdown(f'<div style="background:{C_NAVY_L};border:1px solid {C_BLUE};border-radius:12px;padding:14px 18px;margin-bottom:10px">{ico(20)} <strong style="color:{C_BLUE}">My Students</strong></div>',unsafe_allow_html=True)
        with st.expander("➕ Add Profile",expanded=not st.session_state.students):
            c1,c2=st.columns(2)
            with c1: sn=st.text_input("Name",key="sn"); sib=st.selectbox("Siblings",["0-4","5-8","8+"],key="sb"); me=st.selectbox("Mom Edu",["HS Grad","No HS","Unknown"],key="me")
            with c2: sm=st.selectbox("Single Mom?",["No","Yes","Unknown"],key="sm"); wk=st.selectbox("Works?",["No","Yes","Unknown"],key="wk"); cp=st.selectbox("Computer?",["Never","Rarely","Sometimes","Often"],key="cp")
            nt=st.text_area("Notes",key="nt",height=50)
            if st.button("✅ Save",key="sv") and sn.strip():
                st.session_state.students.append(dict(name=sn.strip(),sib=sib,mom=me,sm=sm,wk=wk,cp=cp,nt=nt.strip())); st.rerun()
        for i,s in enumerate(st.session_state.students):
            rsk=[]
            if s["mom"]=="No HS": rsk.append("🔴 No HS Mom")
            if s["sm"]=="Yes": rsk.append("🔴 Single Mom")
            if s["sib"]=="8+": rsk.append("🟠 8+ siblings")
            if s["wk"]=="Yes": rsk.append("🟠 Works")
            if s["cp"]=="Never": rsk.append("🟡 No computer")
            st.markdown(f'<div class="sc"><strong style="color:{C_BLUE}">{s["name"]}</strong> — {s["sib"]} sib, Mom:{s["mom"]}<br><span style="font-size:.82rem">{" · ".join(rsk) or "🟢 Lower risk"}</span></div>',unsafe_allow_html=True)
            info=f'{s["name"]},{s["sib"]}sib,Mom:{s["mom"]},SM:{s["sm"]},Works:{s["wk"]},Comp:{s["cp"]},{s["nt"]}'
            b1,b2,b3=st.columns(3)
            with b1:
                if st.button("📝 Assignment",key=f"a{i}"):
                    with st.spinner("Creating..."):
                        r,m=best(build_stu(REGIONS[region],country,grade,subject,SIZES[clsz],RESOURCES[res],LANGS[lang],ABILITY[abl],info),f"Tailored {subject} assignment. Max 3 problems.")
                    st.markdown(f'<div class="rb">{r}<div style="font-size:.65rem;color:#556;margin-top:4px">by {m}</div></div>',unsafe_allow_html=True)
            with b2:
                if st.button("📊 Risk",key=f"r{i}"):
                    with st.spinner("Analyzing..."):
                        r,m=best(build_stu(REGIONS[region],country,grade,subject,SIZES[clsz],RESOURCES[res],LANGS[lang],ABILITY[abl],info),"Risk analysis using IBT data. Compare to 183-student dataset.")
                    st.markdown(f'<div class="rb">{r}<div style="font-size:.65rem;color:#556;margin-top:4px">by {m}</div></div>',unsafe_allow_html=True)
            with b3:
                if st.button("🗑️",key=f"d{i}"): st.session_state.students.pop(i); st.rerun()
        if st.session_state.students:
            st.markdown("---"); st.markdown(f"#### {ico(16)} Grade Work")
            gs=st.selectbox("Student:",[s["name"] for s in st.session_state.students],key="gs")
            gw=st.text_area("Student's work:",height=100,key="gw"); gsub=st.selectbox("Subject:",SUBJECTS,key="gsub"); gt=st.text_input("Topic:",key="gt")
            if st.button("🌶️ Grade",type="primary",key="gb") and gw.strip():
                sel=next((s for s in st.session_state.students if s["name"]==gs),None)
                if sel:
                    info=f'{sel["name"]},{sel["sib"]}sib,Mom:{sel["mom"]},SM:{sel["sm"]},Works:{sel["wk"]},Comp:{sel["cp"]},{sel["nt"]}'
                    with st.spinner("Grading..."):
                        r,m=best(build_stu(REGIONS[region],country,grade,gsub,SIZES[clsz],RESOURCES[res],LANGS[lang],ABILITY[abl],info),f"Grade:\nSTUDENT:{info}\n{gsub} {gt}\n\nWORK:\n{gw}\n\nGive: grade, praise, corrections, tips, next step.")
                    st.markdown(f'<div class="rh"><h3>{ico(16)} Feedback: {gs}</h3></div><div class="rb">{r}</div>',unsafe_allow_html=True)

    # TAB 3: CHAT
    if t3:
     with t3:
        st.markdown(f'<div style="background:rgba(139,26,26,.12);border:1px solid rgba(178,34,52,.3);border-radius:12px;padding:14px 18px;margin-bottom:10px">{ico(20)} <strong style="color:{C_GOLD}">Ask Teacher Pehpeh</strong> <span style="color:#C0A070;font-size:.85rem">— {grade} · {subject}</span></div>',unsafe_allow_html=True)
        ec=st.columns(3)
        for i,ex in enumerate(["How to teach fractions with no textbooks?","My students keep failing WASSCE.","Managing 60+ students?"]):
            with ec[i]:
                if st.button(f"💡 {ex[:38]}...",key=f"ex{i}",use_container_width=True):
                    st.session_state.chat_messages.append({"role":"user","content":ex})
                    r,m=best(build_chat(REGIONS[region],country,grade,subject,SIZES[clsz],RESOURCES[res],LANGS[lang],ABILITY[abl]),ex,[{"role":x["role"],"content":x["content"]} for x in st.session_state.chat_messages[:-1]])
                    st.session_state.chat_messages.append({"role":"assistant","content":r,"model":m}); st.rerun()
        st.markdown("---")
        ic1,ic2=st.columns([3,1])
        with ic1: ip=st.text_input("🎨 Generate visual:",key="ip",placeholder=f"e.g., {subject} diagram for {grade}")
        with ic2:
            st.markdown("<br>",unsafe_allow_html=True)
            if st.button("🎨 Image",key="ib") and ip:
                with st.spinner("Creating..."): url=gen_image(ip)
                if url: st.image(url,caption=ip,use_container_width=True)
                else: st.warning("Unavailable. Check OpenAI key.")
        st.markdown("---")
        for msg in st.session_state.chat_messages:
            if msg["role"]=="user": st.markdown(f'<div class="ct"><div style="font-size:.75rem;font-weight:700;color:{C_BLUE};margin-bottom:4px">🧑‍🏫 You</div>{msg["content"]}</div>',unsafe_allow_html=True)
            else: st.markdown(f'<div class="cp"><div style="font-size:.75rem;font-weight:700;color:{C_GOLD};margin-bottom:4px">{ico(16)} Teacher Pehpeh</div>{msg["content"]}<div style="font-size:.65rem;color:#556;margin-top:4px">by {msg.get("model","AI")}</div></div>',unsafe_allow_html=True)
        uq=st.chat_input(f"Ask about {subject}...")
        if uq:
            st.session_state.chat_messages.append({"role":"user","content":uq})
            r,m=best(build_chat(REGIONS[region],country,grade,subject,SIZES[clsz],RESOURCES[res],LANGS[lang],ABILITY[abl]),uq,[{"role":x["role"],"content":x["content"]} for x in st.session_state.chat_messages[-11:-1]])
            st.session_state.chat_messages.append({"role":"assistant","content":r,"model":m}); st.rerun()
        if st.session_state.chat_messages and st.button("🗑️ Clear",key="cc"): st.session_state.chat_messages=[]; st.rerun()

    # TAB 4: QUIZ (works offline)
    with t4:
        if not online or not keys:
            st.markdown(f'<div style="background:rgba(239,83,80,.12);border:2px solid {C_RED_L};border-radius:12px;padding:16px;margin-bottom:12px"><h3 style="color:#EF9A9A;margin:0 0 6px">📴 Offline — Practice Quiz</h3><p style="color:#FFCDD2;font-size:.9rem;margin:0">No internet? These quizzes work offline!</p></div>',unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="background:rgba(43,125,233,.08);border:1px solid {C_BLUE};border-radius:12px;padding:12px 18px;margin-bottom:10px">{ico(16)} <strong style="color:{C_BLUE}">Practice Quiz</strong> <span style="color:#7BB8F5;font-size:.85rem">— Adaptive. Works offline too!</span></div>',unsafe_allow_html=True)

        qsub=st.selectbox("Subject:",list(QUIZ.keys()),key="qs")
        qs=st.session_state[f"qz_{qsub}"]
        bank=QUIZ[qsub]; lv=qs["lv"]; questions=bank.get(lv,bank["easy"]); qi=qs["qi"]%len(questions); cur=questions[qi]
        pct=f"{round(qs['sc']/qs['tot']*100)}%" if qs["tot"] else "—"
        stk=f"🔥 {qs['stk']} streak!" if qs["stk"]>=3 else ""
        st.markdown(f'<div class="qsc">{ico(16)} Score: <strong>{qs["sc"]}/{qs["tot"]}</strong> ({pct}) · Level: <strong>{lv.upper()}</strong> {stk}</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="qbox"><strong style="color:white">Q{qs["tot"]+1}:</strong><br><span style="color:#D0D8E8;line-height:1.6">{cur["q"]}</span></div>',unsafe_allow_html=True)

        if not qs["done"]:
            cols=st.columns(2)
            for j,opt in enumerate(cur["o"]):
                with cols[j%2]:
                    if st.button(f"{'ABCD'[j]}) {opt}",key=f"qo_{qsub}_{qs['tot']}_{j}",use_container_width=True):
                        qs["sel"]=j; qs["done"]=True; qs["tot"]+=1
                        if j==cur["a"]: qs["sc"]+=1; qs["stk"]+=1
                        else: qs["stk"]=0
                        qs["hist"].append({"c":j==cur["a"],"lv":lv}); st.rerun()
        else:
            ok=qs["sel"]==cur["a"]
            if ok: st.markdown(f'<div class="qok"><strong>{random.choice(PRAISE)}</strong><br>✅ {cur["o"][cur["a"]]} is correct!</div>',unsafe_allow_html=True)
            else: st.markdown(f'<div class="qno"><strong>{random.choice(ENCOURAGE)}</strong><br>Answer: <strong>{cur["o"][cur["a"]]}</strong></div>',unsafe_allow_html=True)
            st.markdown(f'<div style="background:rgba(212,168,67,.08);border:1px solid {C_GOLD};border-radius:10px;padding:12px 16px;margin:8px 0"><strong style="color:{C_GOLD}">📖 Explanation:</strong><br><span style="color:#D0D8E8">{cur["e"]}</span></div>',unsafe_allow_html=True)
            st.markdown(f'<div class="qtip"><strong>🧑‍🏫 Teacher Tip:</strong> {cur["t"]}</div>',unsafe_allow_html=True)
            recent=[h for h in qs["hist"][-5:]]; rc=sum(1 for h in recent if h["c"])
            if st.button("➡️ Next",type="primary",key=f"nx_{qsub}_{qs['tot']}",use_container_width=True):
                if len(recent)>=3:
                    if rc>=4 and lv!="hard": qs["lv"]="medium" if lv=="easy" else "hard"; st.toast(f"🌶️ Level UP → {qs['lv'].upper()}")
                    elif rc<=1 and lv!="easy": qs["lv"]="easy" if lv=="medium" else "medium"; st.toast(f"Adjusting → {qs['lv'].upper()}")
                qs["qi"]=(qi+1)%len(bank.get(qs["lv"],bank["easy"])); qs["done"]=False; qs["sel"]=None; st.rerun()

        st.markdown("---")
        r1,r2=st.columns(2)
        with r1:
            if st.button("🔄 Reset",key=f"rst_{qsub}"): st.session_state[f"qz_{qsub}"]={"lv":"easy","qi":0,"sc":0,"tot":0,"stk":0,"done":False,"sel":None,"hist":[]}; st.rerun()
        with r2:
            if st.button("📝 WASSCE Tips",key="wt"): st.markdown(f'<div style="background:{C_NAVY_L};border:1px solid {C_GOLD};border-radius:12px;padding:16px;color:#D0D8E8;white-space:pre-wrap;line-height:1.7">{WASSCE_TIPS}</div>',unsafe_allow_html=True)

    st.markdown(f'<div class="ft">{ico(16)} Built by <strong>Rodney L. Bollie, PhD</strong> · <a href="https://www.institutebasictechnology.org">Institute of Basic Technology</a><br><a href="https://www.institutebasictechnology.org/index.php" style="color:{C_BLUE}">Visit our website →</a></div>',unsafe_allow_html=True)

if __name__=="__main__": main()
