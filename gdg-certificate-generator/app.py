import streamlit as st
import pandas as pd
import os
import shutil
import zipfile
from io import BytesIO
from certificate_generator import CertificateGenerator

# Page configuration
st.set_page_config(
    page_title="GDG Basra Certificate Generator",
    page_icon="🎓",
    layout="wide"
)

# Initialize session state
if 'template_uploaded' not in st.session_state:
    st.session_state.template_uploaded = False
if 'attendees' not in st.session_state:
    st.session_state.attendees = []
if 'generator' not in st.session_state:
    st.session_state.generator = None

# Title and description
st.title("🎓 GDG Basra Certificate Generator")
st.markdown("Generate professional certificates with security features including SHA-256 hashing and QR codes.")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["📤 Upload Template", "📝 Add Attendees", "⚙️ Customize", "🎉 Generate"])

# ============ TAB 1: Upload Template ============
with tab1:
    st.header("Upload Certificate Template")
    st.info("Upload a blank certificate template (JPG/PNG format)")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Event name input
        event_name = st.text_input("Event Name", value="GDG Basra Event", help="This will be used for generating unique hashes")
        
        # Template upload
        template_file = st.file_uploader("Choose a certificate template", type=['jpg', 'jpeg', 'png'])
        
        if template_file is not None:
            # Create temp directory
            os.makedirs("temp/uploads", exist_ok=True)
            
            # Save uploaded template
            template_path = os.path.join("temp/uploads", "template.png")
            with open(template_path, "wb") as f:
                f.write(template_file.getbuffer())
            
            # Initialize generator
            st.session_state.generator = CertificateGenerator(template_path, event_name)
            st.session_state.template_uploaded = True
            st.success("✅ Template uploaded successfully!")
    
    with col2:
        if st.session_state.template_uploaded:
            st.image(template_path, caption="Your Certificate Template", use_container_width=True)

# ============ TAB 2: Add Attendees ============
with tab2:
    st.header("Add Attendees")
    
    if not st.session_state.template_uploaded:
        st.warning("⚠️ Please upload a certificate template first!")
    else:
        # Choose input method
        input_method = st.radio("Choose input method:", ["Manual Entry", "Upload File (CSV/Excel)"])
        
        if input_method == "Manual Entry":
            st.info("Enter attendee names, one per line")
            manual_input = st.text_area("Attendee Names", height=200, placeholder="John Doe\nJane Smith\nأحمد محمد")
            
            if st.button("Load Attendees"):
                if manual_input.strip():
                    st.session_state.attendees = [name.strip() for name in manual_input.split('\n') if name.strip()]
                    st.success(f"✅ Loaded {len(st.session_state.attendees)} attendees")
                else:
                    st.error("Please enter at least one name")
        
        else:  # Upload File
            st.info("Upload a CSV or Excel file with attendee names. The first column should contain the names.")
            uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx', 'xls'])
            
            if uploaded_file is not None:
                try:
                    # Read file based on type
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    
                    # Get first column
                    st.session_state.attendees = df.iloc[:, 0].dropna().astype(str).tolist()
                    st.success(f"✅ Loaded {len(st.session_state.attendees)} attendees")
                    
                    # Show preview
                    st.subheader("Preview")
                    st.dataframe(df.head(10))
                except Exception as e:
                    st.error(f"Error reading file: {e}")
        
        # Display loaded attendees
        if st.session_state.attendees:
            st.subheader(f"Loaded Attendees ({len(st.session_state.attendees)})")
            st.write(", ".join(st.session_state.attendees[:10]) + ("..." if len(st.session_state.attendees) > 10 else ""))

