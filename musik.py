"""Musik latar Reels, dibuat sendiri (tanpa lagu berhak cipta, aman untuk akun bisnis).
Lagu hymn yang dipakai sudah public domain; aransemen & rekamannya dibuat di sini dengan synth sederhana.

  python3 musik.py            # buat semua lagu -> output/musik/*.wav
  python3 musik.py pasang     # pasang musik ke semua Reels yang belum diposting (lihat PILIH_LAGU)

Lagu:
  amazing     Amazing Grace (John Newton, 1779 / New Britain) - piano
  yesus       Jesus Loves Me (W. Bradbury, 1862) - music box + piano
  joyful      Joyful, Joyful (Beethoven, Ode to Joy) - lonceng lembut (Eli pagi)
  kapi        Joyful, Joyful versi ceria: petik, bass, tepuk tangan (Kapi)
  teduh       piano worship lembut, D mayor (komposisi sendiri)
  fajar       piano penuh harapan, C mayor (komposisi sendiri)
  malam       piano malam pelan, A minor (komposisi sendiri)
"""
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
OUT = ROOT / "output"
SR = 44100
NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def hz(name):
    """'F#4' -> frekuensi."""
    n, octv = name[:-1], int(name[-1])
    semi = NOTE[n[0]] + (1 if "#" in n else -1 if n.endswith("b") and len(n) > 1 else 0)
    return 440.0 * 2 ** ((semi + 12 * (octv + 1) - 69) / 12)


CHORD = {  # nada akor (oktaf 3) untuk iringan
    "C": ["C3", "G3", "E4"], "G": ["G2", "D3", "B3"], "D": ["D3", "A3", "F#4"], "Em": ["E3", "B3", "G4"],
    "F": ["F2", "C3", "A3"], "Am": ["A2", "E3", "C4"], "Bm": ["B2", "F#3", "D4"], "A/C#": ["C#3", "A3", "E4"],
    "G7": ["G2", "F3", "B3"], "Dm": ["D3", "A3", "F4"], "Bb": ["Bb2", "F3", "D4"], "Fmaj7": ["F2", "C3", "E4"],
    "Am7": ["A2", "G3", "C4"], "Cmaj7": ["C3", "G3", "B3"], "Gsus": ["G2", "D3", "C4"],
}


# ---------- instrumen ----------

def env(n, attack=0.004, decay=1.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / attack) * np.exp(-t / decay)


def piano(f, dur, vel=0.5):
    n = int(SR * (dur + 1.6))
    t = np.arange(n) / SR
    out = np.zeros(n)
    for k in range(1, 9):
        fk = f * k * (1 + 0.0004 * k * k)  # sedikit inharmonis seperti senar
        if fk > 12000:
            break
        out += np.sin(2 * np.pi * fk * t) * (1 / k ** 1.4) * np.exp(-t * (0.9 + 0.55 * k) * (f / 260) ** 0.35)
    out *= np.minimum(1, t / 0.005)
    rel = np.clip(1 - (t - dur) / 0.35, 0, 1) ** 2  # lepas tuts
    return out * rel * vel * 0.32


def bell(f, dur, vel=0.5):
    n = int(SR * (dur + 2.0))
    t = np.arange(n) / SR
    out = sum(np.sin(2 * np.pi * f * r * t) * a * np.exp(-t * d) for r, a, d in ((1, 1.0, 1.6), (2.0, 0.35, 3.0), (3.0, 0.12, 5.0), (4.2, 0.08, 7.0)))
    return out * np.minimum(1, t / 0.002) * vel * 0.28


def pluck(f, dur, vel=0.5):
    n = int(SR * (dur + 0.4))
    t = np.arange(n) / SR
    out = sum(np.sin(2 * np.pi * f * k * t) * (0.9 ** k) / k * np.exp(-t * (5 + 3 * k)) for k in range(1, 7))
    return out * np.minimum(1, t / 0.002) * np.clip(1 - (t - dur) / 0.1, 0, 1) * vel * 0.45


def bass(f, dur, vel=0.5):
    n = int(SR * (dur + 0.2))
    t = np.arange(n) / SR
    out = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)
    return out * np.minimum(1, t / 0.01) * np.exp(-t * 2.5) * np.clip(1 - (t - dur) / 0.08, 0, 1) * vel * 0.5


