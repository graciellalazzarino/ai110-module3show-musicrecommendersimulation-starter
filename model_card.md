# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

**The biggest weakness: genre is worth so much that one genre match can beat everything else, including the listener's mood.** For the "Happy Pop" profile, Gym Hero (pop, *intense*) ranks #2 above Rooftop Lights (indie pop, *happy*) only because it has the word "pop" in its genre, even though a happy-pop listener asked for happy songs. Gym Hero shows up in the top 5 for **5 of the 6 profiles** I tested, because it is very high energy, very "produced," and is the only song labeled both pop and intense. Genre is also an exact text match, so "indie pop" earns zero genre points from a pop fan.

The catalog is uneven: lofi has 3 songs and pop has 2, but 13 genres have only one song each. A lofi fan gets three strong matches; a metal or folk fan gets one, and after that the list is filled with songs that only share a similar energy level, with scores so close together (about 1.0 each) that the order is basically random.

Other features it ignores: tempo, valence (how positive a song sounds), danceability, lyrics, language, artist, and anything about the listener's history or context (workout vs. studying). It also assumes one fixed taste per user, so a listener who likes both chill lofi and intense rock cannot be represented.

---

## 7. Evaluation  

### Profiles tested

| Profile | Genre | Mood | Energy | Likes acoustic | Why |
|---|---|---|---|---|---|
| Happy Pop (default) | pop | happy | 0.8 | No | Baseline from the starter |
| Chill Lofi | lofi | chill | 0.4 | Yes | Opposite end of the energy scale |
| Deep Intense Rock | rock | intense | 0.9 | No | Genre with only one song |
| EDGE: Sad but High Energy | folk | sad | 0.9 | Yes | Conflicting wishes: sad songs are low energy |
| EDGE: Genre Not In Catalog | k-pop | happy | 0.7 | No | No song can ever get genre points |
| EDGE: Acoustic Metalhead | metal | angry | 0.95 | Yes | Wants acoustic, but metal is never acoustic |

### What I looked for

For each profile I checked whether the #1 song "felt" right, whether the rest of the top 5 made sense, and whether the reasons explained the ranking.

### Comparing profiles

- **Happy Pop vs. Chill Lofi:** The two lists share **zero** songs. Happy Pop picks bright, high-energy, produced tracks (Sunrise City, Gym Hero); Chill Lofi picks quiet, acoustic tracks around 0.4 energy (Library Rain, Midnight Coding). This makes sense because the energy targets are far apart *and* the acoustic preference points in opposite directions, so both numeric features push the lists apart.
- **Happy Pop vs. Deep Intense Rock:** Both lists contain Gym Hero at #2, but for different reasons: for Happy Pop it gets the *genre* points, for Rock it gets the *mood* points (intense). Both profiles want high energy, so the bottom of each list fills with the same loud songs.
- **Chill Lofi vs. Deep Intense Rock:** The lofi fan gets a strong top 3 (three lofi songs exist), while the rock fan's #1 scores 4.44 and #2 drops to 2.44 because there is only one rock song. Same scoring rule, very different experience, purely because of how many songs exist in each genre.
- **Sad but High Energy vs. Acoustic Metalhead:** Both profiles ask for something the catalog does not have. In both, the single exact genre+mood match wins easily (Letters I Never Sent, Iron Tide), even though Letters I Never Sent is far from the requested energy (0.30 vs 0.9) and Iron Tide is almost not acoustic at all (0.03). After #1, both lists are a near-tie of loud songs scoring about 1.0.
- **Genre Not In Catalog vs. Happy Pop:** With no genre points possible, mood becomes the deciding factor, and the k-pop fan gets a reasonable list (Sunrise City and Rooftop Lights, both happy) with Gym Hero dropping from #2 to #5. Removing genre from the equation actually gave a *better* happy list.

### Why does "Gym Hero" keep showing up? (plain-language version)

Imagine a judge who gives 2 points for "right genre," 1 point for "right mood," and up to 1.5 points for "right energy and sound." Gym Hero is labeled pop, so any pop fan gives it 2 points right away, more than a mood match is worth. It is also one of the loudest, most energetic songs, so anyone who asks for high energy gives it nearly full energy points too. It does not need to be the *right* song; it just needs to be close on the things the judge cares about most.

### What surprised me

