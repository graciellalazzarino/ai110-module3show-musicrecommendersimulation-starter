# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeCheck 1.0**

---

## 2. Intended Use  

VibeCheck suggests the top 5 songs from a small catalog that best match one listener's stated taste: a favorite genre, a favorite mood, how energetic they want the music to be, and whether they like an acoustic or a produced sound. It assumes the listener can describe their taste in those four simple terms and that their taste does not change with time of day or activity.

It is built for **classroom exploration**: to show how a recommender turns data into a ranked list and where that process goes wrong.

**Not intended for:**
- Real users or a real music app. The catalog is 18 made-up songs, and the system has no idea what anyone actually listened to.
- Deciding what music is "good" or which artists deserve exposure. The scores only measure closeness to one profile.
- Listeners with mixed tastes (e.g. both lofi and metal), since a profile holds only one genre and one mood.

---

## 3. How the Model Works  

Think of VibeCheck as a judge who looks at every song in the catalog, one at a time, and gives it points:

- **2 points** if the song's genre is exactly the listener's favorite genre.
- **1 point** if the song's mood is exactly the listener's favorite mood.
- **Up to 1 point** for energy: the closer the song's energy is to what the listener wants, the more points. A perfect match gets the full point; a song that is much calmer or much louder than requested gets fewer. It rewards *closeness*, not just "louder is better."
- **Up to half a point** for sound: listeners who like acoustic music get more points for acoustic songs, and listeners who don't get more points for produced, electronic-sounding songs.

After every song has a score, the judge sorts them from highest to lowest and returns the top 5, along with the reasons each song earned its points.

**Changes from the starter:** the starter code returned the first 5 songs in the file with a placeholder explanation. I wrote the CSV loader, the scoring rule above, the ranking step, and explanations for every score, and made the starter's `Recommender` class use the same scoring rule so both versions agree.

---

## 4. Data  

- **18 songs**: the 10 from the starter plus 8 I added (ids 11–18).
- **15 genres**: pop, indie pop, lofi, rock, metal, edm, synthwave, hip hop, r&b, reggae, country, folk, jazz, classical, ambient.
- **14 moods**: happy, chill, intense, relaxed, moody, focused, confident, melancholy, angry, nostalgic, euphoric, romantic, uplifting, sad.
- Each song also has numbers from 0 to 1 for energy, valence, danceability, and acousticness, plus a tempo in beats per minute.

I added the 8 new songs to cover genres and moods the starter file was missing, especially sad and angry moods and low-energy styles like classical and folk.

**Missing from the data:** lyrics, language, artist popularity, release year, and any listening history. Most genres have only one song, so the data cannot represent the variety *within* a genre (for example, not all rock is intense). All songs and artists are made up.

---

## 5. Strengths  

- **Clear, single-genre tastes work well.** Happy Pop, Chill Lofi, Deep Intense Rock, and even Acoustic Metalhead each get the obvious best song at #1 with a score above 4.0.
- **Energy closeness behaves the way a person would expect.** The Chill Lofi listener never sees a loud song in their top 5, and the Happy Pop listener never sees a sleepy one. Happy Pop and Chill Lofi share zero songs in their top 5.
- **Every recommendation explains itself.** Each result lists exactly where its points came from (e.g. "genre match: pop (+2.0)"), which made it easy to spot the Gym Hero problem.
- **It degrades gracefully.** A listener whose genre isn't in the catalog (k-pop) still gets a sensible list of happy, upbeat songs because mood and energy take over.

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

- **Scoring that changes per genre.** Instead of one set of weights for everyone, give each genre its own. A pop listener's list could weigh mood more heavily than the "pop" label, so an intense workout song can't outrank a happy one just by sharing the genre.
- **Partial genre matches.** Give some points when genres are related (pop and indie pop, rock and metal) instead of all-or-nothing text matching.
- **A diversity rule in the ranking step.** Limit the top 5 to one or two songs per genre or artist so a single song like Gym Hero can't appear in almost every list.
- **Lower the genre weight or raise mood.** The experiment showed that a stronger energy weight fixed the Happy Pop list; giving mood more weight would likely fix it more directly.
- **More songs per genre and more features.** Use valence (how positive a song sounds) to help the "sad" profiles, and support listeners with more than one favorite genre.

---

## 9. Personal Reflection  

<!-- DRAFT: rewrite this in your own words and add your own details before submitting. -->

**Biggest learning moment:** I really questioned why Gym Hero scored higher than Rooftop Lights for a happy pop listener, so I took a deeper look at its score breakdown. It wasn't a bug: Gym Hero got 2 points just for being labeled pop, which is more than a happy song gets for matching the mood. Every rule seemed reasonable on its own, but together they let one loud pop song show up in 5 of 6 lists. The weights are a design choice with real consequences, not just numbers.

**How AI helped, and when I had to double-check:** The AI assistant was fast at explaining collaborative vs. content-based filtering, writing the CSV loader, and running the profiles and the weight experiment. It also caught that the starter `main.py` import would break `python -m src.main`. But I didn't just accept the rankings it produced. When Gym Hero kept appearing, I questioned the result and used the reasons printed for each song to trace exactly where its points came from.

**What surprised me:** How much a four-rule point system *feels* like a real recommendation. It also surprised me that the edge-case profiles didn't crash anything; they just gave confident, wrong answers, which is harder to notice than an error.

**What I'd try next:** Change the scoring per genre. One fixed set of weights treats every listener the same, but genre probably matters differently depending on the music: for pop, mood and vibe may matter more than the genre label, while for something like metal or classical the genre itself says a lot. Giving each genre its own weights would have stopped Gym Hero from winning on the "pop" label alone. I'd also add a diversity penalty so the same song can't dominate every list.