def pad(f, dur, vel=0.5):
    n = int(SR * (dur + 1.0))
    t = np.arange(n) / SR
    out = sum(np.sin(2 * np.pi * f * dt * t + ph) for dt, ph in ((1, 0), (1.003, 1.1), (0.997, 2.3), (2.0, 0.4)))
    a = np.minimum(1, t / 0.9) * np.clip(1 - (t - dur) / 1.0, 0, 1)
    return out * a * vel * 0.05


def clap(dur=0.2, vel=0.5, rng=np.random.default_rng(1)):
    n = int(SR * 0.25)
    t = np.arange(n) / SR
    noise = rng.normal(0, 1, n)
    noise = np.convolve(noise, [1, -0.9], "same")  # buang frekuensi rendah
    burst = sum(np.exp(-np.clip(t - o, 0, None) * 60) * (t >= o) for o in (0, 0.011, 0.022))
    return noise * burst * vel * 0.18


def shaker(vel=0.3, rng=np.random.default_rng(2)):
    n = int(SR * 0.08)
    t = np.arange(n) / SR
    return np.convolve(rng.normal(0, 1, n), [1, -1], "same") * np.exp(-t * 60) * vel * 0.08


# ---------- susun lagu ----------

class Lagu:
    def __init__(self, bpm, seconds):
        self.beat = 60 / bpm
        self.buf = np.zeros(int(SR * (seconds + 4)))

    def add(self, sound, at_beat, gain=1.0):
        i = int(at_beat * self.beat * SR)
        if i >= len(self.buf):
            return
        seg = sound[: len(self.buf) - i]
        self.buf[i:i + len(seg)] += seg * gain

    def melody(self, inst, notes, start=0.0, vel=0.55):
        b = start
        for nm, beats in notes:
            if nm != "-":
                self.add(inst(hz(nm), beats * self.beat * 0.95, vel), b)
            b += beats
        return b

    def arpeggio(self, inst, chords, beats_per_bar, start=0.0, pattern=(0, 1, 2, 1), step=0.5, vel=0.32):
        b = start
        for ch in chords:
            notes = CHORD[ch]
            for k in range(int(beats_per_bar / step)):
                self.add(inst(hz(notes[pattern[k % len(pattern)]]), step * self.beat * 1.8, vel * (1.0 if k == 0 else 0.75)), b + k * step)
            b += beats_per_bar
        return b


def reverb(x, seconds=2.4, wet=0.28, seed=3):
    rng = np.random.default_rng(seed)
    n = int(SR * seconds)
    t = np.arange(n) / SR
    out = []
    for ch in range(2):  # stereo: IR berbeda tiap kanal
        ir = rng.normal(0, 1, n) * np.exp(-t / (seconds / 5))
        ir[: int(SR * 0.012)] = 0
        ir /= np.sqrt((ir ** 2).sum())
        size = 1 << int(np.ceil(np.log2(len(x) + n)))
        y = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[: len(x)]
        out.append(x * (1 - wet) + y * wet * 2.2)
    return np.stack(out, 1)


def tulis(stereo, name):
    stereo = stereo / (np.abs(stereo).max() + 1e-9) * 0.7
    path = OUT / "musik" / f"{name}.wav"
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((stereo * 32767).astype(np.int16).tobytes())
    return path


# Amazing Grace (G mayor, 3/4). (nada, ketukan)
AMAZING = [("D4", 1),
           ("G4", 2), ("B4", .5), ("G4", .5), ("B4", 2), ("A4", 1), ("G4", 2), ("E4", 1), ("D4", 2), ("D4", 1),
           ("G4", 2), ("B4", .5), ("G4", .5), ("B4", 2), ("A4", 1), ("D5", 5), ("B4", 1),
           ("D5", 2), ("B4", .5), ("G4", .5), ("B4", 2), ("A4", 1), ("G4", 2), ("E4", 1), ("D4", 2), ("D4", 1),
           ("G4", 2), ("B4", .5), ("G4", .5), ("B4", 2), ("A4", 1), ("G4", 3), ("-", 3)]
AMAZING_AKOR = ["G", "G", "C", "G", "G", "Em", "D", "G", "G", "G", "C", "G", "G", "D", "G", "G"]

