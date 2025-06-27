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
        st.error("Error: [img] folder not found. There might be a bug")
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
        st.warning("No tracks found. Add images to the img folder.")
        st.info("Supported formats: JPG, JPEG, PNG, GIF, BMP, WEBP")
        return
    
    # Initialisiere Session State
    if 'current_track' not in st.session_state:
        st.session_state.current_track = None
    
    if 'available_tracks' not in st.session_state:
        st.session_state.available_tracks = tracks.copy()
    
    if 'used_tracks' not in st.session_state:
        st.session_state.used_tracks = []
    
    # Zeige Track Pool Status
    st.info(f"Available tracks: {len(st.session_state.available_tracks)} / {len(tracks)}")
    
    # Buttons in zwei Spalten
    col1, col2 = st.columns(2)
    
    with col1:
        # Randomizer Button
        if st.button("🎲 Pick Random Track", type="primary", use_container_width=True):
            if st.session_state.available_tracks:
                # Wähle zufällige Strecke aus verfügbaren Strecken
                selected_track = random.choice(st.session_state.available_tracks)
                st.session_state.current_track = selected_track
                
                # Entferne Strecke aus verfügbaren und füge zu verwendeten hinzu
                st.session_state.available_tracks.remove(selected_track)
                st.session_state.used_tracks.append(selected_track)
                
                st.rerun()
            else:
                st.warning("All tracks were used, reset the pool.")
    
    with col2:
        # Pool Reset Button
        if st.button("🔄 Reset Track Pool", use_container_width=True):
            st.session_state.available_tracks = tracks.copy()
            st.session_state.used_tracks = []
            st.success("Reset was successful!")
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
            st.error(f"Error loading image: {e}")
            
    else:
        # Zeige ein Platzhalter-Bild oder Text
        st.markdown("""
        <div style='text-align: center; padding: 50px; background-color: #f0f2f6; border-radius: 10px;'>
            <h3>🏁 Ready to randomize? 🏁</h3>
            <p>Press the button to select a random Mario Kart track!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Zeige verwendete Strecken in einem Expander
    if st.session_state.used_tracks:
        with st.expander(f"Already used tracks: ({len(st.session_state.used_tracks)})"):
            for i, track in enumerate(st.session_state.used_tracks, 1):
                st.write(f"{i}. {track['name']}")

if __name__ == "__main__":
    main()