- The edge-case profiles did not break the code, but they quietly gave bad answers: the "Sad but High Energy" listener got happy pop songs at #3–#4 because nothing in the catalog is both sad and energetic.
- Scores below #1 are often within 0.05 of each other, so tiny differences in acousticness decide the order. The ranking looks precise but isn't.

### Experiment: weight shift (genre 2.0 → 1.0, energy 1.0 → 2.0)

I halved the genre weight and doubled the energy weight. The maximum possible score stays the same (4.5), so the scores are still comparable.

| Profile | Before (top 3) | After (top 3) |
|---|---|---|
| Happy Pop | Sunrise City, Gym Hero, Rooftop Lights | Sunrise City, **Rooftop Lights**, Gym Hero |
| Chill Lofi | Library Rain, Midnight Coding, Focus Flow | (same) |
| Deep Intense Rock | Storm Runner, Gym Hero, Strobe Heart | (same) |
| Sad but High Energy | Letters I Never Sent, Storm Runner, Rooftop Lights | Letters I Never Sent, Storm Runner, Gym Hero |
| Genre Not In Catalog | Sunrise City, Rooftop Lights, Concrete Echoes | **Rooftop Lights**, Sunrise City, Night Drive Loop |
| Acoustic Metalhead | Iron Tide, Storm Runner, Strobe Heart | Iron Tide, Strobe Heart, Gym Hero |

**Result:** The #1 song did not change for any profile. For Happy Pop the change was more *accurate*: Rooftop Lights (actually happy) moved above Gym Hero. For most other profiles it was just *different*: the lower spots reshuffled among loud songs, and the "Sad but High Energy" list got even more intense, since energy now outweighs everything except the one folk match. I kept the original weights in the code.

### Terminal output (original weights)