# Jesus Loves Me (C mayor, 4/4), bait
YESUS = [("G4", 1), ("E4", 1), ("E4", 1), ("D4", 1), ("E4", 1), ("G4", 1), ("G4", 2),
         ("A4", 1), ("A4", 1), ("C5", 1), ("A4", 1), ("A4", 1), ("G4", 1), ("G4", 2),
         ("G4", 1), ("E4", 1), ("E4", 1), ("D4", 1), ("E4", 1), ("G4", 1), ("G4", 2),
         ("A4", 1), ("A4", 1), ("G4", 1), ("C5", 1), ("E4", 1), ("D4", 1), ("C4", 2)]
YESUS_AKOR = ["C", "C", "F", "C", "C", "C", "F", "C"]

# Joyful, Joyful / Ode to Joy (C mayor, 4/4)
JOYFUL = [("E4", 1), ("E4", 1), ("F4", 1), ("G4", 1), ("G4", 1), ("F4", 1), ("E4", 1), ("D4", 1),
          ("C4", 1), ("C4", 1), ("D4", 1), ("E4", 1), ("E4", 1.5), ("D4", .5), ("D4", 2),
          ("E4", 1), ("E4", 1), ("F4", 1), ("G4", 1), ("G4", 1), ("F4", 1), ("E4", 1), ("D4", 1),
          ("C4", 1), ("C4", 1), ("D4", 1), ("E4", 1), ("D4", 1.5), ("C4", .5), ("C4", 2)]
JOYFUL_AKOR = ["C", "G", "C", "G", "C", "G", "C", "G"]


def up(notes, octaves=1):
    return [(n if n == "-" else n[:-1] + str(int(n[-1]) + octaves), b) for n, b in notes]


def buat_amazing(seconds=48):
    L = Lagu(76, seconds)
    b = 0
    while b * L.beat < seconds:
        L.arpeggio(piano, AMAZING_AKOR, 3, b + 1, pattern=(0, 1, 2, 1, 2, 1), step=0.5, vel=0.22)
        b = L.melody(piano, AMAZING, b, vel=0.6)
    return tulis(reverb(L.buf, 2.8, 0.32), "amazing")


def buat_yesus(seconds=40):
    L = Lagu(84, seconds)
    b = 0
    while b * L.beat < seconds:
        L.arpeggio(piano, YESUS_AKOR, 4, b, pattern=(0, 2, 1, 2), step=1, vel=0.2)
        L.melody(bell, up(YESUS), b, vel=0.45)
        b = L.melody(piano, YESUS, b, vel=0.25)
    return tulis(reverb(L.buf, 2.4, 0.3), "yesus")


def buat_joyful(seconds=36):
    L = Lagu(96, seconds)
    b = 0
    while b * L.beat < seconds:
        L.arpeggio(piano, JOYFUL_AKOR, 4, b, pattern=(0, 1, 2, 1), step=1, vel=0.2)
        b = L.melody(bell, up(JOYFUL), b, vel=0.5)
    return tulis(reverb(L.buf, 2.0, 0.25), "joyful")


def buat_kapi(seconds=36):
    L = Lagu(116, seconds)
    b = 0
    while b * L.beat < seconds:
        for bar, ch in enumerate(JOYFUL_AKOR):
            root = CHORD[ch][0]
            for k in range(4):
                bb = b + bar * 4 + k
                L.add(bass(hz(root[:-1] + "2"), L.beat * 0.45, 0.6), bb)
                L.add(pluck(hz(CHORD[ch][1 + k % 2]), L.beat * 0.3, 0.35), bb + 0.5)
                L.add(pluck(hz(CHORD[ch][2]), L.beat * 0.3, 0.3), bb + 0.5)
                if k in (1, 3):
                    L.add(clap(vel=0.7), bb)
                L.add(shaker(), bb + 0.5)
        b = L.melody(pluck, up(JOYFUL), b, vel=0.55)
    return tulis(reverb(L.buf, 1.2, 0.15), "kapi")