# ============ TAB 3: Customize ============
with tab3:
    st.header("Customize Certificate Settings")
    
    if not st.session_state.template_uploaded:
        st.warning("⚠️ Please upload a certificate template first!")
    else:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🎨 Font Settings")
            
            # Font selection
            available_fonts = ['Amiri', 'Cairo', 'Tajawal', 'Almarai', 'Roboto', 'OpenSans', 'Montserrat']
            selected_font = st.selectbox("Select Font", available_fonts, help="Fonts will be downloaded from Google Fonts")
            
            # Download font
            font_path = st.session_state.generator.download_google_font(selected_font)
            if font_path is None:
                st.error(f"Could not download {selected_font} font. Please try another.")
                font_path = st.session_state.generator.download_google_font('Roboto')  # Fallback
            
            # Font size
            font_size = st.slider("Font Size", min_value=20, max_value=150, value=60, step=5)
            
            # Text color
            text_color_hex = st.color_picker("Text Color", "#000000")
            text_color = tuple(int(text_color_hex[i:i+2], 16) for i in (1, 3, 5))
            
            st.subheader("📍 Name Position")
            template_width = st.session_state.generator.template_width
            template_height = st.session_state.generator.template_height
            
            name_x = st.slider("Name X Position", min_value=0, max_value=template_width, value=template_width//2, step=10)
            name_y = st.slider("Name Y Position", min_value=0, max_value=template_height, value=template_height//2, step=10)
            
            st.subheader("🔐 Security Elements Position")
            
            use_custom_hash_pos = st.checkbox("Custom Hash Position")
            if use_custom_hash_pos:
                hash_x = st.slider("Hash X Position", min_value=0, max_value=template_width, value=50, step=10)
                hash_y = st.slider("Hash Y Position", min_value=0, max_value=template_height, value=template_height-100, step=10)
                hash_position = (hash_x, hash_y)
            else:
                hash_position = None
            
            use_custom_qr_pos = st.checkbox("Custom QR Code Position")
            if use_custom_qr_pos:
                qr_x = st.slider("QR Code X Position", min_value=0, max_value=template_width-200, value=template_width-200, step=10)
                qr_y = st.slider("QR Code Y Position", min_value=0, max_value=template_height-200, value=template_height-200, step=10)
                qr_position = (qr_x, qr_y)
            else:
                qr_position = None
            
            qr_size = st.slider("QR Code Size", min_value=80, max_value=300, value=150, step=10)
        
        with col2:
            st.subheader("👁️ Preview")
            
            if st.session_state.attendees:
                preview_name = st.selectbox("Select attendee to preview", st.session_state.attendees)
                
                if st.button("🔄 Generate Preview", type="primary"):
                    with st.spinner("Generating preview..."):
                        try:
                            cert, cert_hash = st.session_state.generator.generate_certificate(
                                attendee_name=preview_name,
                                name_position=(name_x, name_y),
                                font_path=font_path,
                                font_size=font_size,
                                text_color=text_color,
                                hash_position=hash_position,
                                qr_position=qr_position,
                                qr_size=qr_size
                            )
                            
                            st.image(cert, caption=f"Certificate for {preview_name}", use_container_width=True)
                            st.info(f"🔐 Certificate Hash: {cert_hash[:16]}...")
                        except Exception as e:
                            st.error(f"Error generating preview: {e}")
            else:
                st.info("Add attendees in the 'Add Attendees' tab to see a preview")
            
            # Store settings in session state for final generation
            st.session_state.settings = {
                'font_path': font_path,
                'font_size': font_size,
                'text_color': text_color,
                'name_position': (name_x, name_y),
                'hash_position': hash_position,
                'qr_position': qr_position,
                'qr_size': qr_size
            }

# ============ TAB 4: Generate ============
with tab4:
    st.header("Generate Certificates")
    
    if not st.session_state.template_uploaded:
        st.warning("⚠️ Please upload a certificate template first!")
    elif not st.session_state.attendees:
        st.warning("⚠️ Please add attendees first!")
    else:
        st.info(f"Ready to generate {len(st.session_state.attendees)} certificates")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Generation Options")
            save_format = st.radio("Output Format", ["PDF", "PNG"])
            
        with col2:
            st.subheader("Summary")
            st.metric("Total Attendees", len(st.session_state.attendees))
            st.metric("Event Name", event_name)
        
        if st.button("🚀 Bulk Generate All Certificates", type="primary", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Create output directory
                output_dir = "temp/generated"
                if os.path.exists(output_dir):
                    shutil.rmtree(output_dir)
                os.makedirs(output_dir, exist_ok=True)
                
                # Get settings from session state
                settings = st.session_state.get('settings', {
                    'font_path': st.session_state.generator.download_google_font('Roboto'),
                    'font_size': 60,
                    'text_color': (0, 0, 0),
                    'name_position': (st.session_state.generator.template_width//2, st.session_state.generator.template_height//2),
                    'hash_position': None,
                    'qr_position': None,
                    'qr_size': 150
                })
                
                # Generate certificates
                status_text.text("Generating certificates...")
                results = st.session_state.generator.batch_generate(
                    attendees=st.session_state.attendees,
                    output_dir=output_dir,
                    name_position=settings['name_position'],
                    font_path=settings['font_path'],
                    font_size=settings['font_size'],
                    text_color=settings['text_color'],
                    hash_position=settings['hash_position'],
                    qr_position=settings['qr_position'],
                    qr_size=settings['qr_size'],
                    save_as_pdf=(save_format == "PDF")
                )
                
                progress_bar.progress(50)
                
                # Create ZIP file
                status_text.text("Creating ZIP file...")
                zip_path = "temp/output/certificates.zip"
                os.makedirs("temp/output", exist_ok=True)
                
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for result in results:
                        zipf.write(result['path'], os.path.basename(result['path']))
                
                progress_bar.progress(100)
                status_text.text("✅ Generation complete!")
                
                # Download button
                with open(zip_path, 'rb') as f:
                    st.download_button(
                        label="📥 Download All Certificates (ZIP)",
                        data=f.read(),
                        file_name=f"gdg_basra_certificates_{event_name.replace(' ', '_').lower()}.zip",
                        mime="application/zip",
                        type="primary",
                        use_container_width=True
                    )
                
                # Show success message with details
                st.success(f"✅ Successfully generated {len(results)} certificates!")
                
                # Show certificate details in expander
                with st.expander("View Certificate Details"):
                    details_df = pd.DataFrame([
                        {'Attendee': r['name'], 'Hash (First 12)': r['hash'][:12].upper()}
                        for r in results
                    ])
                    st.dataframe(details_df, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error during generation: {e}")
                import traceback
                st.error(traceback.format_exc())

# Footer
st.markdown("---")
st.markdown("Made with ❤️ for **GDG Basra**")