```
Loaded songs: 18

================================================================
Profile: Happy Pop (default)
  genre=pop, mood=happy, energy=0.8, likes_acoustic=False
================================================================
1. Sunrise City by Neon Echo  [pop, happy]
   Score: 4.39
     - genre match: pop (+2.0)
     - mood match: happy (+1.0)
     - energy 0.82 vs target 0.80 (+0.98)
     - produced sound, acousticness 0.18 (+0.41)

2. Gym Hero by Max Pulse  [pop, intense]
   Score: 3.35
     - genre match: pop (+2.0)
     - energy 0.93 vs target 0.80 (+0.87)
     - produced sound, acousticness 0.05 (+0.47)

3. Rooftop Lights by Indigo Parade  [indie pop, happy]
   Score: 2.29
     - mood match: happy (+1.0)
     - energy 0.76 vs target 0.80 (+0.96)
     - produced sound, acousticness 0.35 (+0.33)

4. Concrete Echoes by Blockwise  [hip hop, confident]
   Score: 1.42
     - energy 0.78 vs target 0.80 (+0.98)
     - produced sound, acousticness 0.12 (+0.44)

5. Storm Runner by Voltline  [rock, intense]
   Score: 1.34
     - energy 0.91 vs target 0.80 (+0.89)
     - produced sound, acousticness 0.10 (+0.45)

================================================================
Profile: Chill Lofi
  genre=lofi, mood=chill, energy=0.4, likes_acoustic=True
================================================================
1. Library Rain by Paper Lanterns  [lofi, chill]
   Score: 4.38
     - genre match: lofi (+2.0)
     - mood match: chill (+1.0)
     - energy 0.35 vs target 0.40 (+0.95)
     - acoustic sound, acousticness 0.86 (+0.43)

2. Midnight Coding by LoRoom  [lofi, chill]
   Score: 4.33
     - genre match: lofi (+2.0)
     - mood match: chill (+1.0)
     - energy 0.42 vs target 0.40 (+0.98)
     - acoustic sound, acousticness 0.71 (+0.35)

3. Focus Flow by LoRoom  [lofi, focused]
   Score: 3.39
     - genre match: lofi (+2.0)
     - energy 0.40 vs target 0.40 (+1.00)
     - acoustic sound, acousticness 0.78 (+0.39)

4. Spacewalk Thoughts by Orbit Bloom  [ambient, chill]
   Score: 2.34
     - mood match: chill (+1.0)
     - energy 0.28 vs target 0.40 (+0.88)
     - acoustic sound, acousticness 0.92 (+0.46)

5. Coffee Shop Stories by Slow Stereo  [jazz, relaxed]
   Score: 1.42
     - energy 0.37 vs target 0.40 (+0.97)
     - acoustic sound, acousticness 0.89 (+0.45)

================================================================
Profile: Deep Intense Rock
  genre=rock, mood=intense, energy=0.9, likes_acoustic=False
================================================================
1. Storm Runner by Voltline  [rock, intense]
   Score: 4.44
     - genre match: rock (+2.0)
     - mood match: intense (+1.0)
     - energy 0.91 vs target 0.90 (+0.99)
     - produced sound, acousticness 0.10 (+0.45)

2. Gym Hero by Max Pulse  [pop, intense]
   Score: 2.44
     - mood match: intense (+1.0)
     - energy 0.93 vs target 0.90 (+0.97)
     - produced sound, acousticness 0.05 (+0.47)

3. Strobe Heart by Pulse Theory  [edm, euphoric]
   Score: 1.44
     - energy 0.95 vs target 0.90 (+0.95)
     - produced sound, acousticness 0.02 (+0.49)

4. Iron Tide by Grave Signal  [metal, angry]
   Score: 1.42
     - energy 0.97 vs target 0.90 (+0.93)
     - produced sound, acousticness 0.03 (+0.48)

5. Sunrise City by Neon Echo  [pop, happy]
   Score: 1.33
     - energy 0.82 vs target 0.90 (+0.92)
     - produced sound, acousticness 0.18 (+0.41)

================================================================
Profile: EDGE: Sad but High Energy
  genre=folk, mood=sad, energy=0.9, likes_acoustic=True
================================================================
1. Letters I Never Sent by June Harbor  [folk, sad]
   Score: 3.85
     - genre match: folk (+2.0)
     - mood match: sad (+1.0)
     - energy 0.30 vs target 0.90 (+0.40)
     - acoustic sound, acousticness 0.90 (+0.45)

2. Storm Runner by Voltline  [rock, intense]
   Score: 1.04
     - energy 0.91 vs target 0.90 (+0.99)
     - acoustic sound, acousticness 0.10 (+0.05)

3. Rooftop Lights by Indigo Parade  [indie pop, happy]
   Score: 1.03
     - energy 0.76 vs target 0.90 (+0.86)
     - acoustic sound, acousticness 0.35 (+0.17)

4. Sunrise City by Neon Echo  [pop, happy]
   Score: 1.01
     - energy 0.82 vs target 0.90 (+0.92)
     - acoustic sound, acousticness 0.18 (+0.09)

5. Gym Hero by Max Pulse  [pop, intense]
   Score: 0.99
     - energy 0.93 vs target 0.90 (+0.97)
     - acoustic sound, acousticness 0.05 (+0.03)

================================================================
Profile: EDGE: Genre Not In Catalog
  genre=k-pop, mood=happy, energy=0.7, likes_acoustic=False
================================================================
1. Sunrise City by Neon Echo  [pop, happy]
   Score: 2.29
     - mood match: happy (+1.0)
     - energy 0.82 vs target 0.70 (+0.88)
     - produced sound, acousticness 0.18 (+0.41)

2. Rooftop Lights by Indigo Parade  [indie pop, happy]
   Score: 2.27
     - mood match: happy (+1.0)
     - energy 0.76 vs target 0.70 (+0.94)
     - produced sound, acousticness 0.35 (+0.33)

3. Concrete Echoes by Blockwise  [hip hop, confident]
   Score: 1.36
     - energy 0.78 vs target 0.70 (+0.92)
     - produced sound, acousticness 0.12 (+0.44)

4. Night Drive Loop by Neon Echo  [synthwave, moody]
   Score: 1.34
     - energy 0.75 vs target 0.70 (+0.95)
     - produced sound, acousticness 0.22 (+0.39)

5. Gym Hero by Max Pulse  [pop, intense]
   Score: 1.24
     - energy 0.93 vs target 0.70 (+0.77)
     - produced sound, acousticness 0.05 (+0.47)

================================================================
Profile: EDGE: Acoustic Metalhead
  genre=metal, mood=angry, energy=0.95, likes_acoustic=True
================================================================
1. Iron Tide by Grave Signal  [metal, angry]
   Score: 4.00
     - genre match: metal (+2.0)
     - mood match: angry (+1.0)
     - energy 0.97 vs target 0.95 (+0.98)
     - acoustic sound, acousticness 0.03 (+0.01)

2. Storm Runner by Voltline  [rock, intense]
   Score: 1.01
     - energy 0.91 vs target 0.95 (+0.96)
     - acoustic sound, acousticness 0.10 (+0.05)

3. Strobe Heart by Pulse Theory  [edm, euphoric]
   Score: 1.01
     - energy 0.95 vs target 0.95 (+1.00)
     - acoustic sound, acousticness 0.02 (+0.01)

4. Gym Hero by Max Pulse  [pop, intense]
   Score: 1.01
     - energy 0.93 vs target 0.95 (+0.98)
     - acoustic sound, acousticness 0.05 (+0.03)

5. Rooftop Lights by Indigo Parade  [indie pop, happy]
   Score: 0.99
     - energy 0.76 vs target 0.95 (+0.81)
     - acoustic sound, acousticness 0.35 (+0.17)

```