def buat_original(name, bpm, chords, top, seconds=48, beats_per_bar=4):
    """Piano worship: akor dipecah (arpeggio) + beberapa nada atas yang jarang + pad lembut."""
    L = Lagu(bpm, seconds)
    b = 0
    while b * L.beat < seconds:
        for i, ch in enumerate(chords):
            for nt in CHORD[ch]:
                L.add(pad(hz(nt), beats_per_bar * L.beat, 0.5), b + i * beats_per_bar)
            L.add(piano(hz(CHORD[ch][0][:-1] + str(int(CHORD[ch][0][-1]) - 1)), beats_per_bar * L.beat, 0.3), b + i * beats_per_bar)
            for k, nt in enumerate(top[i]):
                if nt != "-":
                    L.add(piano(hz(nt), 1.5 * L.beat, 0.42), b + i * beats_per_bar + k * (beats_per_bar / len(top[i])))
        b = L.arpeggio(piano, chords, beats_per_bar, b, pattern=(0, 1, 2, 1, 2, 1, 0, 1), step=0.5, vel=0.24)
    return tulis(reverb(L.buf, 3.0, 0.35), name)


def buat_semua():
    return [buat_amazing(), buat_yesus(), buat_joyful(), buat_kapi(),
            buat_original("teduh", 68, ["D", "A/C#", "Bm", "G"], [["F#5", "-"], ["E5", "-"], ["D5", "F#5"], ["B4", "-"]]),
            buat_original("fajar", 78, ["C", "G", "Am", "F"], [["E5", "G5"], ["D5", "-"], ["C5", "E5"], ["A4", "C5"]]),
            buat_original("malam", 60, ["Am7", "Fmaj7", "Cmaj7", "Gsus"], [["E5", "-"], ["C5", "-"], ["G5", "E5"], ["D5", "-"]])]


# ---------- lagu unik per Reels (tidak ada dua Reels dengan musik yang sama) ----------

def mhz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def midi(name):
    return int(round(69 + 12 * np.log2(hz(name) / 440.0)))


QUAL = {"M": [0, 4, 7], "m": [0, 3, 7], "M7": [0, 4, 7, 11], "m7": [0, 3, 7, 10], "sus": [0, 5, 7], "add9": [0, 4, 7, 14]}
PROGS = [
    [(0, "M"), (7, "M"), (9, "m"), (5, "M")], [(9, "m"), (5, "M"), (0, "M"), (7, "M")], [(0, "M"), (9, "m"), (5, "M"), (7, "M")],
    [(0, "M7"), (5, "M7"), (0, "M7"), (5, "M7")], [(5, "M"), (7, "M"), (4, "m"), (9, "m")], [(0, "add9"), (4, "m"), (5, "M"), (7, "sus")],
    [(2, "m7"), (7, "M"), (0, "M7"), (9, "m7")], [(0, "M"), (7, "M"), (9, "m"), (4, "m"), (5, "M"), (0, "M"), (5, "M"), (7, "M")],
    [(9, "m7"), (2, "m7"), (7, "sus"), (0, "M7")], [(0, "M"), (5, "add9"), (9, "m7"), (7, "sus")], [(5, "M7"), (4, "m7"), (2, "m7"), (0, "add9")],
    [(0, "M"), (2, "m"), (5, "M"), (0, "M")],
]
PENTA = [0, 2, 4, 7, 9]
RHYTHMS = [[1, 1, 2], [2, 1, 1], [1.5, .5, 2], [1, 1, 1, 1], [3, 1], [.5, .5, 1, 2], [2, 2], [1, .5, .5, 2]]


def felt(f, dur, vel=0.5):  # piano redup (felt piano): harmonik atas dipotong, serangan lembut
    n = int(SR * (dur + 1.8))
    t = np.arange(n) / SR
    out = sum(np.sin(2 * np.pi * f * k * t) * (1 / k ** 2.2) * np.exp(-t * (0.7 + 0.8 * k)) for k in range(1, 5))
    return out * np.minimum(1, t / 0.02) * np.clip(1 - (t - dur) / 0.5, 0, 1) * vel * 0.4


def musicbox(f, dur, vel=0.5):
    return bell(f * 2, dur * 0.6, vel * 0.8)


def marimba(f, dur, vel=0.5):
    n = int(SR * (dur + 0.6))
    t = np.arange(n) / SR
    out = np.sin(2 * np.pi * f * t) * np.exp(-t * 6) + 0.25 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 18)
    return out * np.minimum(1, t / 0.002) * vel * 0.5


