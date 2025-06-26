import streamlit as st
import os
import random
from pathlib import Path

def get_track_images():
    """
    Lädt alle Bilder aus dem img Ordner und extrahiert die Streckennamen
    """
    img_folder = Path("img")
    
    # Überprüfe ob der img Ordner existiert
    if not img_folder.exists():
        st.error("Der 'img' Ordner wurde nicht gefunden. Bitte stellen Sie sicher, dass der Ordner existiert.")
        return []
    
    # Unterstützte Bildformate
    supported_formats = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    
    tracks = []
    
    # Durchsuche alle Dateien im img Ordner
    for file_path in img_folder.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in supported_formats:
            # Extrahiere den Streckennamen aus dem Dateinamen (ohne Dateiendung)
            track_name = file_path.stem.replace('_', ' ').replace('-', ' ')
            tracks.append({
                'name': track_name,
                'image_path': str(file_path)
            })
    
    return tracks

def main():
    st.set_page_config(
        page_title="Mario Kart Track Randomizer",
        page_icon="🏁",
        layout="centered"
    )
    
    # Titel der App
    st.title("🏁 Mario Kart Track Randomizer")
    
    # Lade alle verfügbaren Strecken
    tracks = get_track_images()
    
    if not tracks:
        st.warning("Keine Streckenbilder gefunden. Bitte fügen Sie Bilder in den 'img' Ordner hinzu.")
        st.info("Unterstützte Formate: JPG, JPEG, PNG, GIF, BMP, WEBP")
        return
    
    # Initialisiere Session State für die aktuelle Strecke
    if 'current_track' not in st.session_state:
        st.session_state.current_track = None
    
    # Randomizer Button
    if st.button("🎲 Zufällige Strecke wählen", type="primary", use_container_width=True):
        st.session_state.current_track = random.choice(tracks)
        st.rerun()
    
    st.markdown("---")
    
    # Zeige die aktuelle Strecke falls vorhanden
    if st.session_state.current_track:
        track = st.session_state.current_track
        
        # Streckenname als großer Titel
        st.markdown(f"## {track['name']}")
        
        # Zeige das Bild
        try:
            st.image(
                track['image_path'],  
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Fehler beim Laden des Bildes: {e}")
            
    else:
        st.info("Klicken Sie auf 'Zufällige Strecke wählen', um zu beginnen!")
        
        # Zeige ein Platzhalter-Bild oder Text
        st.markdown("""
        <div style='text-align: center; padding: 50px; background-color: #f0f2f6; border-radius: 10px;'>
            <h3>🏁 Bereit zum Randomizen? 🏁</h3>
            <p>Drücken Sie den Button, um eine zufällige Mario Kart Strecke auszuwählen!</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