### Terminal output (experiment weights)

```
EXPERIMENT: genre weight 2.0 -> 1.0, energy weight 1.0 -> 2.0

Loaded songs: 18

================================================================
Profile: Happy Pop (default)
  genre=pop, mood=happy, energy=0.8, likes_acoustic=False
================================================================
1. Sunrise City by Neon Echo  [pop, happy]
   Score: 4.37
     - genre match: pop (+1.0)
     - mood match: happy (+1.0)
     - energy 0.82 vs target 0.80 (+1.96)
     - produced sound, acousticness 0.18 (+0.41)

2. Rooftop Lights by Indigo Parade  [indie pop, happy]
   Score: 3.25
     - mood match: happy (+1.0)
     - energy 0.76 vs target 0.80 (+1.92)
     - produced sound, acousticness 0.35 (+0.33)

3. Gym Hero by Max Pulse  [pop, intense]
   Score: 3.22
     - genre match: pop (+1.0)
     - energy 0.93 vs target 0.80 (+1.74)
     - produced sound, acousticness 0.05 (+0.47)

4. Concrete Echoes by Blockwise  [hip hop, confident]
   Score: 2.40
     - energy 0.78 vs target 0.80 (+1.96)
     - produced sound, acousticness 0.12 (+0.44)

5. Night Drive Loop by Neon Echo  [synthwave, moody]
   Score: 2.29
     - energy 0.75 vs target 0.80 (+1.90)
     - produced sound, acousticness 0.22 (+0.39)

================================================================
Profile: Chill Lofi
  genre=lofi, mood=chill, energy=0.4, likes_acoustic=True
================================================================
1. Library Rain by Paper Lanterns  [lofi, chill]
   Score: 4.33
     - genre match: lofi (+1.0)
     - mood match: chill (+1.0)
     - energy 0.35 vs target 0.40 (+1.90)
     - acoustic sound, acousticness 0.86 (+0.43)

2. Midnight Coding by LoRoom  [lofi, chill]
   Score: 4.31
     - genre match: lofi (+1.0)
     - mood match: chill (+1.0)
     - energy 0.42 vs target 0.40 (+1.96)
     - acoustic sound, acousticness 0.71 (+0.35)

3. Focus Flow by LoRoom  [lofi, focused]
   Score: 3.39
     - genre match: lofi (+1.0)
     - energy 0.40 vs target 0.40 (+2.00)
     - acoustic sound, acousticness 0.78 (+0.39)

4. Spacewalk Thoughts by Orbit Bloom  [ambient, chill]
   Score: 3.22
     - mood match: chill (+1.0)
     - energy 0.28 vs target 0.40 (+1.76)
     - acoustic sound, acousticness 0.92 (+0.46)

5. Coffee Shop Stories by Slow Stereo  [jazz, relaxed]
   Score: 2.38
     - energy 0.37 vs target 0.40 (+1.94)
     - acoustic sound, acousticness 0.89 (+0.45)

================================================================
Profile: Deep Intense Rock
  genre=rock, mood=intense, energy=0.9, likes_acoustic=False
================================================================
1. Storm Runner by Voltline  [rock, intense]
   Score: 4.43
     - genre match: rock (+1.0)
     - mood match: intense (+1.0)
     - energy 0.91 vs target 0.90 (+1.98)
     - produced sound, acousticness 0.10 (+0.45)

2. Gym Hero by Max Pulse  [pop, intense]
   Score: 3.42
     - mood match: intense (+1.0)
     - energy 0.93 vs target 0.90 (+1.94)
     - produced sound, acousticness 0.05 (+0.47)

3. Strobe Heart by Pulse Theory  [edm, euphoric]
   Score: 2.39
     - energy 0.95 vs target 0.90 (+1.90)
     - produced sound, acousticness 0.02 (+0.49)

4. Iron Tide by Grave Signal  [metal, angry]
   Score: 2.35
     - energy 0.97 vs target 0.90 (+1.86)
     - produced sound, acousticness 0.03 (+0.48)

5. Sunrise City by Neon Echo  [pop, happy]
   Score: 2.25
     - energy 0.82 vs target 0.90 (+1.84)
     - produced sound, acousticness 0.18 (+0.41)

================================================================
Profile: EDGE: Sad but High Energy
  genre=folk, mood=sad, energy=0.9, likes_acoustic=True
================================================================
1. Letters I Never Sent by June Harbor  [folk, sad]
   Score: 3.25
     - genre match: folk (+1.0)
     - mood match: sad (+1.0)
     - energy 0.30 vs target 0.90 (+0.80)
     - acoustic sound, acousticness 0.90 (+0.45)

2. Storm Runner by Voltline  [rock, intense]
   Score: 2.03
     - energy 0.91 vs target 0.90 (+1.98)
     - acoustic sound, acousticness 0.10 (+0.05)

3. Gym Hero by Max Pulse  [pop, intense]
   Score: 1.96
     - energy 0.93 vs target 0.90 (+1.94)
     - acoustic sound, acousticness 0.05 (+0.03)

4. Sunrise City by Neon Echo  [pop, happy]
   Score: 1.93
     - energy 0.82 vs target 0.90 (+1.84)
     - acoustic sound, acousticness 0.18 (+0.09)

5. Strobe Heart by Pulse Theory  [edm, euphoric]
   Score: 1.91
     - energy 0.95 vs target 0.90 (+1.90)
     - acoustic sound, acousticness 0.02 (+0.01)

================================================================
Profile: EDGE: Genre Not In Catalog
  genre=k-pop, mood=happy, energy=0.7, likes_acoustic=False
================================================================
1. Rooftop Lights by Indigo Parade  [indie pop, happy]
   Score: 3.21
     - mood match: happy (+1.0)
     - energy 0.76 vs target 0.70 (+1.88)
     - produced sound, acousticness 0.35 (+0.33)

2. Sunrise City by Neon Echo  [pop, happy]
   Score: 3.17
     - mood match: happy (+1.0)
     - energy 0.82 vs target 0.70 (+1.76)
     - produced sound, acousticness 0.18 (+0.41)

3. Night Drive Loop by Neon Echo  [synthwave, moody]
   Score: 2.29
     - energy 0.75 vs target 0.70 (+1.90)
     - produced sound, acousticness 0.22 (+0.39)

4. Concrete Echoes by Blockwise  [hip hop, confident]
   Score: 2.28
     - energy 0.78 vs target 0.70 (+1.84)
     - produced sound, acousticness 0.12 (+0.44)

5. Island Time by Coral Sound System  [reggae, uplifting]
   Score: 2.04
     - energy 0.58 vs target 0.70 (+1.76)
     - produced sound, acousticness 0.45 (+0.28)

================================================================
Profile: EDGE: Acoustic Metalhead
  genre=metal, mood=angry, energy=0.95, likes_acoustic=True
================================================================
1. Iron Tide by Grave Signal  [metal, angry]
   Score: 3.98
     - genre match: metal (+1.0)
     - mood match: angry (+1.0)
     - energy 0.97 vs target 0.95 (+1.96)
     - acoustic sound, acousticness 0.03 (+0.01)

2. Strobe Heart by Pulse Theory  [edm, euphoric]
   Score: 2.01
     - energy 0.95 vs target 0.95 (+2.00)
     - acoustic sound, acousticness 0.02 (+0.01)

3. Gym Hero by Max Pulse  [pop, intense]
   Score: 1.99
     - energy 0.93 vs target 0.95 (+1.96)
     - acoustic sound, acousticness 0.05 (+0.03)

4. Storm Runner by Voltline  [rock, intense]
   Score: 1.97
     - energy 0.91 vs target 0.95 (+1.92)
     - acoustic sound, acousticness 0.10 (+0.05)

5. Sunrise City by Neon Echo  [pop, happy]
   Score: 1.83
     - energy 0.82 vs target 0.95 (+1.74)
     - acoustic sound, acousticness 0.18 (+0.09)

```

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