def strings(f, dur, vel=0.5):
    n = int(SR * (dur + 1.2))
    t = np.arange(n) / SR
    vib = 1 + 0.004 * np.sin(2 * np.pi * 5.2 * t)
    out = sum(np.sin(2 * np.pi * f * k * vib * t) / k ** 1.6 for k in range(1, 6))
    return out * np.minimum(1, t / 0.5) * np.clip(1 - (t - dur) / 1.2, 0, 1) * vel * 0.06


HYMN = {"amazing": (AMAZING, 3, 67), "yesus": (YESUS, 4, 60), "joyful": (JOYFUL, 4, 60)}  # (melodi, ketukan/bar, nada dasar)


def gen_melody(rng, prog, key, bars_per_chord, bpb):
    """Melodi baru: motif 2 bar diulang dengan variasi (A A' B A), nada dari pentatonik + nada akor."""
    def motif():
        notes, b = [], 0
        while b < 2 * bpb:
            rh = RHYTHMS[rng.integers(len(RHYTHMS))]
            for d in rh:
                if b + d > 2 * bpb:
                    d = 2 * bpb - b
                if d <= 0:
                    break
                deg = PENTA[rng.integers(5)] + 12 * int(rng.integers(0, 2))
                notes.append((key + 12 + deg if rng.random() > 0.12 else None, d))
                b += d
        return notes
    a, bm = motif(), motif()
    var = [(n + (2 if n is not None and rng.random() < 0.3 else 0), d) if n else (n, d) for n, d in a]
    return a + var + bm + a


def lagu_unik(rel, seconds, used):
    """Susun lagu khusus untuk satu Reels (seed = nama file). Gaya menyesuaikan akun & jenis Reels."""
    seed = abs(hash(rel)) % (2 ** 32)
    import zlib
    seed = zlib.crc32(rel.encode())
    for attempt in range(20):
        rng = np.random.default_rng(seed + attempt)
        name = Path(rel).stem
        if "/kapi" in rel:
            mood, bpm, insts = "ceria", int(rng.integers(100, 126)), [pluck, marimba]
        elif "/eli" in rel:
            mood = "tidur" if "malam" in name else "anak"
            bpm = int(rng.integers(62, 76)) if mood == "tidur" else int(rng.integers(84, 104))
            insts = [musicbox, bell, felt] if mood == "tidur" else [bell, marimba, piano]
        else:
            mood, bpm, insts = "teduh", int(rng.integers(56, 82)), [piano, felt, musicbox, strings]
        key = int(rng.integers(0, 12)) + 48  # C3..B3
        hymn = None
        if rng.random() < 0.3:
            hymn = {"ceria": "joyful", "anak": ["joyful", "yesus"][rng.integers(2)], "tidur": "yesus"}.get(mood, ["amazing", "yesus"][rng.integers(2)])
        prog = PROGS[rng.integers(len(PROGS))]
        lead = insts[rng.integers(len(insts))]
        comp = [piano, felt, strings][rng.integers(3)] if mood != "ceria" else pluck
        sig = (hymn, PROGS.index(prog), key % 12, bpm, lead.__name__, comp.__name__)
        if sig not in used:
            used.add(sig)
            break
    L = Lagu(bpm, seconds)
    bpb = 3 if hymn == "amazing" else 4
    if hymn:
        mel, bpb, base = HYMN[hymn]
        shift = key + 12 - base
        notes = [(None if nm == "-" else midi(nm) + shift, d) for nm, d in mel]
        chords = {"amazing": AMAZING_AKOR, "yesus": YESUS_AKOR, "joyful": JOYFUL_AKOR}[hymn]
        prog = [(midi(CHORD[c][0]) % 12 - base % 12 + (4 if False else 0), "m" if c in ("Em", "Am", "Bm", "Dm") else "M") for c in chords]
        start_offset = 1 if hymn == "amazing" else 0
    else:
        notes = gen_melody(rng, prog, key, 1, bpb)
        start_offset = 0
    b = 0
    total_beats = seconds / L.beat + 4
    while b < total_beats:
        for i, (deg, q) in enumerate(prog):
            root = key + deg % 12 + (12 if (key + deg % 12) < 52 else 0)
            tones = [root + x for x in QUAL[q]]
            at = b + start_offset + i * bpb
            if mood == "ceria":
                for k in range(bpb):
                    L.add(bass(mhz(root - 12), L.beat * 0.45, 0.6), at + k)
                    L.add(comp(mhz(tones[1 + k % 2]), L.beat * 0.3, 0.3), at + k + 0.5)
                    if k % 2 == 1:
                        L.add(clap(vel=0.6), at + k)
                    L.add(shaker(), at + k + 0.5)
            else:
                L.add(felt(mhz(root - 12), bpb * L.beat, 0.35), at)
                pat = [0, 1, 2, 1, 2, 1, 0, 1][: int(bpb / 0.5)] if rng.random() < 0.7 else [0, 2, 1, 2][:bpb]
                step = bpb / len(pat)
                for k, pi in enumerate(pat):
                    L.add(comp(mhz(tones[pi % len(tones)]), step * L.beat * 1.8, 0.22 if k else 0.28), at + k * step)
                if lead is not strings:
                    for tn in tones[:3]:
                        L.add(pad(mhz(tn), bpb * L.beat, 0.35), at)
        mb = b
        for m_note, d in notes:
            if m_note is not None:
                L.add(lead(mhz(m_note), d * L.beat * 0.95, 0.5), mb)
            mb += d
        b += max(len(prog) * bpb, mb - b)
    wet = 0.15 if mood == "ceria" else 0.3 + 0.1 * rng.random()
    return tulis(reverb(L.buf, 1.3 if mood == "ceria" else 2.6, wet, seed=seed % 1000), "unik/" + rel.replace("/", "_")[:-4]), sig


