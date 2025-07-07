from fastapi import FastAPI, File, UploadFile, HTTPException
import speech_recognition as sr
import google.generativeai as genai
import json
from fastapi.middleware.cors import CORSMiddleware

template = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="color-scheme" content="light dark">
    <meta name="print-color-adjust" content="exact">
    <title>CV - Giovanni Carrozza</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --blu-scuro: #0a2d4d;
            --blu-primario: #0077cc;
            --blu-chiaro-accento: #7ac5ff;
            --grigio-sfondo-chiaro: #f8f9fa;
            --grigio-testo: #495057;
            --grigio-testo-chiaro: #6c757d;
            --bianco: #ffffff;
            --font-principale: 'Poppins', sans-serif;
        }

        body {
            font-family: var(--font-principale);
            background-color: #e0e0e0;
            color: var(--grigio-testo);
            margin: 0;
            padding: 0;
            font-size: 10pt;
            line-height: 1.6;
        }

        .cv-container {
            display: flex;
            width: 210mm;
            min-height: 297mm;
            margin: 30px auto;
            background-color: var(--grigio-sfondo-chiaro);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
            border-radius: 8px;
            overflow: hidden;
        }

        /* --- SIDEBAR (COLONNA SINISTRA) --- */
        .sidebar {
            width: 38%;
            background-color: var(--blu-scuro);
            color: var(--bianco);
            padding: 40px 25px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
        }

        .profile-header {
            text-align: center;
            margin-bottom: 30px;
        }

        /* .profile-pic (rimosso come richiesto) */
        /* Stili originali:
        .profile-pic {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            border: 4px solid var(--blu-primario);
            margin: 0 auto 15px;
            object-fit: cover;
            background-color: #ccc;
            display: flex;
            align-items: center;
            justify-content: center;
            fill: var(--blu-chiaro-accento);
        }
        .profile-pic svg {
            width: 70%;
            height: 70%;
            fill: var(--bianco);
        }
        */

        .profile-name {
            font-size: 24pt;
            font-weight: 700;
            margin: 0;
            line-height: 1.2;
            color: var(--bianco);
        }

        .profile-title {
            font-size: 11pt;
            font-weight: 300;
            color: var(--blu-chiaro-accento);
            margin-top: 5px;
            letter-spacing: 0.5px;
        }

        .sidebar-section {
            margin-bottom: 30px;
        }

        .sidebar-section h3 {
            font-size: 14pt;
            font-weight: 600;
            color: var(--bianco);
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid var(--blu-primario);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .sidebar-section h3 svg {
            width: 20px;
            height: 20px;
            fill: var(--blu-chiaro-accento);
        }

        .contact-item {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
            font-size: 9.5pt;
        }

        .contact-item svg {
            width: 16px;
            height: 16px;
            fill: var(--blu-chiaro-accento);
            flex-shrink: 0;
        }

        .contact-item a {
            color: var(--bianco);
            text-decoration: none;
            word-break: break-all;
        }
        .contact-item a:hover {
            color: var(--blu-chiaro-accento);
        }

        .skill-item {
            margin-bottom: 15px;
        }

        .skill-item p {
            margin: 0 0 5px 0;
            font-weight: 400;
        }

        .skill-bar-bg {
            width: 100%;
            height: 8px;
            background-color: rgba(0, 0, 0, 0.2);
            border-radius: 4px;
            overflow: hidden;
        }

        .skill-bar-fill {
            height: 100%;
            background-color: var(--blu-chiaro-accento);
            border-radius: 4px;
        }

        .software-list, .interests-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .software-list li, .interests-list li {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 8px;
        }

        .software-list li svg, .interests-list li svg {
            width: 16px; height: 16px; fill: var(--blu-chiaro-accento);
        }

        /* --- MAIN CONTENT (COLONNA DESTRA) --- */
        .main-content {
            width: 62%;
            padding: 40px;
            box-sizing: border-box;
            background-color: var(--bianco);
        }

        .main-section {
            margin-bottom: 35px;
        }

        .main-section h2 {
            font-size: 18pt;
            font-weight: 700;
            color: var(--blu-scuro);
            margin: 0 0 15px 0;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .main-section h2 svg {
            width: 28px;
            height: 28px;
            fill: var(--blu-primario);
        }

        .section-divider {
            margin: 20px 0;
            border: 0;
            height: 3px;
            background-image: linear-gradient(to right, var(--blu-primario), var(--grigio-sfondo-chiaro));
        }

        .profile-summary p {
            margin: 0;
        }

        /* Timeline per Esperienza e Formazione */
        .timeline {
            position: relative;
            padding-left: 30px;
            border-left: 3px solid var(--blu-primario);
        }

        .timeline-item {
            position: relative;
            margin-bottom: 25px;
        }

        .timeline-item:last-child {
            margin-bottom: 0;
        }

        .timeline-item::before {
            content: '';
            position: absolute;
            left: -39px;
            top: 5px;
            width: 15px;
            height: 15px;
            border-radius: 50%;
            background-color: var(--bianco);
            border: 3px solid var(--blu-primario);
            z-index: 1;
        }

        .timeline-date {
            font-size: 9pt;
            font-weight: 600;
            color: var(--blu-primario);
            margin-bottom: 2px;
        }

        .timeline-title {
            font-size: 13pt;
            font-weight: 600;
            color: var(--blu-scuro);
            margin: 0;
        }

        .timeline-subtitle {
            font-size: 10pt;
            font-weight: 400;
            color: var(--grigio-testo-chiaro);
            margin: 2px 0 10px 0;
            font-style: italic;
        }

        .timeline-details {
            padding-left: 20px;
            margin: 0;
            list-style: none;
        }

        .timeline-details li {
            position: relative;
            margin-bottom: 5px;
            font-size: 9.5pt;
        }

        .timeline-details li::before {
            content: '›';
            position: absolute;
            left: -15px;
            font-weight: 700;
            color: var(--blu-primario);
        }

        .skills-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px;
        }

        .skill-category h4 {
            font-size: 11pt;
            font-weight: 600;
            color: var(--blu-scuro);
            margin: 0 0 10px 0;
            border-bottom: 1px solid #eee;
            padding-bottom: 5px;
        }

        .skill-tag {
            display: inline-block;
            background-color: var(--grigio-sfondo-chiaro);
            color: var(--grigio-testo);
            padding: 4px 10px;
            border-radius: 15px;
            margin: 3px;
            font-size: 9pt;
            border: 1px solid #e0e0e0;
        }
        @media print {
            /* Forza i colori di stampa */
            * {
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }

            /* Mantiene lo sfondo blu scuro nella sidebar */
            .sidebar {
                background-color: var(--blu-scuro) !important;
                color: var(--bianco) !important;
                print-color-adjust: exact !important;
            }

            /* Assicura che il testo rimanga bianco */
            .sidebar, .sidebar h3, .sidebar p, .sidebar a {
                color: var(--bianco) !important;
            }

            /* Mantiene i colori degli elementi della timeline */
            .timeline-item::before {
                background-color: var(--bianco) !important;
                border-color: var(--blu-primario) !important;
            }

            /* Mantiene i colori delle barre delle competenze */
            .skill-bar-fill {
                background-color: var(--blu-chiaro-accento) !important;
            }

            /* Mantiene i colori delle icone */
            .sidebar svg {
                fill: var(--blu-chiaro-accento) !important;
            }

            /* Assicura che il documento si adatti correttamente alla pagina */
            .cv-container {
                width: 100%;
                margin: 0;
                box-shadow: none;
            }

            /* Evita interruzioni di pagina indesiderate */
            .sidebar, .main-content {
                page-break-inside: avoid;
            }
        }
    </style>
</head>
<body>

    <div class="cv-container">
        <!-- =======================
             SIDEBAR (SINISTRA)
        ======================== -->
        <aside class="sidebar">
            <div class="profile-header">
                <!-- La parte relativa alla foto è stata rimossa come richiesto. -->
                <h1 class="profile-name">Giovanni Carrozza</h1>
                <p class="profile-title">Consulente Ingegneristico</p>
            </div>

            <div class="sidebar-content">
                <section class="sidebar-section">
                    <h3>
                        <!-- SVG Icona Contatti -->
                        <svg viewBox="0 0 24 24"><path d="M20,0H4A2,2,0,0,0,2,2V22a2,2,0,0,0,2,2H20a2,2,0,0,0,2-2V2A2,2,0,0,0,20,0ZM8,6a2,2,0,1,1-2,2A2,2,0,0,1,8,6Zm8,12H8V16c0-2.21,3.58-4,8-4s8,1.79,8,4v2H16Z" transform="translate(-2)"/></svg>
                        Contatti
                    </h3>
                    <div class="contact-item">
                        <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
                        <span>Somma Vesuviana (NA), Italia</span>
                    </div>
                    <div class="contact-item">
                        <svg viewBox="0 0 24 24"><path d="M22 6c0-1.1-.9-2-2-2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6zm-2 0l-8 5-8-5h16zm0 12H4V8l8 5 8-5v10z"/></svg>
                        <a href="mailto:giovanni_carrozza@outlook.it">giovanni_carrozza@outlook.it</a>
                    </div>
                    <div class="contact-item">
                        <svg viewBox="0 0 24 24"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.22-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
                        <a href="tel:+393756923375">+39 375 692 3375</a>
                    </div>
                    <div class="contact-item">
                        <svg viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.374-12 12 0 5.302 3.438 9.8 8.207 11.387.6.111.817-.26.817-.577v-2.234c-3.338.726-4.042-1.61-4.042-1.61-.545-1.385-1.332-1.756-1.332-1.756-1.09-.744.082-.729.082-.729 1.205.086 1.838 1.238 1.838 1.238 1.07 1.834 2.807 1.304 3.492.997.107-.775.42-1.304.762-1.604-2.665-.304-5.467-1.334-5.467-5.931 0-1.31.465-2.381 1.236-3.221-.124-.303-.535-1.523.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.046.138 3.003.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.873.118 3.176.772.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.474 5.922.429.369.816 1.102.816 2.222v3.293c0 .319.21.694.825.576C20.565 21.79 24 17.301 24 12 24 5.374 18.627 0 12 0z"/></svg>
                        <a href="https://github.com/GiovanniCarrozza1998" target="_blank">GiovanniCarrozza1998</a>
                    </div>
                </section>

                <section class="sidebar-section">
                    <h3>
                        <!-- SVG Icona Lingue -->
                        <svg viewBox="0 0 24 24"><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zm6.93 6h-2.95c-.32-1.25-.78-2.45-1.38-3.56 1.84.63 3.37 1.91 4.33 3.56zM12 4.04c.83 1.2 1.48 2.53 1.91 3.96h-3.82c.43-1.43 1.08-2.76 1.91-3.96zM4.26 8C5.23 6.44 6.76 5.16 8.6 4.44 8 5.55 7.54 6.75 7.21 8H4.26zM4.44 10h2.81c-.08.66-.14 1.32-.14 2s.06 1.34.14 2H4.44C4.16 13.36 4 12.69 4 12s.16-1.36.44-2zm3.08 4H10.4c.08.66.14 1.32.14 2s-.06 1.34-.14 2H7.52c-.5-1.12-.96-2.31-1.29-3.56H7.52zM12 19.96c-.83-1.2-1.48-2.53-1.91-3.96h3.82c-.43 1.43-1.08 2.76-1.91-3.96zm2.08-4H13.6c-.08-.66-.14-1.32-.14-2s.06-1.34.14-2h2.88c.33 1.25.79 2.44 1.29 3.56H14.08zM15.4 19.56c.6-1.11 1.06-2.31 1.38-3.56h2.95c-.96 1.65-2.49 2.93-4.33 3.56zM16.79 14h2.81c.28-.64.44-1.31.44-2s-.16-1.36-.44-2h-2.81c.08.66.14 1.32.14 2s-.06 1.34-.14 2z"/></svg>
                        Lingue
                    </h3>
                    <div class="skill-item">
                        <p>Italiano (Madrelingua)</p>
                        <div class="skill-bar-bg"><div class="skill-bar-fill" style="width: 100%;"></div></div>
                    </div>
                    <div class="skill-item">
                        <p>Inglese (Certificazione B2)</p>
                        <div class="skill-bar-bg"><div class="skill-bar-fill" style="width: 75%;"></div></div>
                    </div>
                </section>

                <section class="sidebar-section">
                    <h3>
                        <!-- SVG Icona Software -->
                        <svg viewBox="0 0 24 24"><path d="M10 4H4c-1.11 0-2 .9-2 2v12c0 1.1.89 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/></svg>
                        Software
                    </h3>
                    <ul class="software-list">
                        <li><svg viewBox="0 0 24 24"><path d="M10 4H4c-1.11 0-2 .9-2 2v12c0 1.1.89 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/></svg>Excel, Word, PowerPoint, Outlook</li>
                        <li><svg viewBox="0 0 24 24"><path d="M10 4H4c-1.11 0-2 .9-2 2v12c0 1.1.89 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/></svg>RStudio</li>
                        <li><svg viewBox="0 0 24 24"><path d="M10 4H4c-1.11 0-2 .9-2 2v12c0 1.1.89 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/></svg>PyCharm, Anaconda</li>
                    </ul>
                </section>

                 <section class="sidebar-section">
                    <h3>
                        <!-- SVG Icona Interessi -->
                        <svg viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
                        Interessi
                    </h3>
                    <ul class="interests-list">
                        <li><svg viewBox="0 0 24 24"><path d="M18 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-2 15h-2v-2h2v2zm-2-4h-2v-2h2v2zm-4 4H8v-2h2v2zm-2-4H8v-2h2v2zm6-4h-2V7h2v2zm-4-2H8V7h2v2zm-4-2V4h12v3H6z"/></svg>Informatica, Matematica e Fisica</li>
                        <li><svg viewBox="0 0 24 24"><path d="M18 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-2 15h-2v-2h2v2zm-2-4h-2v-2h2v2zm-4 4H8v-2h2v2zm-2-4H8v-2h2v2zm6-4h-2V7h2v2zm-4-2H8V7h2v2zm-4-2V4h12v3H6z"/></svg>Risoluzione Problemi Complessi (Scacchi, Giochi di logica e rompicapo)</li>
                        <li><svg viewBox="0 0 24 24"><path d="M13.5 5.5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM9.8 8.9L7 11.7V15h2v5h2v-6h1l1.1-3.4 1.9-2.2c.5-.6.4-1.5-.2-2-.6-.4-1.5-.4-2 .2l-1.7 2.1-1.2-1.8c-.5-.8-1.5-1.1-2.4-.7-.8.4-1.2 1.3-1 2.2zM4.9 12c-1.7 0-3.1 1.4-3.1 3.1s1.4 3.1 3.1 3.1 3.1-1.4 3.1-3.1-1.4-3.1-3.1-3.1zm14.2 0c-1.7 0-3.1 1.4-3.1 3.1s1.4 3.1 3.1 3.1 3.1-1.4 3.1-3.1-1.4-3.1-3.1-3.1z"/></svg>Sport, Musica, Cinema e Anime</li>
                    </ul>
                </section>
            </div>
        </aside>

        <!-- =======================
             MAIN CONTENT (DESTRA)
        ======================== -->
        <main class="main-content">
            <section class="main-section profile-summary">
                <h2>
                    <svg viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>
                    Profilo
                </h2>
                <p>Fin da piccolo ho sviluppato una forte passione per l’informatica (dall'età di 9 anni, con codice autodidatta dagli 11). Questo interesse si è poi ampliato, assumendo una dimensione trasversale nell'ambito scientifico, coinvolgendo anche la matematica e la fisica. Sono una persona molto stimolata da tutte quelle attività che richiedono la capacità di risolvere problemi complessi, come ad esempio il gioco degli scacchi o altri giochi di logica e di rompicapo.</p>
            </section>

            <hr class="section-divider">

            <section class="main-section">
                <h2>
                    <svg viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6zM6 20V4h7v5h5v11H6z"/></svg>
                    Esperienza Professionale
                </h2>
                <div class="timeline">
                    <div class="timeline-item">
                        <p class="timeline-date">2023 (6 MESI)</p>
                        <h3 class="timeline-title">Stage | Data Analysis</h3>
                        <p class="timeline-subtitle">Alstom, Nola (NA)</p>
                        <ul class="timeline-details">
                            <li>Analisi dati per la costruzione di un tool capace di determinare la variante ottimale di riprofilatura di una coppia di ruote del treno.</li>
                            <li>Sviluppo di una soluzione basata su tecniche di interpolazione matematica come le Cubic Splines per minimizzare la massa da asportare.</li>
                        </ul>
                    </div>
                    <div class="timeline-item">
                        <p class="timeline-date">2023 (6 MESI)</p>
                        <h3 class="timeline-title">Consulente Ingegneristico</h3>
                        <p class="timeline-subtitle">Teoresi Group (per Alstom), Napoli</p>
                        <ul class="timeline-details">
                            <li>Creazione di un servizio di telediagnostica real time, progettando pagine in HTML e CSS per replicare i monitor diagnostici dei treni e rendere disponibili le informazioni agli analisti.</li>
                            <li>Sviluppo di uno script Python per la pulizia di un database di chiamate telefoniche, eliminando ridondanze e duplicazioni.</li>
                        </ul>
                    </div>
                    <div class="timeline-item">
                        <p class="timeline-date">2024 - ATTUALE</p>
                        <h3 class="timeline-title">Consulente Ingegneristico</h3>
                        <p class="timeline-subtitle">Teoresi Group (per Avio Aero), Napoli</p>
                        <ul class="timeline-details">
                            <li>Modellizzazione statistica dei guasti dei motori aeronautici tramite modelli bayesiani.</li>
                            <li>Stima dei parametri delle distribuzioni di probabilità (Weibull e multinomiale) con Python, R e Stan.</li>
                            <li>Analisi di rischio per la manutenzione predittiva e la gestione ottimale dei magazzini di ricambi.</li>
                            <li>Automatizzazione delle analisi, creando script per la manutenzione intelligente dei dati e l’estrazione di conoscenza tramite modelli di question answering basati su Hugging Face.</li>
                            <li>Implementazione di assistenti intelligenti per la navigazione efficiente ed il recupero sicuro e rapido dei dati all’interno dei database.</li>
                        </ul>
                    </div>
                </div>
            </section>

            <hr class="section-divider">

            <section class="main-section">
                <h2>
                    <svg viewBox="0 0 24 24"><path d="M5 13.18v4L12 21l7-3.82v-4L12 17l-7-3.82zM12 3L1 9l11 6 9-4.91V17h2V9L12 3z"/></svg>
                    Formazione e Riconoscimenti
                </h2>
                <div class="timeline">
                    <div class="timeline-item">
                        <p class="timeline-date">2016</p>
                        <h3 class="timeline-title">Diploma di Perito Informatico (97/100)</h3>
                        <p class="timeline-subtitle">Istituto Tecnico Industriale Ettore Majorana, Somma Vesuviana (NA)</p>
                    </div>
                     <div class="timeline-item">
                        <p class="timeline-date">2016</p>
                        <h3 class="timeline-title">Medaglia d'Oro - Olimpiadi Nazionali della Matematica</h3>
                        <p class="timeline-subtitle">Cesenatico</p>
                    </div>
                     <div class="timeline-item">
                        <p class="timeline-date">2018</p>
                        <h3 class="timeline-title">Borsa di Studio</h3>
                        <p class="timeline-subtitle">Istituto Nazionale di Alta Matematica</p>
                    </div>
                    <div class="timeline-item">
                        <p class="timeline-date">2020</p>
                        <h3 class="timeline-title">Laurea Triennale in Matematica (110 e Lode)</h3>
                        <p class="timeline-subtitle">Università degli Studi di Salerno</p>
                    </div>
                    <div class="timeline-item">
                        <p class="timeline-date">2023</p>
                        <h3 class="timeline-title">Laurea Magistrale in Matematica (110 e Lode)</h3>
                        <p class="timeline-subtitle">Università degli Studi di Salerno</p>
                    </div>
                    <div class="timeline-item">
                        <p class="timeline-date">2023</p>
                        <h3 class="timeline-title">Tutor Accademico (Analisi Reale e Topologia)</h3>
                        <p class="timeline-subtitle">Università degli Studi di Salerno</p>
                    </div>
                </div>
            </section>

            <hr class="section-divider">

            <section class="main-section">
                 <h2>
                    <svg viewBox="0 0 24 24"><path d="M16.5 12c1.38 0 2.5-1.12 2.5-2.5S17.88 7 16.5 7s-2.5 1.12-2.5 2.5 1.12 2.5 2.5 2.5zM9 11c1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3 1.34 3 3 3zm7.5 3c-1.83 0-5.5.92-5.5 2.75V19h11v-2.25c0-1.83-3.67-2.75-5.5-2.75zM9 13c-2.33 0-7 1.17-7 3.5V19h7v-2.5c0-.85.33-2.34 2.37-3.41C10.5 13.1 9.66 13 9 13z"/></svg>
                    Competenze Tecniche
                </h2>
                <p style="margin-bottom: 20px;">Possiedo una certificazione B2 di inglese e una solida preparazione in diversi linguaggi di programmazione. Ho anche una conoscenza approfondita del pacchetto Office. Sono competente nell’analisi di dati statistici, ipotesi statistiche, stime degli intervalli di confidenza, catene di Markov e le principali metodologie di stima dei parametri delle distribuzioni di probabilità, inclusa la stima tramite Maximum Likelihood Principle. In parallelo al lavoro, nell'ultimo anno mi sono molto interessato al mondo dell'automazione software e **sto conseguendo un certificato Coursera sul software UIPath Studio**. Ho una buona conoscenza teorica dei principali algoritmi/architetture di Machine Learning.</p>
                <div class="skills-grid">
                    <div class="skill-category">
                        <h4>Linguaggi di Programmazione</h4>
                        <span class="skill-tag">Python</span>
                        <span class="skill-tag">R</span>
                        <span class="skill-tag">Stan</span>
                        <span class="skill-tag">SQL</span>
                    </div>
                     <div class="skill-category">
                        <h4>Analisi Dati e Statistica</h4>
                        <span class="skill-tag">Analisi Dati Statistici</span>
                        <span class="skill-tag">Ipotesi Statistiche</span>
                        <span class="skill-tag">Stime Intervalli Confidenza</span>
                        <span class="skill-tag">Catene di Markov</span>
                        <span class="skill-tag">Stima Parametri (MLE)</span>
                        <span class="skill-tag">Modelli Bayesiani</span>
                    </div>
                    <div class="skill-category">
                        <h4>Framework e Librerie</h4>
                        <span class="skill-tag">Tensorflow</span>
                        <span class="skill-tag">Numpy</span>
                        <span class="skill-tag">Pandas</span>
                        <span class="skill-tag">Pyautogui</span>
                        <span class="skill-tag">Hugging Face</span>
                    </div>
                     <div class="skill-category">
                        <h4>Machine Learning</h4>
                        <span class="skill-tag">Reti Neurali</span>
                        <span class="skill-tag">Reti Convolutive</span>
                        <span class="skill-tag">LSTM</span>
                        <span class="skill-tag">Random Forest</span>
                        <span class="skill-tag">K-Means</span>
                        <span class="skill-tag">Regressione Lineare</span>
                        <span class="skill-tag">Regressione Logistica</span>
                    </div>
                    <div class="skill-category">
                        <h4>Automazione Software & AI</h4>
                        <span class="skill-tag">UIPath Studio</span>
                        <span class="skill-tag">Desktop Automation</span>
                        <span class="skill-tag">Prompt Engineering</span>
                        <span class="skill-tag">Tesseract OCR</span>
                    </div>
                     <div class="skill-category">
                        <h4>Software Office</h4>
                        <span class="skill-tag">Pacchetto Office</span>
                    </div>
                </div>
            </section>

            <hr class="section-divider">

            <section class="main-section">
                <h2>
                    <!-- Icona per i Progetti (es. un'icona di codice o un ingranaggio) -->
                    <svg viewBox="0 0 24 24"><path d="M14.6 16.6l4.6-4.6-4.6-4.6 1.4-1.4 6 6-6 6zM9.4 6.6L4.8 11.2l4.6 4.6-1.4 1.4-6-6 6-6z"/></svg>
                    Progetti
                </h2>
                <div class="timeline">
                    <div class="timeline-item">
                        <p class="timeline-date">2024</p>
                        <h3 class="timeline-title">Tool per la risoluzione autonoma del gioco Queens di LinkedIn</h3>
                        <p class="timeline-subtitle">Progetto Personale</p>
                        <ul class="timeline-details">
                            <li>Sviluppato un tool in Python per risolvere il gioco "Queens" di LinkedIn in totale autonomia.</li>
                            <li>Utilizza tecniche di desktop automation, color clustering e algoritmi di risoluzione di sistemi di equazioni lineari.</li>
                            <li>Disponibile sul mio <a href="https://github.com/GiovanniCarrozza1998" target="_blank">GitHub</a>.</li>
                        </ul>
                    </div>
                    <div class="timeline-item">
                        <p class="timeline-date">2024</p>
                        <h3 class="timeline-title">Creatore Automatico di CV (HTML)</h3>
                        <p class="timeline-subtitle">Progetto Personale</p>
                        <ul class="timeline-details">
                            <li>Software per la generazione automatica di CV in formato HTML tramite input audio o testuale.</li>
                            <li>Fa uso di template predefiniti e informazioni utente per creare il CV.</li>
                            <li>Implementato con tecniche di prompt engineering e il modello Gemini 2.5 Flash tramite API.</li>
                            <li>Utilizzato per la generazione del CV attuale. Disponibile sul mio <a href="https://github.com/GiovanniCarrozza1998" target="_blank">GitHub</a>.</li>
                        </ul>
                    </div>
                    <div class="timeline-item">
                        <p class="timeline-date">2024</p>
                        <h3 class="timeline-title">Estrattore di Sottotitoli da Microsoft Teams</h3>
                        <p class="timeline-subtitle">Progetto Personale</p>
                        <ul class="timeline-details">
                            <li>Tool sviluppato per l'estrazione e il salvataggio dei sottotitoli generati dalle riunioni di Microsoft Teams.</li>
                            <li>Acquisisce i sottotitoli tramite screenshot continui di una regione definita dall'utente, utilizzando Tesseract OCR.</li>
                            <li>Elabora i dati estratti rimuovendo caratteri inutili e ridondanze tramite un prompt ad hoc con Gemini 2.5 Flash tramite API.</li>
                            <li>Disponibile sul mio <a href="https://github.com/GiovanniCarrozza1998" target="_blank">GitHub</a>.</li>
                        </ul>
                    </div>
                    <div class="timeline-item">
                        <p class="timeline-date">ATTUALE</p>
                        <h3 class="timeline-title">Agente Intelligente per Automazione Desktop</h3>
                        <p class="timeline-subtitle">Progetto in Sviluppo</p>
                        <ul class="timeline-details">
                            <li>Agente capace di convertire prompt testuali in azioni concrete tramite desktop automation e prompt engineering.</li>
                            <li>Obiettivo: creare una base per un agente in grado di svolgere compiti complessi (manutenzione di file Excel, creazione script Python, ecc.).</li>
                            <li>Esempi di funzionalità: "apri Youtube e cerca gli highlights di Barcellona - PSG", "apri il Notepad, inventa un finale per One Piece e scrivilo".</li>
                        </ul>
                    </div>
                </div>
            </section>
        </main>
    </div>

</body>
</html>
"""

with open('config.json') as config_file:
    config = json.load(config_file)

genai.configure(api_key=config["api_key"])
model = genai.GenerativeModel("gemini-2.5-flash")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # Aggiorna con il tuo dominio se necessario
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/transcribe-and-create-cv/")
async def transcribe_and_create_cv(file: UploadFile):
    try:
        # Salva il file audio e la foto opzionale
        transcriber = sr.Recognizer()

        # Usa file.file direttamente per la trascrizione
        with sr.AudioFile(file.file) as source:
            audio_data = transcriber.record(source)
            # Ottieni la trascrizione
            transcription = transcriber.recognize_google(audio_data, language="it-IT")
        prompt = "Considera la seguente trascrizione di un file audio in cui vengono riportate tutte le informazioni di una persona da inserire all'interno di un CV: " + transcription + "." + "Modifica lo script html che ti lascio alla fine di questo prompt mantenendo lo stile ed inserendo al posto giusto le informazioni presenti nel testo precedente che ti ho allegato. Le informazioni temporali devon essere riportate secondo il naturale ordine cronologico degli eventi. Non includere foto. Restituisci il codice html delimitato solo ed esclusivamente dai tag di inizio codice. Tutti gli elementi grafici devono essere in SVG. SCRIPT HTML DA MODIFICARE : " + template
        response = model.generate_content(prompt).text.replace("```html", "").replace("```", "")

        # Inserisci il tuo codice qui per la trascrizione e la creazione del CV
        return {"status": "CV creato con successo", "CV" : response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/create-cv-from-string/")
async def create_cv_from_string(info: str):
    global template
    try:
        prompt ="Considera la seguente trascrizione di un file audio in cui vengono riportate tutte le informazioni di una persona da inserire all'interno di un CV: " + info + "." + "Modifica lo script html che ti lascio alla fine di questo prompt mantenendo lo stile ed inserendo al posto giusto le informazioni presenti nel testo precedente che ti ho allegato. Le informazioni temporali devon essere riportate secondo il naturale ordine cronologico degli eventi. Non includere foto. Restituisci il codice html delimitato solo ed esclusivamente dai tag di inizio codice. Tutti gli elementi grafici devono essere in SVG. SCRIPT HTML DA MODIFICARE : " + template
        response = model.generate_content(prompt).text.replace("```html", "").replace("```", "")
        # Inserisci il tuo codice qui per la creazione del CV
        return {"status": "CV creato con successo", "CV" : response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/edit-cv/")
async def edit_cv(cv_file: UploadFile, modifications: str):
    try:
        # Leggi il contenuto del file CV
        html_content = await cv_file.read()
        html_to_edit = html_content.decode('utf-8')

        # Genera il contenuto modificato
        response = model.generate_content(
            f"Riscrivi e RIPORTA SOLAMENTE il codice HTML riportato alla fine apportando le seguenti modifiche: {modifications}. CODICE HTML : {html_to_edit}"
        )

        # Inserisci il tuo codice qui per modificare il CV
        return {"status": "CV modificato con successo", "modified_cv": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