# ---------- pasang ke Reels ----------

def pilih_lagu(rel):
    """Cocokkan lagu dengan jenis Reels."""
    name = Path(rel).stem
    if "/eli" in rel:
        return "yesus" if "malam" in name else "joyful"
    if "/kapi" in rel:
        return "kapi"
    if name.startswith("jalan"):
        return "amazing"
    if name.startswith("kinetik"):
        return ["fajar", "amazing", "teduh"][int("".join(c for c in name if c.isdigit()) or 0) % 3]
    if name.startswith("suasana"):
        return "malam"
    if name.startswith("notif"):
        return "teduh"
    if name.startswith("dinding"):
        return "fajar"
    return "teduh"


def durasi(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                                capture_output=True, text=True).stdout.strip())


def punya_audio(path):
    return "audio" in subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type", "-of", "csv=p=0", str(path)],
                                     capture_output=True, text=True).stdout


def pasang(rel, lagu):
    """Ganti suara Reels dengan lagu (fade in/out). Bunyi 'ting' notifikasi tetap terdengar di atas musik."""
    src = OUT / rel
    tmp = src.with_name(src.stem + "_musik.mp4")
    d = durasi(src)
    music = f"[1:a]atrim=0:{d:.2f},afade=t=in:d=0.6,afade=t=out:st={max(0, d - 1.8):.2f}:d=1.8,volume=0.9[m]"
    if Path(rel).stem.startswith("notif") and punya_audio(src):
        fc, amap = music + ";[0:a]volume=1.0[t];[m][t]amix=inputs=2:duration=first:normalize=0[a]", "[a]"
    else:
        fc, amap = music, "[m]"
    wav = Path(lagu) if str(lagu).endswith(".wav") else OUT / "musik" / f"{lagu}.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-i", str(wav),
                    "-filter_complex", fc, "-map", "0:v", "-map", amap, "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                    "-movflags", "+faststart", str(tmp)], check=True)
    tmp.replace(src)
    return rel


def pasang_semua():
    """Semua Reels di jadwal yang belum diposting -> diberi musik. Mengembalikan daftar file yang diubah."""
    schedule = json.loads((OUT / "schedule.json").read_text())
    posted = json.loads((ROOT / "state/posted.json").read_text())
    done, changed, used = set(), [], set()
    for it in schedule:
        for f in it["files"]:
            if f.endswith(".mp4") and f.startswith("reels/") and it["id"] not in posted and f not in done:
                done.add(f)
                wav, sig = lagu_unik(f, durasi(OUT / f) + 1, used)
                changed.append(pasang(f, str(wav)))
                print(f, "<-", sig)
    return changed


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "pasang":
        pasang_semua()
    else:
        for p in buat_semua():
            print(p)
